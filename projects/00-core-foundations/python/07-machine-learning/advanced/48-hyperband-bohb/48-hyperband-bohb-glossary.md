# Hyperband and BOHB — Glossary 48

Companion lecture: `48-hyperband-bohb-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Multi-fidelity | Strategy | Vary evaluation budget across trials |
| Fidelity | Budget | How much budget one evaluation gets (epochs, data) |
| Successive halving | Algorithm | Keep top 1/eta, multiply budget by eta |
| Hyperband | Algorithm | Automated successive-halving brackets |
| BOHB | Algorithm | Bayesian sampling combined with Hyperband |
| Bracket | Hyperband | One successive-halving run at a given aggressiveness |
| Early stopping | Tool | Stop losing trials to free budget |
| Budget log | Discipline | Record every trial's fidelity and score |
| eta | Parameter | The halving factor (keep 1/eta each round) |

## Detailed Definitions

### Multi-fidelity
**Definition**: The strategy of evaluating many configurations at low budget and
few at high budget, so total compute is spent on promising configs.
**Related**: Fidelity, Successive halving

### Fidelity
**Definition**: The budget of one evaluation — epochs, data fraction, or
resources. High fidelity is accurate and expensive.
**Related**: Multi-fidelity, Budget log

### Successive halving
**Definition**: The algorithm that evaluates all survivors, keeps the top 1/eta,
and multiplies the budget by eta each round, until one config remains.
**Example**:
```python
survivors = survivors[: len(survivors) // eta]
budget *= eta
```
**Related**: Hyperband, eta

### Hyperband
**Definition**: The algorithm that runs successive halving across multiple
brackets — aggressive and conservative — in one sweep, avoiding the single
aggressiveness choice.
**Related**: Bracket, Successive halving

### BOHB
**Definition**: Bayesian Optimization and Hyperband — Hyperband's budget schedule
with a Bayesian (TPE) sampler choosing the configs, for the best of both.
**Related**: Hyperband, Successive halving

### Bracket
**Definition**: One successive-halving run at a given starting count `n_s`; early
brackets are aggressive, later ones conservative.
**Related**: Hyperband

### Early stopping
**Definition**: Terminating a trial whose metric cannot win, freeing its budget
for better configs — the budget-allocation mechanism of multi-fidelity tuning.
**Related**: Successive halving, Fidelity

### eta
**Definition**: The halving factor — keep the top 1/eta configs and multiply the
budget by eta each round.
**Related**: Successive halving

## Key Concepts Summary

### The core loop
- keep top `1/eta`, `budget *= eta`, repeat.

### The two wins
- Resource efficiency: spend budget on survivors.
- Sample efficiency (BOHB): don't re-try similar configs.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Vary budget across trials — ___
2. How much budget one eval gets — ___
3. Keep top 1/eta, multiply budget by eta — ___
4. Automated successive-halving brackets — ___
5. Bayesian + Hyperband — ___
6. One halving run at a given aggressiveness — ___
7. Stop losing trials to free budget — ___
8. Record every trial's fidelity and score — ___

**Answers:** 1-multi-fidelity, 2-fidelity, 3-successive halving, 4-Hyperband,
5-BOHB, 6-bracket, 7-early stopping, 8-budget log
