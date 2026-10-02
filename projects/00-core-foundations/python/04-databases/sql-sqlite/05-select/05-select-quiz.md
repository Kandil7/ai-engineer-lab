# SQL SQLite 05: Select — Quiz

> **Topic Overview**: Projection, `DISTINCT`, aliases, and fetching.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why list columns instead of `SELECT *`?**
- A) Style
- B) Fewer bytes, stable output, no surprise columns
- C) Speed of parsing
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Explicit projection.</details>

### Question 2 — Easy
**What does `DISTINCT` deduplicate?**
- A) One column
- B) Whole rows
- C) Tables
- D) Databases

<details><summary>Reveal Answer</summary>**B.** Row-level dedup.</details>

### Question 3 — Medium
**What are aliases for?**
- A) Renaming tables permanently
- B) Naming output columns, especially computed ones
- C) Indexing
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Output naming.</details>

### Question 4 — Medium
**What is wrong with `LIMIT` without `ORDER BY`?**
- A) Nothing
- B) The ten rows are arbitrary, not a stable page
- C) It errors
- D) It is slow

<details><summary>Reveal Answer</summary>**B.** Undefined page.</details>

### Question 5 — Medium
**`fetchone` vs `fetchall`?**
- A) Same
- B) One row (or `None`) vs everything remaining as a list
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** One vs all.</details>

### Question 6 — Hard
**When should you iterate the cursor instead of `fetchall`?**
- A) Never
- B) For large results, to avoid building a giant list in memory
- C) For small results
- D) For speed of one row

<details><summary>Reveal Answer</summary>**B.** Stream big results.</details>

### Question 7 — Hard
**How do you read rows by column name?**
- A) `row[0]` only
- B) `conn.row_factory = sqlite3.Row`, then `row["name"]`
- C) Aliases
- D) `dict(row)`

<details><summary>Reveal Answer</summary>**B.** Named access.</details>

### Question 8 — Hard
**Why does `DISTINCT` cost?**
- A) It does not
- B) It sorts or hashes the result to remove duplicates
- C) Locking
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Dedup work.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You select well. |
| 5-6 | Review projection and fetching. |
| < 5 | Re-read the lecture. |
