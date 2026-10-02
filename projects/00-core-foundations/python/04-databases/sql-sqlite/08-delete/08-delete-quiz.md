# SQL SQLite 08: Delete — Quiz

> **Topic Overview**: Targeted deletes, `TRUNCATE`, foreign keys, and soft deletes.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `DELETE` without `WHERE` do?**
- A) Nothing
- B) Removes every row
- C) Errors
- D) Drops the table

<details><summary>Reveal Answer</summary>**B.** Whole-table wipe.</details>

### Question 2 — Easy
**How do you preview a delete?**
- A) You cannot
- B) Run the same predicate as a `SELECT` first
- C) `EXPLAIN`
- D) `LIMIT 0`

<details><summary>Reveal Answer</summary>**B.** See the victims.</details>

### Question 3 — Medium
**`DELETE` vs `TRUNCATE`?**
- A) Same
- B) `DELETE` is row-selective, transactional, trigger-aware; `TRUNCATE` is fast, final, structure-preserving
- C) `TRUNCATE` is slower
- D) `DELETE` keeps no log

<details><summary>Reveal Answer</summary>**B.** Selective vs wholesale.</details>

### Question 4 — Medium
**What does `ON DELETE CASCADE` do?**
- A) Blocks the delete
- B) Removes dependent child rows automatically
- C) Backs up
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Cascading removal.</details>

### Question 5 — Medium
**What does `ON DELETE RESTRICT` do?**
- A) Deletes children
- B) Refuses the delete while children exist
- C) Backs up
- D) Ignores

<details><summary>Reveal Answer</summary>**B.** Protective block.</details>

### Question 6 — Hard
**What is a soft delete?**
- A) A slow delete
- B) Marking rows inactive (`is_active = 0`) instead of removing them
- C) A backup
- D) A transaction

<details><summary>Reveal Answer</summary>**B.** Hide, do not remove.</details>

### Question 7 — Hard
**What does soft delete cost on reads?**
- A) Nothing
- B) Every query must filter inactive rows, and unique constraints get complicated
- C) Speed only
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Permanent filter tax.</details>

### Question 8 — Hard
**Why batch large deletes?**
- A) Style
- B) To bound locks and transaction-log growth
- C) Speed of one row
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Bounded batches.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You delete safely. |
| 5-6 | Review `WHERE` discipline and FK actions. |
| < 5 | Re-read the lecture. |
