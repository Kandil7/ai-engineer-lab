# SQL Fundamentals 14: Query Optimization — Quiz

> **Topic Overview**: Plans, sargability, projection, keyset, and N+1.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the first optimization step?**
- A) Add an index
- B) Read the plan (`EXPLAIN`) to see what the database actually does
- C) Rewrite the query
- D) Cache

<details><summary>Reveal Answer</summary>**B.** Evidence first.</details>

### Question 2 — Easy
**What is sargability?**
- A) A cache
- B) Whether a predicate can use an index (a function-wrapped column cannot)
- C) A join type
- D) A lock

<details><summary>Reveal Answer</summary>**B.** Index-usable predicates.</details>

### Question 3 — Medium
**Why does `WHERE YEAR(ts) = 2024` kill the index?**
- A) It does not
- B) The function hides the column from the index; use a range predicate
- C) Years are slow
- D) It locks

<details><summary>Reveal Answer</summary>**B.** Rewrite as a range.</details>

### Question 4 — Medium
**Why project only used columns?**
- A) Style
- B) Fewer bytes over the wire and a chance at index-only scans
- C) Speed of parsing
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Lean projection.</details>

### Question 5 — Medium
**Keyset vs offset for deep pages?**
- A) Same
- B) Keyset continues from a seen key; offset rescans skipped rows
- C) Offset is cheaper
- D) Keyset needs no order

<details><summary>Reveal Answer</summary>**B.** Keyset scales.</details>

### Question 6 — Hard
**What is the N+1 query problem?**
- A) One slow query
- B) One query plus one per row when lazy-loading relations
- C) A deadlock
- D) A cartesian product

<details><summary>Reveal Answer</summary>**B.** Round-trip multiplication.</details>

### Question 7 — Hard
**How do you fix N+1?**
- A) Cache
- B) Eager-load (join/include) or batch the related fetch
- C) Add indexes
- D) Paginate

<details><summary>Reveal Answer</summary>**B.** Fetch together.</details>

### Question 8 — Hard
**When is denormalization the right optimization?**
- A) Never
- B) When a measured read path pays join costs dwarfing the staleness risk
- C) Always
- D) For writes

<details><summary>Reveal Answer</summary>**B.** Measured tradeoff.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You optimize with evidence. |
| 5-6 | Review plans, sargability, N+1. |
| < 5 | Re-read the lecture. |
