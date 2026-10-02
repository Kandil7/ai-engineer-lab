# ML 17: Hierarchical Clustering — Quiz

> **Topic Overview**: Agglomerative merging, dendrograms, and linkage.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does agglomerative clustering build?**
- A) Centroids
- B) A hierarchy by merging the closest clusters repeatedly
- C) A line
- D) A tree split

<details><summary>Reveal Answer</summary>**B.** Bottom-up merging.</details>

### Question 2 — Easy
**What is a dendrogram?**
- A) A centroid
- B) A tree diagram of merges with heights showing distances
- C) A metric
- D) A feature

<details><summary>Reveal Answer</summary>**B.** Merge tree.</details>

### Question 3 — Medium
**What is the advantage over k-means?**
- A) Faster
- B) No need to pre-set k; you cut the dendrogram at a chosen height
- C) Scales better
- D) Spherical only

<details><summary>Reveal Answer</summary>**B.** Explore k after the fact.</details>

### Question 4 — Medium
**What does linkage define?**
- A) The metric
- B) How inter-cluster distance is measured (single, complete, average, Ward)
- C) The depth
- D) The scale

<details><summary>Reveal Answer</summary>**B.** Cluster-distance rule.</details>

### Question 5 — Medium
**Why can single-linkage produce chained clusters?**
- A) It cannot
- B) Nearest-point distance links slender chains across clusters
- C) It sorts
- D) It clusters

<details><summary>Reveal Answer</summary>**B.** Chaining effect.</details>

### Question 6 — Hard
**What is the complexity cost of hierarchical clustering?**
- A) O(n)
- B) Typically O(n²) or worse — memory and time limit scale
- C) O(log n)
- D) O(1)

<details><summary>Reveal Answer</summary>**B.** Pairwise distances.</details>

### Question 7 — Hard
**What does Ward linkage optimise?**
- A) Chaining
- B) Minimising within-cluster variance increase at each merge
- C) Speed
- D) Depth

<details><summary>Reveal Answer</summary>**B.** Variance-based merge.</details>

### Question 8 — Hard
**Why scale features before hierarchical clustering?**
- A) Optional
- B) Distance-based methods are dominated by large-scale features
- C) It sorts
- D) It encodes

<details><summary>Reveal Answer</summary>**B.** Same as other distance methods.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand hierarchical clustering. |
| 5-6 | Review linkage and dendrograms. |
| < 5 | Re-read the lecture. |
