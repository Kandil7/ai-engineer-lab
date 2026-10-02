# SQL Fundamentals 11: Transactions — Quiz

> **Topic Overview**: ACID, isolation levels, savepoints, and deadlocks.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does atomicity guarantee?**
- A) Speed
- B) All statements in the transaction commit, or none do
- C) Isolation
- D) Durability

<details><summary>Reveal Answer</summary>**B.** All-or-nothing.</details>

### Question 2 — Easy
**What does `ROLLBACK` do?**
- A) Commits
- B) Undoes the transaction's writes
- C) Saves
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Undo on failure.</details>

### Question 3 — Medium
**What is a savepoint?**
- A) A backup
- B) A marker allowing partial rollback to a point inside the transaction
- C) A commit
- D) A lock

<details><summary>Reveal Answer</summary>**B.** Sub-transaction bookmark.</details>

### Question 4 — Medium
**What do isolation levels trade?**
- A) Speed for storage
- B) Consistency anomalies against concurrency
- C) Nothing
- D) Reads for writes

<details><summary>Reveal Answer</summary>**B.** The consistency dial.</details>

### Question 5 — Medium
**What is a dirty read?**
- A) Reading committed data
- B) Seeing another transaction's uncommitted write
- C) A slow read
- D) A locked read

<details><summary>Reveal Answer</summary>**B.** Uncommitted visibility.</details>

### Question 6 — Hard
**What causes a deadlock?**
- A) Slow queries
- B) Two transactions each holding a lock the other wants
- C) Big tables
- D) Missing indexes

<details><summary>Reveal Answer</summary>**B.** Circular waiting.</details>

### Question 7 — Hard
**How do you design around deadlocks?**
- A) More locks
- B) Consistent lock ordering, short transactions, and retry on deadlock error
- C) Bigger hardware
- D) No transactions

<details><summary>Reveal Answer</summary>**B.** Order, brevity, retry.</details>

### Question 8 — Hard
**Why keep transactions short?**
- A) Style
- B) Long transactions hold locks, blocking others and raising deadlock risk
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Minimal lock time.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You transact safely. |
| 5-6 | Review isolation and deadlocks. |
| < 5 | Re-read the lecture. |
