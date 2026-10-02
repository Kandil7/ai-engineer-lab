# ML 12: Confusion Matrix — Quiz

> **Topic Overview**: TP/FP/FN/TN, precision, recall, and F1.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What are the four cells of a binary confusion matrix?**
- A) Train/test
- B) TP, FP, FN, TN
- C) Classes
- D) Features

<details><summary>Reveal Answer</summary>**B.** Predicted vs actual.</details>

### Question 2 — Easy
**What is a false positive?**
- A) Predicted positive, actually negative
- B) Predicted negative, actually positive
- C) Correct positive
- D) Correct negative

<details><summary>Reveal Answer</summary>**A.** False alarm.</details>

### Question 3 — Medium
**What is precision?**
- A) TP / (TP + FP) — of predicted positives, how many are correct
- B) TP / (TP + FN)
- C) Accuracy
- D) Recall

<details><summary>Reveal Answer</summary>**A.** Predicted-positive correctness.</details>

### Question 4 — Medium
**What is recall?**
- A) TP / (TP + FN) — of actual positives, how many were found
- B) TP / (TP + FP)
- C) Accuracy
- D) Precision

<details><summary>Reveal Answer</summary>**A.** Actual-positive coverage.</details>

### Question 5 — Medium
**What is F1?**
- A) The mean of precision and recall
- B) The harmonic mean of precision and recall
- C) Accuracy
- D) The sum

<details><summary>Reveal Answer</summary>**B.** Harmonic mean balances both.</details>

### Question 6 — Hard
**When is recall more important than precision?**
- A) Spam filtering
- B) Disease screening, where missing a positive is costly
- C) Never
- D) Always

<details><summary>Reveal Answer</summary>**B.** Missing a case is worse than a false alarm.</details>

### Question 7 — Hard
**Why can accuracy mislead on imbalanced data?**
- A) It cannot
- B) Predicting the majority class everywhere scores high while catching no positives
- C) It sorts
- D) It encodes

<details><summary>Reveal Answer</summary>**B.** Accuracy ignores class ratio.</details>

### Question 8 — Hard
**How is the threshold related to precision/recall?**
- A) Independent
- B) Lowering it raises recall and lowers precision (and vice versa)
- C) Fixed
- D) It only affects accuracy

<details><summary>Reveal Answer</summary>**B.** The operating-point tradeoff.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You read a confusion matrix. |
| 5-6 | Review precision/recall/F1. |
| < 5 | Re-read the lecture. |
