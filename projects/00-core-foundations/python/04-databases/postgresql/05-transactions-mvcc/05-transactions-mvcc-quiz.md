# PostgreSQL 05: Transactions and MVCC — Quiz

> **Topic Overview**: ACID, isolation, and the multiversion engine.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does ACID stand for?**
- A) A cache
- B) Atomicity, Consistency, Isolation, Durability
- C) A join
- D) An index

<details><summary>Reveal Answer</summary>**B.** The transaction contract.</details>

### Question 2 — Easy
**What does MVCC let readers do?**
- A) Block writers
- B) Read a snapshot without blocking writers
- C) Skip indexes
- D) Bypass locks

<details><summary>Reveal Answer</summary>**B.** Non-blocking reads.</details>

### Question 3 — Medium
**What is the cost of MVCC?**
- A) None
- B) Dead row versions accumulate until vacuumed
- C) Slower reads
- D) No isolation

<details><summary>Reveal Answer</summary>**B.** Versions need vacuuming.</details>

### Question 4 — Medium
**What does `READ COMMITTED` see?**
- A) Everything
- B) A new snapshot per statement: rows committed before the statement began
- C) Uncommitted rows
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Per-statement snapshot.</details>

### Question 5 — Medium
**What does `REPEATABLE READ` add?**
- A) Nothing
- B) One snapshot for the whole transaction: repeatable results
- C) Serializable
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Stable view.</details>

### Question 6 — Hard
**Why do long transactions hurt in MVCC?**
- A) They do not
- B) They pin old snapshots, blocking vacuum and bloating the table
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Snapshot pinning.</details>

### Question 7 — Hard
**What causes a deadlock?**
- A) Slow queries
- B) Circular lock waiting between transactions
- C) Big tables
- D) Missing indexes

<details><summary>Reveal Answer</summary>**B.** Order locks consistently.</details>

### Question 8 — Hard
**Why retry on serialization failures?**
- A) They are bugs
- B) Higher isolation levels abort conflicting transactions by design; the app retries
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Expected aborts.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You transact correctly. |
| 5-6 | Review isolation and MVCC costs. |
| < 5 | Re-read the lecture. |
