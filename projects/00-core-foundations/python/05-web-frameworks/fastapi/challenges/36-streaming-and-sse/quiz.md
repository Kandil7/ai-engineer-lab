# Challenge 36 Quiz — Streaming and SSE

Answer from the lecture, the demo (`36-streaming-and-sse.py`), and your own
challenge work. Questions 1–3 are mechanics; 4–8 are judgment. Write your
answer before reading the key — the key is at the bottom on purpose.

---

## Questions

**Q1.** An SSE endpoint yields `json.dumps(event)` with no prefix and no
trailing blank line. What exactly does the browser's `EventSource` do, and
what does the developer see?

**Q2.** `StreamingResponse` responses have no `Content-Length` header. Name
one client or infrastructure component that breaks because of this, and the
streaming-vs-buffered rule that keeps you out of trouble.

**Q3.** In the demo's `llm_stream`, `request.is_disconnected()` is awaited
between every token. What does one such check cost, and what does skipping
it cost when a client leaves after 3 of 500 tokens?

**Q4.** The stream works perfectly under `TestClient` and `curl`, but through
the company's nginx proxy the browser shows nothing until the response
completes. Diagnose: which header(s) are missing, and why does nginx behave
this way by default?

**Q5.** A teammate replaces `await asyncio.sleep(0.01)` in the token
generator with `time.sleep(0.01)` "because it's simpler". What is the blast
radius under 50 concurrent streams?

**Q6.** DevMate's `/ask` streaming branch yields `data: {chunk}\n\n` per
token and then `data: [DONE]\n\n`. Why a sentinel instead of just closing
the connection when generation ends?

**Q7.** For each endpoint, choose streaming or buffered and justify in one
line: (a) a 2 KB JSON list of a user's projects; (b) a 500 MB CSV export;
(c) an agent's reasoning tokens; (d) a job's ingestion progress.

**Q8.** Your Gold `pump` uses `asyncio.Queue(maxsize=8)`. A reviewer asks:
"why not `maxsize=0` (unbounded) — it's faster." Give the failure mode in
production terms, and the condition under which the reviewer would be right.

---

## Answer Key

**A1.** The EventSource parser buffers the bytes and waits for the blank
line that terminates a frame; without it the event never dispatches. The
developer sees a connection that is open and transferring data (curl shows
the JSON) while the UI renders nothing — the framing bug is invisible in
curl and fatal in the browser.

**A2.** Anything that needs the body size up front: a download manager
computing progress/ETA, a client allocating a buffer, or a cache/CDN that
refuses to cache responses without a known length. Rule: stream when tokens
or events arrive over time or first-byte latency matters; buffer when the
body is small and ready instantly (most list endpoints).

**A3.** One check is a cheap local socket-state read — microseconds, no
I/O. Skipping it costs the remaining ~497 tokens of billed generation plus
the compute to produce them: output nobody will ever see. The asymmetry
(microtask vs money) is the entire argument for checking every token.

**A4.** Missing `Cache-Control: no-cache` and `X-Accel-Buffering: no`.
nginx buffers a proxied response by default (`proxy_buffering on`) so it can
serve slow upstreams efficiently — it accumulates the whole body (or up to
its buffer size) before forwarding, which defeats streaming. The headers
tell nginx to disable buffering for this response and let bytes through as
they arrive.

**A5.** `time.sleep` blocks the event loop thread for 10 ms per token. With
50 concurrent streams the loop serializes: every stream's tokens wait behind
every other stream's sleeps, so aggregate throughput collapses and unrelated
endpoints on the same loop stall too. The blast radius is the whole server
process, not one connection.

**A6.** Closing the connection is ambiguous: the client cannot distinguish
"generation finished normally" from "the server crashed / the proxy cut the
connection / a timeout fired". The `[DONE]` sentinel is an in-band,
unambiguous end-of-stream marker, so the client can finalize the UI (and
start the next request) with confidence. It is the same pattern OpenAI's
streaming API uses.

**A7.**
(a) Buffered — small, ready instantly; streaming adds framing complexity
for zero latency win.
(b) Streamed — first-byte latency and bounded memory; the client starts
downloading immediately and the server never holds the file.
(c) Streamed — this is the defining UX of chat/agent interfaces; tokens
arrive over time by nature.
(d) Streamed (SSE) — long job, progress must be live; buffered would leave
the user staring at a spinner for minutes.

**A8.** Unbounded, the queue absorbs the producer's rate instead of the
consumer's: a fast provider against a slow client means the server buffers
the entire generation in memory — under concurrency that is an OOM, and it
also hides the backpressure signal the provider could have throttled to.
The reviewer is right only when the consumer is guaranteed as fast as the
producer (or the total stream is provably tiny), e.g. piping between two
in-process tasks with matched rates. The moment the rate mismatch is
client-controlled, bounded is the only safe default.
