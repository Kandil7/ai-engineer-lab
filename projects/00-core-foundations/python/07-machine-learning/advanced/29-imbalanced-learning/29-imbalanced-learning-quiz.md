# ML 29: Imbalanced Learning — Quiz

> **Topic Overview**: Class weights, resampling, threshold moving, and honest evaluation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is class imbalance?**
- A) Equal classes
- B) One class is far rarer than another
- C) Missing values
- D) Outliers

<details><summary>Reveal Answer</summary>**B.** Rare-event problem.</details>

### Question 2 — Easy
**Why does accuracy fail under imbalance?**
- A) It is slow
- B) Predicting the majority class alone scores high
- C) It needs scaling
- D) It overfits

<details><summary>Reveal Answer</summary>**B.** Minority ignored.</details>

### Question 3 — Medium
**What does `class_weight='balanced'` do?**
- A) Sorts
- B) Reweights the loss so the minority class contributes more
- C) Resamples
- D) Clusters

<details><summary>Reveal Answer</summary>**B.** Loss reweighting.</details>

### Question 4 — Medium
**What are resampling strategies?**
- A) Scaling
- B) Oversample the minority or undersample the majority (or SMOTE)
- C) Clustering
- D) Encoding

<details><summary>Reveal Answer</summary>**B.** Change the class ratio.</details>

### Question 5 — Medium
**Why must resampling happen inside CV folds?**
- A) Speed
- B) Resampling before splitting leaks synthetic/duplicated minority info across folds
- C) It is required
- D) To sort

<details><summary>Reveal Answer</summary>**B.** Fold-local resampling.</details>

### Question 6 — Hard
**What is SMOTE?**
- A) Undersampling
- B) Synthesising minority points by interpolating between neighbours
- C) Scaling
- D) Clustering

<details><summary>Reveal Answer</summary>**B.** Synthetic minority oversampling.</details>

### Question 7 — Hard
**Why can oversampling hurt?**
- A) It cannot
- B) It can overfit duplicated points and distort the probability distribution
- C) It sorts
- D) It scales

<details><summary>Reveal Answer</summary>**B.** Artificial density.</details>

### Question 8 — Hard
**Which metric pairs best with imbalance?**
- A) Accuracy
- B) PR-AUC / F1 / recall at a chosen threshold
- C) R²
- D) MAE

<details><summary>Reveal Answer</summary>**B.** Minority-focused metrics.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You handle imbalance well. |
| 5-6 | Review weights, resampling, metrics. |
| < 5 | Re-read the lecture. |
