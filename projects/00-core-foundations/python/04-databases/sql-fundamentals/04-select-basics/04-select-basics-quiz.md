# SQL Fundamentals 04: Select Basics — Quiz

> **Topic Overview**: Projection, filtering, ordering, and pagination.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why prefer explicit columns over `SELECT *`?**
- A) Style
- B) It documents intent, reduces transfer, and survives schema change
- C) Speed only
- D) It is required

<details><summary>Reveal Answer</summary>**B.** Explicit projection.</details>

### Question 2 — Easy
**What does `WHERE` do?**
- A) Orders
- B) Filters rows before grouping/ordering
- C) Groups
- D) Limits

<details><summary>Reveal Answer</summary>**B.** Row filter.</details>

### Question 3 — Medium
**Where do NULLs sort by default, and why does it matter?**
- A) Always last
- B) Dialect-dependent (first or last); control it with `NULLS FIRST/LAST`
- C) They error
- D) They are dropped

<details><summary>Reveal Answer</summary>**B.** Explicit NULL ordering.</details>

### Question 4 — Medium
**What do `LIMIT`/`OFFSET` implement?**
- A) Filtering
- B) Page windows into an ordered result
- C) Grouping
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Pagination primitive.</details>

### Question 5 — Medium
**What does `DISTINCT` do?**
- A) Sorts
- B) Removes duplicate rows, enforcing set semantics
- C) Groups
- D) Limits

<details><summary>Reveal Answer</summary>**B.** Deduplicate.</details>

### Question 6 — Hard
**Why must pagination always pair `LIMIT/OFFSET` with `ORDER BY`?**
- A) Style
- B) Without a deterministic order, pages overlap or skip rows
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Stable page windows.</details>

### Question 7 — Hard
**What is the cost of large `OFFSET`?**
- A) None
- B) The database scans and discards the skipped rows on every page
- C) It is cached
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Offset skips work.</details>

### Question 8 — Hard
**When is `DISTINCT` a code smell?**
- A) Never
- B) It often masks a join fan-out that should be fixed at the join
- C) Always use it
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Fix the duplication source.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You select correctly. |
| 5-6 | Review projection, NULL order, pagination. |
| < 5 | Re-read the lecture. |
