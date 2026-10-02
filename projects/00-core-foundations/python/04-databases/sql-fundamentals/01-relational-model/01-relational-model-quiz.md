# SQL Fundamentals 01: Relational Model — Quiz

> **Topic Overview**: Tables, keys, NULL semantics, and set thinking.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a primary key?**
- A) Any indexed column
- B) The column(s) uniquely identifying each row, non-null
- C) A foreign key
- D) A sort key

<details><summary>Reveal Answer</summary>**B.** Unique row identity.</details>

### Question 2 — Easy
**What is a foreign key?**
- A) A second primary key
- B) A column referencing another table's primary key, enforcing the relation
- C) An index
- D) A view

<details><summary>Reveal Answer</summary>**B.** The relation link.</details>

### Question 3 — Medium
**What does `NULL = NULL` evaluate to?**
- A) True
- B) NULL (unknown), because NULL is not a value
- C) False
- D) An error

<details><summary>Reveal Answer</summary>**B.** Unknown logic.</details>

### Question 4 — Medium
**How do you test for NULL?**
- A) `= NULL`
- B) `IS NULL`
- C) `== NULL`
- D) `LIKE NULL`

<details><summary>Reveal Answer</summary>**B.** The only correct test.</details>

### Question 5 — Medium
**What is the difference between a bag and a set in SQL?**
- A) They are identical
- B) SQL returns multisets (duplicates allowed) unless `DISTINCT` is used
- C) Sets allow duplicates
- D) Bags are indexed

<details><summary>Reveal Answer</summary>**B.** Duplicates by default.</details>

### Question 6 — Hard
**Why can `NOT IN` with a NULL in the list return no rows?**
- A) It cannot
- B) NULL makes every comparison unknown, so the predicate filters everything
- C) It is slow
- D) It errors

<details><summary>Reveal Answer</summary>**B.** The NULL trap.</details>

### Question 7 — Hard
**Why prefer `NOT EXISTS` over `NOT IN` when NULLs are possible?**
- A) Speed
- B) `NOT EXISTS` uses correlated existence, unaffected by NULL semantics
- C) Style
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** NULL-safe exclusion.</details>

### Question 8 — Hard
**What does three-valued logic mean for `WHERE`?**
- A) More rows
- B) Only TRUE passes; FALSE and UNKNOWN rows are filtered out
- C) NULL rows pass
- D) It errors

<details><summary>Reveal Answer</summary>**B.** Unknown is excluded.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You think relationally. |
| 5-6 | Review NULL logic and keys. |
| < 5 | Re-read the lecture. |
