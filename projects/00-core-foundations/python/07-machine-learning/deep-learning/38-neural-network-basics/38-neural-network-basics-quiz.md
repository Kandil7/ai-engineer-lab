# ML 38: Neural Network Basics — Quiz

> **Topic Overview**: Activations, init, vanishing gradients, batch norm/dropout, LR.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why do networks need non-linear activations?**
- A) For speed
- B) Stacked linear layers collapse to one linear map without them
- C) To cast
- D) To shuffle

<details><summary>Reveal Answer</summary>**B.** Non-linearity gives depth power.</details>

### Question 2 — Easy
**What problem does ReLU help with vs sigmoid?**
- A) Accuracy
- B) Saturating gradients in deep nets; ReLU keeps gradient flow for positive inputs
- C) Memory
- D) Speed only

<details><summary>Reveal Answer</summary>**B.** Better gradient flow.</details>

### Question 3 — Medium
**Why does weight initialisation matter?**
- A) It does not
- B) Bad scale causes vanishing/exploding activations and gradients
- C) For dtype
- D) For device

<details><summary>Reveal Answer</summary>**B.** Signal preservation.</details>

### Question 4 — Medium
**What does batch norm do?**
- A) Drops units
- B) Normalises layer inputs per batch, stabilising and speeding training
- C) Casts
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Normalisation.</details>

### Question 5 — Medium
**What does dropout do?**
- A) Normalises
- B) Randomly zeroes units during training to regularise, and is off at eval
- C) Casts
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Regularisation.</details>

### Question 6 — Hard
**Why is the learning rate "the most important hyperparameter"?**
- A) It is not
- B) Too high diverges, too low stagnates; it dominates training success
- C) It is fixed
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Determines convergence.</details>

### Question 7 — Hard
**What is the vanishing-gradient problem?**
- A) Fast training
- B) Gradients shrink through many layers, so early layers barely learn
- C) Too much memory
- D) Overfitting

<details><summary>Reveal Answer</summary>**B.** Signal decay.</details>

### Question 8 — Hard
**Why is batch norm disabled-like at eval (uses running stats)?**
- A) A bug
- B) Eval must be deterministic and use the population statistics, not batch ones
- C) For speed
- D) To cast

<details><summary>Reveal Answer</summary>**B.** Deterministic inference.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand NN training basics. |
| 5-6 | Review activations, init, regularisation. |
| < 5 | Re-read the lecture. |
