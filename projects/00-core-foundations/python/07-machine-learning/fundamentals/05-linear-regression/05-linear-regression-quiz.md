# ML 05: Linear Regression — Quiz

> **Topic Overview**: Fitting a line, least squares, and the loss.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does simple linear regression model?**
- A) A curve
- B) A straight line `y = mx + b`
- C) Clusters
- D) Classes

<details><summary>Reveal Answer</summary>**B.** Line through the data.</details>

### Question 2 — Easy
**What are the learned parameters?**
- A) Features
- B) Slope and intercept
- C) Labels
- D) Splits

<details><summary>Reveal Answer</summary>**B.** m and b.</details>

### Question 3 — Medium
**What does ordinary least squares minimise?**
- A) The maximum error
- B) The sum of squared residuals
- C) The number of points
- D) The slope

<details><summary>Reveal Answer</summary>**B.** Squared vertical distances.</details>

### Question 4 — Medium
**What does a residual represent?**
- A) A feature
- B) The difference between the actual and predicted value
- C) A weight
- D) A split

<details><summary>Reveal Answer</summary>**B.** Error per point.</details>

### Question 5 — Medium
**Why is squared error sensitive to outliers?**
- A) It is not
- B) Large residuals are squared, so a few points dominate the loss
- C) It sorts
- D) It encodes

<details><summary>Reveal Answer</summary>**B.** Quadratic penalty.</details>

### Question 6 — Hard
**What are the assumptions of linear regression?**
- A) None
- B) Linearity, independent errors, roughly constant variance, and approximately normal residuals
- C) Classes
- D) Clusters

<details><summary>Reveal Answer</summary>**B.** Classic OLS assumptions.</details>

### Question 7 — Hard
**What happens to the fit if the true relationship is curved?**
- A) It is fine
- B) A line underfits; residuals show structure instead of noise
- C) It overfits
- D) It clips

<details><summary>Reveal Answer</summary>**B.** Residual patterns diagnose it.</details>

### Question 8 — Hard
**Why standardise features for regularised/iterative solvers?**
- A) For style
- B) Different scales make the loss ill-conditioned and penalise features unevenly
- C) To sort
- D) To cluster

<details><summary>Reveal Answer</summary>**B.** Scale affects convergence and penalty.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand linear regression. |
| 5-6 | Review least squares and assumptions. |
| < 5 | Re-read the lecture. |
