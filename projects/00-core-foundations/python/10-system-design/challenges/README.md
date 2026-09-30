# 10-system-design — Challenge Sets

Practice sets follow [`PRACTICE_SPEC.md`](../../PRACTICE_SPEC.md). Every set is
framed on the Athar question-and-answer pipeline.

| Challenge | Topic | Skills |
|---|---|---|
| `01-component-contracts/` | [Component Contracts](../01-component-contracts/) | classify change, validate-all, rolling-upgrade plans |
| `02-queues-and-workflows/` | [Queues and Workflows](../02-queues-and-workflows/) | idempotency, retry policy, worker pool accounting |
| `03-consistency-and-staleness/` | [Consistency and Staleness](../03-consistency-and-staleness/) | staleness states, cache-aside TTL, versioned apply |
| `04-failure-modes-and-resilience/` | [Failure Modes and Resilience](../04-failure-modes-and-resilience/) | failure taxonomy, bulkheads, degradation ladder |
| `05-architecture-decision-records/` | [Architecture Decision Records](../05-architecture-decision-records/) | ADR layout, completeness validator, decision lifecycle |

## Running

```powershell
python -m pytest 10-system-design/challenges/<name>/test_challenge.py -q
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 10-system-design/challenges/<name>/test_challenge.py -q
```

Default runs target `starter.py` and fail with `NotImplementedError` until solved.
