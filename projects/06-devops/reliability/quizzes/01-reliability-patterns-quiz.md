# Quiz 01: Reliability and Distributed Systems Patterns

## Topic Overview
This quiz covers the dependency contract and its five defenses: timeouts and deadlines, retries with classification and jitter, idempotency with dedup and outboxes, circuit breakers and bulkheads, backpressure and dead-letter queues — plus graceful shutdown, rate limiting, cache stampede, consistency choices, degradation ladders, and RED-plus-error-budget observability.

---

## Questions

### Question 1
**A service calls four external dependencies. Which set makes up the full dependency contract taught in the lecture?**

- A) Timeout, retry policy, circuit breaker, fallback, metrics
- B) Logging, tracing, metrics, profiling, alerting
- C) Timeout, cache, queue, rate limit, load balancer
- D) Retries, failover, autoscaling, health checks, backup

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** Every external call carries five defenses: a timeout, a retry policy with backoff and jitter, a circuit breaker, a fallback, and metrics. Each one prevents a different failure mode, and omitting any single one moves that failure into a shared resource — a drained pool, an occupied thread, a synchronized herd.
</details>

---

### Question 2
**Why is a network call made with no timeout the worst failure mode rather than the safest?**

- A) It always returns stale data instead of failing
- B) It does not fail; it occupies a thread, socket, and pool slot until the OS gives up
- C) It fails immediately with a connection error
- D) It blocks the Python garbage collector permanently

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A call with no timeout converts a transient fault into a permanent occupation. One wedged call holds a connection; a few wedge and the whole pool is full; a full pool stops healthy traffic. The root cause is one dead host while the blast radius is every caller sharing that pool.
</details>

---

### Question 3
**A dependency returns HTTP 400 on every request because the payload fails schema validation. Should the retry policy re-attempt it?**

- A) Yes, after exponential backoff, three times
- B) Yes, but only with full jitter
- C) No — client and validation errors are not retryable
- D) Yes, if the circuit breaker is closed

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Retryable classes are timeouts, network errors, HTTP 5xx, and 429. A 400 or a local validation failure is deterministic: the identical request will fail identically on every attempt, so retrying only burns budget. DevMate's client maps validation failures to `LLMValidationError` and re-raises them instead of rotating to the next provider.
</details>

---

### Question 4
**Under full jitter, what is the wait before attempt `n`?**

- A) `base * 2^n` with no randomness
- B) `min(cap, base * 2^n) + random(0, cap)`
- C) `base + random(0, base * n)`
- D) `random(0, min(cap, base * 2^n))`

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** Full jitter randomizes uniformly inside the capped exponential bound, so callers that failed together do not retry together. No jitter produces a synchronized herd; equal jitter only decorrelates half the window. Full jitter is the default you should have to argue your way out of.
</details>

---

### Question 5
**What property makes an operation safe to retry?**

- A) It completes quickly
- B) Repeating it yields the same result as performing it once
- C) It returns HTTP 200
- D) It holds no database locks

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** That property is idempotency. Queues are at-least-once and clients retry on timeout, so duplicates are guaranteed to arrive eventually. The side effect must be guarded by an idempotency key, a natural key such as a content hash, or a dedup store — otherwise every retry charges, emails, or writes again.
</details>

---

### Question 6
**A circuit breaker's cooldown has elapsed. What happens next?**

- A) The breaker closes and all traffic resumes immediately
- B) The breaker enters half-open and admits a limited number of probe calls
- C) The breaker opens again and restarts the cooldown
- D) The breaker is deleted and rebuilt from scratch

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** Half-open is the trial state. It admits a small, bounded number of real probe requests: one success closes the breaker, one failure re-opens it and restarts the cooldown. Closing immediately resumes the load that opened it; staying open forever turns a transient outage into a permanent one.
</details>

---

### Question 7
**What is the effect of bounding a queue with `maxsize` while producers `await queue.put(item)`?**

- A) The queue drops items silently when full
- B) Items are spilled to disk automatically
- C) Producers block when the queue is full — backpressure
- D) Consumers run at double speed to keep up

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** A bounded queue converts unlimited buffering into backpressure: the producer waits instead of growing memory without bound. The alternative — an unbounded deque — lets resident memory climb while the service reports itself healthy, then dies with the queue full of work nobody will finish.
</details>

---

### Question 8
**What is a dead-letter queue's job in a message pipeline?**

- A) Prioritize the most expensive messages
- B) Capture messages that exhausted their retries so one poison item stops blocking the stream
- C) Compress messages before storage
- D) Balance load across consumers

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A poison message fails deterministically; retried forever it starves healthy messages behind it. The DLQ captures it with its error and attempt count, then the workflow continues: inspect, alert, replay — idempotently. A DLQ nobody can replay is only a slower outage; the work is off the stream but still not done.
</details>

---

### Question 9
**In what order does a service shut down gracefully?**

- A) Stop accepting, drain in-flight work, flush and checkpoint, exit
- B) Flush and checkpoint, stop accepting, drain, exit
- C) Exit immediately and let the supervisor restart
- D) Drain, stop accepting, restart the event loop, exit

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** First refuse new work so the load balancer routes elsewhere, then finish what was already accepted, then flush caches and checkpoints, then exit inside the container's stop grace period. Skipping the drain means SIGKILL cuts off in-flight requests; flushing before stopping accepts new work halfway through the flush.
</details>

---

### Question 10
**A client receives HTTP 429 with `Retry-After: 12`. What is the correct behavior?**

- A) Retry immediately with a different endpoint
- B) Retry after a random delay between 0 and 12 seconds
- C) Wait at least 12 seconds before retrying, honoring the header
- D) Treat 429 as non-retryable and fail the request permanently

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** 429 is retryable, but the server has told the client exactly when capacity returns; guessing can land inside the same window and extend it. The contract pairs the header with `X-RateLimit-*` values, and a 429 without `Retry-After` forces the client to guess — that is a server defect, not a client problem.
</details>

---

### Question 11
**Why do HTTP clients configure connect and read timeouts separately?**

- A) The OS requires two different socket options
- B) Connect should be tight; read should reflect the slowest legitimate response
- C) Read timeouts apply only to HTTPS, connect timeouts to HTTP
- D) They are merged at runtime into a single timeout anyway

**Difficulty:** Easy

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A TCP+TLS handshake that has not finished in 5–10 seconds will rarely recover, so connect stays tight. Read must accommodate legitimate slowness — an LLM token stream takes minutes while a reranker takes seconds. One number for both either fails healthy slow calls or tolerates unhealthy fast ones.
</details>

---

### Question 12
**Why does the transactional outbox write the event inside the same transaction as the state change?**

- A) To make the event payload smaller
- B) To avoid using a message broker entirely
- C) To let the database publish events directly
- D) So a crash between write and publish cannot lose the event or publish a phantom

**Difficulty:** Medium

<details>
<summary>View Answer</summary>

**Correct Answer: D**

**Explanation:** Writing to the database and then publishing are two operations; a crash between them loses the event or announces one that never committed. The outbox table makes publication atomic with the write: either both are durable or neither happened, and a separate drainer publishes from the table afterward.
</details>

---

### Question 13
**A token bucket (rate 10/s, capacity 20) sits beside a sliding-window limiter (100 per 60s). A caller sends 100 requests in the first second, then nothing for two minutes. How do they differ?**

- A) Both reject the burst; neither admits any of the 100 requests
- B) The token bucket allows a burst of up to its capacity and then refills at the rate; the sliding window admits only its rolling count
- C) The sliding window allows the full burst; the token bucket never allows bursts
- D) They behave identically because both enforce the same sustained rate

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: B**

**Explanation:** A token bucket's capacity is burst headroom: it admits up to 20 in the first instants, then refills at 10/s. A sliding window counts everything inside the rolling 60s, so it caps strictly by count rather than allowing a capacity-sized burst. Both converge on sustained rate; they differ exactly on burst semantics, which is why the bucket suits a page of parallel requests and the window suits paid model calls.
</details>

---

### Question 14
**A hot cache key with a 60-second TTL expires and 200 concurrent requests all miss at once. Which combination directly attacks the stampede?**

- A) A longer TTL and a bigger cache
- B) A write-through cache and a global lock
- C) Single-flight coalescing plus a jittered TTL on the stored entry
- D) Negative caching with a 10-minute TTL

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: C**

**Explanation:** Single-flight collapses the 200 misses into one upstream computation the others await. Jittered TTL spreads future expirations across time so copies of the key never expire in lockstep. A longer TTL only postpones the burst; global locking serializes unrelated keys; long negative caching actively hides the item that just returned.
</details>

---

### Question 15
**A retrieval dependency is down and the service must degrade. Which ladder is correct?**

- A) Full answer with citations, cached or labeled fallback, explicit degraded error — never a confident ungrounded answer
- B) Confident ungrounded answer, cached fallback, explicit error
- C) Explicit error, then confident ungrounded answer, then cached fallback
- D) Retry the dependency forever until it recovers, then answer

**Difficulty:** Hard

<details>
<summary>View Answer</summary>

**Correct Answer: A**

**Explanation:** The ladder is ordered by trust and pre-programmed before the outage: keep serving what is trustworthy, label what is reduced, and fail explicitly when nothing trustworthy remains. A confidently wrong ungrounded answer is the one unrecoverable outcome — the user cannot tell it from a good one. Retrying forever skips the ladder and burns the deadline against a dead dependency.
</details>

---

## Score Tracking

| Question | Difficulty | Your Answer | Correct? |
|----------|------------|-------------|----------|
| 1 | Easy | | |
| 2 | Easy | | |
| 3 | Medium | | |
| 4 | Medium | | |
| 5 | Easy | | |
| 6 | Medium | | |
| 7 | Easy | | |
| 8 | Medium | | |
| 9 | Medium | | |
| 10 | Medium | | |
| 11 | Easy | | |
| 12 | Medium | | |
| 13 | Hard | | |
| 14 | Hard | | |
| 15 | Hard | | |

**Score:** ____/15

---

## Answer Key

| Q | Answer | Q | Answer | Q | Answer |
|---|--------|---|--------|---|--------|
| 1 | A | 6 | B | 11 | B |
| 2 | B | 7 | C | 12 | D |
| 3 | C | 8 | B | 13 | B |
| 4 | D | 9 | A | 14 | C |
| 5 | B | 10 | C | 15 | A |

---

*Generated for AI Engineer Lab DevOps Track - Quiz 01 of 05*
