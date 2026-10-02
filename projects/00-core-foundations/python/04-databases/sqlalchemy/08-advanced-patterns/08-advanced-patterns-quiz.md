# SQLAlchemy 08: Advanced Patterns — Quiz

> **Topic Overview**: Hybrids, custom types, versioning, `RETURNING`, and windows.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does a hybrid property give you?**
- A) Caching
- B) One expression usable both in Python and in SQL
- C) A view
- D) An index

<details><summary>Reveal Answer</summary>**B.** Dual-context logic.</details>

### Question 2 — Easy
**Why write a custom type?**
- A) Style
- B) To bind a Python value (e.g. embeddings as bytes) to a column representation
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Value mapping.</details>

### Question 3 — Medium
**What is optimistic versioning?**
- A) Locking rows
- B) A version column checked on update to detect concurrent writes
- C) Backups
- D) Migrations

<details><summary>Reveal Answer</summary>**B.** Conflict detection.</details>

### Question 4 — Medium
**What does `INSERT ... RETURNING` buy?**
- A) Speed only
- B) Generated values back in one round-trip, no second select
- C) Caching
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Write plus read-back.</details>

### Question 5 — Medium
**Why rank inside the database?**
- A) Style
- B) Window functions avoid shipping all rows to Python for ordering
- C) Speed of Python
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Rank where the data lives.</details>

### Question 6 — Hard
**What does a version guard do on concurrent edits?**
- A) Locks
- B) The second writer's `UPDATE ... WHERE version = n` hits zero rows and retries
- C) Merges
- D) Ignores

<details><summary>Reveal Answer</summary>**B.** Compare-and-swap.</details>

### Question 7 — Hard
**When is a custom type risky?**
- A) Never
- B) When it hides non-portable or lossy conversions the schema should state
- C) Always
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Transparent mapping.</details>

### Question 8 — Hard
**What combines ranked output with safe concurrent updates?**
- A) Caching
- B) Window-function ranking plus version-guarded writes
- C) Locking everything
- D) Raw SQL

<details><summary>Reveal Answer</summary>**B.** The leaderboard pattern.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You apply advanced patterns well. |
| 5-6 | Review hybrids, versioning, `RETURNING`. |
| < 5 | Re-read the lecture. |
