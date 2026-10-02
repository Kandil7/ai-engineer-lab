# ML 45: Data Augmentation — Quiz

> **Topic Overview**: Label-preserving transforms, train-only discipline,
> on-the-fly pipelines, and augmentation across domains.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the hard rule for a valid augmentation?**
- A) It must be fast
- B) It must preserve the label
- C) It must use noise
- D) It must be random

<details><summary>Reveal Answer</summary>**B.** A human would still assign the same label.</details>

### Question 2 — Easy
**When should augmentation be applied?**
- A) To training, validation, and test
- B) Only to the training set
- C) Only to the test set
- D) Never

<details><summary>Reveal Answer</summary>**B.** Train-only, so eval stays honest.</details>

### Question 3 — Medium
**Why is a 180-degree rotation unsafe for handwritten digits?**
- A) It is too slow
- B) It can turn a "6" into a "9", breaking the label
- C) It adds noise
- D) It loses information

<details><summary>Reveal Answer</summary>**B.** A label-breaking transform.</details>

### Question 4 — Medium
**What is the primary benefit of augmentation?**
- A) Faster inference
- B) Regularization that reduces overfitting, especially on small data
- C) Smaller models
- D) Less memory use

<details><summary>Reveal Answer</summary>**B.** It teaches invariances instead of memorization.</details>

### Question 5 — Medium
**What is the difference between on-the-fly and offline augmentation?**
- A) On-the-fly stores the dataset; offline doesn't
- B) On-the-fly applies in the dataloader; offline materializes to disk
- C) They are identical
- D) Offline is always better

<details><summary>Reveal Answer</summary>**B.** A compute-vs-storage trade.</details>

### Question 6 — Hard
**Why must you split before augmenting?**
- A) It is faster
- B) Otherwise an original and its transform leak across train/val folds
- C) It uses less disk
- D) It is required by the framework

<details><summary>Reveal Answer</summary>**B.** Augmenting first leaks near-duplicates into eval.</details>

### Question 7 — Hard
**What is mixup?**
- A) Adding Gaussian noise
- B) Blending two examples and their labels in proportion
- C) Flipping images
- D) Dropping features

<details><summary>Reveal Answer</summary>**B.** A strong smooth-boundary regularizer.</details>

### Question 8 — Hard
**When does augmentation add the least value?**
- A) On a huge, diverse dataset
- B) On tiny data
- C) On a large model with few samples
- D) On imbalanced data

<details><summary>Reveal Answer</summary>**A.** Real data already covers the variance.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You augment safely. |
| 5-6 | Review label invariance and train-only. |
| < 5 | Re-read the lecture. |
