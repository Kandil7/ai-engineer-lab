# SQL SQLite 09: Update — Quiz

> **Topic Overview**: Targeted rewrites, `CASE`, and rowcount verification.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does an `UPDATE` without `WHERE` do?**
- A) Nothing
- B) Rewrites every row
- C) Errors
- D) Inserts

<details><summary>Reveal Answer</summary>**B.** Whole-table rewrite.</details>

### Question 2 — Easy
**How do you set several columns at once?**
- A) Multiple statements
- B) One `SET a = ..., b = ...` list
- C) `CASE` only
- D) You cannot

<details><summary>Reveal Answer</summary>**B.** Single statement.</details>

### Question 3 — Medium
**What is `CASE` in an `UPDATE` for?**
- A) Joins
- B) Different values per row in one atomic statement
- C) Sorting
- D) Filtering

<details><summary>Reveal Answer</summary>**B.** Conditional assignment.</details>

### Question 4 — Medium
**Why check `rowcount` after an `UPDATE`?**
- A) Style
- B) Zero affected rows usually means the predicate matched nothing — a bug
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Verify the hit.</details>

### Question 5 — Medium
**Why preview an update as `SELECT`?**
- A) Style
- B) The `SELECT` shows exactly which rows the `WHERE` will change
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** See before changing.</details>

### Question 6 — Hard
**Why do related updates belong in one transaction?**
- A) Speed
- B) So a mid-way failure rolls everything back instead of leaving half-updated data
- C) Locking
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Atomic multi-write.</details>

### Question 7 — Hard
**What is the risk of splitting one row's changes across statements?**
- A) None
- B) A failure between them leaves the row half-updated
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Partial state.</details>

### Question 8 — Hard
**Why parameterize `SET` values?**
- A) Style
- B) Values are untrusted input; formatting them in is injection
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Parameters everywhere.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You update safely. |
| 5-6 | Review `WHERE` discipline and `CASE`. |
| < 5 | Re-read the lecture. |
