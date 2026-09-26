# DevMate Task — Apply Streaming to `/ask`

Level-2 bridge from Challenge 36: the same three failure modes you just
fixed exist in DevMate's real streaming endpoint. This is a Week-1 (A2)
supporting task — do it after the challenge, before or during the LLM layer.

## Where it lives

`projects/04-ai-engineering/devmate/src/devmate/api/main.py`

- `ask()` — `POST /ask`, line 174
- streaming branch — lines 184–196: `generate()` yields `data: {chunk}\n\n`
  then `data: [DONE]\n\n`, returned as `StreamingResponse` with
  `media_type="text/event-stream"` and an `X-Conversation-ID` header (line 195)
- same pattern again in `rag_query()` (`POST /ai/rag/query`), lines 233–241

## The gaps (verified against the current code)

1. **No disconnect handling.** `generate()` never awaits
   `request.is_disconnected()` — DevMate keeps generating (and billing)
   after the client leaves. This is exactly the Silver-tier failure.
2. **No anti-buffering headers.** The response sets only
   `X-Conversation-ID`; behind nginx the stream will buffer (quiz Q4).
3. **No heartbeat.** An idle stream (slow retrieval, provider stall) gives
   the client and any intermediate proxy no sign of life; both may time out
   and kill a stream that would have recovered.

## The task

1. Add `Request` to the endpoint signature and check
   `await request.is_disconnected()` between chunks in both `generate()`
   functions. On disconnect: stop yielding, log it, and record the wasted
   tokens if the LLM client exposes usage.
2. Add `Cache-Control: no-cache` and `X-Accel-Buffering: no` to both
   streaming responses (keep `X-Conversation-ID`).
3. Add a keepalive: if no chunk has been yielded for N seconds, yield
   `: keepalive\n\n` (an SSE comment — parsers ignore it, proxies don't).
4. Write `tests/unit/test_api_sse.py`: use `TestClient` with a fake RAG
   pipeline (no Qdrant, no LLM, no network) and assert — framing
   (`data: ...\n\n`, `[DONE]` last), the anti-buffering headers, and that a
   disconnecting client stops generation (spy pattern from the challenge).

## Acceptance criteria

- `& .venv\Scripts\python.exe -m pytest tests/unit -q` passes with the new
  test file included.
- ruff and mypy stay clean.
- The engineering decision is written down: in `notes.md`, 5–10 lines on
  SSE vs WebSocket vs chunked JSON for `/ask` — why SSE is the right default
  for one-way token push, and what would force a switch to WebSockets.
- Log any failure you hit in `mistakes.md` (that file is a deliverable).

## Why this task

It converts the challenge's fakes into production code on the vehicle you
are actually shipping, and it closes a real cost leak before A2 wires real
provider tokens through this path.
