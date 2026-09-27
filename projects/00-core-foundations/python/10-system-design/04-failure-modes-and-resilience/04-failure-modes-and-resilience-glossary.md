# Failure Modes and Resilience Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| Failure mode | A specific way a component can break |
| Failure taxonomy | Classes of failure mapped to responses |
| Transient failure | Temporary error worth retrying (timeout, 5xx) |
| Permanent failure | Error that will not change (validation, authz) |
| Partial failure | Work half-done (worker died mid-job) |
| Silent failure | No error raised; damage discovered later |
| FMEA | Failure Mode and Effects Analysis: enumerate, rate, mitigate |
| Blast radius | How far a failure spreads |
| Detection | Metric/log/alarm that makes a failure visible |
| Recovery | The runbook step that restores service |
| Severity | Rating (1–5) ranking what to fix first |
| Timeout | Deadline on an outbound call; bounded damage |
| Deadline budget | The time allowance for one call or request |
| Cascade | Failure chain where each hop amplifies the last |
| Retry storm | Synchronized retries hitting a recovering dependency |
| Backoff + jitter | Delayed, randomized retries preventing storms |
| Attempt cap | Max retries before dead-lettering |
| Load shedding | Explicit rejection of excess work (429/503) |
| Bulkhead | Per-dependency concurrency cap isolating failures |
| Graceful degradation | Designed reduced behavior instead of total outage |
| Degradation ladder | Per-dependency fallbacks, one rung per failure level |
| Integrity rule | Never fabricate data under failure (503 beats lies) |
| Health check | Probe reflecting real dependency capacity |
| Liveness vs readiness | "process is up" vs "can serve correctly" |
| Runbook | Executable procedure for a known failure mode |
| DLQ depth | Count of dead-lettered jobs; a failure-rate metric |
| Job age | Time a job waits; saturation metric |
| Drift | Staleness of derived store vs source (see topic 03) |
| Idempotent resume | Continuing after partial failure without duplication |
| Wedged worker | Worker stuck forever on an unbounded call |

---

## Detailed Definitions

### Failure taxonomy
Transient (retry), permanent (dead-letter), partial (idempotent resume), silent (detect + alert). The response follows the class — retrying everything is the classic mistake.

### FMEA-lite
The table every pipeline deserves: component × failure mode × detection × blast radius × recovery × severity. Written before incidents, reviewed when components change.

### Timeouts
Every outbound call has a deadline. Without one, a slow dependency wedges workers and backs up queues. Timeout converts an unbounded hang into a bounded failure the retry/fallback can handle.

### Cascading failure
A chain of locally reasonable behaviors that amplifies a small failure (the exercise's embedder-blip → queue backup → pool exhaustion → 503 → restart loop). Defenses: backoff + jitter, attempt caps, bulkheads, load shedding.

### Bulkhead
A per-dependency concurrency cap (semaphore/pool). A failing dependency saturates only its own compartment; everything else keeps serving. Rejections are fast and explicit.

### Graceful degradation and the ladder
Designed reduced behavior per failure level — for Athar: full retrieval → retrieval with staleness warning → keyword fallback → cached only → 503 with reason. The integrity rule: never fabricate citations under failure.

### The mastery answer
Worker failure: redelivery + idempotent handlers; no loss, no duplication; DLQ for permanent cases. Stale index: drift metric detects, state machine bounds, rebuild recovers, degradation ladder keeps answers honest meanwhile.

### Detection metrics
DLQ depth, job age, drift, error rates, health checks. Silent failures become loud through metrics, not try/except.

### Runbook
The executable procedure for a known failure mode, extracted from the FMEA's recovery column — written before the incident, not invented during it.
