# ML 26: Validation Strategies — Quiz

> **Topic Overview**: Splitter choice, nested CV, and when CV lies.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why does the splitter matter?**
- A) It is cosmetic
- B) A wrong splitter leaks (time, group) and produces a false estimate
- C) For speed
- D) To sort

<details><summary>Reveal Answer</summary>**B.** Splitting encodes assumptions.</details>

### Question 2 — Easy
**Which splitter for imbalanced classification?**
- A) `KFold`
- B) `StratifiedKFold`
- C) `TimeSeriesSplit`
- D) `ShuffleSplit`

<details><summary>Reveal Answer</summary>**B.** Preserve class ratios.</details>

### Question 3 — Medium
**Which splitter for temporal data?**
- A) `KFold`
- B) `TimeSeriesSplit`
- C) `GroupKFold`
- D) `StratifiedKFold`

<details><summary>Reveal Answer</summary>**B.** Chronological folds.</details>

### Question 4 — Medium
**Which splitter for repeated measurements of the same entity?**
- A) `KFold`
- B) `GroupKFold`
- C) `TimeSeriesSplit`
- D) Random

<details><summary>Reveal Answer</summary>**B.** Keep groups intact.</details>

### Question 5 — Medium
**What is nested CV for?**
- A) Speed
- B) An unbiased generalisation estimate when hyperparameters are tuned
- C) Sorting
- D) Clustering

<details><summary>Reveal Answer</summary>**B.** Inner tuning, outer evaluation.</details>

### Question 6 — Hard
**When does CV lie?**
- A) Never
- B) With leakage, temporal/group structure, or tuning and evaluating on the same folds
- C) Always
- D) On small data only

<details><summary>Reveal Answer</summary>**B.** Structure and selection bias.</details>

### Question 7 — Hard
**What is the train/validation/test division of labour?**
- A) All the same
- B) Train fits, validation tunes, test evaluates once
- C) Test tunes
- D) Validation reports

<details><summary>Reveal Answer</summary>**B.** Distinct roles.</details>

### Question 8 — Hard
**What should you do when CV and test disagree sharply?**
- A) Trust CV
- B) Investigate leakage, splitter choice, or distribution shift before shipping
- C) Ignore
- D) Retune on test

<details><summary>Reveal Answer</summary>**B.** The gap is the signal.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You validate honestly. |
| 5-6 | Review splitters and nested CV. |
| < 5 | Re-read the lecture. |
