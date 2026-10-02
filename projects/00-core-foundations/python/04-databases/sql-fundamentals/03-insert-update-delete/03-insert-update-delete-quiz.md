# SQL Fundamentals 03: Insert, Update, Delete — Quiz

> **Topic Overview**: Writes, upserts, bulk insert, and safe deletes.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `RETURNING` do?**
- A) Rolls back
- B) Returns the written rows (e.g. generated ids) in the same statement
- C) Deletes
- D) Commits

<details><summary>Reveal Answer</summary>**B.** Write plus read-back.</details>

### Question 2 — Easy
**What is an upsert?**
- A) Insert only
- B) Insert, or update on conflict (`ON CONFLICT ... DO UPDATE`)
- C) A delete
- D) A bulk load

<details><summary>Reveal Answer</summary>**B.** Insert-or-update.</details>

### Question 3 — Medium
**Why use `executemany` for bulk insert?**
- A) Style
- B) One round-trip pattern for many rows instead of per-row statements
- C) It is slower
- D) It locks

<details><summary>Reveal Answer</summary>**B.** Batched writes.</details>

### Question 4 — Medium
**Why is `UPDATE` without a `WHERE` dangerous?**
- A) Slow
- B) It rewrites every row in the table
- C) It locks
- D) It errors

<details><summary>Reveal Answer</summary>**B.** Target your writes.</details>

### Question 5 — Medium
**What does `DELETE ... LIMIT` give you?**
- A) Nothing
- B) A portable way to delete a bounded number of rows per statement
- C) Speed
- D) A backup

<details><summary>Reveal Answer</summary>**B.** Bounded deletes.</details>

### Question 6 — Hard
**Why parameterize write values?**
- A) Speed
- B) Prevents SQL injection and lets the planner reuse the statement
- C) Style
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Safety plus plan reuse.</details>

### Question 7 — Hard
**Why preview a destructive `WHERE` with a `SELECT` first?**
- A) Style
- B) The `SELECT` shows exactly which rows the write will touch
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Verify before writing.</details>

### Question 8 — Hard
**What should wrap a multi-row write that must be atomic?**
- A) Nothing
- B) A transaction, so partial writes roll back
- C) A view
- D) An index

<details><summary>Reveal Answer</summary>**B.** Atomic writes.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You write safe DML. |
| 5-6 | Review upserts, bulk, and WHERE discipline. |
| < 5 | Re-read the lecture. |
