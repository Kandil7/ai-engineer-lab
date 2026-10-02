# SQL Fundamentals 08: Subqueries and CTEs — Quiz

> **Topic Overview**: Scalar/table subqueries, correlated traps, and recursive CTEs.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a scalar subquery?**
- A) A table
- B) A query returning one value, usable inline in an expression
- C) A join
- D) A CTE

<details><summary>Reveal Answer</summary>**B.** One value inline.</details>

### Question 2 — Easy
**What is a CTE?**
- A) A temp table
- B) A named `WITH` query step referenced by the main query
- C) A view
- D) An index

<details><summary>Reveal Answer</summary>**B.** Named steps.</details>

### Question 3 — Medium
**Why is a correlated subquery slow?**
- A) It is not
- B) It re-executes per outer row instead of once
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Per-row execution.</details>

### Question 4 — Medium
**What can replace a correlated subquery?**
- A) Nothing
- B) A join or a window function
- C) A view
- D) An index

<details><summary>Reveal Answer</summary>**B.** Set-based rewrite.</details>

### Question 5 — Medium
**What does a recursive CTE walk?**
- A) Arrays
- B) Hierarchies/trees (org charts, parts) with an anchor plus a recursive member
- C) Strings
- D) JSON

<details><summary>Reveal Answer</summary>**B.** Tree traversal.</details>

### Question 6 — Hard
**Why must a recursive CTE terminate?**
- A) It does automatically
- B) Without a stopping condition it recurses forever; bound depth or the base case
- C) It is slow
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Termination is on you.</details>

### Question 7 — Hard
**`NOT IN` vs `NOT EXISTS` with NULLs?**
- A) Same
- B) `NOT IN` with a NULL in the list excludes everything; `NOT EXISTS` is NULL-safe
- C) `NOT EXISTS` is slower
- D) Both error

<details><summary>Reveal Answer</summary>**B.** The NULL trap.</details>

### Question 8 — Hard
**When is a subquery in `FROM` better than a CTE?**
- A) Always
- B) For a single-use inline step; a CTE wins on readability and reuse
- C) Never
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Inline vs named.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You compose subqueries well. |
| 5-6 | Review correlated and recursive CTEs. |
| < 5 | Re-read the lecture. |
