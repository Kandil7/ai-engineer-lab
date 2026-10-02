# SQLAlchemy 06: Eager Loading — Quiz

> **Topic Overview**: N+1, the three loaders, and locking the fix.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the N+1 problem?**
- A) One slow query
- B) One query plus one per row when lazy-loading relations
- C) A deadlock
- D) A cartesian product

<details><summary>Reveal Answer</summary>**B.** Round-trip multiplication.</details>

### Question 2 — Easy
**What does `selectinload` do?**
- A) Joins
- B) Loads children in one extra query with an `IN` on parent ids
- C) Caches
- D) Subqueries

<details><summary>Reveal Answer</summary>**B.** One extra query.</details>

### Question 3 — Medium
**`selectinload` vs `joinedload`?**
- A) Same
- B) `selectinload` is 1+N-shaped (two queries); `joinedload` is one query with a join
- C) `joinedload` is slower always
- D) `selectinload` joins

<details><summary>Reveal Answer</summary>**B.** Two queries vs one.</details>

### Question 4 — Medium
**When is `joinedload` risky?**
- A) Never
- B) One-to-many joins duplicate parents, inflating rows and breaking pagination
- C) Always
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Fan-out duplication.</details>

### Question 5 — Medium
**What does `lazy="raise"` enforce?**
- A) Eager loading
- B) Any implicit lazy load raises, proving no N+1 hides in the code path
- C) Caching
- D) Joins

<details><summary>Reveal Answer</summary>**B.** Fail on lazy access.</details>

### Question 6 — Hard
**How do you lock the fix in tests?**
- A) Trust
- B) Assert the query count for the code path
- C) Logs
- D) Speed

<details><summary>Reveal Answer</summary>**B.** Count queries.</details>

### Question 7 — Hard
**Why is `subqueryload` the third option?**
- A) It is best
- B) It loads via a derived table: one query, no parent duplication, at subquery cost
- C) It is legacy
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Middle path.</details>

### Question 8 — Hard
**What does the batch-loaded listing pattern combine?**
- A) Caching
- B) Explicit loader options on the listing query plus a query-count test
- C) Joins only
- D) Pagination only

<details><summary>Reveal Answer</summary>**B.** Declared loading, verified.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You kill N+1. |
| 5-6 | Review the three loaders. |
| < 5 | Re-read the lecture. |
