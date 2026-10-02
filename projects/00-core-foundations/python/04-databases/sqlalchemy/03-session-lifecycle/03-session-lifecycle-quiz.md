# SQLAlchemy 03: Session Lifecycle — Quiz

> **Topic Overview**: Unit of work, identity map, flush/commit, and per-request sessions.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a session?**
- A) A connection
- B) A unit of work tracking changes to commit or roll back together
- C) A pool
- D) A migration

<details><summary>Reveal Answer</summary>**B.** Change tracker.</details>

### Question 2 — Easy
**What is the identity map?**
- A) A cache of queries
- B) The guarantee that one row maps to one object instance per session
- C) A pool
- D) An index

<details><summary>Reveal Answer</summary>**B.** Object identity.</details>

### Question 3 — Medium
**`flush` vs `commit`?**
- A) Same
- B) `flush` sends SQL within the transaction; `commit` flushes and ends it durably
- C) `commit` is faster
- D) `flush` commits

<details><summary>Reveal Answer</summary>**B.** Send vs finalize.</details>

### Question 4 — Medium
**What happens to instances after commit?**
- A) Nothing
- B) They expire by default and reload on next access (or detach)
- C) They delete
- D) They lock

<details><summary>Reveal Answer</summary>**B.** Expiry semantics.</details>

### Question 5 — Medium
**What is session-per-request?**
- A) One global session
- B) A DI dependency yielding a fresh session per request, closing after
- C) A pool
- D) A migration

<details><summary>Reveal Answer</summary>**B.** Request-scoped.</details>

### Question 6 — Hard
**Why roll back on failure?**
- A) Style
- B) A failed transaction poisons the session; only rollback restores it
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Poisoned session.</details>

### Question 7 — Hard
**What is a detached instance?**
- A) A deleted row
- B) An object no longer bound to a session; lazy loads fail on it
- C) A cached query
- D) A locked row

<details><summary>Reveal Answer</summary>**B.** Sessionless object.</details>

### Question 8 — Hard
**Why never share a session across requests?**
- A) Speed
- B) Identity map and transaction state leak between unrelated work
- C) Locking
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Cross-request contamination.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You manage sessions well. |
| 5-6 | Review flush/commit and expiry. |
| < 5 | Re-read the lecture. |
