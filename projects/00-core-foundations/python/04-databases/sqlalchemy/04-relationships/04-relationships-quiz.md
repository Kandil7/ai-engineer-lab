# SQLAlchemy 04: Relationships — Quiz

> **Topic Overview**: One-to-many, cascades, many-to-many, and self-reference.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you declare one-to-many?**
- A) Two foreign keys
- B) `relationship()` with `back_populates` on both sides
- C) A join table
- D) An index

<details><summary>Reveal Answer</summary>**B.** Bidirectional link.</details>

### Question 2 — Easy
**What does cascade delete do?**
- A) Blocks deletes
- B) Deleting a parent removes its children through the relationship
- C) Backs up
- D) Locks

<details><summary>Reveal Answer</summary>**B.** ORM-level cascade.</details>

### Question 3 — Medium
**How is many-to-many modelled?**
- A) Two foreign keys
- B) An association table plus `secondary=`
- C) An array
- D) JSON

<details><summary>Reveal Answer</summary>**B.** Link table.</details>

### Question 4 — Medium
**What is a self-referential relationship for?**
- A) Duplicates
- B) Trees in one table (categories, prompt templates) via a FK to self
- C) Speed
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Hierarchies.</details>

### Question 5 — Medium
**Why use `back_populates` over `backref`?**
- A) Speed
- B) Explicit two-sided declarations stay greppable and typed
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Explicit beats implicit.</details>

### Question 6 — Hard
**ORM cascade vs DB `ON DELETE CASCADE`?**
- A) Same
- B) ORM cascade runs in Python (events fire); DB cascade runs in the database (faster, no events)
- C) DB cascade is slower
- D) ORM cascade is safer always

<details><summary>Reveal Answer</summary>**B.** Two layers.</details>

### Question 7 — Hard
**What is the "one graph write" pattern?**
- A) One row
- B) Build the whole object graph and commit once, letting cascades persist it
- C) One table
- D) One query

<details><summary>Reveal Answer</summary>**B.** Atomic graph persist.</details>

### Question 8 — Hard
**Why can cascades surprise?**
- A) They are slow
- B) A delete can remove far more than the named object; scope cascades deliberately
- C) They lock
- D) They cache

<details><summary>Reveal Answer</summary>**B.** Blast radius.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You map relationships well. |
| 5-6 | Review cascades and association tables. |
| < 5 | Re-read the lecture. |
