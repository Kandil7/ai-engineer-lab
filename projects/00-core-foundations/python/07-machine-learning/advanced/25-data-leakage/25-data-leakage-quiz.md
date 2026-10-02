# ML 25: Data Leakage — Quiz

> **Topic Overview**: Five leakage classes and the audit checklist.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is data leakage?**
- A) A missing value
- B) Information about the target leaking into training features or preprocessing
- C) An outlier
- D) A duplicate

<details><summary>Reveal Answer</summary>**B.** Target information in the wrong place.</details>

### Question 2 — Easy
**What is the classic symptom of leakage?**
- A) Poor test score
- B) Suspiciously high validation performance that collapses in production
- C) Slow training
- D) Overfitting only

<details><summary>Reveal Answer</summary>**B.** Too good to be true.</details>

### Question 3 — Medium
**Give one leakage class.**
- A) Missing values
- B) Preprocessing fitted on the whole dataset before splitting
- C) Outliers
- D) Duplicates

<details><summary>Reveal Answer</summary>**B.** Fit-on-all leakage.</details>

### Question 4 — Medium
**What is temporal leakage?**
- A) Sorting
- B) Using future information to predict the past (random splits on time-series)
- C) Scaling
- D) Clustering

<details><summary>Reveal Answer</summary>**B.** Future→past.</details>

### Question 5 — Medium
**What is group leakage?**
- A) Sorting
- B) Rows of the same entity (patient/user) appear in both train and test
- C) Scaling
- D) Encoding

<details><summary>Reveal Answer</summary>**B.** Same entity across splits.</details>

### Question 6 — Hard
**What is target-encoding leakage?**
- A) Encoding a category
- B) Computing target means on all data, so the encoding encodes the label itself
- C) Scaling
- D) Clustering

<details><summary>Reveal Answer</summary>**B.** Compute inside CV folds only.</details>

### Question 7 — Hard
**How do pipelines prevent preprocessing leakage?**
- A) They do not
- B) They fit each step only on the training fold during CV
- C) They sort
- D) They cluster

<details><summary>Reveal Answer</summary>**B.** Encapsulated fit/transform.</details>

### Question 8 — Hard
**What is duplicate leakage?**
- A) Repeating features
- B) The same row appearing in train and test, so the model has seen the answer
- C) Scaling
- D) Encoding

<details><summary>Reveal Answer</summary>**B.** Deduplicate before splitting.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You spot leakage. |
| 5-6 | Review the five leakage classes. |
| < 5 | Re-read the lecture. |
