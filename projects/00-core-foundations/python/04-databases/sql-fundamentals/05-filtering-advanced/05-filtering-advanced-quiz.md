# SQL Fundamentals 05: Advanced Filtering — Quiz

> **Topic Overview**: `IN`, `LIKE`, NULL tests, boolean logic, and three-valued traps.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `IN` test?**
- A) A range
- B) Membership in a list or subquery result
- C) NULL
- D) A pattern

<details><summary>Reveal Answer</summary>**B.** Set membership.</details>

### Question 2 — Easy
**What does `LIKE` match?**
- A) Exact equality
- B) Patterns with `%` (any run) and `_` (one char)
- C) Ranges
- D) NULLs

<details><summary>Reveal Answer</summary>**B.** Pattern matching.</details>

### Question 3 — Medium
**Why is `IS NULL` required instead of `= NULL`?**
- A) Style
- B) `= NULL` is unknown for every row, so it filters everything out
- C) Speed
- D) It errors

<details><summary>Reveal Answer</summary>**B.** Unknown predicate.</details>

### Question 4 — Medium
**What does `NOT (A AND B)` equal?**
- A) `NOT A AND NOT B`
- B) `NOT A OR NOT B` (De Morgan)
- C) `A OR B`
- D) `A AND B`

<details><summary>Reveal Answer</summary>**B.** De Morgan's law.</details>

### Question 5 — Medium
**Why is a leading `%` in `LIKE` slow?**
- A) It is not
- B) It prevents index use; the scan must check every row
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Non-sargable pattern.</details>

### Question 6 — Hard
**Give a three-valued logic trap with `NOT`.**
- A) None exist
- B) `NOT (x = NULL)` is unknown, so rows you expected are excluded
- C) It is fast
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Negation of unknown.</details>

### Question 7 — Hard
**Why add `ESCAPE` when matching a literal `%`?**
- A) Style
- B) Otherwise the literal is read as a wildcard
- C) Speed
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Escape wildcards.</details>

### Question 8 — Hard
**When is `BETWEEN` inclusive, and what does that imply?**
- A) Exclusive
- B) Inclusive on both ends; use half-open ranges for dates to avoid double counting
- C) It errors on dates
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Closed intervals.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You filter precisely. |
| 5-6 | Review NULL logic and `LIKE`. |
| < 5 | Re-read the lecture. |
