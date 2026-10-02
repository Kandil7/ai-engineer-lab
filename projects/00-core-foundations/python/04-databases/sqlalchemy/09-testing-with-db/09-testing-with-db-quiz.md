# SQLAlchemy 09: Testing with a Database — Quiz

> **Topic Overview**: Rollback fixtures, factories, and SQLite divergence.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the rollback fixture?**
- A) A backup
- B) Each test runs in a transaction that rolls back, leaving the DB clean
- C) A migration
- D) A seed

<details><summary>Reveal Answer</summary>**B.** Transactional isolation.</details>

### Question 2 — Easy
**Why are factories better than fixtures-in-stone?**
- A) Speed
- B) Explicit defaults per test, no shared mutable rows
- C) Caching
- D) Style

<details><summary>Reveal Answer</summary>**B.** Fresh, explicit data.</details>

### Question 3 — Medium
**When do you need a schema reset?**
- A) Never
- B) When tests change DDL or sequences, so state cannot roll back
- C) Always
- D) For speed

<details><summary>Reveal Answer</summary>**B.** DDL escapes transactions.</details>

### Question 4 — Medium
**What is a SQLite divergence trap?**
- A) Speed
- B) Behavior valid in SQLite but not Postgres (or vice versa), passing locally and failing in CI
- C) Locking
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Dialect differences.</details>

### Question 5 — Medium
**What do Testcontainers buy?**
- A) Speed
- B) Real Postgres per test run for full fidelity
- C) Mocks
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Production-like tests.</details>

### Question 6 — Hard
**Why is test speed vs fidelity a real tradeoff?**
- A) It is not
- B) SQLite is fast but divergent; containers are faithful but slow to boot
- C) Both are fast
- D) Both are slow

<details><summary>Reveal Answer</summary>**B.** Tier your tests.</details>

### Question 7 — Hard
**How do you prove test isolation?**
- A) Trust
- B) Run tests in random order and in parallel; order-dependence is a bug
- C) Logs
- D) Speed

<details><summary>Reveal Answer</summary>**B.** Order independence.</details>

### Question 8 — Hard
**What must never leak between tests?**
- A) Nothing
- B) Rows, sequences, and schema changes
- C) Mocks
- D) Imports

<details><summary>Reveal Answer</summary>**B.** Full isolation.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You test databases well. |
| 5-6 | Review fixtures and divergence. |
| < 5 | Re-read the lecture. |
