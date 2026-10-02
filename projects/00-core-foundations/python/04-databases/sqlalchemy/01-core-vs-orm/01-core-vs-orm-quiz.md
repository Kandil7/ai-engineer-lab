# SQLAlchemy 01: Core vs ORM — Quiz

> **Topic Overview**: The two layers, Core DML, and safe raw SQL.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What are SQLAlchemy's two layers?**
- A) Sync/async
- B) Core (SQL expression language) and ORM (object mapping)
- C) Test/prod
- D) Read/write

<details><summary>Reveal Answer</summary>**B.** Expressions plus objects.</details>

### Question 2 — Easy
**What is `MetaData` for?**
- A) Caching
- B) Holding the table definitions a Core statement is built from
- C) Pooling
- D) Migrating

<details><summary>Reveal Answer</summary>**B.** Schema registry.</details>

### Question 3 — Medium
**How do you run raw SQL safely?**
- A) Format strings
- B) `text()` with bound parameters
- C) `execute` a string
- D) You cannot

<details><summary>Reveal Answer</summary>**B.** Parameterized text.</details>

### Question 4 — Medium
**Who owns the commit?**
- A) The engine
- B) You: the connection/session commits explicitly
- C) Autocommit always
- D) The pool

<details><summary>Reveal Answer</summary>**B.** Explicit commit.</details>

### Question 5 — Medium
**When does Core beat the ORM?**
- A) Never
- B) For bulk loads and set operations where object overhead is pure cost
- C) Always
- D) For relations

<details><summary>Reveal Answer</summary>**B.** Bulk and set work.</details>

### Question 6 — Hard
**What is the table-bounded bulk loader pattern?**
- A) ORM `add_all`
- B) Core `insert()` in batches inside one transaction
- C) Raw CSV
- D) `executemany` only

<details><summary>Reveal Answer</summary>**B.** Batched Core inserts.</details>

### Question 7 — Hard
**Why is Core insert faster than ORM add for bulk?**
- A) It is not
- B) No identity map, no unit-of-work tracking per object
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** No object overhead.</details>

### Question 8 — Hard
**When must you still use the ORM?**
- A) Never
- B) When relationships, cascades, and domain behavior ride along
- C) Always
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Object graph work.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You choose the right layer. |
| 5-6 | Review Core vs ORM and bulk. |
| < 5 | Re-read the lecture. |
