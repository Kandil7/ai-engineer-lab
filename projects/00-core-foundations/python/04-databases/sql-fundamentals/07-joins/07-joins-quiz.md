# SQL Fundamentals 07: Joins — Quiz

> **Topic Overview**: Inner, outer, self, multi-joins, and cardinality.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `INNER JOIN` return?**
- A) All rows from both
- B) Only rows matched on both sides
- C) Unmatched left rows
- D) Unmatched right rows

<details><summary>Reveal Answer</summary>**B.** Matches only.</details>

### Question 2 — Easy
**What does `LEFT JOIN` add?**
- A) Right-only rows
- B) All left rows, with NULLs where no match exists
- C) Duplicates
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Left preserved.</details>

### Question 3 — Medium
**What is a self join for?**
- A) Duplicates
- B) Relating rows within one table (employees to managers)
- C) Speed
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Intra-table relations.</details>

### Question 4 — Medium
**What is the join-cardinality trap?**
- A) Slow joins
- B) A one-to-many join multiplies rows, inflating later sums/counts
- C) Missing indexes
- D) NULL keys

<details><summary>Reveal Answer</summary>**B.** Row explosion.</details>

### Question 5 — Medium
**When is a `CROSS JOIN` correct?**
- A) Never
- B) When you deliberately want the Cartesian product (e.g. every combination)
- C) For speed
- D) For filtering

<details><summary>Reveal Answer</summary>**B.** Deliberate product.</details>

### Question 6 — Hard
**Why do aggregates after a fan-out join overcount?**
- A) They do not
- B) The join duplicates rows before the aggregate sees them
- C) NULLs
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Aggregate before joining.</details>

### Question 7 — Hard
**How do you find orphans (orders with no customer)?**
- A) `INNER JOIN`
- B) `LEFT JOIN` plus `WHERE right.key IS NULL`
- C) `CROSS JOIN`
- D) `GROUP BY`

<details><summary>Reveal Answer</summary>**B.** Anti-join pattern.</details>

### Question 8 — Hard
**Why chain joins in dependency order?**
- A) Style
- B) Each join's keys must exist in the accumulated result, or the fan-out compounds
- C) Speed
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Ordered composition.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You join safely. |
| 5-6 | Review outer joins and fan-out. |
| < 5 | Re-read the lecture. |
