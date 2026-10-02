# ML 10: Train / Test Split — Quiz

> **Topic Overview**: Splitting strategy, random state, and honest evaluation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why split the data?**
- A) Speed
- B) To estimate performance on data the model has not seen
- C) To clean
- D) To encode

<details><summary>Reveal Answer</summary>**B.** Generalisation.</details>

### Question 2 — Easy
**What is a typical split?**
- A) 99/1
- B) 70-80% train / 20-30% test, with a validation set when tuning
- C) 50/50 always
- D) No split

<details><summary>Reveal Answer</summary>**B.** Common default.</details>

### Question 3 — Medium
**What does `random_state` fix?**
- A) The model
- B) Reproducibility of the random split
- C) The metric
- D) The features

<details><summary>Reveal Answer</summary>**B.** Deterministic splits.</details>

### Question 4 — Medium
**What does `stratify=y` do?**
- A) Sorts
- B) Preserves class proportions in both splits
- C) Scales
- D) Encodes

<details><summary>Reveal Answer</summary>**B.** Balance preserved.</details>

### Question 5 — Medium
**Why is cross-validation often better than one split?**
- A) Faster
- B) It averages over folds, giving a more stable estimate
- C) Fewer metrics
- D) No leakage

<details><summary>Reveal Answer</summary>**B.** Lower-variance estimate.</details>

### Question 6 — Hard
**Why can a small test set mislead?**
- A) It cannot
- B) High variance; the estimate swings with the particular split
- C) It leaks
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Sample noise.</details>

### Question 7 — Hard
**What is data leakage through splitting?**
- A) None
- B) Preprocessing fitted on all data before splitting leaks test information
- C) It is required
- D) It speeds up
</details>

<details><summary>Reveal Answer</summary>**B.** Split before fitting preprocessing.</details>

### Question 8 — Hard
**What should you never do with the test set?**
- A) Touch it repeatedly
- B) Evaluate once at the end; repeated peeking corrupts the estimate
- C) Use it at all
- D) Split it

<details><summary>Reveal Answer</summary>**B.** One final evaluation.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You split honestly. |
| 5-6 | Review stratification and leakage. |
| < 5 | Re-read the lecture. |
