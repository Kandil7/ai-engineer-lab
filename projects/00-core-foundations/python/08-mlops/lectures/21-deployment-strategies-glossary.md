# Deployment Strategies — Glossary 21

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Shadow | Strategy | Score live traffic without serving it |
| Canary | Strategy | Route a small live slice, gated at each expansion |
| Blue-green | Strategy | Two environments, one instant traffic switch |
| A/B | Strategy | Split traffic and compare with statistics |
| Rollback | Operation | Restore a prior version, tested and fast |
| Blast radius | Risk | How much damage a bad release does |
| Reversibility | Property | How fast and completely a release can be undone |
| Guardrail | Safety | A metric that must not regress, whatever the lift |
| Promotion | CD | Moving a validated model to more traffic |

## Detailed Definitions
### Shadow
**Definition**: Running a candidate on live traffic without serving it; real
inputs are scored by both versions and compared offline, with zero user impact.
```python
shadow_compare(candidate_scores, champion_scores, tolerance)
```
**Related**: Canary, Reversibility

### Canary
**Definition**: Routing a small fraction of live traffic to the candidate and
expanding the slice through gates. A failure closes the slice.
**Related**: Shadow, Blue-green

### Blue-green
**Definition**: Keeping two production environments and switching all traffic
with one router change; rollback is the same operation in reverse — instant and
total.
**Related**: Canary, Rollback

### A/B
**Definition**: Splitting traffic and comparing a business metric with
statistical significance and guardrails; the winner becomes the default.
**Related**: Canary

### Rollback
**Definition**: A tested, first-class operation restoring a prior version with
its config. Every strategy is judged on how it fails.
**Related**: Reversibility, Blue-green

### Blast radius / reversibility
**Definition**: Blast radius is the damage a bad release does; reversibility is
how fast it can be undone. The two axes of every deployment choice.
**Related**: Rollback

### Guardrail
**Definition**: A metric (fairness, latency, error rate) that must not regress
even when the target metric lifts; a violated guardrail is a failure.
**Related**: A/B

## Key Concepts Summary
### The four strategies
- Shadow (validate), canary (bound), blue-green (revert), A/B (prove).

### The decision order
- Risk → reversibility → cost; test the rollback.

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Shadow — ___
2. Canary — ___
3. Blue-green — ___
4. Rollback — ___
5. Guardrail — ___

**Answers:** 1-e, 2-b, 3-d, 4-a, 5-c where a=a tested undo operation,
b=a live slice gated at each expansion, c=a metric that must not regress,
d=two environments with one instant switch, e=scoring live traffic unserved.
