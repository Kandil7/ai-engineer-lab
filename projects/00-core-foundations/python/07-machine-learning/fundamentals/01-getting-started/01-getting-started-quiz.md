# ML 01: Getting Started — Quiz

> **Topic Overview**: The ML workflow, terminology, and scikit-learn's API shape.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is supervised learning?**
- A) Finding groups
- B) Learning a mapping from features to labelled targets
- C) Reducing dimensions
- D) Clustering

<details><summary>Reveal Answer</summary>**B.** Labels guide learning.</details>

### Question 2 — Easy
**What are features and labels?**
- A) Inputs and outputs
- B) X (inputs) and y (target)
- C) Train and test
- D) Rows and columns only

<details><summary>Reveal Answer</summary>**B.** X and y.</details>

### Question 3 — Medium
**What is the standard scikit-learn estimator API?**
- A) `run`/`stop`
- B) `fit` then `predict` (`transform` for transformers)
- C) `load`/`save`
- D) `open`/`close`

<details><summary>Reveal Answer</summary>**B.** Uniform interface.</details>

### Question 4 — Medium
**Why split data into train and test?**
- A) For speed
- B) To estimate performance on unseen data, not memorised data
- C) To reduce features
- D) To balance classes

<details><summary>Reveal Answer</summary>**B.** Generalisation estimate.</details>

### Question 5 — Medium
**Classification vs regression?**
- A) The same
- B) Classification predicts a class; regression predicts a continuous value
- C) Regression predicts classes
- D) Classification predicts numbers

<details><summary>Reveal Answer</summary>**B.** Output type differs.</details>

### Question 6 — Hard
**What is the risk of evaluating on training data?**
- A) None
- B) The score is optimistic because the model has seen the answers
- C) It is slower
- D) It reduces features

<details><summary>Reveal Answer</summary>**B.** Leakage of the target.</details>

### Question 7 — Hard
**What does `fit_transform` on training data imply for test data?**
- A) Same call
- B) Fit on train; only `transform` the test set, never refit
- C) Refit on test
- D) Ignore test

<details><summary>Reveal Answer</summary>**B.** Fit only on train.</details>

### Question 8 — Hard
**What is an estimator's hyperparameter vs a learned parameter?**
- A) The same
- B) Hyperparameters are set before fit; parameters are learned during fit
- C) Parameters are set first
- D) Neither is set

<details><summary>Reveal Answer</summary>**B.** Chosen vs learned.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You know the ML workflow. |
| 5-6 | Review the estimator API and splitting. |
| < 5 | Re-read the lecture. |
