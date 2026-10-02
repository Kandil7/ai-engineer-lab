# SQL SQLite 03: Create Table — Quiz

> **Topic Overview**: Columns, SQLite types, constraints, and generated ids.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What are SQLite's native type affinities?**
- A) VARCHAR, CHAR, DATE
- B) INTEGER, TEXT, REAL, BLOB
- C) JSON, ARRAY
- D) UUID, MONEY

<details><summary>Reveal Answer</summary>**B.** Four affinities.</details>

### Question 2 — Easy
**What happens to `VARCHAR(255)` in SQLite?**
- A) Error
- B) Accepted with TEXT affinity
- C) Truncated
- D) Ignored

<details><summary>Reveal Answer</summary>**B.** Affinity mapping.</details>

### Question 3 — Medium
**What does `INTEGER PRIMARY KEY` give you?**
- A) Nothing special
- B) Auto-assigned rowids without a separate index
- C) A string key
- D) A UUID

<details><summary>Reveal Answer</summary>**B.** Auto rowid alias.</details>

### Question 4 — Medium
**When is `AUTOINCREMENT` needed beyond it?**
- A) Never
- B) When ids must never be reused after deletes
- C) For speed
- D) For text keys

<details><summary>Reveal Answer</summary>**B.** No-reuse guarantee.</details>

### Question 5 — Medium
**Why declare `NOT NULL`?**
- A) Style
- B) To forbid missing values the application would mishandle
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Presence enforced.</details>

### Question 6 — Hard
**What does a `CHECK` constraint enforce?**
- A) Keys
- B) A value rule on every write (e.g. `age >= 0`)
- C) Indexes
- D) Uniqueness

<details><summary>Reveal Answer</summary>**B.** Domain rule.</details>

### Question 7 — Hard
**Why is `IF NOT EXISTS` important in setup scripts?**
- A) Speed
- B) Re-running setup must not crash on existing tables
- C) Locking
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Idempotent DDL.</details>

### Question 8 — Hard
**Why version schema scripts?**
- A) Style
- B) Ordered, reviewable evolution beats ad-hoc DDL
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Migrations as code.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You define tables well. |
| 5-6 | Review types and constraints. |
| < 5 | Re-read the lecture. |
