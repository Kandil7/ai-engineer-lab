"""
Failure Modes and Resilience - System Design Exercises
=======================================================
Topics: taxonomy of failures (transient/permanent/partial/silent),
failure mode analysis, cascading failure, graceful degradation,
timeouts, bulkheads, the "worker died mid-job" scenario.

Why this matters for AI engineering:
    The Athar mastery question: "explain what happens if a worker
    fails, or the index goes stale." The answer must be a designed
    story, not a shrug. This file builds the failure-mode analysis
    (FMEA-lite) for the ingest pipeline: enumerate what breaks, what
    the blast radius is, how it is detected, and what the recovery is.
    Then it demonstrates the four defensive patterns - timeouts,
    retries (cross-ref topic 02), bulkheads, and graceful degradation -
    with the classic cascading-failure story made concrete.

Environment note:
    Pure standard library. Runnable offline.

Run:      python 04-failure-modes-and-resilience.py
Verify:   python 04-failure-modes-and-resilience.py --verify
Reference: https://sre.google/sre-book/addressing-cascading-failures/
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


# ============================================================
# 1. Failure taxonomy
# ============================================================
# Not all failures deserve the same response. Four classes:
#   transient  - timeout, 5xx, network blip  -> RETRY with backoff
#   permanent  - malformed payload, authz     -> NO retry; log + DLQ
#   partial    - worker died mid-job          -> IDEMPOTENT resume
#   silent     - index stale, wrong citation  -> DETECTION + alarms
# The dangerous class is silent: nothing raises, users discover it.


class FailureClass(Enum):
    TRANSIENT = "transient"  # retry
    PERMANENT = "permanent"  # dead-letter
    PARTIAL = "partial"  # resume idempotently
    SILENT = "silent"  # detect + alert


FAILURE_TABLE = [
    (FailureClass.TRANSIENT, "embedder 503", "retry with backoff, 3 attempts"),
    (FailureClass.PERMANENT, "chunk missing text", "dead-letter with chunk id"),
    (FailureClass.PARTIAL, "worker killed mid-insert", "redelivery + idempotent insert"),
    (FailureClass.SILENT, "index 3 writes behind source", "drift metric + rebuild job"),
]

print("1. failure taxonomy -> response")
for cls, example, response in FAILURE_TABLE:
    print(f"   {cls.value:10} {example:30} -> {response}")
print()


# ============================================================
# 2. FMEA-lite: enumerate, rate, mitigate
# ============================================================
# For each component ask: how does it fail? how bad? how do we know?
# how do we recover? Record it in the ops doc BEFORE the incident.


@dataclass(frozen=True)
class FailureMode:
    component: str
    mode: str
    detection: str
    blast_radius: str
    recovery: str
    severity: int  # 1 (nuisance) .. 5 (data loss)


PIPELINE_FMEA = [
    FailureMode(
        "importer",
        "crashes mid-file",
        "job attempts exceeded; DLQ depth",
        "one batch lost, rest of import continues",
        "re-run import; idempotent inserts make it safe",
        2,
    ),
    FailureMode(
        "worker",
        "killed after insert, before ack",
        "job redelivered (at-least-once)",
        "duplicate insert attempt; idempotency absorbs it",
        "nothing needed; handler is idempotent",
        1,
    ),
    FailureMode(
        "worker",
        "killed before insert",
        "job redelivered (at-least-once)",
        "chunk missing until redelivery succeeds",
        "redelivery; backoff on embedder errors",
        2,
    ),
    FailureMode(
        "vector index",
        "writes rejected (full disk)",
        "ingest job errors; drift grows",
        "search serves stale index; new chunks missing",
        "free space, rebuild index from source",
        3,
    ),
    FailureMode(
        "source DB",
        "primary unreachable",
        "health check fails; writes 503",
        "no new ingests; reads from cache/index continue",
        "failover to replica; RPO from WAL (backup lecture)",
        4,
    ),
    FailureMode(
        "derived index",
        "older than source (stale)",
        "drift metric > 0",
        "retrieval misses recent corrections",
        "rebuild job; degraded-mode banner meanwhile",
        3,
    ),
]

print("2. FMEA-lite for the ingest pipeline")
for fm in PIPELINE_FMEA:
    print(f"   [{fm.severity}] {fm.component}: {fm.mode}")
    print(f"       detect: {fm.detection}")
    print(f"       radius: {fm.blast_radius}")
    print(f"       recover: {fm.recovery}")
print()


# ============================================================
# 3. Timeouts - the first defensive line
# ============================================================
# An un-timed call can hang forever, wedging a worker and backing up
# the queue. Every outbound call gets a deadline. The demo: a slow
# function bounded by a timeout wrapper.


class TimeoutError_(Exception):
    pass


def with_timeout(
    fn: Callable[[], object], budget: float, clock: Callable[[], float] = time.monotonic
) -> object:
    """Cooperative timeout: fn must check elapsed; here we simulate.

    In async code use asyncio.wait_for; in threads, futures with
    timeout. The lesson is the BUDGET, not the mechanism.
    """
    start = clock()
    result = fn()
    if clock() - start > budget:
        raise TimeoutError_(f"operation exceeded {budget}s budget")
    return result


def simulate_slow_embedder(delay: float) -> Callable[[], str]:
    def call() -> str:
        time.sleep(delay)
        return "embedded"

    return call


print("3. timeouts bound the damage")
try:
    with_timeout(simulate_slow_embedder(0.05), budget=0.02)
    print("   [unexpected] no timeout raised")
except TimeoutError_ as exc:
    print(f"   slow call cut off: {exc}")
print()


# ============================================================
# 4. Cascading failure - the story to design against
# ============================================================
# The classic chain:
#   embedder blip -> worker retries (no backoff) -> queue backs up
#   -> workers hold connections -> DB connection pool exhausted
#   -> /search 503 -> health checks fail -> orchestrator restarts
#   -> restarts lose in-flight work -> more redeliveries -> worse.
# Each hop is "reasonable"; the system is the bug. Defenses: backoff
# (topic 02), bulkheads (section 5), timeouts (section 3), shedding.


def cascade_simulation() -> dict[str, int]:
    """Toy model: retries without backoff amplify a 1-job failure."""
    queue_depth = 0
    worker_load = 0
    failed_jobs = 1
    for round_no in range(4):
        # each retry wave re-enqueues failed jobs, doubling load
        queue_depth += failed_jobs * 3  # no backoff: instant retry
        worker_load = min(queue_depth, 20)  # workers saturated
        queue_depth -= worker_load // 2  # half processed per round
        failed_jobs = max(1, failed_jobs * 2)  # failures compound
    return {"queue_depth": queue_depth, "worker_load": worker_load, "failed_jobs": failed_jobs}


print("4. cascade: unbounded retries amplify one blip")
result = cascade_simulation()
print(f"   after 4 rounds: {result}")
print("   defenses: backoff+jitter, attempt caps, bulkheads, load shedding")
print()


# ============================================================
# 5. Bulkheads - isolate failure per dependency
# ============================================================
# A bulkhead caps the concurrent resources one dependency can consume,
# so its failure cannot starve everything else. In Python: separate
# pools/semaphores per dependency (embedder vs DB vs index).


class Bulkhead:
    """Per-dependency concurrency cap with rejection on saturation."""

    def __init__(self, name: str, capacity: int) -> None:
        self.name = name
        self.capacity = capacity
        self.in_flight = 0
        self.rejected = 0

    def try_acquire(self) -> bool:
        if self.in_flight >= self.capacity:
            self.rejected += 1
            return False
        self.in_flight += 1
        return True

    def release(self) -> None:
        self.in_flight = max(0, self.in_flight - 1)


def bulkhead_demo() -> dict[str, int]:
    embedder = Bulkhead("embedder", capacity=3)
    db = Bulkhead("db", capacity=5)
    outcome = {"embedder_served": 0, "embedder_rejected": 0, "db_served": 0}
    # embedder dependency is failing/slow: 10 concurrent requests
    for _ in range(10):
        if embedder.try_acquire():
            outcome["embedder_served"] += 1
        else:
            outcome["embedder_rejected"] += 1
    # DB still healthy and serves - the bulkhead kept it isolated
    for _ in range(4):
        if db.try_acquire():
            outcome["db_served"] += 1
    return outcome


print("5. bulkheads isolate a failing dependency")
b_result = bulkhead_demo()
print(
    f"   embedder: {b_result['embedder_served']} served, "
    f"{b_result['embedder_rejected']} rejected (cap 3)"
)
print(f"   db unaffected: {b_result['db_served']} served")
print()


# ============================================================
# 6. Graceful degradation - what the product does when broken
# ============================================================
# The question "what does the user see when X fails?" must have an
# answer per dependency. Degradation ladder for Athar search:
#   index current      -> full retrieval + citations
#   index stale        -> retrieval + STALENESS WARNING in response
#   index unavailable  -> keyword/SQL fallback over source of truth
#   source also down   -> read-only cached answers, explicit notice
# Never: silently serve wrong citations.


DEGRADATION_LADDER = [
    ("index current", "full retrieval + citations"),
    ("index stale (drift > 0)", "retrieval + 'results may lag recent edits'"),
    ("index unavailable", "keyword fallback over Postgres source"),
    ("source down too", "cached answers only + explicit notice"),
    ("nothing left", "503 with reason; never fabricated citations"),
]

print("6. graceful degradation ladder")
for state, behavior in DEGRADATION_LADDER:
    print(f"   {state:24} -> {behavior}")
print()


# ============================================================
# 7. The mastery question, answered
# ============================================================
# Q: "What happens if a worker fails? What if the index goes stale?"
# A worker failure is PARTIAL/TRANSIENT: at-least-once redelivery +
# idempotent handlers (topic 02) means the chunk is not lost and not
# duplicated; if the failure is permanent, the job dead-letters with
# its identity. A stale index is SILENT: drift metric detects it,
# the state machine bounds it (topic 03), the rebuild job recovers it,
# and the product degrades honestly meanwhile.

print("7. the designed answer to the mastery question")
print("   worker fails  -> redeliver / DLQ, no loss, no dup (idempotent)")
print("   index stale   -> drift detects, state machine bounds, rebuild recovers")
print("   and meanwhile -> degradation ladder keeps answers honest")
print()


# ============================================================
# 8. Self-verification
# ============================================================


def _verify() -> bool:
    checks: list[tuple[str, bool]] = []

    try:
        with_timeout(simulate_slow_embedder(0.05), budget=0.02)
        checks.append(("timeout cuts off slow call", False))
    except TimeoutError_:
        checks.append(("timeout cuts off slow call", True))

    bh = Bulkhead("e", capacity=2)
    checks.append(
        (
            "bulkhead admits up to capacity",
            bh.try_acquire() and bh.try_acquire() and not bh.try_acquire() and bh.rejected == 1,
        )
    )

    checks.append(
        ("all failure classes classified", {f[0] for f in FAILURE_TABLE} == set(FailureClass))
    )

    checks.append(
        (
            "FMEA covers every component",
            {fm.component for fm in PIPELINE_FMEA}
            >= {"importer", "worker", "vector index", "source DB", "derived index"},
        )
    )

    checks.append(
        (
            "FMEA has detection+recovery for every mode",
            all(fm.detection and fm.recovery for fm in PIPELINE_FMEA),
        )
    )

    ladder_ok = (
        len(DEGRADATION_LADDER) == 5
        and "lag" in DEGRADATION_LADDER[1][1].lower()
        and "fallback" in DEGRADATION_LADDER[2][1].lower()
        and DEGRADATION_LADDER[-1][1].startswith("503")
        and "never" in DEGRADATION_LADDER[-1][1].lower()
    )
    checks.append(("degradation ladder never silent", ladder_ok))

    ok = True
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    return ok


if __name__ == "__main__":
    if "--verify" in sys.argv:
        print("Verification:")
        sys.exit(0 if _verify() else 1)
    print("Verification (python 04-failure-modes-and-resilience.py --verify):")
    _verify()
