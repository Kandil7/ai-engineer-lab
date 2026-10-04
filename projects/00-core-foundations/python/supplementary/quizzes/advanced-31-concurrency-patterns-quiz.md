# Advanced Python Quiz 31 — Concurrency Patterns

**Course:** AI Engineer — Core Foundations · Python
**Level:** Advanced · **Topic:** 31 — Concurrency Patterns
**Questions:** 20 (6 Easy · 9 Medium · 5 Hard)
**Time:** 30 minutes

---

## Instructions

- Each question has exactly **one** correct answer (A–D).
- **Code-output questions** show code; choose the output.
- Answers and explanations are at the end — do the quiz **before** reading the key.
- Score yourself: `Score Tracking` section at the end.

---

## Questions

### Easy

**1. What does "backpressure" mean in a producer-consumer pipeline?**

A) The producer slows down or is refused when the buffer is full
B) The consumer requests more data from the producer
C) The queue grows without bound to absorb bursts
D) The system raises an error on every produced item

**2. What does `queue.Queue(maxsize=2)` do when a third `put()` is attempted with a timeout?**

A) Blocks forever until space frees up
B) Raises `queue.Full` after the timeout elapses
C) Silently drops the item
D) Creates a new queue for the overflow

**3. Which primitive makes a token bucket testable without sleeping?**

A) A `Lock` around `try_acquire()`
B) An injected `now` clock callable
C) `time.sleep(0.001)` in tests
D) A `threading.Event` for synchronization

**4. What is the purpose of the GIL warning in this topic?**

A) Threads are ideal for CPU-bound work because of the GIL
B) Threads only speed up I/O-bound work; CPU-bound work needs processes or native libraries
C) The GIL makes all thread programs faster than async
D) The GIL is a bug that only affects Python 2

**5. Which state does a circuit breaker enter after `threshold` consecutive failures?**

A) `closed`
B) `half_open`
C) `open`
D) `draining`

**6. What does a worker's graceful shutdown guarantee?**

A) It kills all threads immediately, losing in-flight work
B) No new work is accepted and all in-flight work completes
C) The queue is discarded and recreated empty
D) It retries every queued item exactly once

### Medium

**7. What happens in the R1.1 deadlock from `04-queues.py`?**

A) Two threads each hold one lock and wait for the other
B) A producer blocks forever on a full buffer because the consumer never runs
C) A consumer spins forever on an empty queue
D) The GIL prevents the producer thread from being scheduled

**8. Given:**

```python
q = queue.Queue(maxsize=2)
q.put(1)
q.put(2)
try:
    q.put(3, timeout=0.05)
except queue.Full:
    print("full")
print(q.get())
```

**What is the output?**

A) `full` then `1`
B) `full` then `3`
C) `1` then `full`
D) `3` then `full`

**9. `pool.map(fetch, range(8))` with `max_workers=4` — what is guaranteed about the results?**

A) They are returned in completion order (fastest first)
B) They are returned in input order (0 to 7)
C) They are returned in random order
D) They are returned in reverse input order

**10. In the token bucket demo, `capacity=3, rate=1.0`. After draining the bucket, how many tokens exist exactly 1.0 second later (fake clock)?**

A) 3
B) 1
C) 0.5
D) 0

**11. Why does retry use "full jitter" (`random.uniform(0, base * 2 ** attempt)`) instead of a fixed delay?**

A) Fixed delays are forbidden by the GIL
B) Random delays desynchronize retrying clients, preventing a thundering herd
C) Jitter makes retries succeed faster than backoff
D) Jitter is required for the token bucket to work

**12. While the breaker is `open`, calling `call()`:**

A) Invokes `fn` once as a probe
B) Raises `RuntimeError` without invoking `fn`
C) Blocks until the cooldown elapses
D) Retries `fn` with jitter

**13. Which pattern isolates slow dependencies so one cannot exhaust the pool of another?**

A) Token bucket
B) Circuit breaker
C) Bulkhead
D) Fan-in

**14. What is the difference between deadlock and livelock?**

A) Deadlock is caused by the GIL; livelock by CPU contention
B) In deadlock threads wait forever; in livelock threads keep acting but never make progress
C) Livelock only happens with processes; deadlock only with threads
D) There is no difference; they are synonyms

**15. Why does idempotency make retries safe?**

A) It guarantees the operation runs at most once
B) Re-applying the operation yields the same result as applying once
C) It removes the need for timeouts
D) It makes every operation O(1)

### Hard

**16. Given a token bucket with `capacity=2, rate=2.0` and a fake clock at t=0 (bucket full), what is the sequence of results for 5 instant `try_acquire()` calls, then advancing the clock by 0.5s and calling once more?**

A) `[T, T, F, F, F]` then `F`
B) `[T, T, F, F, F]` then `T`
C) `[T, T, T, T, T]` then `T`
D) `[F, F, F, F, F]` then `T`

**17. In the circuit breaker, what happens after a success in the `half_open` state?**

A) The circuit returns to `open`
B) The circuit returns to `closed` and failure count resets to 0
C) The circuit stays `half_open` until cooldown expires
D) The circuit increments `short_circuited`

**18. Given the `retry_with_jitter` implementation with `base_delay=0.2`, in which window is the delay for attempt 2 (the 3rd attempt)?**

A) `[0, 0.2]`
B) `[0, 0.4]`
C) `[0, 0.8]`
D) `[0, 1.6]`

**19. In `BoundedPipeline`, `produce` returns `False` when the queue is full. The `max_observed` watermark is updated only when a `put` succeeds. Why does this correctly bound memory?**

A) Because the queue internally compresses items
B) Because items are only counted after successful enqueue, so the queue never exceeds `maxsize`
C) Because `maxsize` is enforced by the GIL
D) Because `consume` drops items automatically

**20. A batch job embeds 10,000 chunks. Which combination of patterns is the correct reliability stack?**

A) Unbounded queue + fixed-delay retry + no breaker
B) Bounded queue with timeout + token bucket per provider + breaker per provider + retry with jitter + idempotent writes
C) Threads for CPU-bound chunking + infinite retries + no rate limit
D) Circuit breaker only, no queue or rate limiting

---

## Score Tracking

| Section | Count | Your Score |
|---------|-------|------------|
| Easy (Q1–6) | 6 | /6 |
| Medium (Q7–15) | 9 | /9 |
| Hard (Q16–20) | 5 | /5 |
| **Total** | **20** | **/20** |

**Rating:** 18–20 → Ready for production pipelines · 14–17 → Review sections 4.1–4.8 · <14 → Re-read the lecture, especially R1.1 and the breaker state machine.

---

## Answer Key

**1. A** — Backpressure slows or refuses the producer when the buffer is full, keeping memory bounded.
*Distractors:* B describes demand signaling, C is the opposite (unbounded growth), D is not backpressure but an error policy.

**2. B** — `Queue.put(item, timeout=...)` blocks up to the timeout, then raises `queue.Full`.
*Distractors:* A is the R1.1 hang (no timeout), C is data loss, D is not how queues work.

**3. B** — The injectable `now` clock lets tests advance time instantly and deterministically.
*Distractors:* A helps thread safety but not time, C introduces flakiness, D is for signaling not time.

**4. B** — The GIL serializes Python bytecode, so threads speed up I/O-bound work only; CPU-bound work needs processes or native libraries.
*Distractors:* A is the opposite of the truth, C ignores asyncio, D is false (it is a design choice).

**5. C** — After `threshold` consecutive failures the breaker goes `open` and fails fast.
*Distractors:* A is the normal state, B is entered after cooldown, D is not a breaker state.

**6. B** — Graceful shutdown sets an Event; the worker drains in-flight work before exiting.
*Distractors:* A is a forced kill, C loses work, D is not what drain means.

**7. B** — The R1.1 producer blocks inside `not_full.wait()` on a full buffer because the consumer never runs (same-thread demo).
*Distractors:* A is classic lock-order deadlock, C is a busy-wait not a deadlock, D is not the R1.1 cause.

**8. A** — `put(3)` on a full queue raises `Full` (printing `full`), then `get()` returns the first item, `1`.
*Distractors:* B puts `3` last — wrong, `3` was never enqueued; C reverses the print order; D shows `3` as first, never enqueued.

**9. B** — `Executor.map` returns results in input order, deterministically.
*Distractors:* A is `as_completed` behavior, C/D are not guaranteed by `map`.

**10. B** — Rate 1.0 tokens/sec × 1.0s = exactly 1 token.
*Distractors:* A is capacity (only if never drained), C is 0.5s worth, D ignores refill.

**11. B** — Jitter desynchronizes retrying clients so they do not re-stampede the provider in waves.
*Distractors:* A is false, C is not what jitter does, D is unrelated.

**12. B** — While open, `call()` raises `RuntimeError` immediately and increments `short_circuited`; `fn` is never invoked.
*Distractors:* A is half-open behavior, C/D are not breaker behavior.

**13. C** — Bulkhead isolates dependencies into separate pools (ship compartments).
*Distractors:* A limits rate, B fails fast, D merges results.

**14. B** — Deadlock: threads wait forever; livelock: threads keep acting but make no progress.
*Distractors:* A/GIL and C/process-vs-thread claims are false, D is false.

**15. B** — Idempotent operations yield the same result on re-application, so retries/replays are no-ops.
*Distractors:* A is exactly-once (different guarantee), C/D are unrelated.

**16. B** — Burst of 2 → `[T, T]`, then `[F, F, F]` (empty). After 0.5s at rate 2.0: 1 token → `T`.
*Distractors:* A would need rate < 2.0, C ignores the bucket being empty, D ignores the initial full bucket.

**17. B** — Success in half-open closes the circuit and resets the failure count to 0.
*Distractors:* A is the failure path, C would never recover, D counts rejections not recoveries.

**18. C** — The window for attempt `n` is `base * 2 ** n`, so attempt 2 → 0.2 × 4 = `[0, 0.8]`.
*Distractors:* A is attempt 0, B is attempt 1, D is attempt 3.

**19. B** — `maxsize` is enforced by `queue.Queue` itself; `max_observed` simply records the largest size actually reached. The queue never exceeds its bound.
*Distractors:* A is false, C misunderstands the GIL (it does not enforce queue bounds), D would lose data.

**20. B** — Bounded queue + backpressure, token bucket (rate contract), breaker (fail fast), retry with jitter (transient failures), idempotent writes (crash-safe resume).
*Distractors:* A is the memory-leak + stampede stack, C abuses threads for CPU work and retries forever, D lacks the pipeline and rate protection entirely.
