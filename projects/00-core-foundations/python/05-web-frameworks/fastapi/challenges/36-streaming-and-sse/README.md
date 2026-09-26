# Challenge 36: Streaming and SSE

DevMate's `/ask` endpoint streams an LLM answer to the browser as Server-Sent
Events. Three things break in production: malformed framing the browser
silently drops, generation that keeps running (and billing) after the user
closes the tab, and a fast provider pumping tokens into unbounded memory
because the client is on hotel Wi-Fi. This challenge makes you fix all three
with measurable guards — never wall-clock time.

Companion material: [`../../36-streaming-and-sse/36-streaming-and-sse-lecture.md`](../../36-streaming-and-sse/36-streaming-and-sse-lecture.md)
and the demo `36-streaming-and-sse.py` (run `--verify`).

---

## Bronze — SSE Framing (~15 min)

**Task:** Implement two pure functions.

`sse_frame(event: dict) -> str` — serialize one event as a correctly framed
SSE event: `data: <json>` followed by a blank line. The browser's
`EventSource` parser treats the blank line as the event terminator; without
it the event never fires.

`parse_sse_stream(chunks: Iterable[str]) -> list[dict]` — reassemble a raw
SSE text stream (arbitrary chunk boundaries) into the parsed event dicts.
Rules: a frame is one or more lines; lines starting with `data: ` carry the
payload (join their payloads with `\n`); lines starting with `:` are
comments/keepalives and are ignored; a frame whose payload is not valid JSON
is skipped, not raised; the final frame may arrive without its trailing
blank line (EOF terminates it).

| Input | Expected |
|---|---|
| `sse_frame({"step": 0})` | `"data: {\"step\": 0}\n\n"` (any valid `json.dumps` spacing) |
| `parse_sse_stream(['data: {"a":1}\n\n'])` | `[{"a": 1}]` |
| `parse_sse_stream(['data: {"a":', '1}\ndata: {"b":2}\n\n'])` | `[{"a": 1}, {"b": 2}]` (frame split mid-JSON) |
| `parse_sse_stream([': keepalive\n\ndata: {"a":1}\n\n'])` | `[{"a": 1}]` (comment ignored) |
| `parse_sse_stream(['data: not-json\n\n'])` | `[]` (bad payload skipped) |
| `parse_sse_stream(['data: {"a":1}'])` | `[{"a": 1}]` (EOF without blank line) |
| `parse_sse_stream([])` | `[]` |

**Constraints:** pure functions, no I/O, no network.

---

## Silver — Disconnect-Aware Token Streaming (~35 min)

**Task:** Implement `token_stream(tokens, request)` as an async generator
that yields tokens one at a time and **stops before yielding anything after
the client disconnects**. `request` is any object with
`async def is_disconnected() -> bool` (duck-typed like Starlette's `Request`).

The naive solutions both fail the guard:

- never checking `is_disconnected()` → keeps yielding to a dead connection;
- checking it exactly once before the loop → a client that leaves mid-stream
  still receives (and you still pay for) every remaining token.

The guard is a spy, not a stopwatch: a `FakeRequest` records when disconnect
flips to `True` and counts every token yielded afterwards. The test asserts
`wasted_tokens == 0` **and** that `is_disconnected()` was awaited at least
once per token boundary (checking between every yield is the contract).

**Signature:**
```python
def token_stream(tokens: Iterable[str], request: Any) -> AsyncIterator[str]:
```

| Scenario | Expected |
|---|---|
| 8 tokens, never disconnects | all 8 yielded, in order |
| disconnects before the 1st token | 0 tokens yielded |
| disconnects after the 3rd token | exactly 3 yielded, `wasted == 0` |
| disconnects after the last token | all 8 yielded, `wasted == 0` |

**Constraints:** check between every yield; no wall-clock assertions.

---

## Gold — Bounded Backpressure Pump (~75 min)

**Task:** Implement `pump(source, queue, sentinel)` as an async task that
drains a fast async producer into a **bounded** `asyncio.Queue` and appends
`sentinel` when the source is exhausted. The consumer may be arbitrarily
slower than the producer; the pump must apply backpressure (await
`queue.put` when full) and must **never materialize the whole stream**.

**Signature:**
```python
async def pump(source: AsyncIterator[str], queue: asyncio.Queue, sentinel: object) -> None:
```

The guard is `tracemalloc`, not wall-clock: the test streams 5,000 chunks of
~200 chars (~1 MB total) through a queue with `maxsize=8` while a slow
consumer drains it. Peak allocated memory must stay under 256 KB — a
solution that collects the source into a list first holds the full ~1 MB and
fails. Correctness guard: the consumer receives all 5,000 chunks **in
order**, then the sentinel.

| Scenario | Expected |
|---|---|
| 5,000 chunks, queue maxsize 8, slow consumer | all chunks in order, then sentinel, peak < 256 KB |
| empty source | sentinel only |
| source raises mid-stream | exception propagates to the consumer's `get()` |

**Follow-up (answer in 2–3 sentences in your notes):** what breaks first at
10^9 chunks — the queue, the consumer, or the network — and what would you
change first? There is no single right answer; the requirement is a
justified one.

---

## Verify

```powershell
# from projects/00-core-foundations/python/
python -m pytest 05-web-frameworks/fastapi/challenges/36-streaming-and-sse/test_challenge.py -q                      # starter: fails loudly
$env:CHALLENGE_USE_SOLUTION = "1"; python -m pytest 05-web-frameworks/fastapi/challenges/36-streaming-and-sse/test_challenge.py -q   # solution: 100% pass
Remove-Item Env:CHALLENGE_USE_SOLUTION
```

All tests run offline: no network, no paid API, no running server — the LLM
and client boundaries are faked with local doubles.
