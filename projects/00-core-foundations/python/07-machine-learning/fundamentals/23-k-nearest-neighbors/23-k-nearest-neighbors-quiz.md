# ML 23: K-Nearest Neighbors — Quiz

> **Topic Overview**: Distance-based prediction, k, and the curse of dimensionality.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How does KNN predict?**
- A) Fits a line
- B) Uses the labels of the k nearest training points
- C) Splits
- D) Clusters

<details><summary>Reveal Answer</summary>**B.** Instance-based, no training phase.</details>

### Question 2 — Easy
**What is KNN called "lazy"?**
- A) It is slow to code
- B) It does no training; all work happens at prediction time
- C) It is inaccurate
- D) It needs scaling

<details><summary>Reveal Answer</summary>**B.** No model is learned.</details>

### Question 3 — Medium
**What does small k do?**
- A) Smooths
- B) Low bias, high variance — sensitive to noise
- C) Underfits
- D) Clusters

<details><summary>Reveal Answer</summary>**B.** Overfits noise.</details>

### Question 4 — Medium
**Why must features be scaled?**
- A) Optional
- B) Distance is dominated by large-scale features otherwise
- C) To cluster
- D) To sort

<details><summary>Reveal Answer</summary>**B.** Distance-based.</details>

### Question 5 — Medium
**What is the curse of dimensionality for KNN?**
- A) No effect
- B) In high dimensions distances concentrate, so "nearest" loses meaning
- C) It is faster
- D) It scales

<details><summary>Reveal Answer</summary>**B.** Distance concentration.</details>

### Question 6 — Hard
**Why is prediction O(n·d) per query (naively)?**
- A) It is O(1)
- B) You compute distance to every training point across d features
- C) It sorts
- D) It clusters

<details><summary>Reveal Answer</summary>**B.** Brute-force search.</details>

### Question 7 — Hard
**How is KNN used for regression?**
- A) Not possible
- B) Average the target of the k nearest neighbours
- C) Majority vote
- D) Sort

<details><summary>Reveal Answer</summary>**B.** Local averaging.</details>

### Question 8 — Hard
**What fixes help KNN scalability?**
- A) Smaller k
- B) KD-trees/Ball-trees or approximate nearest-neighbour indexes
- C) More features
- D) No scaling

<details><summary>Reveal Answer</summary>**B.** Tree/ANN structures.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand KNN. |
| 5-6 | Review k, scaling, and dimensionality. |
| < 5 | Re-read the lecture. |
