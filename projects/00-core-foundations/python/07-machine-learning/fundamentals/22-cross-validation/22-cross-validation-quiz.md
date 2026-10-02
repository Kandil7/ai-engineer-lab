# ML 22: Cross-Validation — Quiz

> **Topic Overview**: k-fold, stratification, and nested tuning.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does k-fold CV do?**
- A) One split
- B) Splits data into k folds, trains on k-1 and validates on the held-out fold, k times
- C) Sorts
- D) Scales

<details><summary>Reveal Answer</summary>**B.** Rotating validation.</details>

### Question 2 — Easy
**Why is CV better than a single split?**
- A) Faster
- B) It averages over folds, giving a more stable performance estimate
- C) Less data
- D) No leakage

<details><summary>Reveal Answer</summary>**B.** Lower variance.</details>

### Question 3 — Medium
**When must you use `StratifiedKFold`?**
- A) Always
- B) For classification, especially imbalanced, to preserve class ratios per fold
- C) For regression
- D) Never

<details><summary>Reveal Answer</summary>**B.** Class balance per fold.</details>

### Question 4 — Medium
**What is `GroupKFold` for?**
- A) Sorting
- B) Keeping all rows of a group in the same fold to prevent leakage
- C) Scaling
- D) Clustering

<details><summary>Reveal Answer</summary>**B.** Grouped leakage prevention.</details>

### Question 5 — Medium
**What is nested CV?**
- A) One loop
- B) An inner loop tunes hyperparameters and an outer loop estimates generalisation
- C) Scaling
- D) Clustering

<details><summary>Reveal Answer</summary>**B.** Unbiased tuning estimate.</details>

### Question 6 — Hard
**Why does tuning on the same CV used for evaluation overfit?**
- A) It does not
- B) The score becomes optimistically biased by selection on that data
- C) It sorts
- D) It scales

<details><summary>Reveal Answer</summary>**B.** Selection bias.</details>

### Question 7 — Hard
**Why is plain k-fold wrong for time-series?**
- A) It is fine
- B) Random folds train on the future to predict the past; use `TimeSeriesSplit`
- C) It is slower
- D) It scales

<details><summary>Reveal Answer</summary>**B.** Temporal order.</details>

### Question 8 — Hard
**What does a large gap between CV and test performance suggest?**
- A) Nothing
- B) Leakage in the CV pipeline or a distribution shift
- C) It is expected
- D) Overfitting only

<details><summary>Reveal Answer</summary>**B.** Investigate the pipeline.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You use CV correctly. |
| 5-6 | Review splitters and nested CV. |
| < 5 | Re-read the lecture. |
