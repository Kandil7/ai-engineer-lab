# ML 18: PCA — Quiz

> **Topic Overview**: Variance-maximising projections, components, and explained variance.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does PCA do?**
- A) Clusters
- B) Projects data onto orthogonal axes of maximum variance
- C) Classifies
- D) Regresses

<details><summary>Reveal Answer</summary>**B.** Dimensionality reduction.</details>

### Question 2 — Easy
**What is a principal component?**
- A) A feature
- B) A linear combination of features capturing a direction of variance
- C) A label
- D) A cluster

<details><summary>Reveal Answer</summary>**B.** Variance direction.</details>

### Question 3 — Medium
**Why scale before PCA?**
- A) Optional
- B) PCA is variance-driven; unscaled large-range features dominate
- C) It sorts
- D) It encodes

<details><summary>Reveal Answer</summary>**B.** Variance is scale-dependent.</details>

### Question 4 — Medium
**How do you choose the number of components?**
- A) Always 2
- B) By explained-variance ratio (e.g. keep 95%)
- C) Randomly
- D) By depth

<details><summary>Reveal Answer</summary>**B.** Cumulative explained variance.</details>

### Question 5 — Medium
**What are principal components guaranteed to be?**
- A) Correlated
- B) Orthogonal (uncorrelated)
- C) Identical
- D) Sparse always

<details><summary>Reveal Answer</summary>**B.** Orthogonal axes.</details>

### Question 6 — Hard
**Does PCA use the target?**
- A) Yes
- B) No; it is unsupervised and may discard class-separating directions with low variance
- C) Sometimes
- D) Always

<details><summary>Reveal Answer</summary>**B.** Blind to labels.</details>

### Question 7 — Hard
**Why can PCA hurt classification?**
- A) It cannot
- B) The most discriminative direction may have low variance and be dropped
- C) It sorts
- D) It clusters

<details><summary>Reveal Answer</summary>**B.** Unsupervised reduction ignores labels.</details>

### Question 8 — Hard
**What is the role of eigenvectors/eigenvalues here?**
- A) None
- B) Covariance eigenvectors give directions; eigenvalues give captured variance
- C) Clustering
- D) Scaling

<details><summary>Reveal Answer</summary>**B.** Spectral decomposition of covariance.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand PCA. |
| 5-6 | Review components and explained variance. |
| < 5 | Re-read the lecture. |
