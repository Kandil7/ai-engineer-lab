"""Unit tests for DevMate's SSE streaming (devmate.api.main).

Covers the three production failure modes fixed in the streaming endpoints:
client disconnect (stop generating), anti-buffering headers, and keepalive
on idle streams. No Qdrant, no LLM, no network — the RAG pipeline is faked.
"""

import asyncio
from collections.abc import AsyncIterator
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi.testclient import TestClient

from devmate.api import main as api_main
from devmate.api.main import _sse_events, app


class FakeRequest:
    """Duck-typed Starlette Request; disconnect flips after N yields."""

    def __init__(self, disconnect_after: int | None) -> None:
        self._disconnect_after = disconnect_after
        self._yield_count = 0
        self.checks = 0

    async def is_disconnected(self) -> bool:
        self.checks += 1
        if self._disconnect_after is None:
            return False
        return self._yield_count >= self._disconnect_after

    def note_yield(self) -> None:
        self._yield_count += 1


def _fake_pipeline(stream_chunks: list[str]):
    """Return an async factory standing in for get_rag_pipeline."""

    class FakePipeline:
        async def query(self, request: Any):
            if not request.stream:
                return SimpleNamespace(
                    answer="full answer", contexts=[], usage=None, latency_ms=1.0
                )

            async def _stream() -> AsyncIterator[Any]:
                for text in stream_chunks:
                    await asyncio.sleep(0)
                    yield SimpleNamespace(content=text)

            return _stream()

    async def _get() -> FakePipeline:
        return FakePipeline()

    return _get


def _collect(gen: AsyncIterator[str], request: FakeRequest) -> list[str]:
    async def _run() -> list[str]:
        out = []
        async for event in gen:
            request.note_yield()
            out.append(event)
        return out

    return asyncio.run(_run())


# =====================================================================
# _sse_events — framing, disconnect, keepalive, error propagation
# =====================================================================
def test_sse_frames_chunks_and_ends_with_done() -> None:
    async def source():
        for text in ["a", "b", "c"]:
            yield SimpleNamespace(content=text)

    request = FakeRequest(disconnect_after=None)
    events = _collect(_sse_events(source(), request, lambda c: c.content), request)
    assert events == ["data: a\n\n", "data: b\n\n", "data: c\n\n", "data: [DONE]\n\n"]
    # disconnect is checked at every data-event boundary (3 chunks)
    assert request.checks >= 3


def test_sse_stops_on_disconnect_with_zero_wasted() -> None:
    async def source():
        for i in range(10):
            yield SimpleNamespace(content=f"chunk-{i}")

    request = FakeRequest(disconnect_after=3)
    events = _collect(_sse_events(source(), request, lambda c: c.content), request)
    assert events == ["data: chunk-0\n\n", "data: chunk-1\n\n", "data: chunk-2\n\n"]
    assert "data: [DONE]\n\n" not in events, (
        "a disconnected stream must not claim normal completion"
    )


def test_sse_keepalive_during_idle() -> None:
    async def source():
        await asyncio.sleep(0.2)  # longer than the keepalive window below
        yield SimpleNamespace(content="late")

    request = FakeRequest(disconnect_after=None)
    events = _collect(
        _sse_events(source(), request, lambda c: c.content, keepalive_after=0.05), request
    )
    keepalives = [e for e in events if e.startswith(":")]
    assert keepalives, "an idle stream must emit keepalive comments"
    assert events[-1] == "data: [DONE]\n\n"
    assert events[-2] == "data: late\n\n"


def test_sse_source_exception_propagates() -> None:
    class Boom(Exception):
        pass

    async def source():
        yield SimpleNamespace(content="ok")
        raise Boom("provider died")

    request = FakeRequest(disconnect_after=None)
    with pytest.raises(Boom):
        _collect(_sse_events(source(), request, lambda c: c.content), request)


# =====================================================================
# POST /ask streaming — end to end through TestClient
# =====================================================================
@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setattr(api_main, "get_rag_pipeline", _fake_pipeline(["Hello", " ", "world"]))
    return TestClient(app)


def test_ask_stream_framing_and_headers(client: TestClient) -> None:
    response = client.post("/ask", json={"question": "hi", "stream": True})
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert response.headers["cache-control"] == "no-cache"
    assert response.headers["x-accel-buffering"] == "no"
    assert response.headers["x-conversation-id"]

    events = [line for line in response.text.split("\n") if line.startswith("data: ")]
    assert events == ["data: Hello", "data:  ", "data: world", "data: [DONE]"]


def test_ask_non_stream_returns_answer(client: TestClient) -> None:
    response = client.post("/ask", json={"question": "hi", "stream": False})
    assert response.status_code == 200
    payload = response.json()
    assert payload["answer"] == "full answer"
    assert payload["sources"] == []
    assert payload["conversation_id"]
