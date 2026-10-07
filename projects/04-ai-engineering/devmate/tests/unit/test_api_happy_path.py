"""Happy-path tests for DevMate's HTTP surface (devmate.api.main).

Covers the endpoints test_api_sse.py does not: liveness, root, usage,
traces, readiness shape, ingest validation + happy path, and the
non-streaming RAG query. No Qdrant, no LLM, no network: the RAG pipeline,
document loader, and chunker are faked via monkeypatch, following the
pattern in test_api_sse.py.
"""

from types import SimpleNamespace
from typing import Any

import pytest
from fastapi.testclient import TestClient

from devmate.api import main as api_main
from devmate.api.main import app


def _fake_pipeline(answer: str = "canned answer", n_contexts: int = 1):
    """RAG pipeline double: non-stream query returns a fixed result."""

    class FakePipeline:
        async def query(self, request: Any):
            assert not request.stream
            return SimpleNamespace(
                answer=answer,
                contexts=[
                    SimpleNamespace(
                        id=f"ctx-{i}",
                        content=f"content {i}",
                        metadata={"file": f"f{i}.py"},
                        score=0.9,
                    )
                    for i in range(n_contexts)
                ],
                usage={"prompt_tokens": 10, "completion_tokens": 5},
                latency_ms=2.0,
                request_id="req-test",
            )

        async def ingest_documents(self, documents: list) -> int:
            return len(documents) * 2

    async def _get() -> FakePipeline:
        return FakePipeline()

    return _get


class _FakeChunker:
    pass


def _fake_get_chunker(*args: Any, **kwargs: Any) -> _FakeChunker:
    """get_chunker double accepting the real call signature."""
    return _FakeChunker()


class _FakeLoader:
    """DocumentLoader double yielding two fixed documents."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def load_repository(self, path: object):
        yield SimpleNamespace(
            content="def f():\n    pass\n",
            metadata={"extension": ".py", "language": "python"},
        )
        yield SimpleNamespace(
            content="# title\n",
            metadata={"extension": ".md", "language": "markdown"},
        )


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setattr(api_main, "get_rag_pipeline", _fake_pipeline())
    monkeypatch.setattr(api_main, "DocumentLoader", _FakeLoader)
    monkeypatch.setattr(api_main, "get_chunker", _fake_get_chunker)
    return TestClient(app)


def test_health_reports_healthy() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "healthy"
    assert payload["components"] == {"api": "ok"}


def test_root_describes_service() -> None:
    payload = TestClient(app).get("/").json()
    assert payload["name"] == "DevMate API"
    assert payload["health"] == "/health"


def test_usage_shape_with_zero_traffic() -> None:
    payload = TestClient(app).get("/ai/usage").json()
    assert set(payload) >= {
        "total_requests",
        "total_tokens",
        "total_cost_usd",
        "avg_latency_ms",
        "by_model",
        "by_provider",
    }
    assert isinstance(payload["total_requests"], int)


def test_usage_rejects_bad_date() -> None:
    response = TestClient(app).get("/ai/usage", params={"since": "not-a-date"})
    assert response.status_code == 400


def test_traces_returns_list() -> None:
    payload = TestClient(app).get("/traces").json()
    assert isinstance(payload["traces"], list)


def test_ready_reports_shape_offline() -> None:
    """Without services running every dependency degrades, honestly."""
    payload = TestClient(app).get("/ready").json()
    assert payload["status"] == "degraded"
    assert set(payload["components"]) == {"api", "qdrant", "redis", "llm"}
    assert payload["components"]["api"] == "ok"


def test_ingest_missing_path_is_404(client: TestClient, tmp_path: object) -> None:
    response = client.post("/ingest", json={"repo_path": str(tmp_path) + "/nope"})
    assert response.status_code == 404


def test_ingest_happy_path(client: TestClient, tmp_path: object) -> None:
    repo = str(tmp_path)
    response = client.post("/ingest", json={"repo_path": repo})
    assert response.status_code == 200
    payload = response.json()
    assert payload["documents_ingested"] == 2
    assert payload["chunks_created"] == 4
    assert payload["elapsed_ms"] >= 0


def test_rag_query_non_stream(client: TestClient) -> None:
    response = client.post("/ai/rag/query", json={"query": "what?", "stream": False})
    assert response.status_code == 200
    payload = response.json()
    assert payload["answer"] == "canned answer"
    assert payload["contexts"] == [
        {
            "id": "ctx-0",
            "content": "content 0",
            "metadata": {"file": "f0.py"},
            "score": 0.9,
        }
    ]
    assert payload["usage"] == {"prompt_tokens": 10, "completion_tokens": 5}
    assert payload["request_id"] == "req-test"
