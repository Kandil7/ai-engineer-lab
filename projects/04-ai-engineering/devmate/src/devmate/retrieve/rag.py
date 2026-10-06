"""
RAG Pipeline - End-to-end retrieval augmented generation.
"""

import time
import uuid
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, cast

from devmate.config import settings
from devmate.index.vector_store import get_vector_store
from devmate.llm.client import LLMResponse, StreamingChunk
from devmate.obs.tracing import tracer
from devmate.retrieve.retriever import RerankResult, get_retriever


@dataclass
class RAGRequest:
    """RAG query request."""

    query: str
    conversation_history: list[dict[str, str]] = field(default_factory=list)
    filter: dict[str, Any] | None = None
    use_reranker: bool = True
    stream: bool = False
    max_tokens: int | None = None
    temperature: float | None = None


@dataclass
class RAGResult:
    """RAG pipeline result."""

    answer: str
    contexts: list[RerankResult]
    usage: dict[str, Any]
    latency_ms: float
    request_id: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


# System prompt for RAG
RAG_SYSTEM_PROMPT = """You are a helpful AI assistant that answers questions based on the provided context.

Guidelines:
1. Use ONLY the information provided in the context to answer the question
2. If the context doesn't contain enough information, say so honestly
3. Cite your sources using [1], [2], etc. corresponding to the context chunks
4. Be concise but thorough
5. If asked about code, explain it clearly with examples if helpful

Context:
{context}

Answer the user's question based on the above context."""


class RAGPipeline:
    """End-to-end RAG pipeline."""

    def __init__(
        self,
        retriever=None,
        embedding_service=None,
        llm_client=None,
    ) -> None:
        self.retriever = retriever
        self._embedding_service = embedding_service
        self._llm_client = llm_client

    @property
    def embedding_service(self):
        """Lazy default to the global embedding service (Ollama offline)."""
        if self._embedding_service is None:
            from devmate.index.embeddings import embedding_service as _default_service

            self._embedding_service = _default_service
        return self._embedding_service

    @property
    def llm_client(self):
        """Lazy default to the global LLM client (Ollama offline)."""
        if self._llm_client is None:
            from devmate.llm.client import get_llm_client

            self._llm_client = get_llm_client()
        return self._llm_client

    async def _ensure_initialized(self) -> None:
        """Ensure all components are initialized."""
        if self.retriever is None:
            self.retriever = await get_retriever()

    def _build_context(self, results: list[RerankResult]) -> str:
        """Build context string from retrieved results.

        Enforces a character budget: retrieval top_k is a *candidate* count,
        not a prompt guarantee. Stuffing every chunk into the system prompt
        overflows small local models (Ollama returns HTTP 500) and dilutes
        the context that actually matters. Always includes the first chunk
        even if it alone exceeds the budget.
        """
        budget = settings.rag_context_char_budget
        context_parts: list[str] = []
        used = 0
        for i, result in enumerate(results, 1):
            filename = result.metadata.get("filename", "unknown")
            chunk_type = result.metadata.get("chunk_type", "")
            name = result.metadata.get("name", "")

            header = f"[Source {i}: {filename}"
            if chunk_type:
                header += f" | {chunk_type}"
            if name:
                header += f" | {name}"
            header += "]"

            part = f"{header}\n{result.content}"
            if context_parts and used + len(part) > budget:
                break
            context_parts.append(part)
            used += len(part)

        return "\n\n---\n\n".join(context_parts)

    def _build_messages(
        self,
        query: str,
        context: str,
        conversation_history: list[dict[str, str]] = None,
    ) -> list[dict[str, str]]:
        """Build messages for LLM."""
        messages = [
            {"role": "system", "content": RAG_SYSTEM_PROMPT.format(context=context)},
        ]

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": query})

        return messages

    async def query(self, request: RAGRequest) -> RAGResult | AsyncIterator[StreamingChunk]:
        """Execute RAG query; returns RAGResult, or an async iterator when streaming."""
        await self._ensure_initialized()

        request_id = str(uuid.uuid4())[:8]

        start_time = time.perf_counter()

        async with tracer.trace("rag.query", request_id=request_id):
            # Step 1: Embed query
            query_embedding_result = await self.embedding_service.embed([request.query])
            query_vector = query_embedding_result.embeddings[0]

            # Step 2: Retrieve relevant documents
            retrieved = await self.retriever.retrieve(
                query=request.query,
                query_vector=query_vector,
                filter=request.filter,
                use_reranker=request.use_reranker,
            )

            # Step 3: Build context
            context = self._build_context(retrieved)

            # Step 4: Build messages
            messages = self._build_messages(
                query=request.query,
                context=context,
                conversation_history=request.conversation_history,
            )

            # Step 5: Generate answer
            max_tokens = request.max_tokens or settings.max_tokens
            temperature = (
                request.temperature if request.temperature is not None else settings.temperature
            )

            if request.stream:
                # Calling an async-generator function returns the generator
                # directly — awaiting it raises TypeError.
                return self._query_streaming(
                    request_id=request_id,
                    messages=messages,
                    retrieved=retrieved,
                    start_time=start_time,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )

            response = cast(
                LLMResponse,
                await self.llm_client.complete(
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stream=False,
                ),
            )

            latency_ms = (time.perf_counter() - start_time) * 1000

            # Build result
            return RAGResult(
                answer=response.content,
                contexts=retrieved,
                usage={
                    "embedding": query_embedding_result.usage.to_dict(),
                    "generation": response.usage.to_dict(),
                    "total_tokens": query_embedding_result.usage.total_tokens
                    + response.usage.total_tokens,
                },
                latency_ms=latency_ms,
                request_id=request_id,
            )

    async def _query_streaming(
        self,
        request_id: str,
        messages: list[dict[str, str]],
        retrieved: list[RerankResult],
        start_time: float,
        max_tokens: int,
        temperature: float,
    ) -> AsyncIterator[StreamingChunk]:
        """Stream RAG response."""
        stream = cast(
            AsyncIterator[StreamingChunk],
            await self.llm_client.complete(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True,
            ),
        )
        async for chunk in stream:
            yield chunk

    async def ingest_documents(self, documents: list) -> int:
        """Ingest documents into the vector store."""
        await self._ensure_initialized()

        # Generate embeddings
        texts = [doc.content for doc in documents]
        embedding_result = await self.embedding_service.embed(texts)

        # Attach embeddings to documents
        for doc, embedding in zip(documents, embedding_result.embeddings):
            doc.embedding = embedding

        # Upsert to vector store
        vector_store = self.retriever.vector_store
        if vector_store is None:
            vector_store = await get_vector_store()
            self.retriever.vector_store = vector_store

        return await vector_store.upsert(documents)


# Global RAG pipeline
_rag_pipeline_instance: RAGPipeline | None = None


async def get_rag_pipeline() -> RAGPipeline:
    """Get or create global RAG pipeline."""
    global _rag_pipeline_instance

    if _rag_pipeline_instance is None:
        _rag_pipeline_instance = RAGPipeline()

    return _rag_pipeline_instance
