# ML 08: Multiple Regression — Quiz

> **Topic Overview**: Several predictors, coefficient interpretation, and multicollinearity.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does multiple regression extend?**
- A) To classes
- B) Simple linear regression to several independent variables
- C) To clusters
- D) To trees

<details><summary>Reveal Answer</summary>**B.** Multiple predictors.</details>

### Question 2 — Easy
**How is a coefficient interpreted?**
- A) In isolation
- B) The predicted change in y per unit change in that feature, holding others fixed
- C) As accuracy
- D) As a split

<details><summary>Reveal Answer</summary>**B.** Holding others constant.</details>

### Question 3 — Medium
**What is multicollinearity?**
- A) A missing value
- B) Predictors that are linearly related, making coefficients unstable
- C) An outlier
- D) A cluster

<details><summary>Reveal Answer</summary>**B.** Correlated predictors.</details>

### Question 4 — Medium
**What does VIF measure?**
- A) Accuracy
- B) How much a predictor's variance is inflated by correlation with others
- C) The slope
- D) The count

<details><summary>Reveal Answer</summary>**B.** Collinearity diagnostic.</details>

### Question 5 — Medium
**Why add predictors cautiously?**
- A) For speed
- B) Each adds complexity and can overfit; validate the gain
- C) To cluster
- D) To encode

<details><summary>Reveal Answer</summary>**B.** Justify each feature.</details>

### Question 6 — Hard
**What does a large VIF imply for coefficients?**
- A) They are stable
- B) They are unreliable/interpretation is unsafe because of shared variance
- C) The model is perfect
- D) Causality

<details><summary>Reveal Answer</summary>**B.** Unstable estimates.</details>

### Question 7 — Hard
**Why standardise features before comparing coefficient magnitudes?**
- A) For style
- B) Features on different scales have non-comparable coefficients
- C) To cluster
- D) To sort

<details><summary>Reveal Answer</summary>**B.** Standardised coefficients compare fairly.</details>

### Question 8 — Hard
**What is the risk of dropping a relevant correlated feature?**
- A) None
- B) Omitted-variable bias; remaining coefficients absorb its effect
- C) It clusters
- D) It encodes

<details><summary>Reveal Answer</summary>**B.** Omitted-variable bias.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You read multiple regression well. |
| 5-6 | Review collinearity and interpretation. |
| < 5 | Re-read the lecture. |
