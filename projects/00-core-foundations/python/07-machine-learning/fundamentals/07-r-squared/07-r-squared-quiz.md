# ML 07: R-Squared — Quiz

> **Topic Overview**: Variance explained, adjusted R², and its limits.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does R² measure?**
- A) Accuracy
- B) The fraction of target variance explained by the model
- C) The slope
- D) The count

<details><summary>Reveal Answer</summary>**B.** Variance explained.</details>

### Question 2 — Easy
**What does R² = 1 mean?**
- A) No fit
- B) A perfect fit on the data
- C) Overfit
- D) Zero variance

<details><summary>Reveal Answer</summary>**B.** All variance explained.</details>

### Question 3 — Medium
**What does R² = 0 mean?**
- A) Perfect
- B) The model does no better than predicting the mean
- C) Negative
- D) Overfit

<details><summary>Reveal Answer</summary>**B.** Baseline performance.</details>

### Question 4 — Medium
**Can R² be negative?**
- A) No
- B) Yes, on test data a model can do worse than the mean
- C) Only for classification
- D) Only for trees

<details><summary>Reveal Answer</summary>**B.** Worse than baseline.</details>

### Question 5 — Medium
**Why is R² insufficient alone?**
- A) It is enough
- B) It never decreases when features are added, so it can reward useless complexity
- C) It is negative
- D) It is slow

<details><summary>Reveal Answer</summary>**B.** Use adjusted R² or validation.</details>

### Question 6 — Hard
**What does adjusted R² add?**
- A) Nothing
- B) A penalty for the number of predictors, discouraging noise features
- C) Causality
- D) Classes

<details><summary>Reveal Answer</summary>**B.** Complexity penalty.</details>

### Question 7 — Hard
**Why compare R² on train vs test?**
- A) For speed
- B) A large gap signals overfitting
- C) It clusters
- D) It encodes

<details><summary>Reveal Answer</summary>**B.** Generalisation gap.</details>

### Question 8 — Hard
**What does a high R² not prove?**
- A) Nothing
- B) Causation or correctness of the model form
- C) Correlation
- D) A fit

<details><summary>Reveal Answer</summary>**B.** Fit is not truth.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You interpret R² correctly. |
| 5-6 | Review adjusted R² and its limits. |
| < 5 | Re-read the lecture. |
