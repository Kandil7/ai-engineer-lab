# SQL Fundamentals 06: Aggregation — Quiz

> **Topic Overview**: Whole-table aggregates, `GROUP BY`, and `HAVING`.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `COUNT(*)` count?**
- A) Non-null values
- B) Rows, including those with NULLs
- C) Distinct rows
- D) Columns

<details><summary>Reveal Answer</summary>**B.** Every row.</details>

### Question 2 — Easy
**What does `COUNT(col)` skip?**
- A) Duplicates
- B) NULLs in that column
- C) Zeros
- D) Negatives

<details><summary>Reveal Answer</summary>**B.** NULLs excluded.</details>

### Question 3 — Medium
**Where does `GROUP BY` put the computation?**
- A) Before `WHERE`
- B) After `WHERE`, producing one row per group for aggregates
- C) After `ORDER BY`
- D) It errors

<details><summary>Reveal Answer</summary>**B.** Per-group aggregates.</details>

### Question 4 — Medium
**`HAVING` vs `WHERE`?**
- A) Same
- B) `WHERE` filters rows before grouping; `HAVING` filters groups after
- C) `HAVING` filters rows
- D) `WHERE` filters groups

<details><summary>Reveal Answer</summary>**B.** Stage decides.</details>

### Question 5 — Medium
**What is a bare column in a grouped query?**
- A) Fine
- B) A non-aggregated column not in `GROUP BY`, whose value is arbitrary — an error in strict SQL
- C) An index
- D) A key

<details><summary>Reveal Answer</summary>**B.** Undefined pick.</details>

### Question 6 — Hard
**Why does `COUNT(DISTINCT x)` cost more than `COUNT(*)`?**
- A) It does not
- B) It must track seen values, not just increment
- C) It sorts
- D) It caches

<details><summary>Reveal Answer</summary>**B.** State plus dedup.</details>

### Question 7 — Hard
**What does a NULL group mean?**
- A) An error
- B) Rows with NULL keys form their own group
- C) They are dropped
- D) They join

<details><summary>Reveal Answer</summary>**B.** NULLs group together.</details>

### Question 8 — Hard
**When can you filter on an aggregate without `HAVING`?**
- A) Never
- B) By wrapping the grouped query in a subquery/CTE and filtering the outer query
- C) With `WHERE`
- D) With `DISTINCT`

<details><summary>Reveal Answer</summary>**B.** Outer filter.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You aggregate correctly. |
| 5-6 | Review `GROUP BY`/`HAVING` stages. |
| < 5 | Re-read the lecture. |
