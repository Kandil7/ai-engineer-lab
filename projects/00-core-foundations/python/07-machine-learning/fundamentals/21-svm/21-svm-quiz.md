# ML 21: SVM — Quiz

> **Topic Overview**: Maximal margin, the kernel trick, and C/gamma.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does an SVM find?**
- A) Clusters
- B) A hyperplane (or margin) that best separates classes
- C) A tree
- D) A centroid

<details><summary>Reveal Answer</summary>**B.** Max-margin separator.</details>

### Question 2 — Easy
**What are support vectors?**
- A) All points
- B) The training points closest to the boundary that define the margin
- C) Centroids
- D) Features

<details><summary>Reveal Answer</summary>**B.** Boundary-defining points.</details>

### Question 3 — Medium
**What does the kernel trick enable?**
- A) Scaling
- B) Non-linear separation via implicit high-dimensional mapping
- C) Clustering
- D) Pruning

<details><summary>Reveal Answer</summary>**B.** Non-linear boundaries cheaply.</details>

### Question 4 — Medium
**What does C control?**
- A) The kernel
- B) The tradeoff between margin width and training-error tolerance
- C) The scale
- D) The depth

<details><summary>Reveal Answer</summary>**B.** Regularisation strength.</details>

### Question 5 — Medium
**Why is SVM sensitive to feature scaling?**
- A) It is not
- B) Margins/distances depend on feature scales
- C) It clusters
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Distance-based.</details>

### Question 6 — Hard
**What does a large C do?**
- A) Wider margin
- B) Fewer margin violations (narrower margin), risking overfitting
- C) Ignores data
- D) Clusters

<details><summary>Reveal Answer</summary>**B.** Penalise errors strongly.</details>

### Question 7 — Hard
**What does the gamma parameter do for RBF kernels?**
- A) Sets C
- B) Controls the reach of a single point's influence; high gamma overfits
- C) Sets the margin
- D) Sets depth

<details><summary>Reveal Answer</summary>**B.** Kernel width.</details>

### Question 8 — Hard
**Why can SVM be expensive on large n?**
- A) It is O(1)
- B) Training is roughly O(n²)–O(n³); it does not scale to millions of rows
- C) It hashes
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Kernel matrix cost.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand SVMs. |
| 5-6 | Review kernels and C/gamma. |
| < 5 | Re-read the lecture. |
