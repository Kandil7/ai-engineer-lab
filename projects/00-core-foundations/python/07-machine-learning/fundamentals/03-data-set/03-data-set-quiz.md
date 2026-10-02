# ML 03: Data Set — Quiz

> **Topic Overview**: Datasets, splits, and the train/validation/test discipline.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a dataset in ML?**
- A) A model
- B) A table of examples: features plus (for supervised) a target
- C) A file
- D) A plot

<details><summary>Reveal Answer</summary>**B.** Rows are examples, columns are features.</details>

### Question 2 — Easy
**Why hold out a test set?**
- A) Speed
- B) To measure generalisation once, at the end
- C) To tune
- D) To clean

<details><summary>Reveal Answer</summary>**B.** Unseen data estimate.</details>

### Question 3 — Medium
**What is the validation set for?**
- A) Final reporting
- B) Model selection and tuning without touching the test set
- C) Cleaning
- D) Encoding

<details><summary>Reveal Answer</summary>**B.** Tuning without leakage.</details>

### Question 4 — Medium
**What does a ragged/jagged dataset require?**
- A) Packing/truncation/padding to a fixed shape for tensors
- B) Sorting
- C) Hashing
- D) Encoding

<details><summary>Reveal Answer</summary>**A.** Uniform shape for batches.</details>

### Question 5 — Medium
**Why is a random split wrong for time-series?**
- A) It is fine
- B) It leaks the future into the past; split chronologically
- C) It is slower
- D) It balances classes

<details><summary>Reveal Answer</summary>**B.** Time order matters.</details>

### Question 6 — Hard
**What is a group split for?**
- A) Speed
- B) Keeping all rows of a group (e.g. a patient) in one split to avoid leakage
- C) Sorting
- D) Encoding

<details><summary>Reveal Answer</summary>**B.** Grouped leakage prevention.</details>

### Question 7 — Hard
**Why must the test set be touched only once?**
- A) For speed
- B) Repeated peeking turns it into a tuning set and inflates the estimate
- C) It is smaller
- D) To clean

<details><summary>Reveal Answer</summary>**B.** Its only value is being unseen.</details>

### Question 8 — Hard
**What does stratification preserve?**
- A) Order
- B) The class ratio in each split, important for imbalanced data
- C) Scale
- D) Types

<details><summary>Reveal Answer</summary>**B.** Balance across splits.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You split data correctly. |
| 5-6 | Review validation, time, and group splits. |
| < 5 | Re-read the lecture. |
