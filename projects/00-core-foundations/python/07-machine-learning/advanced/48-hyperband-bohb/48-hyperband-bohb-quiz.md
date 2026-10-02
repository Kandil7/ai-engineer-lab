# ML 48: Hyperband and BOHB — Quiz

> **Topic Overview**: Multi-fidelity, successive halving, Hyperband, BOHB, and
> reproducibility controls.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the multi-fidelity premise?**
- A) Evaluate everything fully
- B) Many cheap evals to rank, few expensive evals on survivors
- C) Only one budget
- D) Random budgets

<details><summary>Reveal Answer</summary>**B.** Rank cheaply, spend on survivors.</details>

### Question 2 — Easy
**What does successive halving do each round?**
- A) Keeps the top 1/eta and multiplies the budget by eta
- B) Keeps everyone
- C) Drops the best
- D) Halves the budget

<details><summary>Reveal Answer</summary>**A.** Halve survivors, double budget.</details>

### Question 3 — Medium
**Why does Hyperband run multiple brackets?**
- A) To use more GPUs
- B) To avoid choosing between aggressive and conservative halving
- C) To train faster models
- D) To add more layers

<details><summary>Reveal Answer</summary>**B.** Different brackets cover the aggressiveness tradeoff.</details>

### Question 4 — Medium
**What does BOHB add to Hyperband?**
- A) More random sampling
- B) A Bayesian (TPE) sampler choosing the configs
- C) Grid search
- D) More epochs

<details><summary>Reveal Answer</summary>**B.** Bayesian sample efficiency on top of budget efficiency.</details>

### Question 5 — Medium
**What is the role of early stopping in multi-fidelity tuning?**
- A) A safety net only
- B) The budget-freeing mechanism that re-spends on survivors
- C) Unnecessary
- D) A regularization

<details><summary>Reveal Answer</summary>**B.** Stopping losers frees budget for winners.</details>

### Question 6 — Hard
**When does multi-fidelity tuning NOT pay off?**
- A) For trivially fast models where bracket overhead exceeds the model cost
- B) For slow models
- C) For large datasets
- D) For fine-tuning

<details><summary>Reveal Answer</summary>**A.** Cheap fits are better served by plain random/Bayesian search.</details>

### Question 7 — Hard
**Why is a minimum-budget floor needed before early stopping?**
- A) To use more GPU
- B) A noisy early signal could kill a good config at 1 epoch
- C) To slow the search
- D) To match the grid

<details><summary>Reveal Answer</summary>**B.** Stop too early and ranking is pure noise.</details>

### Question 8 — Hard
**Which three controls make a tuning search reproducible?**
- A) Seeds, budget log, frozen search space
- B) GPU, RAM, CPU
- C) Epochs, layers, batches
- D) Only seeds

<details><summary>Reveal Answer</summary>**A.** The result is a function of the search config; log all three.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You tune expensive models efficiently. |
| 5-6 | Review successive halving and brackets. |
| < 5 | Re-read the lecture. |
