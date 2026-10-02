# ML 32: Feature Selection — Quiz

> **Topic Overview**: Filter, wrapper, embedded methods, VIF, and stability.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why select features?**
- A) Style
- B) Less overfitting, faster training, better interpretability
- C) To sort
- D) To cluster

<details><summary>Reveal Answer</summary>**B.** Signal over noise and cost.</details>

### Question 2 — Easy
**What is a filter method?**
- A) Model-based
- B) Ranks features by a statistic independent of the model (correlation, mutual information)
- C) A wrapper
- D) Embedded

<details><summary>Reveal Answer</summary>**B.** Fast, model-agnostic.</details>

### Question 3 — Medium
**What is a wrapper method?**
- A) Fast statistics
- B) Searches feature subsets using the model's performance (RFE)
- C) A cache
- D) A scaler

<details><summary>Reveal Answer</summary>**B.** Model-aware, expensive.</details>

### Question 4 — Medium
**Give an embedded method.**
- A) Correlation
- B) L1/Lasso coefficients or tree feature importances
- C) RFE
- D) VIF

<details><summary>Reveal Answer</summary>**B.** Selection during training.</details>

### Question 5 — Medium
**What does VIF flag?**
- A) Outliers
- B) Multicollinearity among features
- C) Missing values
- D) Class balance

<details><summary>Reveal Answer</summary>**B.** Redundant features.</details>

### Question 6 — Hard
**Why is permutation importance often preferred to impurity importance?**
- A) Faster
- B) Impurity importance is biased toward high-cardinality features; permutation measures actual effect
- C) It is model-agnostic
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Less biased.</details>

### Question 7 — Hard
**Why must selection happen inside CV?**
- A) Speed
- B) Selecting features using all data leaks target information
- C) It is required
- D) To sort

<details><summary>Reveal Answer</summary>**B.** Fold-local selection.</details>

### Question 8 — Hard
**What does stability mean for selection?**
- A) Speed
- B) The chosen feature set should not flip wildly across folds/resamples
- C) Scalability
- D) Sparsity

<details><summary>Reveal Answer</summary>**B.** Robust choices.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You select features soundly. |
| 5-6 | Review filters vs wrappers vs embedded. |
| < 5 | Re-read the lecture. |
