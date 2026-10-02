# SQL SQLite 04: Insert — Quiz

> **Topic Overview**: Single/bulk inserts, parameters, and write verification.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you insert one row safely?**
- A) Format values into the string
- B) `INSERT INTO ... VALUES (?, ?)` with parameters
- C) `SELECT` first
- D) `UPDATE`

<details><summary>Reveal Answer</summary>**B.** Parameters, never formatting.</details>

### Question 2 — Easy
**What does `lastrowid` return?**
- A) Row count
- B) The auto-generated id of the inserted row
- C) The table name
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Generated key.</details>

### Question 3 — Medium
**Why use `executemany`?**
- A) Style
- B) One statement shape for many rows, far faster than a loop
- C) It commits
- D) It validates

<details><summary>Reveal Answer</summary>**B.** Batched writes.</details>

### Question 4 — Medium
**What does `INSERT INTO ... SELECT` do?**
- A) Reads only
- B) Copies query results into a table without Python round-trips
- C) Deletes
- D) Updates

<details><summary>Reveal Answer</summary>**B.** In-database copy.</details>

### Question 5 — Medium
**What does `rowcount` mean after an `UPDATE`?**
- A) Total rows
- B) Rows actually affected; 0 usually signals a wrong predicate
- C) Inserted ids
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Affected rows.</details>

### Question 6 — Hard
**Why wrap a big load in one transaction?**
- A) Style
- B) One commit is faster and atomic; per-row commits are slow and partial
- C) Locking
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Speed plus atomicity.</details>

### Question 7 — Hard
**What is lost closing without commit?**
- A) Nothing
- B) Every uncommitted write in the transaction
- C) The table
- D) The file

<details><summary>Reveal Answer</summary>**B.** Uncommitted work vanishes.</details>

### Question 8 — Hard
**Why list columns explicitly in `INSERT INTO ... SELECT`?**
- A) Style
- B) A schema change would otherwise misalign the copy silently
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Explicit mapping.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You write safe inserts. |
| 5-6 | Review parameters and bulk patterns. |
| < 5 | Re-read the lecture. |
