# ML 16: K-Means — Quiz

> **Topic Overview**: Centroid clustering, k selection, and its assumptions.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is unsupervised clustering?**
- A) Predicting labels
- B) Grouping unlabelled points by similarity
- C) Regression
- D) Classification

<details><summary>Reveal Answer</summary>**B.** No target labels.</details>

### Question 2 — Easy
**What does k-means minimise?**
- A) Accuracy
- B) Within-cluster sum of squared distances to centroids
- C) Depth
- D) Impurity

<details><summary>Reveal Answer</summary>**B.** Inertia.</details>

### Question 3 — Medium
**How does k-means iterate?**
- A) One pass
- B) Assign points to nearest centroid, then recompute centroids, repeat
- C) Sort
- D) Split

<details><summary>Reveal Answer</summary>**B.** Alternating optimisation.</details>

### Question 4 — Medium
**How do you choose k?**
- A) Randomly
- B) Elbow method or silhouette score
- C) Always 2
- D) By depth

<details><summary>Reveal Answer</summary>**B.** Diagnostics.</details>

### Question 5 — Medium
**Why does k-means need scaled features?**
- A) For speed
- B) Distance is dominated by large-scale features otherwise
- C) To cluster
- D) To sort

<details><summary>Reveal Answer</summary>**B.** Distance-based.</details>

### Question 6 — Hard
**What shape clusters does k-means assume?**
- A) Any shape
- B) Roughly spherical, similar-sized clusters
- C) Arbitrary manifolds
- D) Trees

<details><summary>Reveal Answer</summary>**B.** Voronoi/spherical assumption.</details>

### Question 7 — Hard
**Why is the result sensitive to initialisation?**
- A) It is not
- B) It finds local minima; use k-means++ or multiple restarts
- C) It sorts
- D) It scales

<details><summary>Reveal Answer</summary>**B.** Initialisation matters.</details>

### Question 8 — Hard
**Why is k-means a poor fit for non-convex clusters?**
- A) It is fine
- B) Centroids and Euclidean distance cannot separate rings/crescents; use density methods
- C) It is slow
- D) It overfits

<details><summary>Reveal Answer</summary>**B.** Geometry mismatch.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand k-means. |
| 5-6 | Review k selection and assumptions. |
| < 5 | Re-read the lecture. |
