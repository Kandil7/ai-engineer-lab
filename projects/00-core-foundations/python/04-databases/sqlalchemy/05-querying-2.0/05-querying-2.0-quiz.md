# SQLAlchemy 05: Querying 2.0 — Quiz

> **Topic Overview**: `select()`, scalars, joins, and pagination.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the 2.0 read path?**
- A) `query()`
- B) `select()` plus `scalars()`/`execute()`
- C) Raw SQL
- D) `filter()`

<details><summary>Reveal Answer</summary>**B.** Select-style.</details>

### Question 2 — Easy
**`execute()` vs `scalars()`?**
- A) Same
- B) `execute` returns rows; `scalars` unwraps single-column objects
- C) `scalars` is slower
- D) `execute` is legacy

<details><summary>Reveal Answer</summary>**B.** Rows vs objects.</details>

### Question 3 — Medium
**How do you filter?**
- A) `filter()`
- B) `where()`, with `in_`, `like`, `and_`/`or_` combinators
- C) `having()`
- D) Python `if`

<details><summary>Reveal Answer</summary>**B.** Expression filters.</details>

### Question 4 — Medium
**How do you join the same table twice?**
- A) Twice in `join`
- B) `aliased()` for distinct table references
- C) A subquery
- D) You cannot

<details><summary>Reveal Answer</summary>**B.** Aliased joins.</details>

### Question 5 — Medium
**OFFSET vs keyset pagination?**
- A) Same
- B) OFFSET rescans; keyset continues from a seen key
- C) Keyset is slower
- D) OFFSET is stable

<details><summary>Reveal Answer</summary>**B.** Keyset scales.</details>

### Question 6 — Hard
**Why can `unique()` be needed on joined scalars?**
- A) Style
- B) Joined eager loads duplicate parent rows; `unique` dedups the object list
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Dedup joined rows.</details>

### Question 7 — Hard
**When does an aggregate need a subquery instead of a join?**
- A) Never
- B) When the join fans out and would inflate the aggregate
- C) Always
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Aggregate before joining.</details>

### Question 8 — Hard
**Why is `select()` composable?**
- A) It is not
- B) Clauses chain and subqueries embed, building complex queries from parts
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Expression composition.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You query in 2.0 style. |
| 5-6 | Review scalars, joins, pagination. |
| < 5 | Re-read the lecture. |
