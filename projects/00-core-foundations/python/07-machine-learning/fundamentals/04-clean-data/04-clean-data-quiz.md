# ML 04: Cleaning Data — Quiz

> **Topic Overview**: Missing values, outliers, duplicates, and types.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a missing value?**
- A) Zero
- B) An absent entry (NaN/None), not the same as zero
- C) An outlier
- D) A duplicate

<details><summary>Reveal Answer</summary>**B.** Absence, not a value.</details>

### Question 2 — Easy
**Name three ways to handle missing values.**
- A) Delete, impute (mean/median/mode), or model-aware impute
- B) Sort, hash, encode
- C) Scale, split, tune
- D) There is one way

<details><summary>Reveal Answer</summary>**A.** Drop or fill.</details>

### Question 3 — Medium
**Why impute with the training statistic only?**
- A) Speed
- B) Computing the mean over the test set leaks information
- C) Simplicity
- D) It is required

<details><summary>Reveal Answer</summary>**B.** Fit on train, apply to test.</details>

### Question 4 — Medium
**What is a duplicate row, and why remove it?**
- A) Two identical rows; they bias frequency-based learning and can leak across splits
- B) A missing value
- C) An outlier
- D) A feature

<details><summary>Reveal Answer</summary>**A.** Duplicates overweight examples.</details>

### Question 5 — Medium
**Why must dtypes be fixed before modelling?**
- A) For style
- B) Numbers stored as strings silently break arithmetic and split logic
- C) To sort
- D) To encode

<details><summary>Reveal Answer</summary>**B.** Type errors hide.</details>

### Question 6 — Hard
**How should outliers be treated?**
- A) Always remove
- B) Investigate; they may be errors or signal. Use robust statistics before deciding
- C) Always keep
- D) Round them

<details><summary>Reveal Answer</summary>**B.** Context decides.</details>

### Question 7 — Hard
**Why is median often preferred over mean for imputation?**
- A) It is faster
- B) It is robust to skew and outliers
- C) It is exact
- D) It is required

<details><summary>Reveal Answer</summary>**B.** Robust central tendency.</details>

### Question 8 — Hard
**What is the risk of dropping every row with a missing value?**
- A) None
- B) You may drop most of the data and bias the sample if missingness is systematic
- C) It is slower
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Missingness is often informative.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You clean data carefully. |
| 5-6 | Review imputation and leakage. |
| < 5 | Re-read the lecture. |
