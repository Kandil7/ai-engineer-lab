# Glossary: Reliability and Distributed Systems Patterns

Quick-reference table of every term used in Lecture 01, followed by detailed definitions with runnable or verifiable examples. Where a pattern is illustrated, the example is drawn from this repository's own services — DevMate's LLM client, embedding service, API stream pump, or the Compose/CI infrastructure — so each definition maps to code you can open.

## Quick Reference Table

| Term | Definition | Lecture section |
|------|------------|-----------------|
| Availability | Fraction of time a service answers correctly, not just answers at all | 12 |
| Backpressure | Signal from a slow consumer to a fast producer to slow down | 7 |
| Bulkhead | Isolated pool per dependency so one outage cannot drain shared capacity | 6 |
| Cache Stampede | Thundering herd of recomputations when a hot key expires | 12 |
| Circuit Breaker | Proxy that stops calling a failing dependency after a threshold | 5 |
| Closed | Normal breaker state; calls pass through and failures are counted | 5 |
| Connection Pool | Bounded set of reusable network connections to a dependency | 6 |
| Deadline | Absolute time budget passed down a call chain as remaining time | 2 |
| Dead-Letter Queue | Queue that captures messages which exhausted retries | 8 |
| Deduplication | Suppressing a repeated side effect by key or natural key | 4 |
| Error Budget | Allowed unreliability derived from an SLO; spending it pauses feature work | 15 |
| Eventual Consistency | Reads may lag writes by a bounded, documented delay | 13 |
| Exponential Backoff | Doubling wait between retries to give a recovering dependency room | 3 |
| Fallback | Pre-programmed lower-tier response when the primary path fails | 1, 14 |
| Fallback Chain | Ordered list of providers tried until one succeeds | 14 |
| Full Jitter | Randomizing each backoff wait uniformly in `[0, backoff]` | 3 |
| Graceful Degradation | Serving a reduced but correct answer instead of an error | 14 |
| Graceful Shutdown | Stop accepting, drain in-flight work, then exit | 9 |
| Half-Open | Breaker trial state allowing a limited number of probe calls | 5 |
| Idempotency | Performing an operation multiple times yields the same result as once | 4 |
| Idempotency Key | Client- or queue-supplied unique key used to dedupe retries | 4 |
| Latency | Time from request accepted to response delivered | 15 |
| MTBF | Mean time between failures of a component | 15 |
| MTTR | Mean time to restore service after a failure | 15 |
| Negative Caching | Caching a miss or error result for a short TTL | 12 |
| Natural Key | Domain-unique identifier (hash of content) used instead of a synthetic key | 4 |
| Open | Breaker state that fails fast without calling the dependency | 5 |
| Outbox | Table written in the same transaction as the state change, drained asynchronously | 4 |
| Poison Message | Message that fails permanently and would loop forever without a DLQ | 8 |
| Rate Limit | Cap on requests per caller per window | 10 |
| Rate Limit Headers | `X-RateLimit-*` / `Retry-After` contract returned to clients | 10 |
| Read-Your-Writes | Guarantee that a caller immediately sees their own writes | 13 |
| Read Timeout | Max time to receive a complete response after the connection is established | 2 |
| RED Metrics | Rate, Errors, Duration — the three signals for request-path health | 15 |
| Reliability | Probability a system performs its function correctly for a period | 1 |
| Request Coalescing | Collapse concurrent identical lookups into one upstream call | 12 |
| Retry | Re-attempting a failed call, the most common and most dangerous defense | 3 |
| Retry-After | Server-suggested delay a client must honor before retrying | 3, 10 |
| Saturation | How close a resource is to capacity; the leading indicator of latency | 15 |
| Single-Flight | At most one in-flight computation per cache key | 12 |
| SLI | Measured indicator of service quality (latency, error rate, throughput) | 15 |
| SLO | Target value for one or more SLIs over a window | 15 |
| Stop Grace Period | Container runtime window between SIGTERM and SIGKILL | 9 |
| Timeout | Hard bound on how long an operation may take | 2 |
| Token Bucket | Rate limiter that refills tokens at a fixed rate and spends per request | 10 |
| Transactional Outbox | See Outbox; publication is atomic with the write that caused it | 4 |
| TTL | Time-to-live; the max age of a cached entry | 12 |

## Detailed Definitions

### Timeout

A timeout is the maximum wall-clock time an operation is allowed to take before the caller treats it as failed. Every outbound network call must carry one; an unbounded call converts a transient fault into a permanent occupation of a worker slot, a connection, and often a thread.

This repository splits connect from read on every HTTP client it owns:

```python
# llm/client.py:146 — LLM chat calls
self._client = httpx.AsyncClient(
    timeout=httpx.Timeout(60.0, connect=10.0),
    ...
)
# index/embeddings.py:73 — OpenAI embeddings
self._client = httpx.AsyncClient(
    timeout=httpx.Timeout(60.0, connect=10.0),
    ...
)
# retrieve/retriever.py:56 — Cohere reranker
self._client = httpx.AsyncClient(
    timeout=httpx.Timeout(30.0, connect=10.0),
)
```

Connect should stay tight (a TCP+TLS handshake that has not completed in 5–10 seconds will rarely recover within the request). Read should reflect the slowest legitimate response — an LLM token stream legitimately takes minutes, so its read timeout is larger than a reranker's.

The gap in this codebase is documented and intentional teaching material: `index/vector_store.py:101` constructs `QdrantClient(...)` with no `timeout=` argument, so Qdrant calls inherit the client library's default rather than a policy the service chose. The lecture's exercise has you close that gap.

### Deadline

A deadline is an absolute point in time by which the whole operation must complete, propagated down every layer as *remaining budget*. Unlike a per-attempt timeout, a deadline bounds the total time including retries, queue waits, and fallbacks.

```python
import time


class Deadline:
    def __init__(self, budget_s: float):
        self._expires_at = time.monotonic() + budget_s

    def remaining(self) -> float:
        return max(0.0, self._expires_at - time.monotonic())

    def expired(self) -> bool:
        return self.remaining() <= 0.0

    def slice_for(self, attempts_left: int) -> float:
        """Give each remaining attempt an equal slice of what is left."""
        return self.remaining() / max(1, attempts_left)
```

The rule the lecture drills: never start an attempt that cannot finish inside the remaining budget. A retry loop with a 2-second deadline and 3 attempts must refuse the third attempt at t=1.9s instead of starting it and blowing past the caller's patience.

### Retry

A retry is a re-attempt of a failed call. Retries are the most common reliability defense and the most common cause of self-inflicted outages: retried storms multiply load on exactly the dependency that is already failing.

The classification rule separates what is safe to retry from what is not:

| Class | Examples | Retry? |
|-------|----------|--------|
| Transient network | connect reset, DNS blip, `httpx.ConnectError` | yes |
| Timeout | `httpx.TimeoutException` | often, with deadline check |
| Server error | HTTP 5xx | yes |
| Rate limited | HTTP 429 | yes, honoring `Retry-After` |
| Client error | HTTP 4xx | no — the same request will fail again |
| Validation | local schema or content validation | no |

DevMate applies exactly this classification with tenacity:

```python
# llm/client.py:157-162
@retry(
    wait=wait_exponential_jitter(initial=1, max=30),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
    reraise=True,
)
async def chat(self, ...): ...
```

429 is mapped to `LLMRateLimitError` and 401 to an auth error (`llm/client.py:214-219`); neither is silently swallowed into a generic retry.

### Exponential Backoff

Backoff is the wait between retries. Exponential backoff multiplies a base delay by a factor (classically 2) each attempt: 1s, 2s, 4s, 8s... Its purpose is to give a recovering dependency room instead of hammering it at the original rate.

The failure mode of naive exponential backoff is *synchronization*: every caller that failed at the same moment retries at the same delay, producing a synchronized herd. That is what jitter fixes.

```python
# Deterministic exponential backoff for comparison (no jitter — REL007)
delay = min(base * (factor**attempt), cap)
```

A cap is mandatory. Without it, the tenth retry of a 1-second base waits 512 seconds — longer than any request deadline you actually have.

### Full Jitter

Jitter randomizes the backoff wait so callers do not retry in lockstep. AWS's canonical guide defines three variants; this repository teaches full jitter as the default:

| Variant | Formula | Property |
|---------|---------|----------|
| No jitter | `delay = min(cap, base * 2^n)` | synchronized herd |
| Equal jitter | `delay = cap/2 + random(0, cap/2)` | partial decorrelation |
| Full jitter | `delay = random(0, min(cap, base * 2^n))` | maximal decorrelation |

```python
import random


def full_jitter(base: float, attempt: int, cap: float, rng: random.Random) -> float:
    ceiling = min(cap, base * (2**attempt))
    return rng.uniform(0.0, ceiling)
```

The seeded simulator in `exercises/01-reliability-patterns.py` runs 100 callers under all three policies so you can see the timestamp spread. Under full jitter the retry arrivals smear across the window; under no jitter they land in one burst that can re-open a breaker the moment it half-opens.

### Idempotency

An operation is idempotent when performing it multiple times has the same effect as performing it once. Retries make idempotency non-optional: at-least-once delivery plus automatic retries means every consumer *will* see duplicates.

```python
# Natural key: the content hash identifies the work
key = sha256(text.encode()).hexdigest()
# Synthetic key: the caller supplies a unique id per logical request
key = request.headers["Idempotency-Key"]
```

Two mechanisms, one rule: a retried HTTP call carries the same key; a queue consumer stores the key (or a natural key) before applying the side effect and skips on the second arrival.

### Idempotency Key

An idempotency key is a unique identifier attached to a request that lets the receiver suppress the duplicate side effect. It is usually a client-generated UUID, returned with the response so the client can safely retry on timeout and present the same key.

```python
class IdempotencyStore:
    def __init__(self):
        self._seen: set[str] = set()

    def first_time(self, key: str) -> bool:
        if key in self._seen:
            return False
        self._seen.add(key)
        return True
```

The exercise's REL006 rule fires when a retryable operation mutates state with no key check — a queue consumer that charges a subscription, sends an email, or writes a Qdrant point twice.

### Natural Key

A natural key is a domain-unique identifier derived from the content itself rather than supplied by the caller. For a document chunk, `sha256(text)` is natural: the same text should map to the same point no matter how many times the pipeline runs.

Natural keys give you idempotent *ingestion* for free: re-running an upsert with the same payload and the same id overwrites rather than duplicates. Synthetic keys give you idempotent *user actions* where the content legitimately differs per attempt.

### Transactional Outbox

The outbox pattern makes event publication atomic with the state change that caused it. Instead of writing to the database and then publishing to a broker in two steps, you write the event into an `outbox` table in the same transaction; a separate drainer publishes from the table and marks rows sent.

```text
BEGIN
  UPDATE document SET status = 'ready' WHERE id = $1;
  INSERT INTO outbox (aggregate_id, event_type, payload)
    VALUES ($1, 'document.ready', $2);
COMMIT
-- drainer: SELECT ... FOR UPDATE SKIP LOCKED → publish → DELETE/ack sent row
```

Without the outbox, a crash between the two steps loses the event or publishes a phantom; with it, the event is either durably recorded or the whole transaction rolled back.

### Circuit Breaker

A circuit breaker is a proxy that stops calling a dependency after failures cross a threshold, fails fast locally, and periodically allows probe calls to test recovery. It exists because retries against a dead dependency waste the caller's budget and worsen the outage for everyone.

Three states:

```text
closed ──(failures ≥ threshold)──▶ open
open ──(cooldown elapsed)──▶ half-open
half-open ──(trial succeeds)──▶ closed
half-open ──(trial fails)──▶ open
```

```python
class CircuitBreaker:
    def __init__(self, failure_rate=0.5, min_samples=20, cooldown_s=30.0):
        self.state = "closed"
        self._fails = 0
        self._total = 0
        ...
```

Thresholds need a minimum sample size: a 50% failure rate over 2 calls (1 of 2) must not open a breaker. DevMate currently has **no** circuit breaker anywhere in `src/` — a verified gap and the reason Exercise 2 builds one from scratch.

### Half-Open

Half-open is the breaker's trial state. After the cooldown, the breaker admits a small, limited number of probe calls. One success closes it; one failure re-opens it and restarts the cooldown.

The subtlety the lecture stresses: the probe must be a *real* request, not a synthetic ping, and the trial limit must be tiny (often 1). Too many probes and half-open becomes open-but-leaking; zero probes and the breaker never recovers.

### Bulkhead

A bulkhead isolates capacity per dependency so one slow or dead downstream cannot consume every worker, connection, or thread the service owns. The name comes from ship compartments: one flooding does not sink the vessel.

```python
# Two pools, not one shared client
llm_client = httpx.AsyncClient(timeout=..., limits=Limits(max_connections=20))
qdrant_client = QdrantClient(..., limit=10)
```

The anti-pattern is a single shared `httpx.AsyncClient` with default limits used for LLM calls, embeddings, reranking, and Qdrant: a reranker stall exhausts the pool and the LLM path starves with it.

### Connection Pool

A connection pool is the bounded set of reusable TCP connections to one host. Its size is the bulkhead's physical mechanism. Too large and you exhaust file descriptors or the server's own limit; too small and healthy requests queue behind a slow one.

```python
httpx.Limits(max_connections=20, max_keepalive_connections=10)
```

DevMate's clients each construct their own `AsyncClient` with explicit timeouts; the lecture asks you to verify each also has an explicit `Limits` so the bulkhead is real.

### Backpressure

Backpressure is the signal a slow consumer sends a fast producer: stop or slow down. Without it, the producer races ahead, the queue grows without bound, latency climbs, and the process eventually dies of memory pressure while reporting itself healthy.

```python
# api/main.py:146 — the SSE pump bounds its internal queue
_QUEUE_MAX = 1000
queue: asyncio.Queue[bytes | None] = asyncio.Queue(maxsize=_QUEUE_MAX)
# Producers await queue.put(...); when full, put blocks — that block IS backpressure.
```

The two standard mechanisms are a bounded queue (producer blocks or is rejected when full) and explicit rejection with 429 + `Retry-After` at the edge, which moves the pain to the caller that can act on it.

### Bounded Queue

A bounded queue has a fixed maximum length. When it fills, the producer is blocked (async `await queue.put`) or rejected. An unbounded queue is a memory leak with a time axis.

```python
asyncio.Queue(maxsize=1000)  # bounded — api/main.py:146
queue.Queue(maxsize=256)  # bounded — worker pattern
collections.deque()  # unbounded — REL005 defect
```

The lecture's Exercise on backpressure has you run the BAD pack's unbounded deque beside the GOOD pack's bounded queue and watch the resident memory curve diverge under the same producer rate.

### Dead-Letter Queue

A dead-letter queue (DLQ) captures messages that cannot be processed after the retry budget is exhausted — poison payloads, permanently failing downstreams, schema violations — so one bad item stops blocking the stream.

The four-step workflow is the whole pattern:

```text
capture  → move to DLQ with the error, attempts, and original payload
inspect  → dashboards + alerts on DLQ depth and age
alert    → page when depth grows or age exceeds the SLO
replay   → fix the consumer or the payload, re-drive idempotently
```

A DLQ nobody can replay is just a slower outage: the messages are gone from the main stream but the work is still not done. DevMate has no DLQ today; the lecture treats that as a known gap, not a feature.

### Poison Message

A poison message fails on every attempt for a deterministic reason — malformed JSON, a foreign key that will never exist, a content filter that always rejects. Retrying it forever blocks the partition and starves healthy messages behind it.

The DLQ is the standard answer; the alternative is a per-message attempt counter that dead-letters after N tries even when the error is classified retryable.

### Graceful Shutdown

Graceful shutdown stops accepting new work, drains in-flight requests, flushes buffers and checkpoints, then exits. The order matters; skipping a step loses data or returns errors to callers who were already accepted.

```text
1. receive SIGTERM
2. stop accepting new connections / fail readiness probes
3. drain in-flight requests (bounded by the stop grace period)
4. flush caches, checkpoint offsets, close clients
5. exit 0
```

DevMate's API lifespan implements step 4 for the LLM client (`api/main.py:65`, `await llm_client.close()`) but there is **no** SIGTERM handler anywhere in `src/` — a verified gap. In containers, the runtime sends SIGTERM and then SIGKILL after the stop grace period; code that ignores SIGTERM gets the kill and loses the drain entirely.

### Stop Grace Period

The stop grace period is the window the container runtime gives a process between SIGTERM and SIGKILL. Compose sets it per service; Docker's default is 10 seconds.

```yaml
# infra/docker/docker-compose.yml — implicit default; make it explicit for the API
devmate-api:
  stop_grace_period: 30s   # drain must finish here or the kill cuts it off
```

The drain code must complete inside this window or the shutdown is not graceful — it is just a delayed crash.

### Rate Limiting

Rate limiting caps how many requests a caller may make per window. It protects the service from accidental loops, misbehaving clients, and deliberate abuse, and it gives you a clean 429 contract instead of an OOM.

DevMate ships a global configuration:

```python
# config.py:90-91
rate_limit_requests: int = 100
rate_limit_window_seconds: int = 60
```

The API layer exposes it as middleware; the lecture's critique is that a single global number is wrong for someone — a batch ingest and an interactive chat user should not share one bucket. Tier limits per user, per IP, per endpoint, and per model.

### Token Bucket

A token bucket is a rate limiter that refills tokens at a fixed rate and spends one (or more) per request. When the bucket is empty the request is rejected with 429. Burst capacity equals the bucket size.

```python
class TokenBucket:
    def __init__(self, rate_per_s: float, capacity: int, clock=time.monotonic):
        self._rate, self._cap = rate_per_s, capacity
        self._tokens = float(capacity)
        self._clock = clock

    def allow(self, n: int = 1) -> bool:
        now = self._clock()
        self._tokens = min(self._cap, self._tokens + (now - self._last) * self._rate)
        self._last = now
        if self._tokens >= n:
            self._tokens -= n
            return True
        return False
```

Token bucket is the right default for API limits because it allows a legitimate burst (a page of parallel requests) while enforcing the sustained rate.

### Sliding Window

A sliding window rate limiter counts requests over a window that moves with the clock, avoiding the boundary bug of fixed windows where a caller can send 2× the limit in two seconds straddling the edge.

```text
fixed window:   |—— 100 ——|—— 100 ——|   → 200 in 2s across the boundary
sliding window: each request expires 60s after it was made
```

Sliding windows cost more memory (timestamps or a log per caller) and are worth it exactly where burst across the boundary matters — auth endpoints, paid model calls.

### Rate Limit Headers

Rate limit headers are the HTTP contract that makes limiting usable: how many requests remain, when the window resets, and how long to wait after a 429.

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 12
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1730000000
```

A 429 without `Retry-After` forces the client to guess; the retry classifier in the LLM client honors the header when the server sends it (`llm/client.py` maps 429 to `LLMRateLimitError`).

### Cache Stampede

A cache stampede is the thundering herd that hits the backing store the instant a hot key expires: every concurrent request that missed the same key recomputes it simultaneously, multiplying load on the thing the cache was protecting.

Three mitigations, used together:

```python
# 1. single-flight / request coalescing
_inflight: dict[str, asyncio.Future] = {}


async def get_or_compute(key, compute):
    if key in _inflight:
        return await asyncio.shield(_inflight[key])
    fut = asyncio.get_event_loop().create_future()
    _inflight[key] = fut
    try:
        value = await compute()
        fut.set_result(value)
        return value
    finally:
        _inflight.pop(key, None)


# 2. jittered TTL — never let all copies of a key expire at the same instant
ttl = base_ttl * rng.uniform(0.8, 1.2)

# 3. probabilistic early refresh — refresh before expiry under load
```

### Single-Flight

Single-flight (request coalescing) guarantees at most one in-flight computation per key. Concurrent callers await the same future instead of each issuing their own upstream call. It is the cheapest stampede defense and the one DevMate's semantic cache currently lacks — a verified gap the lecture calls out: `index/embeddings.py:342` holds a plain `dict` cache with a TTL check but no coalescing of concurrent misses on the same key.

### Negative Caching

Negative caching stores the *absence* of a result — a 404, an empty retrieval, a validation failure — for a short TTL so repeated bad keys do not hammer the backend. The TTL must be short (seconds to a minute) because the negative state can become stale the moment the document is indexed.

```python
EMPTY = object()
cache[key] = (EMPTY, time.monotonic() + 30)  # 30s negative TTL
```

Long negative TTLs are a correctness bug: the document exists, but every query for the next hour still says it does not.

### CAP Theorem

CAP states that a distributed data store cannot simultaneously provide more than two of Consistency, Availability, and Partition tolerance. In practice partitions happen, so the real choice is CP versus AP *during* a partition: refuse some requests (CP) or serve possibly-stale data (AP).

The operational reading the lecture gives: pick per surface. A payment or a dedup store is CP — wrong data is worse than no data. A document search index is usually AP — a slightly stale chunk is better than a 503.

### Eventual Consistency

Eventual consistency promises that if no new updates are made, all replicas will converge to the same value — after some delay. The delay is not specified by the theorem; it must be specified by you, measured, and published in the SLI.

```text
write to primary → async replication → replica serves reads after lag bound (e.g. 200ms p99)
```

The failure mode the lecture drills: "eventual" with no measured bound is indistinguishable from "lost" from the caller's point of view.

### Read-Your-Writes

Read-your-writes is the guarantee that a caller who just wrote a value will see that value in their next read, even when reads are served from a replica. It is usually implemented by routing the caller's next N reads to the primary, or by a session-sticky replica with a lag check.

For a RAG service the user-facing case is clear: a user uploads a document and immediately asks a question about it. If the retrieval path can lag, the UI must either wait for the ingest acknowledgment or tell the user the document is still indexing — a silent lag reads as "the system lost my file."

### Graceful Degradation

Graceful degradation is serving a reduced but correct answer when a dependency is unavailable, instead of failing the whole request. The ladder is pre-programmed and ordered by trust:

```text
full RAG answer with citations
  → answer from cached summary / smaller context
  → direct LLM answer labeled "no retrieval"
  → explicit "retrieval is degraded, try again" error
```

The hard rule from the lecture: never degrade into a *wrong* answer. A refusal or a labeled fallback is recoverable; a confidently wrong ungrounded answer is not.

### Fallback Chain

A fallback chain is an ordered list of providers tried until one succeeds. DevMate builds one explicitly:

```python
# llm/client.py:684-709
fallback_chain = [...]   # primary → secondary → ...
providers = {"ollama": ..., "openai": ..., ...}  # Ollama always registered
# llm/client.py:753-778 — the loop
for provider in fallback_chain:
    try:
        return await provider.chat(...)
    except (LLMUnavailable, LLMRateLimitError) as e:
        last = e
        continue
raise last
```

Two details that make the chain safe: `LLMValidationError` is *not* caught for fallback (a bad prompt will fail identically on the next provider — retrying wastes budget and can double-bill), and each provider carries its own timeout so one slow entry cannot starve the rest.

### RED Metrics

RED stands for Rate, Errors, Duration — the three signals that describe the request path. A service can be "up" while failing every request; RED is what tells you.

| Signal | Question | Example |
|--------|----------|---------|
| Rate | How many requests per second? | 50 rps into `/chat` |
| Errors | What fraction fail? | 2% 5xx + 0.5% timeouts |
| Duration | How long do they take? | p99 = 4.2s |

RED pairs with saturation (queue depth, pool utilization, breaker state) as the alerting surface the lecture recommends; alerting on symptoms catches the outage before the error-rate page does.

### Saturation

Saturation measures how close a resource is to capacity: queue depth, connection-pool utilization, CPU steal, memory pressure. It is the leading indicator — queues grow and pools saturate minutes to hours before the error rate moves.

```text
healthy:       queue depth ~ 0, pool utilization < 50%
warning:       queue depth steady > 100, pool utilization > 80%
critical:      queue full (backpressure engaged), pool 100%, breaker open
```

DevMate's SSE pump exposes the pattern: the bounded queue's current size *is* its saturation metric (`api/main.py`), and it is the number to alert on before the keepalive timeout starts firing.

### Error Budget

An error budget is the allowed unreliability derived from an SLO. If the SLO is 99.9% availability over 30 days, the budget is 43.2 minutes of downtime; spending it on a risky deploy or a known incident pauses feature work until the budget recovers.

```text
SLO: 99.9% of requests succeed with p99 < 2s, 30-day window
error budget: 0.1% × 30d = 43.2 min
budget spent this month: 12 min → 28% remaining → ship with guardrails
budget spent this month: 41 min → 5% remaining → freeze, reliability work only
```

DevMate's eval gate in CI (`ci.yml:71-77`, Hit@5 ≥ 1.0, MRR ≥ 0.70) is a correctness budget of the same shape: the moment a change would spend the quality budget, the pipeline stops the change.

### MTBF and MTTR

Mean time between failures (MTBF) and mean time to restore (MTTR) are the two numbers that compose availability for repairable systems: `availability ≈ MTBF / (MTBF + MTTR)`.

The engineering lever is almost always MTTR, not MTBF. You rarely get to make a dependency dramatically less likely to fail; you can always make detection faster (RED alerts), rollback faster (the CI gate and a known rollback order), and drain faster (graceful shutdown). Halving MTTR is usually cheaper and more reliable than trying to halve MTBF.

## Summary

The quick-reference table is the map; the detailed definitions are the terrain. The five families in Lecture 01 — timeouts and deadlines, retries with jitter, idempotency and outboxes, breakers and bulkheads, backpressure and DLQs — each have one job, and the absence of any one of them moves the failure into a shared resource you did not intend to share. Every example above either points at a verified line in this repository or names the gap explicitly; treat the gaps as the backlog.
