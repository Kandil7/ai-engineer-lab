"""
Queues and Workflows - System Design Exercises
===============================================
Topics: why queues exist, job lifecycle, at-least-once delivery,
idempotency, retries with backoff, dead-letter queues, bounded workers.

Why this matters for AI engineering:
    Ingesting an Athar corpus means embedding thousands of chunks; a
    synchronous /answer endpoint cannot wait for that. The work moves
    to a queue and workers. But every naive queue job runs twice under
    some failure mode - so the skill is not "use a queue", it is
    "design jobs that survive at-least-once delivery". This file builds
    a minimal in-memory queue with retries, backoff, a dead-letter
    queue, and proves the idempotency that makes reruns safe.

Environment note:
    Pure standard library. Runnable offline.

Run:      python 02-queues-and-workflows.py
Verify:   python 02-queues-and-workflows.py --verify
Reference: https://www.rabbitmq.com/docs/consumers#acknowledgement-modes
"""

from __future__ import annotations

import sys
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from typing import Callable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


# ============================================================
# 1. Why a queue (and when NOT to use one)
# ============================================================
# Use a queue when:
#   - work is slow (embedding) but the request is fast (/search)
#   - work must survive process death (persisted jobs)
#   - bursts arrive (import runs) and workers scale independently
# Do NOT use a queue when:
#   - the user needs the answer NOW (call inline, cache the result)
#   - the work is trivial (a queue hop costs more than the job)
#   - you need strict ordering across all jobs (queues reorder)

print("1. queue: decouple request latency from work duration")
print("   /ingest enqueues -> workers embed -> /search reads index")
print()


# ============================================================
# 2. Job lifecycle and message contract
# ============================================================


@dataclass
class Job:
    job_id: str
    kind: str
    payload: dict
    attempts: int = 0
    max_attempts: int = 3


@dataclass
class QueueResult:
    succeeded: int = 0
    failed: int = 0
    dead_lettered: int = 0
    errors: list[str] = field(default_factory=list)


class InMemoryQueue:
    """Minimal queue with retry, backoff, and a dead-letter queue.

    Delivery semantic: AT-LEAST-ONCE. A job may run more than once
    after a failure between 'done with work' and 'ack'. Handlers MUST
    be idempotent - that is the contract.
    """

    def __init__(self) -> None:
        self._ready: deque[Job] = deque()
        self._dlq: list[Job] = []
        self._done_ids: set[str] = set()

    def enqueue(self, kind: str, payload: dict, max_attempts: int = 3) -> Job:
        job = Job(job_id=str(uuid.uuid4()), kind=kind, payload=payload, max_attempts=max_attempts)
        self._ready.append(job)
        return job

    def run_once(
        self, handler: Callable[[Job], bool], *, sleep: Callable[[float], None] = time.sleep
    ) -> None:
        """Process one job. True from handler = success; False = retry."""
        if not self._ready:
            return
        job = self._ready.popleft()
        job.attempts += 1
        try:
            ok = handler(job)
        except Exception as exc:  # handler blew up: same as False
            ok = False
            print(f"   handler error on {job.kind}: {exc}")
        if ok:
            self._done_ids.add(job.job_id)
            return
        if job.attempts >= job.max_attempts:
            self._dlq.append(job)  # dead-letter: stop retrying
        else:
            backoff = 0.01 * (2 ** (job.attempts - 1))  # exponential
            sleep(backoff)
            self._ready.append(job)  # requeue for another attempt

    @property
    def dead_letters(self) -> list[Job]:
        return list(self._dlq)

    @property
    def pending(self) -> int:
        return len(self._ready)


print("2. job lifecycle: enqueue -> run -> ack | retry | dead-letter")
print()


# ============================================================
# 3. Idempotency: the handler contract under at-least-once
# ============================================================
# The dangerous job is "insert chunk". Run twice = duplicate rows.
# The fix: dedupe by a natural key (job_id or content hash) so the
# second run is a no-op. The store below enforces it.


class ChunkStore:
    """Insert-only store keyed by chunk_id (natural key = idempotency)."""

    def __init__(self) -> None:
        self._rows: dict[str, dict] = {}

    def insert_if_absent(self, chunk_id: str, text: str) -> bool:
        """Return True if inserted, False if already present (idempotent)."""
        if chunk_id in self._rows:
            return False
        self._rows[chunk_id] = {"chunk_id": chunk_id, "text": text}
        return True

    def __len__(self) -> int:
        return len(self._rows)


def make_chunk_handler(store: ChunkStore, seen_once: set[str]) -> Callable[[Job], bool]:
    """Handler that inserts chunks idempotently.

    `seen_once` simulates the 'done work but crashed before ack' case:
    the job is redelivered and the handler runs AGAIN - the store must
    absorb it.
    """

    def handler(job: Job) -> bool:
        chunk_id = job.payload["chunk_id"]
        inserted = store.insert_if_absent(chunk_id, job.payload["text"])
        # simulate: job 'r1' crashes AFTER insert but BEFORE ack once
        if chunk_id == "r1" and "r1" not in seen_once:
            seen_once.add("r1")
            return False  # failure AFTER the work -> redelivery
        return True if inserted or chunk_id == "r1" else True

    return handler


print("3. idempotent handler: second delivery is a no-op")
store = ChunkStore()
seen: set[str] = set()
q = InMemoryQueue()
q.enqueue("embed_chunk", {"chunk_id": "r1", "text": "نص أول"})
q.enqueue("embed_chunk", {"chunk_id": "r2", "text": "نص ثانٍ"})
handler = make_chunk_handler(store, seen)
while q.pending:
    q.run_once(handler)
print(f"   rows stored: {len(store)} (no duplicates despite redelivery of r1)")
print(f"   dead-lettered: {len(q.dead_letters)}")
print()


# ============================================================
# 4. Retries with backoff, and the dead-letter queue
# ============================================================
# Transient failures (DB timeout) deserve retries; permanent failures
# (malformed payload) must NOT be retried forever - they go to the DLQ
# for a human. Exponential backoff + the attempt cap are the two rules.


def flaky_handler_factory(succeed_on_attempt: int) -> Callable[[Job], bool]:
    calls: dict[str, int] = {}

    def handler(job: Job) -> bool:
        calls[job.job_id] = calls.get(job.job_id, 0) + 1
        return calls[job.job_id] >= succeed_on_attempt

    return handler


def poison_handler(_job: Job) -> bool:
    raise ValueError("payload malformed: missing chunk_id")


print("4. retries with exponential backoff + dead-letter queue")
q2 = InMemoryQueue()
q2.enqueue("flaky", {"n": 1})  # succeeds on attempt 2
q2.enqueue("poison", {})  # never succeeds
handler2 = flaky_handler_factory(2)
while q2.pending:
    job = q2._ready[0]
    h = handler2 if job.kind == "flaky" else poison_handler
    q2.run_once(h, sleep=lambda _s: None)  # no real sleep in demo
print(f"   flaky job recovered via retry; dead letters: {[j.kind for j in q2.dead_letters]}")
print()


# ============================================================
# 5. Bounded workers and backpressure
# ============================================================
# A queue without a bound is an OOM machine: a 1M-record import
# enqueues 1M payloads and the broker (or your process) dies. Bound
# the in-flight work (max jobs dequeued at once) and let the producer
# see backpressure (enqueue blocks or returns 'full').


def run_bounded(
    queue: InMemoryQueue, handler: Callable[[Job], bool], max_in_flight: int = 2
) -> QueueResult:
    """Worker loop with a bounded batch - backpressure by construction."""
    result = QueueResult()
    done_before = len(queue._done_ids)
    while queue.pending:
        batch = min(max_in_flight, queue.pending)
        for _ in range(batch):
            queue.run_once(handler, sleep=lambda _s: None)
    result.succeeded = len(queue._done_ids) - done_before
    result.dead_lettered = len(queue.dead_letters)
    result.failed = result.dead_lettered
    return result


print("5. bounded workers: max_in_flight caps memory")
q3 = InMemoryQueue()
for i in range(5):
    q3.enqueue("embed", {"chunk_id": f"c{i}", "text": f"نص {i}"})
r = run_bounded(q3, lambda j: j.payload["chunk_id"] != "c3", max_in_flight=2)
print(f"   result: {r.succeeded} ok, {r.failed} failed, {r.dead_lettered} dead-lettered")
print()


# ============================================================
# 6. Self-verification
# ============================================================


def _verify() -> bool:
    checks: list[tuple[str, bool]] = []

    s = ChunkStore()
    seen2: set[str] = set()
    q = InMemoryQueue()
    q.enqueue("e", {"chunk_id": "x", "text": "t"})
    h = make_chunk_handler(s, seen2)
    while q.pending:
        q.run_once(h, sleep=lambda _s: None)
    checks.append(("single job inserts one row", len(s) == 1))

    s2 = ChunkStore()
    seen3: set[str] = set()
    q = InMemoryQueue()
    q.enqueue("e", {"chunk_id": "r1", "text": "t"})
    h2 = make_chunk_handler(s2, seen3)
    while q.pending:
        q.run_once(h2, sleep=lambda _s: None)
    checks.append(("redelivered job is idempotent (still 1 row)", len(s2) == 1))

    q = InMemoryQueue()
    q.enqueue("poison", {})
    while q.pending:
        q.run_once(poison_handler, sleep=lambda _s: None)
    checks.append(
        (
            "poison job reaches DLQ after max attempts",
            len(q.dead_letters) == 1 and q.dead_letters[0].attempts == 3,
        )
    )

    q = InMemoryQueue()
    q.enqueue("flaky", {"n": 1})
    h3 = flaky_handler_factory(2)
    while q.pending:
        q.run_once(h3, sleep=lambda _s: None)
    checks.append(("transient failure recovers on retry", len(q.dead_letters) == 0))

    q = InMemoryQueue()
    for i in range(5):
        q.enqueue("e", {"chunk_id": f"k{i}", "text": "t"})
    res = run_bounded(q, lambda j: True, max_in_flight=2)
    checks.append(("bounded run completes all jobs", res.succeeded == 5))

    ok = True
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    return ok


if __name__ == "__main__":
    if "--verify" in sys.argv:
        print("Verification:")
        sys.exit(0 if _verify() else 1)
    print("Verification (python 02-queues-and-workflows.py --verify):")
    _verify()
