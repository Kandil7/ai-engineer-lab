# ML 31: Feature Engineering — Quiz

> **Topic Overview**: Numeric transforms, encoding, interactions, binning, dates, text.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is feature engineering?**
- A) Model tuning
- B) Creating/transforming inputs to expose signal to the model
- C) Splitting
- D) Clustering

<details><summary>Reveal Answer</summary>**B.** Better inputs, better model.</details>

### Question 2 — Easy
**Why encode categorical variables?**
- A) For speed
- B) Models need numbers; strings carry no arithmetic
- C) To cluster
- D) To sort

<details><summary>Reveal Answer</summary>**B.** Numeric representation.</details>

### Question 3 — Medium
**One-hot vs ordinal encoding?**
- A) Same
- B) One-hot for nominal (no order); ordinal for genuinely ordered categories
- C) Ordinal for nominal
- D) One-hot for ordered

<details><summary>Reveal Answer</summary>**B.** Respect cardinality/order.</details>

### Question 4 — Medium
**What do interaction/polynomial features add?**
- A) Noise
- B) Products of features that capture joint effects a linear model misses
- C) Clusters
- D) Scaling

<details><summary>Reveal Answer</summary>**B.** Non-additive effects.</details>

### Question 5 — Medium
**What is the golden rule?**
- A) Fit encoders on all data
- B) Fit encoders/transformers on train only, then apply to test
- C) Use all features
- D) Scale last

<details><summary>Reveal Answer</summary>**B.** Leakage prevention.</details>

### Question 6 — Hard
**When is target encoding risky and how do you do it safely?**
- A) Never
- B) It leaks the label; compute inside CV folds with smoothing
- C) Always safe
- D) Only for numeric

<details><summary>Reveal Answer</summary>**B.** Fold-local target encoding.</details>

### Question 7 — Hard
**Why can binning help?**
- A) It always does
- B) It handles non-linearity and outliers for linear models, at the cost of resolution
- C) It sorts
- D) It clusters

<details><summary>Reveal Answer</summary>**B.** Discretise to linearise.</details>

### Question 8 — Hard
**What date features are useful?**
- A) The raw timestamp
- B) Day-of-week, month, is-holiday, elapsed time; raw timestamps rarely help
- C) None
- D) Only year

<details><summary>Reveal Answer</summary>**B.** Extract cycles and deltas.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You engineer features well. |
| 5-6 | Review encoding and leakage. |
| < 5 | Re-read the lecture. |
