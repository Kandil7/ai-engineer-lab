# ML 14: Linear Regression Example — Quiz

> **Topic Overview**: An end-to-end regression workflow on a real dataset.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the first step of an end-to-end regression workflow?**
- A) Fit the model
- B) Understand the data and the target
- C) Tune
- D) Deploy

<details><summary>Reveal Answer</summary>**B.** Understand before modelling.</details>

### Question 2 — Easy
**Why split before preprocessing?**
- A) Speed
- B) To fit any preprocessing on train only and avoid leakage
- C) To clean
- D) To encode

<details><summary>Reveal Answer</summary>**B.** Leakage prevention.</details>

### Question 3 — Medium
**How do you report regression quality?**
- A) Accuracy
- B) RMSE/MAE plus R² on the test set
- C) F1
- D) Precision

<details><summary>Reveal Answer</summary>**B.** Error plus fit.</details>

### Question 4 — Medium
**Why inspect residuals?**
- A) For speed
- B) Patterns reveal model misspecification (non-linearity, heteroscedasticity)
- C) To sort
- D) To cluster

<details><summary>Reveal Answer</summary>**B.** Residual diagnostics.</details>

### Question 5 — Medium
**What does a pipeline bundle?**
- A) Only the model
- B) Preprocessing and the estimator as one fit/predict unit
- C) The data
- D) The metrics

<details><summary>Reveal Answer</summary>**B.** Reproducible steps.</details>

### Question 6 — Hard
**Why compare against a baseline (predict the mean)?**
- A) For style
- B) To know whether the model adds anything
- C) To cluster
- D) To encode

<details><summary>Reveal Answer</summary>**B.** Beat the trivial baseline.</details>

### Question 7 — Hard
**What does RMSE penalise more than MAE?**
- A) Small errors
- B) Large errors, because of the square
- C) Nothing
- D) Outliers equally

<details><summary>Reveal Answer</summary>**B.** Quadratic penalty.</details>

### Question 8 — Hard
**What is the final step before reporting?**
- A) Tune on test
- B) Evaluate once on the untouched test set
- C) Refit on all data first
- D) Drop features

<details><summary>Reveal Answer</summary>**B.** One honest estimate.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You run a regression workflow. |
| 5-6 | Review splitting and metrics. |
| < 5 | Re-read the lecture. |
