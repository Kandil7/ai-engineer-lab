# SQL SQLite 11: Join — Quiz

> **Topic Overview**: Inner/outer/self joins, aliases, and fan-out.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `INNER JOIN` keep?**
- A) All left rows
- B) Only matched rows
- C) All right rows
- D) All rows

<details><summary>Reveal Answer</summary>**B.** Matches only.</details>

### Question 2 — Easy
**What does `LEFT JOIN` preserve?**
- A) Right rows
- B) All left rows, NULL-filling misses
- C) Matches only
- D) Duplicates

<details><summary>Reveal Answer</summary>**B.** Left intact.</details>

### Question 3 — Medium
**How do you emulate `RIGHT JOIN` in SQLite?**
- A) You cannot
- B) Swap the tables and use `LEFT JOIN`
- C) `FULL JOIN`
- D) `CROSS JOIN`

<details><summary>Reveal Answer</summary>**B.** Swap sides.</details>

### Question 4 — Medium
**What is a self-join?**
- A) A duplicate table
- B) A table joined to itself under two aliases (e.g. employee→manager)
- C) A cross join
- D) An error

<details><summary>Reveal Answer</summary>**B.** Intra-table relations.</details>

### Question 5 — Medium
**What is join fan-out?**
- A) Slow joins
- B) One-to-many matches multiplying rows before later steps see them
- C) Missing indexes
- D) NULL keys

<details><summary>Reveal Answer</summary>**B.** Row multiplication.</details>

### Question 6 — Hard
**Why does `SUM` after a fan-out overcount?**
- A) It does not
- B) Duplicated rows inflate the aggregate; aggregate before joining
- C) NULLs
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Aggregate first.</details>

### Question 7 — Hard
**How do you find users with no orders?**
- A) `INNER JOIN`
- B) `LEFT JOIN ... WHERE orders.id IS NULL`
- C) `CROSS JOIN`
- D) `GROUP BY`

<details><summary>Reveal Answer</summary>**B.** Anti-join.</details>

### Question 8 — Hard
**What happens with no `ON` clause?**
- A) An error
- B) A `CROSS JOIN`: every row times every row
- C) An inner join
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Accidental product.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You join safely. |
| 5-6 | Review outer joins and fan-out. |
| < 5 | Re-read the lecture. |
