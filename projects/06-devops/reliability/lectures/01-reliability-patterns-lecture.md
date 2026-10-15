# Lecture 01: Reliability and Distributed Systems Patterns

## Topic Overview

Every outage in a system built from parts you do not own follows the same shape: one dependency slows or fails, the calling code waits longer than it should, retries amplify the load, a shared pool drains, and a local fault becomes a global one. This lecture teaches the patterns that break that chain, with one spine running through all of them: the dependency contract. Every external call carries a timeout, a retry policy with backoff and jitter, a circuit breaker, a fallback, and metrics — five defenses for five different failure modes, none of them optional. The examples are grounded in DevMate, the LLM service in this repository (Qdrant + Redis + Ollama/cloud providers), in the real Compose stack at `infra/docker/docker-compose.yml`, and in the repository's own CI. Claims labeled FACT were verified at the cited path; everything else is stated as general practice.

**Duration:** 3-4 hours
**Difficulty:** Intermediate
**Prerequisites:** Python, HTTP fundamentals, basic Docker and CI concepts; the Docker containerization lecture (`projects/06-devops/docker/`) helps but is not required

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **State** the dependency contract and explain which failure mode each of its five layers prevents
2. **Configure** connect and read timeouts separately, and propagate a request deadline as remaining budget instead of a fixed number
3. **Design** retry policies with exponential backoff, full jitter, attempt caps, total-time budgets, and retryable-class predicates
4. **Apply** idempotency keys, dedup stores, natural keys, and the transactional outbox so at-least-once delivery produces exactly-once effects
5. **Operate** a circuit breaker through closed, open, and half-open states without letting it mask the bugs it is hiding
6. **Isolate** dependencies with bulkheads and bound overload with backpressure instead of accepting until the process dies
7. **Build** dead-letter queues with replay, and shut down gracefully from SIGTERM through the Docker stop grace period
8. **Compare** token bucket, sliding window, and leaky bucket rate limiters, and pick the right tier per user, IP, endpoint, and model
9. **Choose** caching patterns and stampede protection appropriate for an LLM service's embedding, retrieval, and response caches
10. **Explain** what consistency you actually promise users, how graceful degradation ladder works when the LLM is down, and which RED and saturation signals to alert on

---

## Key Concepts

### 1. The Dependency Contract

One rule organizes this entire lecture: **every external call carries five things — timeout, retry, circuit breaker, fallback, metrics.** An external call is anything outside your process: a database, a vector store, a cache, an LLM provider, an embedding API, a queue.

| Layer | Question it answers | Failure it prevents |
|---|---|---|
| Timeout | How long will I wait? | Worker threads and connections wedged on a dead peer |
| Retry | Should I try again, how, and how many times? | Transient blips becoming user-visible errors |
| Circuit breaker | Should I try at all right now? | Hammering a dependency you already know is down |
| Fallback | What do I serve when the call fails? | A failed dependency meaning a failed page |
| Metrics | What is happening, right now? | Silent degradation discovered by users first |

The layers compose along one request path:

```text
                    request
                       │
                       ▼
              ┌─────────────────┐
   deny ──────┤  rate limiter   │──────► 429 + Retry-After
              └────────┬────────┘
                       │ allow
                       ▼
              ┌─────────────────┐
   open ──────┤ circuit breaker │──────► fallback / degraded response
              └────────┬────────┘
                       │ closed / half-open
                       ▼
              ┌─────────────────┐
  exhausted ──┤ timeout+retry   │──────► DLQ / typed error upstream
              └────────┬────────┘
                       │ success
                       ▼
                 dependency ──► response
                       │
                       ▼
              metrics (RED + saturation) ──► alerts
```

**FACT vs general practice.** DevMate already implements three of the five layers in one place: `projects/04-ai-engineering/devmate/src/devmate/llm/client.py:146` sets a split timeout, `client.py:157-162` wraps calls in a tenacity retry, and `client.py:684-686` plus `client.py:753-778` walk a provider fallback chain. FACT: a repository-wide search of `projects/04-ai-engineering/devmate/src/` finds no circuit breaker today. The pattern is in this lecture because the service needs it, not because it already exists. Every section below says which parts are already wired and which are gaps.

### 2. Timeouts: Connect, Read, and Deadlines

A single "timeout" number is a fiction. A call has at least three distinct waits, and collapsing them into one value hides where the time goes.

| Tier | What it bounds | Typical value | Failure it catches |
|---|---|---|---|
| Connect | TCP + TLS handshake | 1-10 s | Host down, DNS broken, network blackhole |
| Read (idle) | Gap between received bytes | 5-60 s | Wedged process, slow query, garbage-collection pause |
| Whole call | One logical attempt end to end | ≤ remaining deadline | Server accepted the request and never finishes |
| Deadline | The entire request, retries included | Request budget | Cascades across retry loops |

DevMate sets the split form wherever it talks HTTP directly:

```python
# FACT: projects/04-ai-engineering/devmate/src/devmate/llm/client.py:146
timeout = httpx.Timeout(60.0, connect=10.0)  # 60 s read, 10 s connect

# FACT: projects/04-ai-engineering/devmate/src/devmate/index/embeddings.py:73
timeout = httpx.Timeout(60.0, connect=10.0)  # cloud embeddings
# FACT: same file, line 246 — local Ollama embeddings gets a 5 s connect
timeout = httpx.Timeout(60.0, connect=5.0)
```

A 10-second connect timeout on a call that should connect in 20 milliseconds is already generous: it converts "the network is broken" from an instant error into ten seconds of held resources. The read timeout is where the real waits hide, because a server that accepted your connection can stall between bytes forever.

**No timeout is the worst failure mode, not the safest one.** A call with no timeout does not fail — it occupies a thread, a socket, and possibly a pool slot until the OS gives up, which on a healthy network is effectively never. One wedged call becomes a full pool, a full pool becomes a full worker fleet, and the outage's root cause is one dead host while the blast radius is everything.

**Deadline propagation.** A request arrives with a total budget. Each hop must spend `min(its own limit, whatever is left)` and pass the remainder down:

```python
import time


class Deadline:
    """A request budget that shrinks as it is spent."""

    def __init__(self, total_seconds: float, clock=time.monotonic) -> None:
        self._clock = clock
        self._start = clock()
        self.total = total_seconds

    @property
    def elapsed(self) -> float:
        return self._clock() - self._start

    @property
    def remaining(self) -> float:
        return max(0.0, self.total - self.elapsed)

    def expired(self) -> bool:
        return self.remaining <= 0.0
```

The two rules that make propagation work:

1. **Next attempt timeout = `min(per_call_limit, deadline.remaining)`.** A retry loop inside a call that already spent 18 of its 20 budget seconds gets 2 seconds, not a fresh 60.
2. **Do not start an attempt you cannot finish.** If `deadline.remaining` is smaller than the smallest useful attempt (say, one round trip plus processing), fail now with a typed timeout error instead of guaranteeing a second timeout.

Fixed per-attempt timeouts without a deadline are how retry loops multiply latency: three attempts of 60 seconds plus backoff turns a 20-second request into a 3-minute one, and every downstream service along the way is still waiting.

### 3. Retries: Backoff, Jitter, and Classification

A retry policy answers four questions: **which errors, how many attempts, how long to wait, and what the total time cost may be.**

**Exponential backoff with full jitter.** The canonical delay is `min(cap, base * 2^attempt)`. The improvement is to randomize inside that bound — AWS's builders'-library experiment compared strategies under a synchronized recovery and full jitter won because it spreads the herd across the whole window:

```python
import random


def full_jitter(base: float, cap: float, attempt: int, rng: random.Random) -> float:
    """Delay before `attempt` (0-based): uniform in [0, min(cap, base * 2^attempt)]."""
    ceiling = min(cap, base * (2**attempt))
    return rng.uniform(0.0, ceiling)
```

| Strategy | Delay formula | What happens when 100 callers recover together |
|---|---|---|
| No backoff | `0` | 100 simultaneous retries; the dependency is hit before it recovered |
| Fixed delay | `base` | One synchronized burst per attempt, phase-locked across callers |
| Exponential, no jitter | `base * 2^n` | Bursts, still aligned — every client computes the same schedule |
| Equal jitter | `base * 2^(n-1) + rand(0, base * 2^(n-1))` | Halved bursts, partially spread |
| **Full jitter** | `rand(0, min(cap, base * 2^n))` | Spread across the entire window; no shared phase |

No jitter is a thundering herd waiting to happen; equal jitter only halves the problem. Full jitter is the default you should have to argue your way out of. DevMate's retry already uses it: `wait_exponential_jitter(initial=1, max=30)` with `stop_after_attempt(3)` at `client.py:157-162` — three attempts, one to thirty seconds of jittered wait.

**Attempt caps and budget caps are different things.** `max_attempts=3` caps the count; a time budget caps the wall clock. Both are needed: a count cap with generous delays can still blow a deadline, and a time budget without a count cap lets a fast-failing dependency be attempted hundreds of times. Cap both.

**Retryable vs non-retryable.** Retrying a deterministic failure wastes the attempt and delays the error the user needs:

| Error class | Examples | Retry? |
|---|---|---|
| Transient server error | HTTP 500, 502, 503, 504 | Yes, with backoff + jitter |
| Timeout / network | Connect refused, read timeout, reset | Yes |
| Rate limited | HTTP 429, provider "overloaded" codes | Yes, and **honor `Retry-After`** |
| Client errors | HTTP 400, 401, 403, 404 | No — the request is wrong or unauthorized |
| Validation | Schema mismatch, unparseable response | No — it will fail identically every time |

DevMate classifies on exceptions rather than status codes: `retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError))` at `client.py:160`, while the provider layer maps `429 → LLMRateLimitError` and `401 → LLMAuthError` at `client.py:214-219`. The fallback chain refuses to retry validation failures: `client.py:773-775` re-raises `LLMValidationError` instead of rotating providers. That is the classification discipline in working code.

**Retry storms and thundering herd.** A retry storm is retries growing faster than the dependency recovers: each failure triggers more attempts, each attempt consumes a slot, and the recovery capacity is consumed by retries instead of real traffic. The defenses are the whole contract working together — jitter spreads the timing, attempt and budget caps bound the volume, the breaker stops attempts entirely, and rate limiting caps admission at the edge. Note the repository's own CI applies the same discipline to its readiness wait: `.github/workflows/ci.yml:140-154` polls Qdrant and Redis with `timeout=1`, a hard cap of 30 attempts, and one second of sleep — a bounded retry loop, not a `while True`.

### 4. Idempotency: Making Retries Safe

Retries are only safe if repeating a call does not change the outcome. That property is idempotency, and it is a prerequisite for retrying anything with a side effect — not an optimization you add later.

**Delivery semantics decide where the burden falls:**

| Semantics | Definition | Where you meet it |
|---|---|---|
| At-most-once | Fire it once or lose it; never twice | Fire-and-forget jobs where loss is acceptable |
| At-least-once | Delivered one or more times | Nearly every queue: standard SQS, Kafka with auto-commit, Redis streams |
| Exactly-once *effect* | The effect is applied exactly once | At-least-once delivery **plus** an idempotent consumer |

Queues are at-least-once because "exactly-once delivery" across a network is not achievable; message brokers do not try to sell you otherwise. The consumer must therefore dedupe, and the dedup key is the contract:

- **Idempotency key** — a unique token per logical operation (a UUID minted by the caller), sent with the request. The server records the key the first time and replays the stored response for any repeat. This is how payment APIs make `POST /charges` retryable.
- **Natural key** — an identity derived from the payload itself: `(user_id, action, day)` or a content hash. Free when your data has one; ambiguous exactly when you most need it.
- **Dedup store** — the record of keys already applied: `SETNX`-style semantics in Redis, a unique index in Postgres, or a materialized `processed_messages` table. The check and the effect must be atomic in the same transaction, or you have only moved the race.

```text
 write side (producer)                    read side (consumer)
┌─────────────────────────────┐          ┌──────────────────────────────┐
│ BEGIN                       │          │ receive message              │
│   UPDATE accounts  ...      │          │ BEGIN                        │
│   INSERT INTO outbox ...    │  queue   │   INSERT processed(key) ...  │
│ COMMIT (one transaction)    │ ───────► │   apply effect               │
└─────────────────────────────┘          │ COMMIT                       │
      relay drains the outbox            └──────────────────────────────┘
```

**The transactional outbox** closes the gap between "I changed my database" and "I published an event." Writing both in one transaction means either both landed or neither did; a relay then drains the outbox table to the queue. The alternative — commit, then publish — has a window where the crash loses the event forever, and no retry brings it back.

**FACT vs this repository.** Pipeline-level idempotency (stable keys, upserts, checkpoints) is taught separately at `projects/00-core-foundations/data-engineering/03-idempotency/` and registered as node `data.reliability` in `registries/knowledge-registry.yaml`. This lecture's contribution is the service-level half: idempotency keys on HTTP calls, dedup in queue consumers, and the outbox as the producer-side companion to retries.

### 5. Circuit Breaker: Stop Calling What You Know Is Down

A retry makes three attempts against a dependency that is down; the tenth caller in a second makes three more. The circuit breaker is the layer that says *enough* — after the failure is established, calls short-circuit instead of waiting for a timeout that will not help.

```text
      failure rate over threshold (with minimum sample)
 CLOSED ──────────────────────────────────► OPEN
    ▲                                        │
    │ trial succeeds                         │ cooldown elapsed
    │                                        ▼
    └──────────── trial fails ◄────────── HALF-OPEN
                   (reopens)          (limited probes only)
```

| State | Behavior | Entry condition |
|---|---|---|
| Closed | Calls pass through; failures are counted in a rolling window | Initial state; trial success from half-open |
| Open | Calls fail immediately — no network attempt | Failure rate ≥ threshold over ≥ minimum calls |
| Half-open | A small number of trial calls (1-3) are allowed through | Cooldown timer expires |

Two thresholds matter, not one:

- **Failure-rate threshold** — the classic setting is 50% failures, but only after a minimum sample (commonly 10 calls) so a single early failure on a fresh service does not trip the breaker.
- **Slow-call ratio** — a dependency that answers every request in 30 seconds is "successful" and still broken. Resilience4j-style breakers take a slow-call threshold (say 50% of calls slower than a 5-second limit) alongside the failure rate. Without it, the breaker ignores the most common real-world degradation: latency creep.

**What it protects.** Threads and connections. Waiting callers consume both, so an unbroken breaker against a dead peer is a pool-exhaustion machine: one dependency's outage converts into every dependency's outage once the shared pool empties. The breaker converts "wait 60 seconds for a yes-or-no" into "fail in a millisecond and go do something else."

**What it must not do: mask bugs.** A breaker that opens silently turns an outage into a mystery — callers see fallbacks, dashboards look green, and nobody knows the dependency is down until a user complains. Three rules keep it honest:

1. **Every short-circuited call still emits a metric and a log line**, labeled by dependency and breaker state.
2. **Opening an breaker is an alert-worthy event**, not routine noise; page on state transitions, not on individual failures.
3. **The breaker never replaces fixing the failure.** It buys recovery time; the incident still needs a cause.

**FACT:** DevMate has no circuit breaker today (verified by searching `projects/04-ai-engineering/devmate/src/` for `circuit`). Its fallback chain at `client.py:753-778` provides the *fallback* half of the contract, but every provider attempt inside that loop still pays its full timeout — which is exactly the behavior a breaker exists to eliminate.

### 6. Bulkheads: One Pool per Dependency

A bulkhead partitions a shared resource so that one dependency's failure cannot consume the whole allocation. In practice the resource is almost always a connection or worker pool.

```text
  ❌ shared pool (hidden coupling)            ✅ per-dependency pools
┌──────────────────────────────┐      ┌──────────┬──────────┬──────────┐
│      one pool, 50 conns      │      │ qdrant   │  redis   │  llm     │
│                              │      │ 10 conns │ 10 conns │ 20 conns │
│  qdrant ──► takes all 50     │      │ 10 held  │ 10 free │ 20 free  │
│  redis  ──► waits forever    │      │ max harm │ isolated │ isolated │
│  llm    ──► waits forever    │      └──────────┴──────────┴──────────┘
└──────────────────────────────┘
```

A shared pool is hidden coupling: two services that never call each other directly still fail together because they drew from the same budget. With separate pools, the worst case of a Qdrant stall is "retrieval is degraded," not "the API cannot talk to Redis either." The same reasoning applies to worker threads, asyncio semaphore counts, and even concurrency slots in an HTTP client.

The sizing rule: **give each dependency the concurrency it can actually absorb, not an equal share of everything.** A slow dependency needs a *smaller* pool (it is the slow one), while a fast, cheap one can have more. DevMate's Compose file caps the API container at 2 GB of memory (`infra/docker/docker-compose.yml:155-160`) — that is a host-level bulkhead; per-dependency pools are the in-process version of the same idea.

### 7. Backpressure: Reject Early, Not at OOM

Backpressure is the discipline of telling producers to slow down while there is still time. The alternative — accepting everything until memory runs out — fails in the worst possible way, because an out-of-memory kill is sudden, global, and loses everything in flight.

**Bounded queues are the primitive.** An unbounded queue is not a buffer; it is a slow-motion OOM. The queue absorbs jitter between producer and consumer; once it is full, something must give:

```text
producer ──► [ bounded queue, maxsize N ] ──► consumer
                    │ full
                    ▼
      block the producer (preferred)
      / drop low-value work (shedding)
      / reject with 429 + Retry-After (admission control)
```

**FACT:** DevMate streams responses through exactly this shape. `projects/04-ai-engineering/devmate/src/devmate/api/main.py:146` creates `asyncio.Queue(maxsize=_SSE_PUMP_QUEUE_MAX)`, and the docstring at `main.py:117-122` states the intent: a bounded queue plus an awaited `put` means the server buffers at the *client's* rate, not the provider's. The pump task's only job is to apply backpressure between a fast provider and a slow reader.

**Reject-early beats accept-until-death.** A `429` with a `Retry-After` header is a recoverable, honest answer that keeps the process healthy; accepting until OOM kills workers produces dropped connections, lost in-flight work, and cascading restarts. Load shedding extends the same idea: when saturated, shed the cheapest-to-identify or least-valuable work first (uncached reads, expensive reranking, nonessential enrichment) rather than degrading everything equally.

**Ingestion must never outpace processing.** A document ingester that pushes chunks into a queue faster than the embedding worker drains it grows the queue without bound — memory climbs, latency climbs, and the system is "up" while being useless. Two fixes, used together: cap the producer's rate to the measured consumer rate, and put a hard bound on the queue so the producer blocks instead of the process dying.

### 8. Dead-Letter Queues: Capture, Inspect, Alert, Replay

A dead-letter queue (DLQ) captures messages that cannot be processed after retries — poison messages, malformed payloads, permanent downstream failures — so one bad item stops blocking the stream instead of being retried forever.

A DLQ is only half a mechanism. **Capture without replay is a landfill:** messages pile up, nobody looks at them, and the work they represent is silently lost forever while the dashboard shows a healthy queue. The four steps are mandatory:

| Step | What you do | What it looks like |
|---|---|---|
| Capture | Move the failed message with its error metadata | Original payload + `reason`, `attempt_count`, `first_failed_at` |
| Inspect | Give the messages a readable form | A queryable store, not a binary blob in a log |
| Alert | Notice growth | DLQ depth over threshold pages someone |
| Replay | Fix the cause, re-inject, verify | Reprocess **idempotently** — replay is a retry |

Two details decide whether the DLQ is an asset:

1. **Carry the diagnosis with the message.** A payload with no error class, no stack, and no attempt count forces whoever inspects it to reproduce the failure from scratch.
2. **Replay must be idempotent** (section 4). Replaying a batch that was half-processed before it dead-lettered will duplicate work unless the consumer dedupes by key. The DLQ is where the idempotency contract proves it was not optional.

Where messages are the wrong fit — a synchronous call that must not be lost — the equivalent is a typed error with retry context passed upstream, so the caller decides whether to queue it, fail the request, or degrade.

### 9. Graceful Shutdown: Stop, Drain, Checkpoint, Release

A shutdown that kills in-flight work converts a routine deploy into data loss and user-visible errors. The sequence is fixed:

```text
SIGTERM received (or `docker stop`)
  1. stop accepting      — fail readiness, let the load balancer drain
  2. drain in-flight     — finish current requests within the grace period
  3. checkpoint          — flush offsets, commit outbox rows, persist cursors
  4. release             — close pools, release locks, drop leases
                           (then exit; the runtime sends SIGKILL if you stall)
```

- **The signal is SIGTERM, and `docker stop` sends it.** The Docker lecture's exec-form rule matters here: `CMD ["uvicorn", "app:app"]` makes the server PID 1 and the signal reaches it; the shell-form `CMD uvicorn app:app` parks a shell in between that swallows the signal, and the app only learns about shutdown when SIGKILL arrives with no warning.
- **The grace period is bounded.** Docker waits 10 seconds after SIGTERM by default, then SIGKILLs the container; Compose sets it per service with `stop_grace_period: 30s`, and `docker stop --time 30` overrides it. Your drain deadline must fit *inside* that number, which means knowing your worst-case in-flight time rather than guessing.
- **Checkpoint before exit, not after.** A worker that dies before committing its offset redelivers the whole batch (harmless if consumers dedupe) or, worse, marks work done that is not (harmful if it does not). The checkpoint is the line between at-least-once and lost.

**FACT:** DevMate's FastAPI lifespan at `projects/04-ai-engineering/devmate/src/devmate/api/main.py:41-65` runs a startup block and closes the LLM client on shutdown (`await llm_client.close()` at line 65) — resource release is wired. Readiness draining and checkpointing are general practice for this service to add as it grows queues and leases.

### 10. Rate Limiting: Algorithms and Tiers

Rate limiting is admission control: it protects *you* from a misbehaving client and protects *every other client* from that client's traffic. Three algorithms dominate, and they differ in burst behavior more than in anything else:

| Algorithm | Allows bursts? | Memory | Accuracy | Best for |
|---|---|---|---|---|
| Token bucket | Up to bucket capacity | O(buckets) | Approximate under concurrency | API quotas where bursts are fine |
| Leaky bucket | No — constant output rate | O(buckets) | Exact output shaping | Smoothing traffic toward a slow downstream |
| Fixed window counter | Burst at window edges | O(buckets) | Edge double-counting | Cheap coarse limits |
| Sliding window log | Naturally bounded | O(events) | Precise | Strict per-user limits |
| Sliding window counter | Bounded | O(buckets) | Weighted approximation | Production default when precision matters |

**Token bucket** refills at a steady rate and holds up to `capacity` tokens: a client idle for a minute can spend the whole accumulated burst at once, which is usually what you want for user-facing APIs. **Leaky bucket** drains at a fixed rate regardless of arrival: ideal when the downstream wants a smooth flow, wrong when you want bursts to be possible. **Sliding window** counts events in a moving window instead of resetting on a fixed boundary, eliminating the classic double-burst at `T:00`.

**Tiers, not one global number.** Different keys deserve different budgets:

| Tier | Key | Typical use |
|---|---|---|
| Per-IP | Source address | Unauthenticated endpoints; cheap abuse control |
| Per-user | Account or API key | Fairness between tenants |
| Per-endpoint | Route | Protect the expensive route without starving the cheap ones |
| Per-model | Model identifier | GPT-4-class calls get a tighter budget than a local model |

**FACT:** DevMate carries rate-limit settings end to end — `config.py:90-91` defaults to 100 requests per 60-second window, and `infra/docker/docker-compose.yml:141-143` passes the same values into the API container as `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_WINDOW_SECONDS`.

**429 plus `Retry-After` is the contract.** The rejection must be early (before the work is accepted), typed (a client can distinguish it from a 500), and instructive — `Retry-After` in seconds tells the client when to come back so its own retry policy can honor yours instead of guessing. A limiter that rejects without the header pushes every client into blind backoff; a limiter that rejects *after* accepting the work protects nothing.

### 11. Caching: Patterns, TTL, and Stampede Protection

Caching is the cheapest latency and cost lever an LLM service has — and the easiest way to serve stale or wrong answers if you skip the invalidation and stampede rules.

| Pattern | Read path | Write path | Main risk |
|---|---|---|---|
| Cache-aside | App checks cache; fills on miss | App writes DB, then invalidates | App must remember to invalidate |
| Read-through | Cache itself loads on miss | Same as cache-aside | Same |
| Write-through | — | App writes cache; cache writes DB | Added write latency |
| Write-behind | — | App writes cache; cache flushes async | Data loss window if the cache dies |

**TTL vs invalidation.** A TTL is a self-cleaning staleness bound: simple, automatic, and wrong for as long as the TTL lasts. Explicit invalidation is correct but only as reliable as every writer remembering to do it. The pragmatic default: TTL on everything (DevMate's semantic cache uses `cache_ttl_seconds: 3600`, `config.py:125`), plus explicit invalidation for the few keys where an hour of staleness genuinely hurts — permissions, prices, freshly ingested documents.

**Cache stampede.** A hot key expires and every concurrent reader misses at the same instant, all issuing the underlying call at once — a self-inflicted thundering herd at exactly the moment your backend can least afford it. Two defenses, both cheap:

1. **Single-flight** — only one caller computes the value; the others wait for it and share the result.
2. **Jittered TTL** — expire at `ttl * (1 + rand(0, 0.1))` so identical keys do not expire at identical instants.

**Negative caching** caches the *misses*: a query that found nothing is still a query you can avoid re-running. Keep negative entries on a much shorter TTL than positive ones — the whole point of a miss is that new data may exist any second.

**The caches that matter for an LLM service**, in order of payoff:

| Cache | Key | What it saves | FACT in this repo |
|---|---|---|---|
| Embedding | Hash of the text | Embedding API cost + latency per duplicate chunk | `EmbeddingService` keeps a sha256-keyed dict at `index/embeddings.py:342-391` |
| Retrieval | Normalized query + filters | Reranking and vector search on repeated questions | General practice; not implemented in DevMate today |
| Prompt/response | Semantic similarity of the question | A full LLM generation | Semantic cache with threshold 0.85, `config.py:126`, `cache/semantic_cache.py:40` |

Note the honest gaps in the FACT column: DevMate's embedding cache is an in-process dict with no TTL and no size bound, and neither it nor the semantic cache implements single-flight. Those are the two stampede-relevant upgrades this lecture asks for.

### 12. CAP and Consistency: What You Actually Promise

CAP is usually taught as choosing two of three, which is the wrong frame. Partitions happen — you do not get to opt out — so the real question is: **during a partition, do you stay consistent or stay available?** And outside partitions, what do users experience?

| Promise | What the user sees | How you deliver it |
|---|---|---|
| Read-your-writes | "I just saved it; it is still there on refresh" | Route the follow-up read to the writer (session stickiness), or wait for the write to be visible |
| Monotonic reads | Never go backward in time | Pin a user to a replica set; never alternate between replicas at different lag |
| Eventual consistency | "It will show up shortly" — for everyone | Accept async replication, and *say so* in the UI when freshness matters |

**Eventual consistency is a contract, not a shrug.** It is fine for a like count, a search index, or a leaderboard; it is not fine when a user's action appears and then vanishes. The engineering failure is promising consistency you cannot deliver: a retrieval index that is 30 seconds stale is eventual consistency, and a UI that implies instant is a bug in the promise, not in the index.

**What to promise users, practically:**

- **Their own actions:** read-your-writes, always. Anything else reads as data loss.
- **Shared lists and dashboards:** eventual with an explicit freshness signal when staleness crosses a threshold (a "last updated" timestamp is often enough).
- **Search and retrieval results:** eventual — but bounded, measured, and honest; DevMate's CI records this as a gate on retrieval quality (`.github/workflows/ci.yml:71-77` floors Hit@5 at 1.0 and MRR at 0.70 offline), which measures *whether* answers are findable while freshness remains an operational concern.

The pattern that ties this section to the rest of the lecture: read-your-writes is a *routing* decision, eventual consistency needs *detection* (drift metrics), and both need the *fallback* to degrade honestly when the replica you need is the one that is partitioned.

### 13. Graceful Degradation: The Ladder When the LLM Is Down

Graceful degradation answers one question per dependency: **what does the user see when this breaks?** For an LLM service the ladder runs from full service down to an honest, clearly-labeled partial one:

```text
 1. primary model (cloud)          full answer, grounded in retrieval
 2. fallback model (local/other)   full answer, possibly slower or weaker
 3. retrieval without generation   "here are the sources" — snippets, no prose
 4. cached / stale answer          served with an explicit staleness notice
 5. typed error + Retry-After      never a blank page, never a wrong answer
```

**FACT:** DevMate already walks the first two rungs. `config.py:43` sets the default provider to `ollama` (local), the provider registry always includes Ollama because it needs no key (`client.py:688-691`), and `client.py:684-686` builds a fallback chain of the configured default followed by every other registered provider. The loop at `client.py:753-778` rotates through that chain on rate-limit, auth, and timeout errors, and raises a single typed `LLMError` only when every provider is exhausted.

Two rules keep the ladder honest:

1. **Degrade visibly.** A cached or fallback answer must be labeled — a weaker model answering as if it were the primary one, or a stale response with no notice, hides regression behind availability.
2. **Never degrade into wrongness.** If retrieval is down, saying "I could not find sources" beats fabricating an answer. The ladder's bottom rung is a truthful error, not a confident guess.

### 14. Observability of Failure: RED, Saturation, Error Budgets

You cannot operate the patterns above without knowing when they fire. Three signal groups carry a service:

| Signal group | Questions it answers | Examples |
|---|---|---|
| **RED** — Rate, Errors, Duration | Are users being served, and how fast? | Requests/s, 5xx and fallback rates, p50/p95/p99 latency |
| **Saturation** | How close are we to the wall? | Queue depth, pool utilization, breaker state, memory headroom |
| **Business / quality** | Is it *right*, not just up? | Retrieval hit rate, faithfulness, cache hit ratio |

Breaker state, DLQ depth, and queue depth deserve first-class dashboard placement precisely because they are *leading* indicators: they rise before the error rate does. Rate-limit rejections (429 counts) are a signal too — a sudden spike means either abuse or an under-sized budget, and both deserve an answer.

**Error budgets turn availability into arithmetic.** An SLO of 99.9% over 30 days spends a budget of `43,200 min × 0.001 = 43.2 minutes` of allowed downtime. Burn the budget and you stop shipping risky changes until it regenerates; that is the mechanism that makes reliability a shared product decision instead of an ops afterthought. Fast-burn alerts (for example, 2% of the monthly budget consumed in one hour) catch an unfolding incident while the budget is still mostly intact.

**Alert on symptoms, not causes.** "CPU high" pages someone who then has to ask "is anyone hurting?". "p95 latency over 2 s for 5 minutes" or "5xx rate over 1% for 5 minutes" starts with the user's experience and lets the cause be discovered during the response. The same logic runs in this repository's own gates: CI fails on measured quality symptoms (Hit@5 and MRR floors at `.github/workflows/ci.yml:71-77`) rather than on build-process trivia.

### 15. Worked Scenario: One LLM Request, Three Failures

Take a real request against DevMate's shape: `POST /ask` with a question, pipeline = rate limit → retrieval (Qdrant) → rerank → embed query → LLM → stream. Three failures land in one minute.

```text
 t=0s    POST /ask arrives; per-user limiter admits (100/60s budget)
 t=0.1s  Qdrant search call issued  ──► HANGS (worst case: no explicit
         │                              call timeout configured)
         │ deadline rules: attempt bounded by min(per_call, remaining)
 t=1s    3rd consecutive Qdrant failure ──► breaker for "qdrant" OPENS
         │ fallback: skip vector search, flag degraded retrieval
 t=2s    query embedding needed; cloud embedding API returns 429
         │ retry policy: retryable class, honor Retry-After, jittered
         │ breaker for "embeddings" opens after sustained 429s
 t=3s    fallback embedding provider (local Ollama) answers  ✅
 t=4s    LLM call: primary provider overloaded (429)
         │ fallback chain rotates to next registered provider
         │ (FACT: client.py:753-778)
 t=5s    answer streams back, labeled degraded retrieval
 t=60s   DLQ depth check, breaker metrics, RED dashboard: all visible
```

Every line maps to a pattern from this lecture:

| What happened | Pattern that handled it | If it were missing |
|---|---|---|
| The hanging Qdrant call could not stall the request | Timeout + deadline propagation (§2) | One request pins a worker until SIGKILL |
| Established Qdrant failure stopped new attempts | Circuit breaker (§5) | Every request pays the full timeout × attempts |
| 429 from the embedder was retried correctly | Retryable classification + jitter (§3) | Retry storm into an already-limited API |
| Embeddings fell back to a local provider | Fallback ladder (§13) | Hard failure of the whole request |
| The degraded answer was labeled | Graceful degradation, visibly (§13) | Users trust a weaker path as the strong one |
| Limiter admitted only budgeted traffic | Rate limiting + backpressure (§7, §10) | Overload cascades to every endpoint |
| Failures were visible in dashboards and paged | RED + saturation + alert on symptoms (§14) | The incident is discovered by a user |

**The one gap this scenario exposes (FACT):** `QdrantClient` is constructed at `projects/04-ai-engineering/devmate/src/devmate/index/vector_store.py:101-106` with no timeout argument, and the installed client's own `timeout` parameter defaults to `None`. Of every external call DevMate makes, this is the one most exposed to the "no timeout" failure mode from section 2 — and it is the first fix this lecture recommends applying to the real service.

---

## Common Mistakes to Avoid

### 1. Calling a Dependency With No Timeout

```python
# ❌ BAD: this call can hold the worker until the process is killed
results = qdrant_client.search(collection, vector)

# ✅ GOOD: bound the attempt, and bound the total request too
deadline = Deadline(total_seconds=2.0)
results = await asyncio.wait_for(
    search_async(collection, vector),
    timeout=min(1.0, deadline.remaining),
)
```

### 2. Retrying Everything, With Fixed Delays, Including 4xx

```python
# ❌ BAD: retries a 400 forever, synchronizes every caller, ignores budget
for _ in range(5):
    resp = requests.post(url, json=payload)
    if resp.ok:
        return resp
    time.sleep(1)

# ✅ GOOD: classify first, jitter the wait, cap attempts and time
if error_class not in policy.retryable:
    raise  # 4xx and validation never retry
if attempt >= policy.max_attempts or deadline.expired():
    raise
await asyncio.sleep(full_jitter(policy.base, policy.cap, attempt, rng))
```

### 3. Retrying a Non-Idempotent Side Effect

```python
# ❌ BAD: a timeout after the charge landed means the retry double-charges
charge_card(order)  # timed out, but succeeded server-side
charge_card(order)  # retry

# ✅ GOOD: the key makes the second call a replay of the first
charge_card(order, idempotency_key=request.uuid)  # server dedupes by key
```

### 4. One Shared Pool for Every Dependency

```text
❌ BAD:  qdrant stall ──► fills the only pool ──► redis and llm starve too
✅ GOOD: qdrant has its own small pool; its stall degrades retrieval only
```

### 5. A Circuit Breaker That Never Opens, or Opens Silently

```python
# ❌ BAD: threshold unreachable (100%+) and no signal when it trips
breaker = CircuitBreaker(failure_threshold=1.0, minimum_calls=0)

# ✅ GOOD: reachable threshold, sample floor, and every state change emits
breaker = CircuitBreaker(
    failure_threshold=0.5, minimum_calls=10, on_transition=log_and_alert
)
```

### 6. A Dead-Letter Queue Nobody Can Replay

```text
❌ BAD:  failed messages archived to an S3 bucket no one queries
         → work vanishes, dashboards stay green, nobody notices

✅ GOOD: capture with error metadata → alert on depth → fix →
         replay idempotently → verify the dedup store suppressed repeats
```

---

## Best Practices

1. **Put the five-part dependency contract in one wrapper** so no call site can quietly drop a layer
2. **Configure connect and read timeouts separately**; connect should be tight, read should reflect the slowest legitimate response
3. **Propagate deadlines as remaining budget**, and refuse to start attempts that cannot finish inside them
4. **Retry only retryable classes** — timeouts, network errors, 5xx, 429 — and honor `Retry-After` when present
5. **Use full jitter by default**; treat no-jitter backoff as a defect that needs justification
6. **Cap attempts and total retry time**, not just one or the other
7. **Make every retried operation idempotent** with a key, a natural key, or a dedup store; use an outbox for event publication
8. **Set breaker thresholds on both failure rate and slow-call ratio**, with a minimum sample, and alert on every transition
9. **Give each dependency its own pool**; a shared pool is coupling nobody declared
10. **Bound every queue** and reject early with 429 + `Retry-After` instead of accepting toward OOM
11. **Treat the DLQ as a workflow**: capture, inspect, alert, replay — idempotently
12. **Shut down in order** — stop accepting, drain, checkpoint, release — inside the container's stop grace period
13. **Tier rate limits** per user, IP, endpoint, and model; a single global number is always wrong for someone
14. **Cache with a TTL everywhere**, add single-flight and jittered TTL for hot keys, and keep negative caching short
15. **Promise read-your-writes to users**, label eventual consistency honestly, and never degrade into a wrong answer
16. **Alert on symptoms** — RED, saturation, breaker and DLQ depth — and give each SLO an error budget you actually enforce

---

## Practice Exercises

### Exercise 1: Prove Full Jitter Spreads the Herd
Using the seeded simulator in `exercises/01-reliability-patterns.py`, run 100 callers recovering from the same outage under no-jitter, equal-jitter, and full-jitter policies. Record the spread of retry timestamps for each and explain which schedule a recovering dependency would actually survive.

### Exercise 2: Drive a Breaker to Half-Open
Feed the `CircuitBreaker` in the exercise a sustained failure stream and confirm it opens at the configured failure rate. Advance through the cooldown, allow one successful trial, and confirm the state returns to closed. Then find the configuration in the BAD pack that prevents the breaker from ever opening and explain the production consequence.

### Exercise 3: Verify Dedup Suppresses the Second Side Effect
Run the `IdempotencyStore` against a counter side effect twice with the same key and confirm the counter advanced once. Repeat without the key and confirm it advances twice — that second run is REL006, and it is what a queue consumer does by default.

### Exercise 4: Budget a Retry Loop
Give `Deadline` a 2-second budget and a retry policy with a 1-second base. Run retries against the flaky dependency and verify no attempt starts with less than a workable slice of the budget. Compute what the same loop would cost with fixed per-attempt timeouts and no deadline, and compare it to the request budget.

### Exercise 5: Audit the Real Service's Call Sites
Write out the three HTTP timeouts DevMate configures today — `llm/client.py:146`, `index/embeddings.py:73`, `retrieve/retriever.py:56` — as a policy pack in the JSON format the exercise accepts, run it through the rules, and add the missing Qdrant timeout from `index/vector_store.py:101` until the pack passes with zero findings.

---

## Summary

Reliability is not one feature; it is five defenses applied consistently at every boundary:

1. **The dependency contract is the spine.** Timeout, retry, circuit breaker, fallback, metrics — each prevents a different failure, and the absence of any one of them moves the failure into a shared resource.
2. **Timeouts need splits and budgets.** Connect versus read, plus a deadline passed down as remaining budget; no timeout is the worst failure mode because it converts a fault into a permanent occupation.
3. **Retries need classification, jitter, and caps.** Retry timeouts, network errors, 5xx, and 429; never 4xx or validation; full jitter beats equal jitter; cap attempts *and* total time.
4. **Idempotency is the price of retrying.** Queues are at-least-once, so consumers dedupe by idempotency key or natural key, and the transactional outbox makes publication atomic with the write.
5. **Breakers, bulkheads, and backpressure bound the blast radius.** Stop calling what is down, isolate pools so one dependency cannot drain everything, and reject early instead of accepting until OOM.
6. **DLQs need replay; shutdown needs an order.** Capture-inspect-alert-replay, idempotently; stop, drain, checkpoint, release, inside the stop grace period.
7. **The promise layer is where users feel all of it.** Rate-limit tiers, stampede-proof caches, read-your-writes and honest eventual consistency, a visible degradation ladder, and RED-plus-saturation alerting that fires on symptoms before users do.

**Next lecture:** Observability and incident response for LLM services, where the RED metrics, breaker transitions, DLQ depths, and error budgets from this lecture become dashboards, alerts, and runbooks with a fixed rollback order.
