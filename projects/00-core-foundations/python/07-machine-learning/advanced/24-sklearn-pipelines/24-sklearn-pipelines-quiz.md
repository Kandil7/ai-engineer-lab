# ML 24: scikit-learn Pipelines — Quiz

> **Topic Overview**: `Pipeline`, `ColumnTransformer`, custom transformers, and tuning.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does a `Pipeline` bundle?**
- A) Only the model
- B) Preprocessing steps and the estimator as one fit/predict object
- C) The dataset
- D) The metrics

<details><summary>Reveal Answer</summary>**B.** Reproducible chain.</details>

### Question 2 — Easy
**What is the main benefit of a pipeline?**
- A) Speed
- B) It prevents leakage by fitting all steps on train and applying to test
- C) Fewer features
- D) Clustering

<details><summary>Reveal Answer</summary>**B.** Correct fit/transform discipline.</details>

### Question 3 — Medium
**What is `ColumnTransformer` for?**
- A) Sorting
- B) Applying different preprocessing to different column groups
- C) Clustering
- D) Scaling only

<details><summary>Reveal Answer</summary>**B.** Per-column recipes.</details>

### Question 4 — Medium
**What two base classes define a custom transformer?**
- A) `BaseEstimator, TransformerMixin`
- B) `Classifier, Regressor`
- C) `Pipe, Step`
- D) `Fit, Predict`

<details><summary>Reveal Answer</summary>**A.** Implementing `fit`/`transform`.</details>

### Question 5 — Medium
**How do you tune a pipeline?**
- A) Manually
- B) `GridSearchCV` with keys like `stepname__param`
- C) Sort
- D) Cluster

<details><summary>Reveal Answer</summary>**B.** Nested parameter names.</details>

### Question 6 — Hard
**What is `FeatureUnion` for?**
- A) Unioning rows
- B) Running parallel transformers and concatenating their outputs
- C) Scaling
- D) Clustering

<details><summary>Reveal Answer</summary>**B.** Parallel feature extraction.</details>

### Question 7 — Hard
**Why can a custom transformer silently leak?**
- A) It cannot
- B) If `fit` computes statistics on all data or `transform` refits, test info leaks
- C) It is slower
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** fit/transform must be separated.</details>

### Question 8 — Hard
**Why does the pipeline make deployment safer?**
- A) It is faster
- B) The exact same preprocessing travels with the model, so inference matches training
- C) It sorts
- D) It clusters

<details><summary>Reveal Answer</summary>**B.** Train/serve consistency.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You build pipelines correctly. |
| 5-6 | Review ColumnTransformer and tuning. |
| < 5 | Re-read the lecture. |
