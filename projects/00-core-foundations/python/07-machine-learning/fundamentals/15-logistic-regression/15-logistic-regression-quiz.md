# ML 15: Logistic Regression — Quiz

> **Topic Overview**: Probabilities for classification, the sigmoid, and log loss.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does logistic regression predict?**
- A) A line value
- B) A probability in [0, 1] for a class
- C) A cluster
- D) A count

<details><summary>Reveal Answer</summary>**B.** Class probability.</details>

### Question 2 — Easy
**What function maps the linear score to a probability?**
- A) ReLU
- B) The sigmoid
- C) Tanh
- D) Softmax only

<details><summary>Reveal Answer</summary>**B.** Squashes to (0, 1).</details>

### Question 3 — Medium
**What loss does logistic regression minimise?**
- A) MSE
- B) Log loss (cross-entropy)
- C) MAE
- D) Hinge

<details><summary>Reveal Answer</summary>**B.** Cross-entropy on probabilities.</details>

### Question 4 — Medium
**What is the decision boundary?**
- A) A curve
- B) The set where p = 0.5, a hyperplane in feature space
- C) A leaf
- D) A cluster

<details><summary>Reveal Answer</summary>**B.** Linear in features.</details>

### Question 5 — Medium
**How do you turn probabilities into class labels?**
- A) Round the score
- B) Apply a threshold (default 0.5), adjustable to trade precision/recall
- C) Sort
- D) Hash

<details><summary>Reveal Answer</summary>**B.** Threshold is a choice.</details>

### Question 6 — Hard
**Why is MSE a poor loss for classification?**
- A) It is fine
- B) With a sigmoid it is non-convex and penalises confidently wrong predictions weakly
- C) It is slow
- D) It overfits

<details><summary>Reveal Answer</summary>**B.** Log loss is the right objective.</details>

### Question 7 — Hard
**What does the coefficient sign mean?**
- A) Accuracy
- B) Positive raises the log-odds of the positive class; negative lowers it
- C) Causality
- D) Scale

<details><summary>Reveal Answer</summary>**B.** Effect on log-odds.</details>

### Question 8 — Hard
**Why is class weighting relevant here?**
- A) For speed
- B) Under imbalance it reweights the loss so the minority class matters
- C) To cluster
- D) To scale

<details><summary>Reveal Answer</summary>**B.** Balanced objective.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand logistic regression. |
| 5-6 | Review sigmoid, log loss, thresholds. |
| < 5 | Re-read the lecture. |
