# Learning Path: FastAPI AI Services

**Last updated:** 2026-08-02

**Goal:** build and serve the Python AI layer — RAG, embeddings, agents — as a production API.

**Primary project:** `projects/04-ai-engineering/devmate/` (week 4 of the
[active track](../../roadmap/active-track-10-week.md))

> **Status note.** Under [ADR-0004](../../decisions/0004-adopt-10-week-ai-engineer-track.md)
> this service is standalone — the Go backend track was retired to focus on AI Engineering.
> The `/ai/*` contract below stays valid.
>
> **Coverage note.** `projects/00-core-foundations/python/05-web-frameworks/fastapi/` already
> contains 25 topics with a matching exercise for each. The fundamentals below are largely
> done — the value now is in sections 3–6, the production patterns.

---

## Milestones

1. **FastAPI fundamentals** — routers, dependency injection, middleware, Pydantic validation.
   *(largely complete — see `05-web-frameworks/fastapi/`)*
2. **LLM integration** — chat endpoint, structured outputs, streaming.
3. **Embeddings + Qdrant** — embed, upsert with metadata, similarity search.
4. **RAG endpoint** — `/ai/rag/query`: chunk → embed → retrieve → rerank → LLM → cited answer.
5. **Agents + tool calling** — agent loop, tool registry, memory, step caps.
6. **Eval + cost** — token accounting, latency budget, eval harness (`evaluations/rag/`).

---

## 1. The 20% that unlocks 80%

- Pydantic models as the request/response contract — not raw dicts on anything that matters
- Async endpoints and background tasks; knowing when async actually helps
- Embedding dimensions and distance metrics in Qdrant
- Prompt structure: system + context + question; faithfulness vs. hallucination

---

## 2. Why FastAPI for AI work

A trained model or an LLM pipeline is only useful when something else can call it. FastAPI is
the standard way to put an HTTP surface on Python AI code: Pydantic validation, automatic
`/docs`, native async, and low ceremony.

`/docs` (Swagger UI) is worth calling out specifically — it lets you exercise every endpoint
visually without Postman or curl, which matters most in the early days of a service.

---

## 3. Pydantic as the contract

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class PredictionRequest(BaseModel):
    text: str
    max_length: int = 100


class PredictionResponse(BaseModel):
    text: str
    label: str
    confidence: float


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    result = run_model(request.text)
    return PredictionResponse(
        text=request.text,
        label=result["label"],
        confidence=result["confidence"],
    )
```

Wrong types produce an automatic 422 with a precise error body — no hand-written validation.
`response_model` additionally guarantees the shape of what you return, catching drift between
the code and the documented contract.

---

## 4. Production patterns

### Load heavy resources once

```python
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load("model.pkl")  # startup — once
    app.state.qdrant = QdrantClient(...)
    yield
    app.state.qdrant.close()  # shutdown


app = FastAPI(lifespan=lifespan)
```

**Loading a model inside the request handler is the most common serious mistake in AI
services.** It multiplies latency by the load time on every single call.

### Health endpoint

```python
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}
```

Required by orchestrators and uptime monitors to know whether the process is alive. Consider a
separate `/ready` that also checks Qdrant and Redis connectivity — liveness and readiness are
different questions.

### Explicit errors

```python
from fastapi import HTTPException

if not input_data.text.strip():
    raise HTTPException(status_code=400, detail="Text must not be empty")
```

Return a clear error rather than letting an exception surface as a 500.

### Async where it pays

```python
@app.post("/ask")
async def ask(request: AskRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(LLM_URL, json=payload)
    return response.json()
```

Async lets the server handle other requests while waiting on I/O. For CPU-bound local
inference it buys little. For **calls to an external LLM API — the dominant case here — it
matters a great deal**, since those calls take seconds.

### Streaming — essential for LLMs

```python
from fastapi.responses import StreamingResponse


async def generate_tokens(prompt: str):
    async for token in llm_stream(prompt):
        yield f"data: {token}\n\n"


@app.post("/ask")
async def ask(prompt: str):
    return StreamingResponse(generate_tokens(prompt), media_type="text/event-stream")
```

Without streaming, the user stares at nothing for several seconds. Time-to-first-token is the
latency metric users actually perceive.

### Dependency injection for cross-cutting concerns

```python
from fastapi import Depends, Header, HTTPException


def verify_api_key(x_api_key: str = Header(...)) -> str:
    if not is_valid(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


@app.post("/ask")
def ask(request: AskRequest, api_key: str = Depends(verify_api_key)): ...
```

Auth, rate limiting, database sessions, and tracing all belong here rather than repeated in
each handler.

---

## 5. Project structure

```text
devmate/src/devmate/api/
├── main.py              # app + lifespan
├── deps.py              # shared dependencies
├── routers/
│   ├── ask.py           # /ask   — streaming Q&A
│   ├── ingest.py        # /ingest — repo ingestion
│   └── health.py        # /health, /ready
└── middleware/
    ├── ratelimit.py
    └── auth.py
```

Routers keep `main.py` small and make each surface independently testable:

```python
# routers/ask.py
from fastapi import APIRouter

router = APIRouter(prefix="/ask", tags=["qa"])

# main.py
app.include_router(ask.router)
```

---

## 6. Deployment

```bash
# development
uvicorn devmate.api.main:app --reload

# production — no --reload
uvicorn devmate.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry && \
    poetry export -f requirements.txt --output requirements.txt && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /install /usr/local
WORKDIR /app
COPY src/ ./src/
CMD ["uvicorn", "devmate.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Multi-stage keeps build tooling out of the runtime image. Note that free-tier hosts sleep on
idle — a recruiter clicking a cold link waits ~30s, so add a keep-warm ping or say so in the
README.

---

## API surface (target)

`/health` · `/ready` · `/ask` (SSE) · `/ingest` · `/ai/embeddings` · `/ai/agents/run`

---

## Self-check

Can you explain: the RAG pipeline stages · embedding vs. token · tool calling · agent vs.
chatbot · recall@k vs. faithfulness · **why the model loads at startup rather than per
request** · **when async helps and when it doesn't** · **why streaming changes perceived
latency**?

---

## Related

- [`../../reference/llm-production-architecture.md`](../../reference/llm-production-architecture.md)
  — the layers around the API
- [`../../roadmap/active-track-10-week.md`](../../roadmap/active-track-10-week.md) — week 4
- [`rag-qdrant.md`](rag-qdrant.md)
- fastapi.tiangolo.com/tutorial — sufficient on its own

## ملخص عربي (Arabic Summary)

مسار FastAPI لطبقة الذكاء: RAG وembeddings وagents كخدمة Python.
أهم النقاط الإنتاجية: تحميل الموديل مرة واحدة عند بدء التشغيل مش مع كل request،
و`/health` endpoint للمراقبة، والـ streaming لأن الـ LLM بياخد ثواني مش milliseconds،
و Pydantic كعقد واضح للـ request والـ response، مع تتبع التكلفة والجودة.
