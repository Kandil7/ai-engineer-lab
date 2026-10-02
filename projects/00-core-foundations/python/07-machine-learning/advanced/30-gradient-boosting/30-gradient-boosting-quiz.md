# ML 30: Gradient Boosting — Quiz

> **Topic Overview**: Sequential error correction, key hyperparameters, and early stopping.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How does boosting differ from bagging?**
- A) Same
- B) Trees are added sequentially, each fitting the previous errors
- C) It is parallel
- D) It clusters

<details><summary>Reveal Answer</summary>**B.** Sequential correction.</details>

### Question 2 — Easy
**What is the learning rate in boosting?**
- A) The step for gradient descent only
- B) The shrinkage applied to each tree's contribution
- C) The depth
- D) The scale

<details><summary>Reveal Answer</summary>**B.** Shrinkage per round.</details>

### Question 3 — Medium
**What does the number of trees (`n_estimators`) control?**
- A) Depth
- B) How many boosting rounds run (more can overfit)
- C) The scale
- D) The kernel

<details><summary>Reveal Answer</summary>**B.** Rounds of boosting.</details>

### Question 4 — Medium
**What is early stopping for?**
- A) Speed
- B) Stop when validation error stops improving, avoiding overfitting
- C) Scaling
- D) Clustering

<details><summary>Reveal Answer</summary>**B.** Best-iteration selection.</details>

### Question 5 — Medium
**Why do GBDTs beat neural nets on tabular data?**
- A) They are newer
- B) They model threshold interactions natively and need less tuning/data
- C) They are linear
- D) They cluster

<details><summary>Reveal Answer</summary>**B.** Tabular inductive bias.</details>

### Question 6 — Hard
**How do learning rate and n_estimators interact?**
- A) Independently
- B) Lower rate needs more trees; they trade off
- C) Higher rate needs more trees
- D) No relation

<details><summary>Reveal Answer</summary>**B.** Joint tuning.</details>

### Question 7 — Hard
**What does `max_depth` control in boosting?**
- A) The number of trees
- B) Interaction order/complexity per tree; shallow trees are the norm
- C) The learning rate
- D) The scale

<details><summary>Reveal Answer</summary>**B.** Individual tree complexity.</details>

### Question 8 — Hard
**Why are boosted models prone to overconfidence?**
- A) They are not
- B) Each round pushes harder on hard examples, sharpening probabilities
- C) They are linear
- D) They cluster

<details><summary>Reveal Answer</summary>**B.** Motivating calibration.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand boosting. |
| 5-6 | Review rate, rounds, early stopping. |
| < 5 | Re-read the lecture. |
