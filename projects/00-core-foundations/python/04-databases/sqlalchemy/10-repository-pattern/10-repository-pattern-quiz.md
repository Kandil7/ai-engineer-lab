# SQLAlchemy 10: Repository Pattern — Quiz

> **Topic Overview**: Domain rules out of the ORM, in-memory doubles, and unit of work.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a repository?**
- A) A migration
- B) An interface over persistence, hiding storage behind domain operations
- C) A session
- D) A model

<details><summary>Reveal Answer</summary>**B.** Storage abstraction.</details>

### Question 2 — Easy
**Why keep domain rules out of the ORM?**
- A) Speed
- B) Rules then work against any storage, including fakes
- C) Style
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Testable logic.</details>

### Question 3 — Medium
**What is the in-memory implementation for?**
- A) Production
- B) Fast, deterministic domain tests with no database
- C) Caching
- D) Migrations

<details><summary>Reveal Answer</summary>**B.** Fake storage.</details>

### Question 4 — Medium
**What is the unit of work?**
- A) A query
- B) The object committing a set of repository changes atomically
- C) A session
- D) A migration

<details><summary>Reveal Answer</summary>**B.** Atomic commit boundary.</details>

### Question 5 — Medium
**Where does the service layer sit?**
- A) In the ORM
- B) Above repositories, orchestrating domain operations inside one unit of work
- C) In the router
- D) In the migration

<details><summary>Reveal Answer</summary>**B.** Orchestration.</details>

### Question 6 — Hard
**What does "swap storage, keep logic" prove?**
- A) Speed
- B) Domain tests pass unchanged against SQL and in-memory stores
- C) Caching
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Storage independence.</details>

### Question 7 — Hard
**When is a repository overkill?**
- A) Never
- B) For thin CRUD with no domain rules, a direct query layer is simpler
- C) Always
- D) For tests

<details><summary>Reveal Answer</summary>**B.** Match the abstraction.</details>

### Question 8 — Hard
**Why inject the unit of work instead of importing it?**
- A) Style
- B) Tests substitute fakes and production substitutes sessions
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Seams for testing.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You structure persistence well. |
| 5-6 | Review repositories and unit of work. |
| < 5 | Re-read the lecture. |
