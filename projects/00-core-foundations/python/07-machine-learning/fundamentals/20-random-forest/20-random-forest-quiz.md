# ML 20: Random Forest — Quiz

> **Topic Overview**: Bagging trees, feature randomness, and out-of-bag estimates.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a random forest?**
- A) One deep tree
- B) An ensemble of decorrelated decision trees whose votes are aggregated
- C) A line
- D) A cluster

<details><summary>Reveal Answer</summary>**B.** Many trees vote.</details>

### Question 2 — Easy
**How does it reduce overfitting vs a single tree?**
- A) It does not
- B) Averaging many decorrelated trees lowers variance
- C) It prunes
- D) It scales

<details><summary>Reveal Answer</summary>**B.** Variance reduction.</details>

### Question 3 — Medium
**What is bagging?**
- A) Boosting
- B) Training each tree on a bootstrap sample with replacement
- C) Clustering
- D) Scaling

<details><summary>Reveal Answer</summary>**B.** Bootstrap aggregating.</details>

### Question 4 — Medium
**What does `max_features` control?**
- A) The depth
- B) How many features each split considers, adding decorrelation
- C) The leaves
- D) The scale

<details><summary>Reveal Answer</summary>**B.** Feature subsampling.</details>

### Question 5 — Medium
**What is the out-of-bag estimate?**
- A) A cache
- B) Validation from the samples a tree did not see, a free generalisation estimate
- C) A split
- D) A metric

<details><summary>Reveal Answer</summary>**B.** Bootstrap validation.</details>

### Question 6 — Hard
**Why must trees be decorrelated for the ensemble gain?**
- A) Speed
- B) Averaging identical trees changes nothing; diversity cancels errors
- C) It sorts
- D) It scales

<details><summary>Reveal Answer</summary>**B.** Diversity is the engine.</details>

### Question 7 — Hard
**Does a random forest need feature scaling?**
- A) Yes
- B) No; it is threshold-based and scale-invariant
- C) Only for depth
- D) Only for leaves

<details><summary>Reveal Answer</summary>**B.** Tree-based.</details>

### Question 8 — Hard
**What does a random forest trade away vs boosting?**
- A) Accuracy always
- B) Some peak accuracy for robustness and fewer tuning knobs
- C) Speed always
- D) Interpretability only

<details><summary>Reveal Answer</summary>**B.** Robust and simple.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand random forests. |
| 5-6 | Review bagging, max_features, OOB. |
| < 5 | Re-read the lecture. |
