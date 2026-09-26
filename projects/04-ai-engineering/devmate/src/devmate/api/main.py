"""
FastAPI application with lifespan, routing, and middleware.
"""

import asyncio
import logging
import uuid
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Protocol

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from devmate.config import settings
from devmate.ingest.chunker import DocumentLoader, get_chunker
from devmate.llm.client import llm_client
from devmate.llm.schemas import (
    AskRequest,
    AskResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    ErrorResponse,
    HealthResponse,
    IngestRequest,
    IngestResponse,
    RAGRequest,
    RAGResponse,
)
from devmate.obs.cost import cost_tracker
from devmate.obs.tracing import tracer
from devmate.retrieve.rag import RAGRequest as InternalRAGRequest
from devmate.retrieve.rag import get_rag_pipeline


# Lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown."""
    # Startup

    # Initialize clients
    try:
        # This will initialize vector store, retriever, etc.
        await get_rag_pipeline()
    except Exception:
        pass

    yield

    # Shutdown
    await llm_client.close()


# Create FastAPI app
app = FastAPI(
    title="DevMate API",
    description="AI Assistant for Code Repositories - RAG + Agents + MCP",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("devmate.api")

# ---------------------------------------------------------------------------
# SSE streaming helpers
#
# The three production failure modes this block prevents:
#   1. generating (and billing) for a client that closed the tab
#   2. a reverse proxy buffering the stream until completion
#   3. an idle stream (slow retrieval / provider stall) timing out silently
# ---------------------------------------------------------------------------

_SSE_DONE = "data: [DONE]\n\n"
_SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "X-Accel-Buffering": "no",
}
_SSE_PUMP_QUEUE_MAX = 64
_SSE_KEEPALIVE_SECONDS = 15.0
_SSE_SENTINEL = object()


class DisconnectCheck(Protocol):
    """Anything that can report client disconnect (Starlette Request does)."""

    async def is_disconnected(self) -> bool: ...


async def _pump_to_queue(
    source: AsyncIterator[Any],
    queue: asyncio.Queue,
    sentinel: object,
) -> None:
    """Drain a fast producer into a bounded queue, then append the sentinel.

    Bounded + awaited put = backpressure: the server buffers at the client's
    rate, not the provider's. An exception from the source is enqueued so the
    consumer (the only party that can react) sees it instead of the task
    dying silently.
    """
    try:
        async for chunk in source:
            await queue.put(chunk)
    except BaseException as exc:  # noqa: BLE001 — enqueued on purpose
        await queue.put(exc)
    finally:
        await queue.put(sentinel)


async def _sse_events(
    source: AsyncIterator[Any],
    request: DisconnectCheck,
    render: Callable[[Any], str],
    keepalive_after: float = _SSE_KEEPALIVE_SECONDS,
) -> AsyncIterator[str]:
    """Frame a chunk source as SSE events with disconnect stop + keepalive.

    WHY a pump task instead of wait_for on __anext__: cancelling an async
    generator's __anext__ closes the generator mid-flight and loses the rest
    of the stream. A queue.get() timeout is cancellation-safe, and the pump
    applies backpressure in between.
    """
    queue: asyncio.Queue = asyncio.Queue(maxsize=_SSE_PUMP_QUEUE_MAX)
    pump_task = asyncio.create_task(_pump_to_queue(source, queue, _SSE_SENTINEL))
    try:
        while True:
            try:
                item = await asyncio.wait_for(queue.get(), timeout=keepalive_after)
            except TimeoutError:
                if await request.is_disconnected():
                    logger.info("sse: client disconnected during idle wait")
                    return
                yield ": keepalive\n\n"
                continue
            if item is _SSE_SENTINEL:
                break
            if isinstance(item, BaseException):
                logger.error("sse: source failed mid-stream: %r", item)
                raise item
            if await request.is_disconnected():
                logger.info("sse: client disconnected — stopping generation")
                return
            yield f"data: {render(item)}\n\n"
        yield _SSE_DONE
    finally:
        if not pump_task.done():
            pump_task.cancel()


# Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
    request.state.request_id = request_id

    with tracer.trace("http.request", method=request.method, path=request.url.path) as span:
        span.set_attribute("request_id", request_id)

        start_time = datetime.utcnow()
        response = await call_next(request)
        latency_ms = (datetime.utcnow() - start_time).total_seconds() * 1000

        span.set_attribute("status_code", response.status_code)
        span.set_attribute("latency_ms", latency_ms)

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{latency_ms:.2f}ms"

        return response


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            request_id=getattr(request.state, "request_id", None),
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)

    with tracer.trace("http.error", error_type=type(exc).__name__) as span:
        span.set_status("error", str(exc))

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc) if settings.debug else None,
            request_id=request_id,
        ).model_dump(),
    )


# Health endpoints
@app.get("/health", response_model=HealthResponse)
async def health():
    """Liveness probe."""
    return HealthResponse(
        status="healthy",
        components={"api": "ok"},
    )


@app.get("/ready")
async def ready():
    """Readiness probe - checks dependencies."""
    components = {"api": "ok"}

    # Check Qdrant
    try:
        from devmate.index.vector_store import get_vector_store

        vs = await get_vector_store()
        count = await vs.count()
        components["qdrant"] = f"ok ({count} vectors)"
    except Exception as e:
        components["qdrant"] = f"error: {e}"

    # Check Redis
    try:
        import redis.asyncio as redis

        r = redis.from_url(settings.redis_connection_url)
        await r.ping()
        await r.close()
        components["redis"] = "ok"
    except Exception as e:
        components["redis"] = f"error: {e}"

    # Check LLM
    try:
        provider = llm_client.get_provider()
        components["llm"] = f"ok ({provider.provider_name.value})"
    except Exception as e:
        components["llm"] = f"error: {e}"

    all_healthy = all("ok" in v for v in components.values())

    return {
        "status": "ready" if all_healthy else "degraded",
        "components": components,
    }


# Ask endpoint (simple Q&A with RAG)
@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest, http_request: Request):
    """Ask a question - returns streaming or full response."""
    rag_pipeline = await get_rag_pipeline()

    rag_request = InternalRAGRequest(
        query=request.question,
        stream=request.stream,
    )

    if request.stream:

        async def generate():
            result = await rag_pipeline.query(rag_request)
            async for event in _sse_events(result, http_request, lambda chunk: chunk.content):
                yield event

        headers = {
            **_SSE_HEADERS,
            "X-Conversation-ID": request.conversation_id or str(uuid.uuid4()),
        }
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers=headers,
        )
    result = await rag_pipeline.query(rag_request)

    sources = []
    for ctx in result.contexts:
        sources.append(
            {
                "id": ctx.id,
                "content": ctx.content[:200] + "..." if len(ctx.content) > 200 else ctx.content,
                "metadata": ctx.metadata,
                "score": ctx.score,
            }
        )

    return AskResponse(
        answer=result.answer,
        conversation_id=request.conversation_id or str(uuid.uuid4()),
        sources=sources,
    )


# RAG endpoint (full control)
@app.post("/ai/rag/query", response_model=RAGResponse)
async def rag_query(request: RAGRequest, http_request: Request):
    """Full RAG query with all options."""
    rag_pipeline = await get_rag_pipeline()

    internal_request = InternalRAGRequest(
        query=request.query,
        conversation_history=request.conversation_history,
        filter=request.filter,
        use_reranker=request.use_reranker,
        stream=request.stream,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
    )

    if request.stream:

        async def generate():
            result = await rag_pipeline.query(internal_request)
            async for event in _sse_events(
                result, http_request, lambda chunk: chunk.model_dump_json()
            ):
                yield event

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers=_SSE_HEADERS,
        )

    result = await rag_pipeline.query(internal_request)

    return RAGResponse(
        answer=result.answer,
        contexts=[
            {
                "id": ctx.id,
                "content": ctx.content,
                "metadata": ctx.metadata,
                "score": ctx.score,
            }
            for ctx in result.contexts
        ],
        usage=result.usage,
        latency_ms=result.latency_ms,
        request_id=result.request_id,
    )


# Ingestion endpoint
@app.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest):
    """Ingest a repository or directory."""
    import time

    start_time = time.perf_counter()

    repo_path = Path(request.repo_path)
    if not repo_path.exists():
        raise HTTPException(404, f"Path not found: {request.repo_path}")

    # Get chunker
    chunker = get_chunker(
        request.chunker, chunk_size=request.chunk_size, overlap=request.chunk_overlap
    )
    loader = DocumentLoader(chunker=chunker)

    # Load documents
    documents = list(loader.load_repository(repo_path))

    # Ingest via RAG pipeline
    rag_pipeline = await get_rag_pipeline()
    chunks_created = await rag_pipeline.ingest_documents(documents)

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    return IngestResponse(
        documents_ingested=len(documents),
        chunks_created=chunks_created,
        elapsed_ms=elapsed_ms,
    )


# Embedding endpoint
@app.post("/ai/embeddings", response_model=EmbeddingResponse)
async def embeddings(request: EmbeddingRequest):
    """Generate embeddings for texts."""
    from devmate.index.embeddings import embedding_service

    result = await embedding_service.embed(request.texts)

    return EmbeddingResponse(
        embeddings=result.embeddings,
        usage=result.usage,
        model=result.model,
    )


# Cost/usage endpoint
@app.get("/ai/usage")
async def usage(since: str = None):
    """Get usage and cost statistics."""
    from datetime import datetime

    since_dt = None
    if since:
        try:
            since_dt = datetime.fromisoformat(since)
        except ValueError:
            raise HTTPException(400, "Invalid date format. Use ISO format.")

    summary = cost_tracker.get_summary(since=since_dt)

    return {
        "total_requests": summary.total_requests,
        "total_tokens": summary.total_tokens,
        "total_cost_usd": round(summary.total_cost_usd, 6),
        "avg_latency_ms": round(summary.total_latency_ms / max(summary.total_requests, 1), 2),
        "by_model": {
            model: {
                "requests": int(data["requests"]),
                "tokens": int(data["tokens"]),
                "cost_usd": round(data["cost"], 6),
                "avg_latency_ms": round(data["latency_ms"] / max(data["requests"], 1), 2),
            }
            for model, data in summary.by_model.items()
        },
        "by_provider": {
            provider: {
                "requests": int(data["requests"]),
                "tokens": int(data["tokens"]),
                "cost_usd": round(data["cost"], 6),
                "avg_latency_ms": round(data["latency_ms"] / max(data["requests"], 1), 2),
            }
            for provider, data in summary.by_provider.items()
        },
    }


# Traces endpoint
@app.get("/traces")
async def traces(limit: int = 50):
    """Get recent traces."""
    recent = tracer.get_recent_traces(limit=limit)
    return {
        "traces": [t.to_dict() for t in recent],
    }


# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "DevMate API",
        "version": "0.1.0",
        "description": "AI Assistant for Code Repositories",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "devmate.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )


# Import at bottom to avoid circular imports
from pathlib import Path  # noqa: E402
