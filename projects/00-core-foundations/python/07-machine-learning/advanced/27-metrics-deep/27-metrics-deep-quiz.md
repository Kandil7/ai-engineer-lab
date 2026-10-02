# ML 27: Metrics Deep — Quiz

> **Topic Overview**: Precision/recall, ROC vs PR, F-beta, log loss, and threshold cost.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why is accuracy usually a lie?**
- A) It is always wrong
- B) Under imbalance, the majority class dominates it
- C) It is slow
- D) It needs scaling

<details><summary>Reveal Answer</summary>**B.** Class-ratio blind.</details>

### Question 2 — Easy
**What does ROC-AUC measure?**
- A) Accuracy
- B) Ranking quality across all thresholds
- C) Precision
- D) Recall

<details><summary>Reveal Answer</summary>**B.** Threshold-independent ranking.</details>

### Question 3 — Medium
**When does ROC mislead and PR-AUC is better?**
- A) Balanced data
- B) Severe imbalance, where the large TN count flatters ROC
- C) Regression
- D) Clustering

<details><summary>Reveal Answer</summary>**B.** PR focuses on the minority.</details>

### Question 4 — Medium
**What does F-beta weight?**
- A) Accuracy
- B) beta>1 favours recall; beta<1 favours precision
- C) Speed
- D) Scale

<details><summary>Reveal Answer</summary>**B.** Precision/recall emphasis.</details>

### Question 5 — Medium
**What does log loss penalise?**
- A) Ranking
- B) Confident wrong probabilities
- C) Accuracy
- D) Recall

<details><summary>Reveal Answer</summary>**B.** Calibrated confidence.</details>

### Question 6 — Hard
**Why is threshold selection a cost decision?**
- A) It is arbitrary
- B) Different FP/FN costs map to different optimal thresholds
- C) It is fixed at 0.5
- D) It affects speed

<details><summary>Reveal Answer</summary>**B.** Encode the business cost.</details>

### Question 7 — Hard
**What two regression metrics anchor error reporting?**
- A) Precision/recall
- B) RMSE (penalises large errors) and MAE (robust)
- C) F1
- D) ROC

<details><summary>Reveal Answer</summary>**B.** Error scale measures.</details>

### Question 8 — Hard
**What does multi-class averaging (macro vs micro) change?**
- A) Nothing
- B) Macro weights classes equally; micro weights by support
- C) Speed
- D) Scale

<details><summary>Reveal Answer</summary>**B.** Different emphasis.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You pick metrics by problem. |
| 5-6 | Review ROC vs PR, F-beta, log loss. |
| < 5 | Re-read the lecture. |
