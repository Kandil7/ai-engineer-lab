# ML 11: Decision Trees — Quiz

> **Topic Overview**: Recursive splitting, impurity, and overfitting control.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How does a decision tree predict?**
- A) A line
- B) By routing an example through feature-threshold splits to a leaf
- C) By distance
- D) By probability only

<details><summary>Reveal Answer</summary>**B.** Threshold rules.</details>

### Question 2 — Easy
**What is a leaf?**
- A) The root
- B) A terminal node holding a prediction (class or value)
- C) A split
- D) A feature

<details><summary>Reveal Answer</summary>**B.** Terminal prediction.</details>

### Question 3 — Medium
**What does Gini/entropy measure?**
- A) Accuracy
- B) Node impurity — how mixed the classes are
- C) Depth
- D) Scale

<details><summary>Reveal Answer</summary>**B.** Impurity.</details>

### Question 4 — Medium
**What limits an unconstrained tree?**
- A) Nothing; it grows until pure leaves, overfitting
- B) Memory
- C) Speed
- D) Classes

<details><summary>Reveal Answer</summary>**A.** Perfect memorisation.</details>

### Question 5 — Medium
**Name a way to control tree complexity.**
- A) Increase depth
- B) `max_depth`, `min_samples_leaf`, or pruning
- C) Add features
- D) Remove the splitter

<details><summary>Reveal Answer</summary>**B.** Pre- or post-pruning.</details>

### Question 6 — Hard
**Why are trees prone to overfitting?**
- A) They are not
- B) They can split until every training point is isolated, capturing noise
- C) They are linear
- D) They need scaling

<details><summary>Reveal Answer</summary>**B.** Unbounded flexibility.</details>

### Question 7 — Hard
**What is the key advantage of trees over linear models?**
- A) Faster
- B) They capture non-linear interactions without feature engineering
- C) Less overfitting
- D) Scale-invariant only

<details><summary>Reveal Answer</summary>**B.** Non-linear, interaction-aware.</details>

### Question 8 — Hard
**Why do trees not need feature scaling?**
- A) They do
- B) Splits compare thresholds; monotone rescaling does not change the split
- C) They are linear
- D) They cluster

<details><summary>Reveal Answer</summary>**B.** Scale-invariant splits.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand trees. |
| 5-6 | Review impurity and overfitting control. |
| < 5 | Re-read the lecture. |
