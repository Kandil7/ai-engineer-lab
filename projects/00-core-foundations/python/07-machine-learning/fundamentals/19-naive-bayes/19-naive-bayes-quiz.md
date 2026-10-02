# ML 19: Naive Bayes — Quiz

> **Topic Overview**: Bayes' rule, the independence assumption, and text classification.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does Naive Bayes rely on?**
- A) Distances
- B) Bayes' rule with a conditional-independence assumption
- C) Splits
- D) Centroids

<details><summary>Reveal Answer</summary>**B.** Probabilistic with an assumption.</details>

### Question 2 — Easy
**Why "naive"?**
- A) It is simple code
- B) It assumes features are independent given the class, which is rarely true
- C) It is slow
- D) It needs scaling

<details><summary>Reveal Answer</summary>**B.** The independence assumption.</details>

### Question 3 — Medium
**Why does it work well for text?**
- A) Text is independent
- B) High dimensions and many weak word signals make it fast and effective despite the assumption
- C) It clusters
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Good on sparse counts.</details>

### Question 4 — Medium
**What is the role of Laplace smoothing?**
- A) Scaling
- B) Avoiding zero probabilities for unseen feature values
- C) Clustering
- D) Encoding

<details><summary>Reveal Answer</summary>**B.** Add-one smoothing.</details>

### Question 5 — Medium
**Why use log probabilities?**
- A) Speed only
- B) Multiplying many small probabilities underflows; summing logs is stable
- C) To sort
- D) To cluster

<details><summary>Reveal Answer</summary>**B.** Numerical stability.</details>

### Question 6 — Hard
**What is the difference between Gaussian and Multinomial NB?**
- A) None
- B) Gaussian assumes normal features; Multinomial models counts (e.g. word frequencies)
- C) Gaussian is for text
- D) Multinomial is for continuous

<details><summary>Reveal Answer</summary>**B.** Feature assumptions differ.</details>

### Question 7 — Hard
**Why is NB a strong baseline?**
- A) It is accurate always
- B) It is fast, needs little data, and is hard to beat on small text datasets
- C) It needs scaling
- D) It is deep

<details><summary>Reveal Answer</summary>**B.** Cheap and effective.</details>

### Question 8 — Hard
**When does the independence assumption break badly?**
- A) Never
- B) Highly correlated features double-count evidence, overconfident probabilities
- C) For text
- D) For counts

<details><summary>Reveal Answer</summary>**B.** Correlated evidence.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand Naive Bayes. |
| 5-6 | Review Bayes, smoothing, and log-space. |
| < 5 | Re-read the lecture. |
