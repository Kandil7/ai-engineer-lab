# ML 09: Feature Scaling — Quiz

> **Topic Overview**: Standardisation, normalisation, and why scale matters.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is standardisation (z-score)?**
- A) Mapping to [0, 1]
- B) Subtracting the mean and dividing by the standard deviation
- C) Rounding
- D) One-hot encoding

<details><summary>Reveal Answer</summary>**B.** Mean 0, std 1.</details>

### Question 2 — Easy
**What is min-max normalisation?**
- A) Map values to [0, 1] using min and max
- B) Mean 0
- C) Rank
- D) Encode

<details><summary>Reveal Answer</summary>**A.** Bounded scaling.</details>

### Question 3 — Medium
**Why do distance-based models need scaling?**
- A) For speed
- B) A large-scale feature dominates distance (e.g. KNN, SVM, K-means)
- C) To cluster
- D) To encode

<details><summary>Reveal Answer</summary>**B.** Undue influence otherwise.</details>

### Question 4 — Medium
**Do tree models need scaling?**
- A) Yes always
- B) Not for correctness; splits are threshold-based and scale-invariant
- C) Only for depth
- D) Only for leaves

<details><summary>Reveal Answer</summary>**B.** Trees are scale-insensitive.</details>

### Question 5 — Medium
**Why fit the scaler on train only?**
- A) Speed
- B) Using test statistics leaks information
- C) It is required
- D) To sort

<details><summary>Reveal Answer</summary>**B.** Fit train, transform test.</details>

### Question 6 — Hard
**What does scaling not fix?**
- A) Everything
- B) Skew or outliers; it shifts the location, not the shape
- C) Distance
- D) Convergence

<details><summary>Reveal Answer</summary>**B.** Shape unchanged.</details>

### Question 7 — Hard
**When is min-max risky?**
- A) Never
- B) With outliers, which compress all other values near 0
- C) Always
- D) For trees

<details><summary>Reveal Answer</summary>**B.** Outlier sensitive.</details>

### Question 8 — Hard
**Why does scaling speed up gradient descent?**
- A) It does not
- B) A better-conditioned loss surface allows a larger stable learning rate and fewer steps
- C) It clusters
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Conditioning.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You scale correctly. |
| 5-6 | Review which models need scaling. |
| < 5 | Re-read the lecture. |
