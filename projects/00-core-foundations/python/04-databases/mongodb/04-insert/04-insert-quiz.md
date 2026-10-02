# MongoDB 04: Insert — Quiz

> **Topic Overview**: Bulk writes, `_id` strategy, and write errors.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `insert_one` return?**
- A) The document
- B) A result carrying `inserted_id`
- C) Nothing
- D) A cursor

<details><summary>Reveal Answer</summary>**B.** Generated id.</details>

### Question 2 — Easy
**Why use `insert_many`?**
- A) Style
- B) One round-trip for the batch
- C) Validation
- D) Indexing

<details><summary>Reveal Answer</summary>**B.** Batched writes.</details>

### Question 3 — Medium
**Ordered vs unordered bulk?**
- A) Same
- B) Ordered aborts at first failure; unordered continues and reports
- C) Unordered is slower
- D) Ordered skips errors

<details><summary>Reveal Answer</summary>**B.** Failure semantics.</details>

### Question 4 — Medium
**When should you supply `_id`?**
- A) Never
- B) When the id is meaningful or retries must be idempotent
- C) Always
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Meaningful or idempotent ids.</details>

### Question 5 — Medium
**What does `DuplicateKeyError` on retry mean?**
- A) Failure
- B) Already done — treat as success
- C) Corruption
- D) Retry again

<details><summary>Reveal Answer</summary>**B.** Idempotent signal.</details>

### Question 6 — Hard
**Why is majority write concern needed for critical writes?**
- A) Speed
- B) So acknowledged data survives a primary failover
- C) Style
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Durability guarantee.</details>

### Question 7 — Hard
**What must a bulk import handle per result?**
- A) Nothing
- B) Partial success: inserted ids plus the error list
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Partial outcomes.</details>

### Question 8 — Hard
**Why validate before the batch?**
- A) Style
- B) Failures mid-batch leave partial state to reconcile
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Pre-validate bulk.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You write safely in bulk. |
| 5-6 | Review ordering and idempotency. |
| < 5 | Re-read the lecture. |
