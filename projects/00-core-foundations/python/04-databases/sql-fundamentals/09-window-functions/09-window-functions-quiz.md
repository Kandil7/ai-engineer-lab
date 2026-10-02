# SQL Fundamentals 09: Window Functions — Quiz

> **Topic Overview**: `OVER`, ranking, `LAG`/`LEAD`, running totals, and frames.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does a window function compute over?**
- A) The whole table
- B) A defined partition of rows, keeping one output row per input row
- C) Groups only
- D) One row

<details><summary>Reveal Answer</summary>**B.** Per-row with context.</details>

### Question 2 — Easy
**`ROW_NUMBER()` vs `RANK()`?**
- A) Same
- B) `ROW_NUMBER` never ties; `RANK` ties share a rank and skip the next
- C) `RANK` never ties
- D) Both skip

<details><summary>Reveal Answer</summary>**B.** Tie handling.</details>

### Question 3 — Medium
**What do `LAG`/`LEAD` return?**
- A) Aggregates
- B) The previous/next row's value within the partition
- C) The rank
- D) The count

<details><summary>Reveal Answer</summary>**B.** Neighbor access.</details>

### Question 4 — Medium
**How do you compute a running total?**
- A) `SUM(x) GROUP BY`
- B) `SUM(x) OVER (ORDER BY t)` accumulating rows seen so far
- C) A join
- D) A subquery only

<details><summary>Reveal Answer</summary>**B.** Ordered accumulation.</details>

### Question 5 — Medium
**What is a frame?**
- A) A table
- B) The subset of the partition the function sees (e.g. 3 preceding rows)
- C) A CTE
- D) An index

<details><summary>Reveal Answer</summary>**B.** Window inside the window.</details>

### Question 6 — Hard
**Why must the `ORDER BY` inside `OVER` be deterministic?**
- A) Style
- B) Ties make `ROW_NUMBER` assign ranks arbitrarily across runs
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Tiebreaker required.</details>

### Question 7 — Hard
**Why can't you use a window function in `WHERE`?**
- A) You can
- B) Windows evaluate after `WHERE`; filter in an outer query or qualify
- C) Syntax error always
- D) It is slow

<details><summary>Reveal Answer</summary>**B.** Evaluation order.</details>

### Question 8 — Hard
**`RANK` vs `DENSE_RANK` on tied second place?**
- A) Same
- B) `RANK` skips to 4th next; `DENSE_RANK` continues at 3rd
- C) `DENSE_RANK` skips
- D) Both skip equally

<details><summary>Reveal Answer</summary>**B.** Gap vs no gap.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You window correctly. |
| 5-6 | Review ranking and frames. |
| < 5 | Re-read the lecture. |
