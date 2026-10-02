# ML 33: Hyperparameter Tuning — Quiz

> **Topic Overview**: Grid vs random vs Bayesian, pruning, and tuning inside CV.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a hyperparameter?**
- A) A learned weight
- B) A setting chosen before training that controls the learning process
- C) A feature
- D) A metric

<details><summary>Reveal Answer</summary>**B.** Set, not learned.</details>

### Question 2 — Easy
**What is grid search?**
- A) Random sampling
- B) Exhaustive evaluation of a parameter grid
- C) Bayesian
- D) Gradient

<details><summary>Reveal Answer</summary>**B.** Try every combination.</details>

### Question 3 — Medium
**Why does random search often beat grid search on the same budget?**
- A) It is exhaustive
- B) It samples the space more diversely, which matters when few parameters matter
- C) It is deterministic
- D) It is Bayesian

<details><summary>Reveal Answer</summary>**B.** Better coverage.</details>

### Question 4 — Medium
**What does Bayesian search (Optuna) do?**
- A) Random
- B) Models the objective and proposes promising trials adaptively
- C) Exhaustive
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Sample-efficient.</details>

### Question 5 — Medium
**What is pruning in tuning?**
- A) Removing features
- B) Stopping unpromising trials early to save budget
- C) Cutting trees
- D) Scaling

<details><summary>Reveal Answer</summary>**B.** Early trial termination.</details>

### Question 6 — Hard
**What is the cardinal rule of tuning?**
- A) Tune on test
- B) Tune inside CV (train/validation), never on the test set
- C) Tune on all data
- D) Tune by hand

<details><summary>Reveal Answer</summary>**B.** Avoid test leakage.</details>

### Question 7 — Hard
**Why can tuning for too long overfit the validation set?**
- A) It cannot
- B) Repeated selection on the same validation data makes the chosen score optimistic
- C) It is slow
- D) It clusters

<details><summary>Reveal Answer</summary>**B.** Selection overfitting.</details>

### Question 8 — Hard
**What should the search space include?**
- A) Everything
- B) Parameters likely to matter: learning rate, depth/regularisation, capacity — not noise
- C) Only defaults
- D) Only one parameter

<details><summary>Reveal Answer</summary>**B.** Focused ranges.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You tune efficiently. |
| 5-6 | Review random/Bayesian and pruning. |
| < 5 | Re-read the lecture. |
