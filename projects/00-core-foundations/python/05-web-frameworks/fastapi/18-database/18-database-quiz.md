# FastAPI 18: Database — Quiz

> **Topic Overview**: DB connections, sessions, and lifecycle.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Where should a DB engine/pool be created?**
- A) Per request
- B) Once at startup, shared across requests
- C) Per route
- D) In each model

<details><summary>Reveal Answer</summary>**B.** Pool once, reuse.</details>

### Question 2 — Easy
**What is a session for?**
- A) Auth
- B) A unit of work (transaction) against the database
- C) Caching
- D) Templating

<details><summary>Reveal Answer</summary>**B.** Transaction scope.</details>

### Question 3 — Medium
**How is a session usually provided to handlers?**
- A) Globally
- B) As a dependency that yields a session and closes it after the request
- C) In a header
- D) In the body

<details><summary>Reveal Answer</summary>**B.** DI-managed lifetime.</details>

### Question 4 — Medium
**Why must connections be returned to the pool?**
- A) Style
- B) Leaks exhaust the pool and block all DB access
- C) For speed
- D) For caching

<details><summary>Reveal Answer</summary>**B.** Pool exhaustion.</details>

### Question 5 — Medium
**What does a transaction protect?**
- A) Speed
- B) Atomicity of multiple writes
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** All-or-nothing.</details>

### Question 6 — Hard
**Why is a leaked session worse than a slow query?**
- A) It is not
- B) A slow query eventually returns; a leaked connection permanently removes capacity
- C) For speed
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Permanent capacity loss.</details>

### Question 7 — Hard
**What is the pool-sizing guidance?**
- A) As large as possible
- B) Bound by the database's capacity and worker count; too large can overwhelm the DB
- C) Always 100
- D) 1

<details><summary>Reveal Answer</summary>**B.** Match DB capacity.</details>

### Question 8 — Hard
**Why avoid doing blocking DB calls in async handlers?**
- A) Style
- B) They block the event loop; use an async driver or a threadpool
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Keep the loop free.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You wire the database well. |
| 5-6 | Review sessions and pooling. |
| < 5 | Re-read the lecture. |
