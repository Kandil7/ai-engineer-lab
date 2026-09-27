# System Design Lecture 04: Failure Modes and Resilience

## Topic Overview

The skills map's hardest question: *explain what happens when a worker fails, or the index goes stale.* A team that answers with a shrug ships systems that discover failures from user complaints. This lecture builds the designed answer: a failure taxonomy (transient, permanent, partial, silent) mapped to responses, an FMEA-lite table for the ingest pipeline where every mode has a detection, a blast radius, and a recovery, and the four defensive patterns — timeouts, retries with backoff, bulkheads, graceful degradation — that keep one dependency's failure from becoming the system's outage. The cascading-failure story is the enemy: each hop reasonable, the system the bug.

The theme: **every failure mode gets a detection, a blast radius, and a recovery — written before the incident.**

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Classify failures as transient, permanent, partial, or silent and map each to a response.
2. Produce an FMEA-lite table for a pipeline (mode, detection, radius, recovery).
3. Set timeouts on outbound calls and explain why unbounded calls wedge workers.
4. Describe a cascading failure and the four defenses against it.
5. Implement a bulkhead and explain what isolation protects.
6. Design a graceful degradation ladder per dependency — never silent wrongness.
7. Answer the mastery question as a designed story.

---

## Prerequisites

| Need | Where |
|---|---|
| Queues, retries, idempotency | `10-system-design/02-queues-and-workflows/` |
| Consistency & drift | `10-system-design/03-consistency-and-staleness/` |
| Resilience patterns in FastAPI | `05-web-frameworks/fastapi/47-resilience-patterns` |
| Exception design | `02-advanced-python/47-exceptions-advanced` |

---

## 1. The failure taxonomy

Different failures deserve different responses — the mistake is treating them all as "retry":

| Class | Example | Response |
|---|---|---|
| **Transient** | embedder 503, network blip | retry with backoff, capped attempts |
| **Permanent** | malformed chunk, missing field | no retry; log + dead-letter |
| **Partial** | worker killed mid-job | redelivery + idempotent resume |
| **Silent** | index stale, wrong citation | detection metrics + alarms |

The **silent** class is the dangerous one: no exception raises, no request fails, and users discover the damage later as wrong citations. Silent failures are fought with *invariants and metrics* (drift, no-loss checks), not with try/except.

## 2. FMEA-lite: enumerate, rate, mitigate

For each component, answer four questions **before** the incident:

1. **How does it fail?** (mode)
2. **How do we know?** (detection — metric, alarm, log pattern)
3. **How far does it spread?** (blast radius)
4. **How do we recover?** (runbook)

The exercise's table covers the ingest pipeline: importer crash (one batch, re-run safe because idempotent), worker killed before/after insert (redelivery absorbs both), vector index write rejection (drift grows → rebuild), source DB unreachable (failover, RPO from WAL), stale index (drift metric → rebuild + degraded mode).

Severity 1–5 ranks *what to fix first*: a lost duplicate attempt (1) is nothing; data loss (4–5) is an incident. The table lives in the ops doc and is reviewed when components change.

## 3. Timeouts

An un-timed external call can hang forever — wedging a worker thread, holding a connection, and backing up the queue until the whole pipeline is stuck on one slow dependency. **Every outbound call gets an explicit deadline**: `httpx.Timeout(...)`, `asyncio.wait_for`, or a client-level budget.

The rule from the FastAPI resilience lecture: "no exceptions" — a call without a timeout is a defect. The timeout converts an unbounded hang into a bounded failure that the retry policy (or the fallback) can handle.

## 4. Cascading failure

The canonical chain, made concrete in the exercise:

> embedder blip → workers retry without backoff → queue backs up → workers hold DB connections → connection pool exhausted → `/search` 503 → health checks fail → orchestrator restarts workers → in-flight work is lost → more redeliveries → worse.

Each step is locally reasonable; the *system* is the bug. Four defenses:

1. **Backoff + jitter** (topic 02) — retries don't synchronize into a storm when a dependency recovers.
2. **Attempt caps** — bounded amplification; exhaustion goes to the DLQ.
3. **Bulkheads** (section 5) — a failing dependency cannot consume every worker.
4. **Load shedding** — reject excess work explicitly (429/503) instead of queueing unboundedly.

## 5. Bulkheads

A bulkhead caps the concurrent resources one dependency may consume — named after the ship compartments that keep one breach from sinking the hull. In Python: a semaphore or pool **per dependency** (embedder vs DB vs index), so a slow embedder saturates its own bulkhead and the database keeps serving.

The exercise: an embedder bulkhead of capacity 3 rejects 7 of 10 concurrent requests while the DB bulkhead serves everything. The rejected requests fail *fast and explicitly* — which the degradation ladder (section 6) turns into an honest product behavior.

## 6. Graceful degradation

"What does the user see when X fails?" must have a designed answer per dependency. The Athar ladder:

| State | Behavior |
|---|---|
| index current | full retrieval + citations |
| index stale (drift > 0) | retrieval + "results may lag recent edits" |
| index unavailable | keyword fallback over the Postgres source |
| source down too | cached answers only + explicit notice |
| nothing left | 503 with reason — **never fabricated citations** |

The final rung is the integrity rule of a scholarly product: an honest "cannot answer now" beats a confident wrong citation. Degradation is a *product decision*, made in advance and encoded in the API contract — not an accident of which exception happened to raise.

## 7. The mastery question, answered

**"What happens if a worker fails?"**
A worker failure is partial/transient. At-least-once redelivery plus idempotent handlers (topic 02) means the chunk is neither lost nor duplicated; the job either succeeds on redelivery or dead-letters with its identity for a human. Detection: DLQ depth and job age. Recovery: replay is safe.

**"What happens if the index goes stale?"**
Staleness is silent, so it is *measured*: drift = source version − index version (topic 03). The staleness state machine bounds it (healthy → stale → degraded → broken); the product degrades honestly (ladder rung 2); the rebuild job re-derives the index from Postgres through lineage refs and advances the version stamp. Detection: drift alert. Recovery: rebuild runbook.

Both answers are *designed stories with detections and recoveries* — which is the difference between a system and a hope.

## 8. Best-practice checklist

| Practice | Payoff |
|---|---|
| Classify failures before responding | no retrying validation errors |
| FMEA-lite per pipeline in the ops doc | failures have runbooks, not surprises |
| Timeout on every outbound call | no wedged workers, bounded damage |
| Backoff + jitter + attempt caps | retries heal; no storm on recovery |
| Bulkhead per dependency | one failure can't starve the system |
| Degradation ladder per dependency | product stays honest under failure |
| Never fabricate under failure | integrity of a scholarly product |
| Alert on DLQ depth, drift, job age | silent failures become loud |
| Review FMEA when components change | the table stays true |

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Retry everything | classify: transient vs permanent vs silent |
| No timeout on a dependency call | explicit budget on every outbound call |
| One connection pool for everything | bulkheads per dependency |
| Silent wrong citations under failure | degradation ladder; 503 beats fabrication |
| Failure modes documented only in memory | FMEA table in the repo, reviewed |
| Cascading retries, no backoff | backoff + jitter + caps |
| Health checks that don't reflect real capacity | check dependency health, not just liveness |
| Recovery invented during the incident | runbook written from the FMEA |

---

## Mastery Check

You can claim this topic when you can:

1. Answer "what happens if the worker fails?" and "what if the index is stale?" as designed stories.
2. Produce the FMEA table for your own pipeline with detections and recoveries.
3. Point at every outbound call and its timeout.
4. Describe one cascading chain and the defenses that break it.
5. State the degradation behavior for each dependency failure — and prove nothing is silently wrong.

---

## Next Steps

- Record the key resilience decisions: `05-architecture-decision-records/`.
- Retry/circuit mechanics in code: `05-web-frameworks/fastapi/47-resilience-patterns`.
- The consistency model that detection relies on: `03-consistency-and-staleness/`.
