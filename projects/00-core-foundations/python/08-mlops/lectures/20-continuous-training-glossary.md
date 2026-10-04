# Continuous Training — Glossary 20

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Continuous training | Practice | Rebuilding a model automatically on signal |
| Concept drift | Degradation | The meaning of the label changes |
| Data drift | Degradation | The inputs change while the label rule stays |
| Label shift | Degradation | The base rate changes |
| Trigger | CT | A named condition that starts a retrain |
| Champion | CT | The current production model |
| Challenger | CT | A retrained candidate awaiting comparison |
| Thrash | Failure | Retraining so often the system promotes noise |
| Cooldown | Guard | A quiet period after promotion before re-evaluation |
| Minimum interval | Guard | The shortest allowed time between retrains |

## Detailed Definitions
### Continuous training
**Definition**: The automation that rebuilds a model when a trigger fires —
drift, performance drop, new data, or schedule — then evaluates and promotes
only winners.
**Related**: Trigger, Champion

### Concept / data / label drift
**Definition**: Three ways a distribution moves: the label's meaning changes,
the inputs change, or the base rate changes. All degrade accuracy without
touching the code.
**Related**: Trigger

### Trigger
**Definition**: A named, checkable condition (schedule, drift threshold,
performance floor, data volume, manual) that starts a retraining run. Recorded
for the audit trail.
```python
should_retrain(metrics, thresholds)  # -> ["drift", "data"]
```
**Related**: Continuous training, Thrash

### Champion / challenger
**Definition**: The champion is the live production model; the challenger is a
retrained candidate that must beat it on the frozen eval set before promoting.
**Related**: Continuous training

### Thrash
**Definition**: The failure mode of retraining constantly — promoting noise,
burning compute, never settling. Prevented by minimum intervals and cooldowns.
**Related**: Cooldown, Minimum interval

### Cooldown / minimum interval
**Definition**: Guards that space retrains apart: no retrain sooner than the
minimum interval, and a quiet period after each promotion.
**Related**: Thrash, Trigger

## Key Concepts Summary
### The loop
- Monitor → trigger → retrain → evaluate → compare → promote.

### The two poles
- Stale (never retraining) vs thrash (retraining constantly).

### The audit
- Every retrain names its reasons; every promotion names its gates.

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Trigger — ___
2. Champion — ___
3. Challenger — ___
4. Thrash — ___
5. Cooldown — ___

**Answers:** 1-c, 2-a, 3-e, 4-d, 5-b where a=the live production model,
b=a quiet period after promotion, c=a named condition that starts a retrain,
d=retraining so often the system promotes noise, e=a candidate awaiting
comparison.
