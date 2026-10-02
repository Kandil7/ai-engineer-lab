# PostgreSQL 06: Connection Pooling — Quiz

> **Topic Overview**: Why pool, sizing, pgbouncer, and leak detection.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why pool connections?**
- A) Speed of queries
- B) Opening a connection is expensive; reuse amortizes it and caps concurrency
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Reuse plus a ceiling.</details>

### Question 2 — Easy
**What happens without a pool under load?**
- A) Nothing
- B) Connection storms exhaust `max_connections` and new work fails
- C) Faster queries
- D) Better caching

<details><summary>Reveal Answer</summary>**B.** Exhaustion.</details>

### Question 3 — Medium
**How do you size a pool?**
- A) As large as possible
- B) From worker count × concurrency, bounded by what the database can serve
- C) Always 100
- D) Always 1

<details><summary>Reveal Answer</summary>**B.** Both sides of the pipe.</details>

### Question 4 — Medium
**What is pgbouncer for?**
- A) Query cache
- B) An external pooler multiplexing many clients onto few server connections
- C) Backups
- D) Migrations

<details><summary>Reveal Answer</summary>**B.** Connection multiplexing.</details>

### Question 5 — Medium
**What breaks in transaction pooling mode?**
- A) Nothing
- B) Session-level features (prepared statements, temp tables, advisory locks) do not survive
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Mode limits.</details>

### Question 6 — Hard
**How do you detect a leak?**
- A) Guess
- B) Pool checkout counts and `pg_stat_activity` idle-in-transaction growth
- C) Logs only
- D) Restarts

<details><summary>Reveal Answer</summary>**B.** Measure the pool.</details>

### Question 7 — Hard
**Why are idle-in-transaction connections dangerous?**
- A) They are harmless
- B) They hold locks and pin snapshots, blocking vacuum and others
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Held resources.</details>

### Question 8 — Hard
**Why set a checkout timeout?**
- A) Speed
- B) A stuck pool should fail fast with a clear error, not queue forever
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Fail fast.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You size and watch pools. |
| 5-6 | Review sizing and pgbouncer modes. |
| < 5 | Re-read the lecture. |
