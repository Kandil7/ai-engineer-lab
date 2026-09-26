"""
Challenge 36: Streaming and SSE — Starter Code
==============================================
Fill in the function bodies. Do not modify signatures.

Run the tests against this file (default) or the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Iterable
from typing import Any


# ---------------------------------------------------------------
# Bronze — SSE framing
# ---------------------------------------------------------------
def sse_frame(event: dict) -> str:
    """Serialize one event as a correctly framed SSE event.

    The browser's EventSource parser fires an event only when it sees the
    blank line that terminates the frame.
    """
    raise NotImplementedError


def parse_sse_stream(chunks: Iterable[str]) -> list[dict]:
    """Reassemble a raw SSE text stream into parsed event dicts.

    Rules: `data: ` lines carry the payload (join multi-line payloads with
    "\\n"); `:` lines are comments/keepalives (ignore); non-JSON payloads are
    skipped; a final frame without its trailing blank line is terminated by
    EOF.
    """
    raise NotImplementedError


# ---------------------------------------------------------------
# Silver — disconnect-aware token streaming
# ---------------------------------------------------------------
def token_stream(tokens: Iterable[str], request: Any) -> AsyncIterator[str]:
    """Async generator: yield tokens one at a time, stop before yielding
    anything after `request.is_disconnected()` turns True.

    Check disconnect between EVERY yield — a single check before the loop
    fails the wasted-token guard.
    """
    raise NotImplementedError


# ---------------------------------------------------------------
# Gold — bounded backpressure pump
# ---------------------------------------------------------------
async def pump(source: AsyncIterator[str], queue: asyncio.Queue, sentinel: object) -> None:
    """Drain `source` into the bounded `queue`, then append `sentinel`.

    Backpressure: await queue.put when the queue is full. Never materialize
    the whole stream — the memory guard fails if you do.
    """
    raise NotImplementedError
