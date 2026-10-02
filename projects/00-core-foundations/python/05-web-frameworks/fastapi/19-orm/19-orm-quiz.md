# FastAPI 19: ORM — Quiz

> **Topic Overview**: SQLAlchemy models, mapping, and the N+1 problem.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does an ORM do?**
- A) Serves HTTP
- B) Maps Python objects to database tables and queries
- C) Validates JSON
- D) Caches

<details><summary>Reveal Answer</summary>**B.** Object-relational mapping.</details>

### Question 2 — Easy
**Why separate ORM models from Pydantic schemas?**
- A) Style
- B) They have different concerns: persistence vs API contract
- C) For speed
- D) It is required

<details><summary>Reveal Answer</summary>**B.** Do not couple storage to API.</details>

### Question 3 — Medium
**What is the N+1 query problem?**
- A) One slow query
- B) One query per row when loading a relationship, multiplying round-trips
- C) A pool issue
- D) A cache miss

<details><summary>Reveal Answer</summary>**B.** Fix with eager loading.</details>

### Question 4 — Medium
**How do you avoid N+1?**
- A) Cache
- B) Eager-load relationships (`selectinload`/`joinedload`) or batch
- C) Add indexes
- D) Use raw SQL only

<details><summary>Reveal Answer</summary>**B.** Load in one round-trip.</details>

### Question 5 — Medium
**What is the identity map?**
- A) A cache of rows per session
- B) A unit-of-work guarantee that one row maps to one object
- C) A pool
- D) A schema

<details><summary>Reveal Answer</summary>**A.** Session-level identity.</details>

### Question 6 — Hard
**Why is lazy loading dangerous in async code?**
- A) It is not
- B) It triggers implicit I/O at attribute access, which is unsafe in async contexts
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Implicit IO; eager-load instead.</details>

### Question 7 — Hard
**What does `expire_on_commit` control?**
- A) Cache
- B) Whether objects are expired (reloaded) after commit, affecting later attribute access
- C) Pool size
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Reload behavior.</details>

### Question 8 — Hard
**Why are migrations essential with an ORM?**
- A) Style
- B) Schema changes must be versioned and applied deterministically
- C) For caching
- D) For sorting

<details><summary>Reveal Answer</summary>**B.** Reproducible schema evolution.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You use the ORM well. |
| 5-6 | Review N+1 and model separation. |
| < 5 | Re-read the lecture. |
