# SQL SQLite 06: Where — Quiz

> **Topic Overview**: Predicates, logic, special operators, and parameters.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `WHERE age >= ?` do?**
- A) Sorts
- B) Keeps only rows matching the predicate
- C) Groups
- D) Limits

<details><summary>Reveal Answer</summary>**B.** Row filter.</details>

### Question 2 — Easy
**How do you test for NULL?**
- A) `= NULL`
- B) `IS NULL`
- C) `== NULL`
- D) `LIKE NULL`

<details><summary>Reveal Answer</summary>**B.** Only correct test.</details>

### Question 3 — Medium
**Why parenthesize `a OR b AND c`?**
- A) Style
- B) `AND` binds tighter; explicit parens prevent silent misreads
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Precedence trap.</details>

### Question 4 — Medium
**How do you pass a list to `IN` safely?**
- A) Format it in
- B) One `?` per element, built dynamically
- C) A single `?`
- D) `LIKE`

<details><summary>Reveal Answer</summary>**B.** Placeholder per element.</details>

### Question 5 — Medium
**What do `%` and `_` mean in `LIKE`?**
- A) Nothing special
- B) `%` matches any run, `_` matches one character
- C) They escape
- D) They sort

<details><summary>Reveal Answer</summary>**B.** Wildcards.</details>

### Question 6 — Hard
**What does `= NULL` return?**
- A) True
- B) Unknown, filtering the row out with no error
- C) False
- D) An error

<details><summary>Reveal Answer</summary>**B.** Silent exclusion.</details>

### Question 7 — Hard
**Why is an empty `IN ()` a problem?**
- A) It matches all
- B) It is a syntax error; guard or short-circuit
- C) It is slow
- D) It matches none safely

<details><summary>Reveal Answer</summary>**B.** Guard empty lists.</details>

### Question 8 — Hard
**Is `BETWEEN` inclusive?**
- A) Exclusive
- B) Inclusive on both ends
- C) Depends
- D) Half-open

<details><summary>Reveal Answer</summary>**B.** Closed interval.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You filter safely. |
| 5-6 | Review NULL logic and parameters. |
| < 5 | Re-read the lecture. |
