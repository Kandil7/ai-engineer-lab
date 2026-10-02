# ML 35: Explainability — Quiz

> **Topic Overview**: Global vs local explanations, PDP, and their limits.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a global explanation?**
- A) One prediction
- B) How a feature affects the model overall
- C) A cluster
- D) A metric

<details><summary>Reveal Answer</summary>**B.** Overall behavior.</details>

### Question 2 — Easy
**What is a local explanation?**
- A) Overall
- B) Why this specific prediction came out as it did
- C) A metric
- D) A cluster

<details><summary>Reveal Answer</summary>**B.** Per-instance.</details>

### Question 3 — Medium
**What does a partial dependence plot show?**
- A) Accuracy
- B) The average predicted response as one feature varies
- C) A confusion matrix
- D) A cluster

<details><summary>Reveal Answer</summary>**B.** Marginal effect.</details>

### Question 4 — Medium
**What does permutation importance measure?**
- A) Model speed
- B) The performance drop when a feature is shuffled
- C) Accuracy
- D) Scaling

<details><summary>Reveal Answer</summary>**B.** Feature reliance.</details>

### Question 5 — Medium
**What is a common local method?**
- A) PDP
- B) SHAP / LIME attributions per prediction
- C) VIF
- D) Correlation

<details><summary>Reveal Answer</summary>**B.** Instance attributions.</details>

### Question 6 — Hard
**Why can PDP mislead with correlated features?**
- A) It cannot
- B) It averages over unrealistic feature combinations
- C) It is slow
- D) It needs scaling

<details><summary>Reveal Answer</summary>**B.** Off-manifold averaging.</details>

### Question 7 — Hard
**What is the difference between global and local?**
- A) They are the same
- B) Global describes average behavior; local explains one case — a globally weak feature can drive a single prediction
- C) Local is slower
- D) Global is exact

<details><summary>Reveal Answer</summary>**B.** Different questions.</details>

### Question 8 — Hard
**Why are explanations not proof of causation?**
- A) They are
- B) They describe model behavior, which may reflect correlations, not real causes
- C) Because of scaling
- D) Because of speed

<details><summary>Reveal Answer</summary>**B.** Model, not world.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You interpret explanations well. |
| 5-6 | Review global vs local and their limits. |
| < 5 | Re-read the lecture. |
