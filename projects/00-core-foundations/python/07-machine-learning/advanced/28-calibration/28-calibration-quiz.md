# ML 28: Calibration — Quiz

> **Topic Overview**: Turning scores into trustworthy probabilities.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is calibration?**
- A) Scaling
- B) Making predicted probabilities match observed frequencies
- C) Clustering
- D) Encoding

<details><summary>Reveal Answer</summary>**B.** Probabilities mean what they say.</details>

### Question 2 — Easy
**Which model is typically well-calibrated by nature?**
- A) SVM
- B) Logistic regression
- C) Random forest
- D) KNN

<details><summary>Reveal Answer</summary>**B.** Trained on log loss.</details>

### Question 3 — Medium
**Why do boosted trees often need calibration?**
- A) They do not
- B) They chase the hardest examples, producing overconfident scores
- C) They are linear
- D) They cluster

<details><summary>Reveal Answer</summary>**B.** Overconfidence.</details>

### Question 4 — Medium
**What does a reliability diagram show?**
- A) Accuracy
- B) Predicted probability vs observed frequency per bin
- C) Ranking
- D) Speed

<details><summary>Reveal Answer</summary>**B.** Calibration curve.</details>

### Question 5 — Medium
**What are the two common calibration methods?**
- A) Scaling/normalising
- B) Platt scaling (sigmoid) and isotonic regression
- C) Voting/stacking
- D) Bagging/boosting

<details><summary>Reveal Answer</summary>**B.** Parametric vs non-parametric.</details>

### Question 6 — Hard
**Why does calibration matter downstream?**
- A) For speed
- B) Decisions that weight probabilities (expected cost, auto-approval) depend on honest scores
- C) For sorting
- D) For clustering

<details><summary>Reveal Answer</summary>**B.** Decisions use the numbers.</details>

### Question 7 — Hard
**What metric measures calibration, e.g. Brier score?**
- A) Accuracy
- B) Mean squared difference between probability and outcome
- C) ROC
- D) F1

<details><summary>Reveal Answer</summary>**B.** Brier score.</details>

### Question 8 — Hard
**Why is calibration distinct from discrimination?**
- A) They are the same
- B) A model can rank well (discriminate) but still output miscalibrated probabilities
- C) Calibration needs more data
- D) Discrimination is accuracy

<details><summary>Reveal Answer</summary>**B.** Ranking vs probability truth.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand calibration. |
| 5-6 | Review reliability diagrams and methods. |
| < 5 | Re-read the lecture. |
