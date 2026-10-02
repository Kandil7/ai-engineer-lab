# 07-machine-learning — 48: Hyperband and BOHB — Multi-Fidelity Tuning

Companion exercise: `48-hyperband-bohb.py`

---

## Topic Overview

Tuning a hyperparameter configuration is expensive because each
evaluation is a
training run. Multi-fidelity optimization makes it cheap by evaluating
*many*
configurations with *little* budget, then progressively giving more
budget only
to the survivors. Hyperband automates this "successive halving" across
brackets;
BOHB adds a Bayesian surrogate so the configs you try are not random.
Together
they are how you tune a slow model (a fine-tune, a large network)
without
burning a month of GPU.

The key insight is that a cheap, noisy evaluation predicts a good
configuration
well enough to discard the bad ones early. You spend most of your budget
on the
few configs that survived, not on evaluating every config to completion.
This is
the same "spend budget where it matters" logic as
`33-hyperparameter-tuning`
pruning, generalized into a standalone scheduling algorithm.

This topic covers successive halving, the Hyperband bracket schedule,
BOHB's
Bayesian + Hyperband combination, and the practical disciplines that
come with
multi-fidelity tuning: early stopping as a first-class tool,
resource-efficient
exploration, and reproducibility via seeds and logged budgets.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the multi-fidelity premise: many cheap evals, few expensive evals.
2. Implement successive halving (halve survivors, double budget).
3. Explain how Hyperband automates the bracket schedule.
4. Describe BOHB as Bayesian sampling on top of Hyperband.
5. Use early stopping as a budget-allocation mechanism, not just a safety net.
6. Reason about the resource-efficiency win over full-grid evaluation.
7. Apply reproducibility controls: seeds, budget logs, and frozen search spaces.
8. Choose multi-fidelity versus plain search by the cost of one evaluation.

## Prerequisites

| Need | Where |
|---|---|
| Grid/random/Bayesian search | `33-hyperparameter-tuning.py` |
| Cross-validation | `22-cross-validation.py` |

## 1. The Multi-Fidelity Premise

### Budget as a dial

"Fidelity" is how much budget you give one evaluation — epochs, data
fraction,
or resource. High fidelity is accurate and expensive; low fidelity is
noisy and
cheap. Multi-fidelity tuning *varies* the fidelity: probe many configs
cheaply,
then spend heavily on the few that look promising.

### Why it works

A config that is terrible at 10% of epochs is almost never good at 100%.
The
early signal, though noisy, is enough to *rank* configs and discard the
bottom
half. Ranking is a much weaker requirement than accurate scoring, and it
is all
successive halving needs.

### The real-world analogy

A hiring pipeline screens a hundred resumes with a five-minute skim,
then
interviews the ten that survived, then does a full-day interview for the
two
finalists. You do not give every candidate the full-day interview.
Multi-fidelity
tuning is the same: a cheap screen, then progressively more expensive
rounds for
the survivors.

### When it fails

The cheap screen only works if the early signal correlates with the
final one. If
a config's first-epoch score says nothing about its hundredth-epoch
score, the
screen discards good configs by accident. Verifying that correlation is
the
precondition for trusting multi-fidelity search.

## 2. Successive Halving

### The loop

Start with `n` configs at a small budget. Evaluate all, keep the top
`1/eta`,
multiply the budget by `eta`, repeat until one config remains:

```python
def successive_halving(configs, min_budget, max_budget, eta, eval_fn):
    survivors = list(configs)
    budget = min_budget
    while len(survivors) > 1 and budget <= max_budget:
        scored = sorted((eval_fn(c, budget), c) for c in survivors, reverse=True)
        survivors = [c for _, c in scored[:max(1, len(survivors) // eta)]]
        budget *= eta
    return survivors[0]
```

### The guarantee

Successive halving spends most of its budget on the survivors, so it
reaches a
good config with far less total compute than evaluating every config at
full
fidelity. The saving is a constant factor per round, and it compounds.

## 3. Hyperband — Automating the Brackets

### The trade successive halving ignores

Successive halving with a large `n` probes aggressively but gives each
config
little budget (risky: a good config might look bad early). With a small
`n` it is
conservative. Hyperband runs *multiple* brackets — aggressive and
conservative —
in one sweep, so it does not have to choose.

### The bracket schedule

For `s_max = floor(log_eta(max_budget / min_budget))`, bracket `s`
starts with
`n_s = ceil((s_max+1)/(s+1) * eta^s)` configs and runs successive
halving. The
early brackets are aggressive, the later ones conservative.

### Why it is clean

Hyperband has essentially one knob (`eta`, usually 3) and a budget, and
it
allocates across the aggressiveness spectrum automatically. That is why
it became
the standard multi-fidelity baseline — you get the tradeoff handled for
you.

## 4. BOHB — Bayesian + Hyperband

### Adding the surrogate

BOHB (Bayesian Optimization and Hyperband) replaces Hyperband's random
config
sampling with a Bayesian model — a tree-structured Parzen estimator, the
same
family as Optuna's TPE — so each new config is chosen where past results
suggest
improvement. You get Hyperband's budget efficiency *and* Bayesian sample
efficiency in one loop.

### Why the combination matters

Hyperband wastes budget re-trying similar configs; Bayesian sampling
avoids that.
BOHB is the state of the art for tuning expensive models without a
massive
compute budget, and it is available in Optuna via `HyperbandPruner`
combined
with a `TPESampler`.

## 5. Early Stopping as a First-Class Tool

### More than a safety net

In multi-fidelity tuning, early stopping is the mechanism that frees
budget. A
trial that is clearly losing at epoch 10 is stopped, and its budget is
re-spent
on a promising config. This is exactly `33-hyperparameter-tuning`
pruning, but
the point here is that it is *essential*, not optional.

### The discipline

Early stopping needs a well-defined rule (metric plateau, percentile of
running
trials) and a floor (never stop before a minimum budget), or a noisy
early
signal stops a config that would have won. The floor is what protects
against the
"good config looks bad early" failure.

## 6. Resource-Efficient Exploration

### The budget accounting

The win over full-grid is quantifiable: full grid costs `n_configs x
max_budget`;
Hyperband costs roughly `s_max x n_top x max_budget`, a large
constant-factor
saving. The saving grows with the cost of a single full-fidelity
evaluation.

### When it helps most

Multi-fidelity tuning pays off exactly when a full evaluation is
expensive —
slow models, big datasets. For fast models (a small sklearn fit), the
overhead
of the bracket machinery can exceed the saving, and plain
random/Bayesian search
is the better tool. Match the method to the cost of one evaluation.

## 7. Reproducibility Controls

### The three controls

- **Seeds** — pin the sampler, the data splits, and any stochastic training.
- **Budget log** — record every trial's fidelity and score, so a result is
  attributable to a budget, not magic.
- **Frozen space** — log the exact search space; a result is meaningless without
  the ranges it was found in.

### Why they matter for tuning specifically

Tuning is a *search*, so its result is a function of the search
configuration.
Without seeds, budget logs, and a frozen space, "the best config was
0.92" is
unreproducible — you cannot re-run the search or compare it to the next
one.

## 8. A Worked Hyperband Example

### The setup

Suppose `max_budget = 27` epochs and `min_budget = 1`, with `eta = 3`.
Then
`s_max = floor(log_3(27)) = 3`, giving four brackets. Each bracket runs
successive halving at a different starting configuration count.

### The brackets

Bracket `s = 0` is the most aggressive: `n = ceil(4/1 * 3^0) = 4`
configs, each
getting little budget, halving to 1 survivor quickly. Bracket `s = 3` is
the most
conservative: `n = ceil(4/4 * 3^3) = 27` configs, run nearly to
completion. The
middle brackets span the tradeoff.

### What you observe

Across the four brackets, Hyperband explores a wide range of configs
cheaply and
confirms the best few expensively, all in one sweep. The aggressive
brackets find
promising regions; the conservative brackets confirm them. The total
budget is
bounded and far below a full 27-epoch grid over every config.

### The intuition to keep

Hyperband is not magic — it is a *budget scheduler*. The intelligence
comes from
the observation that cheap rankings are usually good enough to discard
the
bottom half, and the brackets exist to cover the cases where that
observation is
wrong.

## 9. Choosing eta and Budgets

### The eta dial

`eta` is the halving factor — how aggressively you cut. `eta = 3` is the
standard; larger `eta` (more aggressive) spends less per round but risks
more on
early noise, smaller `eta` is gentler but pricier. In practice `eta = 3`
is
rarely worth changing.

### The budget floor

The `min_budget` floor is the single most important choice, because it
is the
guard against the "good config looks bad early" failure. A floor of 1
epoch is
pure noise; a floor of a few epochs is a real signal. Set it to the
smallest
budget at which a cheap evaluation still *correlates* with a full one.

### The reproducibility tie-in

Whatever you choose, record `eta`, `min_budget`, `max_budget`, and the
seed.
Because Hyperband's result is a function of its schedule, the budget
parameters
are part of the answer, not an implementation detail — the same point
the
reproducibility section (`7`) makes about the whole search.

## 10. Common Failure Modes of Multi-Fidelity Search

### Failure 1: No cheap-signal correlation

If a config's score at low fidelity does not predict its score at high
fidelity,
the screen discards good configs by accident. This is the precondition
failure,
and it is silent — the search runs, returns a config, and the config is
simply
not the best. Diagnose it by measuring the rank correlation between
cheap and
full evaluations on a sample.

### Failure 2: A floor that is too low

A minimum budget of one epoch is noise, and the first halving round is
then a
coin flip. Good configs get eliminated early, and the search converges
on
whichever config got lucky. The fix is a floor at which cheap evals are
at least
weakly predictive.

### Failure 3: Too few negatives for the Bayesian sampler

BOHB's TPE needs enough completed trials to build a meaningful
surrogate. In a
tiny budget, the Bayesian component has nothing to learn from and
behaves like
random search. The fix is either more trials or accepting random search
for the
first bracket.

### Failure 4: Ignoring the fixed-cost overhead

Every trial has a fixed startup cost (data loading, compilation)
separate from
its budget. When that fixed cost dominates, multi-fidelity's
proportional saving
evaporates. The fix is to measure the fixed cost and include it in the
decision.

### Failure 5: Reporting the best trial, not the search result

The best trial's score is optimistically biased — you selected it. The
honest
report is the search's budget, the search space, and a fresh evaluation
of the
chosen config. This is the selection-optimism trap (`33`) in
multi-fidelity form.

## 11. Multi-Fidelity vs Plain Search — A Decision Table

### The table

| Situation | Best method |
|---|---|
| Fast model, small space | Grid or random search |
| Fast model, many dimensions | Random search |
| Slow model, bounded budget | Successive halving |
| Slow model, unknown aggressiveness | Hyperband |
| Slow model, want sample efficiency | BOHB (TPE + Hyperband) |
| No cheap-signal correlation | Plain search on full budget |

### How to read it

The first question is the cost of one full evaluation: cheap models do
not need
multi-fidelity. The second is whether cheap evals rank correctly: if
not, plain
search is the only honest option. Only when the model is slow *and* the
signal
correlates does multi-fidelity pay.

### The one-line rule

Multi-fidelity is a bet that a cheap ranking predicts an expensive one.
When that
bet is good, it saves most of the budget; when it is bad, it is worse
than doing
nothing. Verify the bet before making it.

## Real-World Application

- **Fine-tuning hyperparameters** — a LoRA or full fine-tune where one run is hours
  on a single GPU.
- **Neural architecture search** — treating architecture choices as the search
  space, with multi-fidelity ranking.
- **Slow training pipelines** — any job where a full evaluation is the bottleneck.
- **The DevMate case** — tuning retrieval chunking/embedding parameters where a
  full eval run is expensive.

## Common Mistakes to Avoid

### Mistake 1: Full-grid evaluation of expensive models
```
# WRONG — every config trained to completion when a single run takes hours
# CORRECT — successive halving / Hyperband: rank cheaply, spend on survivors
```

### Mistake 2: Stopping trials too early
```
# WRONG — a minimum-budget floor of 1 epoch, so noise kills good configs
# CORRECT — a floor (min_budget) and a percentile-based stop rule
```

### Mistake 3: Forgetting the cheap-signal assumption
```
# WRONG — using multi-fidelity when low fidelity gives no ranking signal at all
# CORRECT — verify cheap evals correlate with full evals before trusting them
```

### Mistake 4: Unlogged budgets and seeds
```
# WRONG — "best config 0.92" with no record of budget or seed
# CORRECT — log budget, seed, and the frozen search space
```

### Mistake 5: Using Hyperband for trivially fast models
```
# WRONG — bracket overhead exceeding the cost of the model itself
# CORRECT — plain random/Bayesian for cheap fits; multi-fidelity for slow ones
```

### Mistake 6: A single bracket as a poor man's Hyperband
```
# WRONG — one successive-halving run, which must pick an aggressiveness it cannot know
# CORRECT — the full bracket sweep, which is the whole point of Hyperband
```

## Best Practices

1. Match the method to the cost of one full evaluation.
2. Verify the cheap-signal assumption before committing to multi-fidelity.
3. Set a minimum budget floor so early stopping never kills on noise.
4. Use BOHB (TPE + Hyperband) for the best of both worlds.
5. Log every trial's fidelity, score, and seed.
6. Freeze and record the search space.
7. Re-run the search with different seeds to check stability.
8. Report the budget used, not just the final metric.

## Complexity and Cost

| Method | Evals | Notes |
|---|---|---|
| Full grid | n x max_budget | Baseline; prohibitive for slow models |
| Successive halving | ~n x min_budget + survivors | Rank cheaply, spend on survivors |
| Hyperband | multiple brackets | No single aggressiveness choice |
| BOHB | Hyperband + TPE | Best budget + sample efficiency |

## AI Engineering Relevance

**Where this shows up:** tuning a fine-tune or a large model where one full run is
hours on a GPU. On this workstation a single RTX 5000 makes every full
evaluation
precious, so multi-fidelity tuning is the difference between tuning in a
day and
tuning in a month.

| Concept here | Used for |
|---|---|
| Successive halving | Ranking configs cheaply |
| Hyperband | Automating bracket aggressiveness |
| BOHB | Adding Bayesian sampling to Hyperband |
| Budget log | Reproducible search results |

**Scale note:** the resource argument is the same as `33`'s — a well-designed
search (Bayesian + pruning) cuts GPU hours. Hyperband/BOHB is that
argument
taken to its logical conclusion for expensive models.

## Key Takeaways

1. Multi-fidelity ranks many configs cheaply and spends budget on survivors.
2. Successive halving keeps the top 1/eta and multiplies budget by eta each round.
3. Hyperband runs aggressive and conservative brackets so you don't choose.
4. BOHB adds a Bayesian sampler to Hyperband for sample efficiency.
5. Early stopping is the budget-freeing mechanism; a floor protects against noise.
6. Reproducibility needs seeds, a budget log, and a frozen search space.

## Self-Check Questions

1. What is the multi-fidelity premise, and what precondition must hold for it to work?
2. Walk through one round of successive halving with eta = 3.
3. Why does Hyperband run multiple brackets instead of one halving run?
4. What does BOHB add to Hyperband, and why does the combination matter?
5. Why is a minimum-budget floor needed before early stopping?
6. Which three controls make a tuning search reproducible?

## Summary

| Concept | Description |
|---|---|
| Multi-fidelity | Many cheap evals, few expensive evals |
| Successive halving | Keep top 1/eta, multiply budget by eta |
| Hyperband | Automated brackets, aggressive to conservative |
| BOHB | Bayesian sampling on Hyperband |
| Reproducibility | Seeds, budget log, frozen space |

## Quick Reference

| Task | Idiom |
|---|---|
| Halving round | keep top `n // eta`, `budget *= eta` |
| Bracket size | `n_s = ceil((s_max+1)/(s+1) * eta**s)` |
| BOHB in Optuna | `HyperbandPruner` + `TPESampler` |
| Reproduce | seed everything + log budget |

## Further Reading / Connections

- `33-hyperparameter-tuning-lecture.md` — the single-fidelity search this extends.
- `22-cross-validation-lecture.md` — the honest-evaluation discipline.
- Li et al., "Hyperband"; Falkner et al., "BOHB".
- Official docs: <https://optuna.readthedocs.io/en/stable/reference/pruners.html>

## Next Steps

Next: **[49 — Quantization](../advanced/49-quantization-lecture.md)** —
shrink the model, not the quality.



