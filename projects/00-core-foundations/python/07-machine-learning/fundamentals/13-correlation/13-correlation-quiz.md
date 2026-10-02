# ML 13: Correlation — Quiz

> **Topic Overview**: Linear association, coefficients, and correlation vs causation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does Pearson's r measure?**
- A) Causation
- B) The strength and direction of a linear relationship, in [-1, 1]
- C) A count
- D) A rank

<details><summary>Reveal Answer</summary>**B.** Linear association.</details>

### Question 2 — Easy
**What does r = 0 mean?**
- A) Strong linear
- B) No linear relationship (a non-linear one may still exist)
- C) Perfect
- D) Negative

<details><summary>Reveal Answer</summary>**B.** No linear component.</details>

### Question 3 — Medium
**When is Spearman correlation preferred?**
- A) Always
- B) For monotonic but non-linear relationships or ordinal data
- C) For causation
- D) Never

<details><summary>Reveal Answer</summary>**B.** Rank-based.</details>

### Question 4 — Medium
**Why can correlation mislead?**
- A) It cannot
- B) A confounder or a non-linear relationship can produce misleading r
- C) It sorts
- D) It clusters

<details><summary>Reveal Answer</summary>**B.** Hidden structure.</details>

### Question 5 — Medium
**What does a negative r mean?**
- A) No relation
- B) As one variable rises, the other tends to fall
- C) Error
- D) Causality

<details><summary>Reveal Answer</summary>**B.** Inverse linear trend.</details>

### Question 6 — Hard
**What is Anscombe's quartet a warning about?**
- A) Small data
- B) Identical summary statistics/correlation can hide very different data shapes — always plot
- C) Outliers
- D) Scaling

<details><summary>Reveal Answer</summary>**B.** Visualise, do not trust one number.</details>

### Question 7 — Hard
**Why is correlation not causation?**
- A) It is
- B) A third variable may drive both, or the direction may be reversed
- C) Because of scaling
- D) Because of encoding

<details><summary>Reveal Answer</summary>**B.** Confounders/direction.</details>

### Question 8 — Hard
**Why check correlation before linear regression?**
- A) Required
- B) It flags multicollinearity and impossible linear claims
- C) For speed
- D) For causality

<details><summary>Reveal Answer</summary>**B.** Diagnostic.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You interpret correlation well. |
| 5-6 | Review Pearson vs Spearman and pitfalls. |
| < 5 | Re-read the lecture. |
