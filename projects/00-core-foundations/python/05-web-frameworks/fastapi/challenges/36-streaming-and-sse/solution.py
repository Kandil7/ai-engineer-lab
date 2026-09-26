"""
Challenge 36: Streaming and SSE — Reference Solution
====================================================
Each docstring says WHY, not just what.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator, Iterable
from typing import Any


# ---------------------------------------------------------------
# Bronze — SSE framing
# ---------------------------------------------------------------
def sse_frame(event: dict) -> str:
    """Frame one SSE event.

    WHY the trailing blank line: the EventSource parser dispatches an event
    only when it hits the empty line that terminates the frame. Without it
    the browser buffers forever and the event never fires — the classic
    "stream works in curl, UI shows nothing" bug.
    """
    return f"data: {json.dumps(event)}\n\n"


def parse_sse_stream(chunks: Iterable[str]) -> list[dict]:
    """Reassemble a chunked SSE text stream into event dicts.

    WHY buffer-then-split: chunk boundaries are arbitrary — a frame can be
    split mid-JSON across chunks, so parsing per-chunk is wrong. Accumulate
    into one buffer, split on the frame terminator "\\n\\n", and flush the
    trailing partial frame at EOF (the spec allows a final frame without its
    blank line).
    """
    events: list[dict] = []
    buffer = ""
    for chunk in chunks:
        buffer += chunk
        while "\n\n" in buffer:
            frame, buffer = buffer.split("\n\n", 1)
            event = _parse_frame(frame)
            if event is not None:
                events.append(event)
    # EOF terminates a final frame that lacks its blank line
    if buffer.strip():
        event = _parse_frame(buffer)
        if event is not None:
            events.append(event)
    return events


def _parse_frame(frame: str) -> dict | None:
    """Parse one SSE frame; WHY skip-not-raise: a keepalive or a partial
    write must never kill the whole stream — drop the bad frame, keep going."""
    payload_lines = []
    for line in frame.split("\n"):
        if line.startswith(":"):
            continue  # comment / keepalive
        if line.startswith("data: "):
            payload_lines.append(line[len("data: ") :])
        elif line.startswith("data:"):
            payload_lines.append(line[len("data:") :].lstrip(" "))
    if not payload_lines:
        return None
    payload = "\n".join(payload_lines)
    try:
        parsed = json.loads(payload)
    except (json.JSONDecodeError, ValueError):
        return None
    return parsed if isinstance(parsed, dict) else None


# ---------------------------------------------------------------
# Silver — disconnect-aware token streaming
# ---------------------------------------------------------------
async def token_stream(tokens: Iterable[str], request: Any) -> AsyncIterator[str]:
    """Yield tokens; stop before yielding anything after disconnect.

    WHY check between EVERY yield: is_disconnected() is a cheap local socket
    state read, while each yielded token is a billed LLM output token. The
    asymmetry is the whole argument — skipping the check to save a microtask
    costs real money the moment a client leaves mid-generation. Checking only
    once before the loop misses every disconnect that happens later, which is
    the common case (users read the first tokens, then close the tab).
    """
    for tok in tokens:
        if await request.is_disconnected():
            return
        yield tok


# ---------------------------------------------------------------
# Gold — bounded backpressure pump
# ---------------------------------------------------------------
async def pump(source: AsyncIterator[str], queue: asyncio.Queue, sentinel: object) -> None:
    """Drain a fast producer into a bounded queue, then append the sentinel.

    WHY bounded + awaited put: an unbounded queue converts backpressure into
    memory growth — the server buffers the provider's output at the provider's
    rate, not the client's. Awaiting put on a maxsize-bounded queue makes the
    producer wait for the consumer, which is what "backpressure" means. The
    sentinel lets the consumer detect normal end-of-stream without relying on
    connection close (which can also mean an error).
    """
    try:
        async for chunk in source:
            await queue.put(chunk)
    except BaseException as exc:
        # WHY enqueue the exception: the consumer is the only party that can
        # react to it — a task that dies silently leaves the consumer waiting
        # on get() forever, and re-raising in the task would surface the error
        # in a place nobody is watching.
        await queue.put(exc)
    finally:
        await queue.put(sentinel)
