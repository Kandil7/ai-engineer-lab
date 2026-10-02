# SQL Fundamentals 02: DDL and Schema — Quiz

> **Topic Overview**: `CREATE TABLE`, constraints, and evolving a live schema.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `CREATE TABLE` define?**
- A) Rows
- B) Columns, types, and constraints
- C) Indexes only
- D) Views

<details><summary>Reveal Answer</summary>**B.** Structure plus rules.</details>

### Question 2 — Easy
**How do you query the schema itself?**
- A) You cannot
- B) Via `information_schema` / system catalogs
- C) `SELECT *`
- D) `DESCRIBE` only

<details><summary>Reveal Answer</summary>**B.** Schema is data.</details>

### Question 3 — Medium
**What is the `PRIMARY KEY` vs `UNIQUE` NULL asymmetry?**
- A) None
- B) `UNIQUE` allows NULLs (one or many, dialect-dependent); `PRIMARY KEY` forbids them
- C) `PRIMARY KEY` allows NULLs
- D) They are identical

<details><summary>Reveal Answer</summary>**B.** NULL handling differs.</details>

### Question 4 — Medium
**What does `ON DELETE CASCADE` do?**
- A) Prevents deletes
- B) Deletes dependent rows when the parent is deleted
- C) Backs up
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Cascading delete.</details>

### Question 5 — Medium
**Why is `ON DELETE RESTRICT` safer by default?**
- A) Faster
- B) It refuses to delete a parent with children, preventing accidental data loss
- C) It is slower
- D) It locks

<details><summary>Reveal Answer</summary>**B.** Fail closed.</details>

### Question 6 — Hard
**How do you evolve a live schema?**
- A) Drop and recreate
- B) `ALTER TABLE` migrations, backward compatible, applied in order
- C) Edit the dumps
- D) Restart

<details><summary>Reveal Answer</summary>**B.** Versioned migrations.</details>

### Question 7 — Hard
**Why is `DROP TABLE` dangerous without a migration record?**
- A) It is slow
- B) It destroys data with no reversible path and desyncs environments
- C) It locks
- D) It errors

<details><summary>Reveal Answer</summary>**B.** Irreversible.</details>

### Question 8 — Hard
**What is a check constraint for?**
- A) Keys only
- B) Enforcing a value rule at the database level (e.g. `price >= 0`)
- C) Indexing
- D) Views

<details><summary>Reveal Answer</summary>**B.** Data-rule enforcement.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You design schemas well. |
| 5-6 | Review constraints and migrations. |
| < 5 | Re-read the lecture. |
