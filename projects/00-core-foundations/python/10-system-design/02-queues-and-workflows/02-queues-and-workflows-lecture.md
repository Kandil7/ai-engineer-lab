# System Design Lecture 02: Queues and Workflows

## Topic Overview

Embedding a corpus is minutes of work; a search request is milliseconds of latency. The queue is the component that lets both be true — but the naive queue is a duplicate-row factory. Every real message broker delivers **at-least-once**: a worker that finishes the work and dies before acknowledging will be redelivered the job, and the job runs twice. The skill is not "add a queue"; it is designing jobs that survive redelivery, retry transient failures without storming, and divert poison messages to a dead-letter queue where a human looks at them. This lecture builds the job lifecycle, the idempotency contract, backoff and the DLQ, bounded workers, and backpressure — anchored on the Athar ingest flow (`/ingest` enqueues, workers embed, `/search` reads).

The theme: **at-least-once is the only delivery guarantee you can assume — design every handler accordingly.**

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Decide when a queue belongs in the design and when inline is correct.
2. Describe the job lifecycle: enqueue → run → ack | retry | dead-letter.
3. Write idempotent handlers keyed by natural keys.
4. Implement retry with exponential backoff and an attempt cap.
5. Explain the dead-letter queue's role in handling poison messages.
6. Bound worker concurrency for memory and reason about backpressure.

---

## Prerequisites

| Need | Where |
|---|---|
| Async/concurrency basics | `02-advanced-python/04-async-await` |
| Exception design | `02-advanced-python/47-exceptions-advanced` |
| Component contracts | `10-system-design/01-component-contracts/` |
| Background jobs in FastAPI | `05-web-frameworks/fastapi/35-background-jobs` |

---

## 1. When a queue belongs (and when it does not)

**Use a queue when** work is slow (embedding thousands of chunks) but the request must be fast; when work must survive process death (persisted jobs); when bursts arrive (a corpus import) and workers must scale independently of the API.

**Do not use a queue when** the user needs the answer now (call inline, cache the result); when the work is trivial (the queue hop costs more than the job); when strict global ordering is required (queues reorder under retry and scaling).

The Athar split: `/ingest` returns immediately after enqueueing; workers embed in the background; `/search` reads the already-built index. `/answer` synthesizes — if the answer must be immediate, it is inline with a timeout, not queued.

## 2. The job lifecycle

```
enqueue -> ready queue -> worker runs -> success: ack + done
                                    -> failure: retry (attempt < max)
                                    -> failure: dead-letter (attempt = max)
```

A **job** carries `job_id`, `kind`, `payload`, `attempts`, `max_attempts`. The worker acknowledges only after the work is durable (row inserted, index updated). Everything between "work durable" and "ack" is the **at-least-once window** — the reason handlers must be idempotent.

## 3. Idempotency: the handler contract

The dangerous job is "insert chunk". Run twice → duplicate rows → duplicated citations in retrieval. The fix is a **natural key** (content hash, `chunk_id`) and an insert-if-absent store:

```python
def insert_if_absent(self, chunk_id: str, text: str) -> bool:
    if chunk_id in self._rows:
        return False  # second delivery: no-op
    self._rows[chunk_id] = {...}
    return True
```

The exercise simulates the exact failure: the handler inserts `r1`'s chunk and *then* returns failure (crash before ack). The job is redelivered, the handler runs again — and the row count stays 1. That is idempotency under at-least-once.

Rules: every write path in a queued workflow is keyed (natural key or `job_id` with a dedupe table); the key is part of the **contract** (lecture 01) so producers and consumers agree on it.

## 4. Retries with exponential backoff

Transient failures (network blip, DB timeout) deserve retries; permanent failures (malformed payload, missing field) must not be retried — they will fail the same way forever. Two rules keep retries from becoming the outage:

1. **Exponential backoff** — `sleep(base * 2**attempt)` with jitter in production (the classic retry storm: a dependency recovers and 10,000 jobs hit it in the same second).
2. **Attempt cap** — `max_attempts` (3 is typical) bounds the work and routes exhaustion to the DLQ.

The exercise's `flaky_handler_factory` succeeds on attempt 2 and proves the recovery; the poison handler raises on every attempt and lands in the dead-letter queue after the cap.

Classify failures *before* retrying: `except TransientError: retry` vs `except ValidationError: dead-letter`. Retrying a validation error three times is noise that hides the real failures.

## 5. The dead-letter queue

The DLQ is where jobs go when the system gives up — and it is not a garbage bin, it is an **operational surface**:

- A job in the DLQ means a human must decide: fix the data and replay, or drop it.
- DLQ size is a metric; growth means a producer is sending bad payloads.
- Replay is safe *because handlers are idempotent* (section 3).

The rule: **every queue has a DLQ and an owner.** A queue without one accumulates silent failures until the corpus is missing pages nobody noticed.

## 6. Bounded workers and backpressure

A queue without bounds is an OOM machine: a million-record import enqueues a million payloads and the broker (or the Python process) dies. Bound the in-flight work:

```python
while queue.pending:
    batch = min(max_in_flight, queue.pending)
    for _ in range(batch):
        queue.run_once(handler)
```

`max_in_flight` caps memory (the batch is all that is materialized) and gives the producer **backpressure**: when workers are slow, the queue grows; when the queue is bounded, `enqueue` blocks or returns "full" and the producer slows down. Backpressure is how a fast import cannot kill the embedding workers.

The exercise's `run_bounded` reports `4 ok, 1 failed, 1 dead-lettered` for 5 jobs with one poison — the accounting counts *completed* jobs, not attempts.

## 7. The Athar ingest workflow end to end

1. `/ingest` validates the upload (contract, lecture 01) and enqueues one job per batch.
2. Workers pull jobs: normalize text (topic 35), embed chunks, insert into the index keyed by `source_ref`.
3. Idempotency key = `(source_ref, chunk_index)` — a rerun of the import is a no-op.
4. Transient embedder failures retry with backoff; permanent chunk failures dead-letter with the chunk's identity.
5. `/search` reads the index; a "rebuild" job re-derives it from Postgres (the source of truth, backup lecture 07).

The mastery criterion from the skills map — *reruns never produce duplicates* — is this workflow's idempotency contract.

## 8. Best-practice checklist

| Practice | Payoff |
|---|---|
| Idempotent handlers keyed by natural key | at-least-once is safe |
| Attempt cap + exponential backoff + jitter | retries heal, not storm |
| Transient vs permanent error classes | no retrying validation errors |
| DLQ per queue with an owner | failures are visible and replayable |
| Bounded in-flight work | memory capped, backpressure flows |
| Jobs carry identity (`job_id`, `source_ref`) | logs and DLQ entries are actionable |
| Contract for job payloads | producer/consumer agree on shape |
| Monitor DLQ depth and job age | degradation visible before loss |
| Producers rate-limited | import bursts cannot starve the API |

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Handler inserts without a dedupe key | natural key + insert-if-absent |
| Retrying every exception | classify transient vs permanent |
| No attempt cap | cap at 3, dead-letter on exhaustion |
| No DLQ (or unowned DLQ) | one per queue, with an owner |
| Unbounded in-flight batch | `max_in_flight` bound + backpressure |
| Queue as the source of truth | queue is transport; Postgres is truth |
| Assumes exactly-once | assume at-least-once; make handlers idempotent |
| Retry storm on dependency recovery | backoff + jitter |

---

## Mastery Check

You can claim this topic when you can:

1. Write a handler that is a no-op on its second delivery and prove it with a test.
2. Design the retry policy (classes, backoff, cap) for one real dependency.
3. Say what happens to a poison message and who looks at it.
4. Bound a worker loop and explain the backpressure consequence.
5. Draw the Athar ingest flow and mark where idempotency lives.

---

## Next Steps

- Caching and consistency in derived indexes: `03-consistency-and-staleness/`.
- What happens when the worker dies mid-job: `04-failure-modes-and-resilience/`.
- Queue implementations (Redis streams, Celery): `04-databases/redis/05-pubsub-and-streams`.
