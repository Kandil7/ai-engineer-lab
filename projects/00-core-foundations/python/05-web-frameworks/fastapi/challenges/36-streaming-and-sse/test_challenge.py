"""
Challenge 36: Streaming and SSE — Tests
=======================================
Default run targets the learner's starter.py and MUST FAIL (NotImplementedError)
until the challenge is solved.

Validate the reference solution with:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 05-web-frameworks/fastapi/challenges/36-streaming-and-sse/test_challenge.py -q

Guards use spies and tracemalloc — never wall-clock time. Fully offline.
"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import tracemalloc
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402


# =====================================================================
# Fakes (local doubles — no network, no server)
# =====================================================================
class FakeRequest:
    """Duck-typed Starlette Request whose disconnect flips on schedule.

    `disconnect_after` = number of tokens that may be yielded before
    disconnect flips True. Records every check and every post-disconnect
    yield the stream makes.
    """

    def __init__(self, tokens: list[str], disconnect_after: int | None) -> None:
        self._tokens = tokens
        self._disconnect_after = disconnect_after
        self.checks = 0
        self.yielded_after_disconnect = 0
        self._yield_count = 0

    async def is_disconnected(self) -> bool:
        self.checks += 1
        if self._disconnect_after is None:
            return False
        return self._yield_count >= self._disconnect_after

    def note_yield(self) -> None:
        self._yield_count += 1
        if self._disconnect_after is not None and self._yield_count > self._disconnect_after:
            self.yielded_after_disconnect += 1


class SpyStream:
    """Wraps the challenge's token_stream to count post-disconnect yields."""

    def __init__(self, request: FakeRequest) -> None:
        self._request = request

    async def run(self, tokens: list[str]) -> list[str]:
        out = []
        async for tok in mod.token_stream(tokens, self._request):
            self._request.note_yield()
            out.append(tok)
        return out


# =====================================================================
# Bronze — SSE framing
# =====================================================================
class TestSseFrame:
    def test_frame_shape(self):
        frame = mod.sse_frame({"step": 0})
        assert frame.startswith("data: ")
        assert frame.endswith("\n\n")
        assert json.loads(frame[len("data: ") :].strip()) == {"step": 0}

    def test_frame_roundtrip_through_parser(self):
        event = {"step": 3, "message": "ingesting file 4/10"}
        assert mod.parse_sse_stream([mod.sse_frame(event)]) == [event]

    def test_frame_is_two_distinct_events(self):
        stream = mod.sse_frame({"a": 1}) + mod.sse_frame({"b": 2})
        assert mod.parse_sse_stream([stream]) == [{"a": 1}, {"b": 2}]


class TestParseSseStream:
    def test_single_frame(self):
        assert mod.parse_sse_stream(['data: {"a":1}\n\n']) == [{"a": 1}]

    def test_frame_split_mid_json(self):
        # network chunks do not align with lines: the boundary can fall
        # mid-JSON without any newline at the split point
        chunks = ['data: {"a":', '1}\n\ndata: {"b":2}\n\n']
        assert mod.parse_sse_stream(chunks) == [{"a": 1}, {"b": 2}]

    def test_comment_keepalive_ignored(self):
        assert mod.parse_sse_stream([': keepalive\n\ndata: {"a":1}\n\n']) == [{"a": 1}]

    def test_bad_json_skipped_not_raised(self):
        assert mod.parse_sse_stream(["data: not-json\n\n"]) == []

    def test_eof_without_blank_line(self):
        assert mod.parse_sse_stream(['data: {"a":1}']) == [{"a": 1}]

    def test_empty_stream(self):
        assert mod.parse_sse_stream([]) == []

    def test_multi_line_payload_joined(self):
        # a frame with two `data: ` lines: their payloads join with "\n"
        chunks = ['data: {"a":\ndata: 1}\n\n']
        assert mod.parse_sse_stream(chunks) == [{"a": 1}]

    def test_awkward_one_char_chunks(self):
        text = 'data: {"n": 42}\n\ndata: {"n": 43}\n\n'
        assert mod.parse_sse_stream(list(text)) == [{"n": 42}, {"n": 43}]


# =====================================================================
# Silver — disconnect-aware token streaming
# =====================================================================
def _run_stream(tokens: list[str], disconnect_after: int | None) -> tuple[list[str], FakeRequest]:
    request = FakeRequest(tokens, disconnect_after)
    received = asyncio.run(SpyStream(request).run(tokens))
    return received, request


class TestTokenStream:
    TOKENS = [f"t{i} " for i in range(8)]

    def test_no_disconnect_yields_all(self):
        received, request = _run_stream(self.TOKENS, None)
        assert received == self.TOKENS
        assert request.checks >= len(self.TOKENS), "must check disconnect between every yield"

    def test_disconnect_before_first_token(self):
        received, request = _run_stream(self.TOKENS, 0)
        assert received == []
        assert request.yielded_after_disconnect == 0

    def test_disconnect_mid_stream_zero_wasted(self):
        received, request = _run_stream(self.TOKENS, 3)
        assert received == self.TOKENS[:3]
        assert request.yielded_after_disconnect == 0, "no token may be yielded after disconnect"

    def test_disconnect_after_last_token(self):
        received, request = _run_stream(self.TOKENS, 8)
        assert received == self.TOKENS
        assert request.yielded_after_disconnect == 0

    def test_check_per_yield_contract(self):
        # A solution that checks once before the loop yields everything to a
        # dead client — the spy catches it via wasted_after_disconnect.
        received, request = _run_stream(self.TOKENS, 2)
        assert request.checks >= len(received), "disconnect must be checked at every token boundary"
        assert request.yielded_after_disconnect == 0


# =====================================================================
# Gold — bounded backpressure pump
# =====================================================================
SENTINEL = object()


async def _fast_producer(n: int, size: int):
    """Deterministic producer: n chunks of `size` chars, no awaits."""
    for i in range(n):
        yield f"chunk-{i:06d}-" + "x" * size


async def _slow_consumer(queue: asyncio.Queue, expected: int):
    """Drains the queue, yielding control between gets (deterministic pacing).

    Validates order incrementally and DISCARDS each chunk — the memory guard
    measures the pump, not the test's own bookkeeping.
    """
    errors = None
    seen = 0
    while True:
        await asyncio.sleep(0)
        item = await queue.get()
        if item is SENTINEL:
            break
        if isinstance(item, BaseException):
            errors = item
            break
        assert item == f"chunk-{seen:06d}-" + "x" * 180, f"out of order at {seen}: {item[:20]}"
        seen += 1
        if seen > expected:
            break
    return seen, errors


def _run_pump(n: int, maxsize: int, source=None):
    """Run pump + consumer concurrently; surface a pump crash instead of
    deadlocking on queue.get() (an unsolved starter raises before putting
    anything — the consumer must not wait forever)."""

    async def _scenario():
        queue: asyncio.Queue = asyncio.Queue(maxsize=maxsize)
        src = source if source is not None else _fast_producer(n, 180)
        task = asyncio.create_task(mod.pump(src, queue, SENTINEL))
        consumer = asyncio.create_task(_slow_consumer(queue, n))
        done, pending = await asyncio.wait(
            {task, consumer}, return_when=asyncio.FIRST_EXCEPTION, timeout=30
        )
        if task in done:
            exc = task.exception()
            if exc is not None:
                consumer.cancel()
                raise exc  # surface the learner's error directly
        if not done:  # timeout: neither side finished — deadlock, fail loudly
            for t in (task, consumer):
                t.cancel()
            raise AssertionError("pump/consumer deadlocked (no sentinel, no exception)")
        seen, errors = consumer.result()
        await task
        return seen, errors

    return asyncio.run(_scenario())


class TestPump:
    N = 5000
    CHUNK_SIZE = 180  # ~0.9 MB total — a materializing solution fails the guard

    def test_all_chunks_in_order_then_sentinel(self):
        seen, errors = _run_pump(self.N, maxsize=8)
        assert errors is None
        assert seen == self.N

    def test_empty_source_yields_sentinel_only(self):
        async def empty():
            return
            yield  # pragma: no cover — makes this an async generator

        seen, errors = _run_pump(0, maxsize=8, source=empty())
        assert seen == 0
        assert errors is None

    def test_source_exception_propagates_to_consumer(self):
        class Boom(Exception):
            pass

        async def bad_source():
            yield "chunk-a"
            raise Boom("provider died")

        async def _scenario():
            queue: asyncio.Queue = asyncio.Queue(maxsize=4)
            task = asyncio.create_task(mod.pump(bad_source(), queue, SENTINEL))
            first = await asyncio.wait_for(queue.get(), timeout=10)
            item = await asyncio.wait_for(queue.get(), timeout=10)
            await task
            return first, item

        first, item = asyncio.run(_scenario())
        assert first == "chunk-a"
        assert isinstance(item, Boom), "the source's exception must reach the consumer"

    def test_memory_guard_no_materialization(self):
        tracemalloc.start()
        try:
            seen, errors = _run_pump(self.N, maxsize=8)
            assert errors is None
            assert seen == self.N
            peak = tracemalloc.get_traced_memory()[1]
        finally:
            tracemalloc.stop()
        # 5000 * ~188 chars ≈ 0.9 MB; a collect-then-enqueue solution holds it all
        assert peak < 256 * 1024, (
            f"peak {peak / 1024:.0f} KB — the stream was materialized; "
            "pump must apply backpressure, not buffer the world"
        )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
