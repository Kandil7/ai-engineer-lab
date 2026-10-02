# MongoDB 09: Delete — Quiz

> **Topic Overview**: Targeted deletes, `deleted_count`, and soft deletes.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `delete_many({})` do?**
- A) Nothing
- B) Removes every document, keeping the collection
- C) Drops the collection
- D) Errors

<details><summary>Reveal Answer</summary>**B.** Empty the collection.</details>

### Question 2 — Easy
**How do you preview a delete?**
- A) You cannot
- B) Run the filter as `find`/`count_documents` first
- C) `EXPLAIN`
- D) `limit(0)`

<details><summary>Reveal Answer</summary>**B.** See the victims.</details>

### Question 3 — Medium
**What does `deleted_count` prove?**
- A) Nothing
- B) How many documents actually went away
- C) The filter
- D) The time

<details><summary>Reveal Answer</summary>**B.** Verified outcome.</details>

### Question 4 — Medium
**Why delete by `_id` for precision?**
- A) Speed
- B) Non-unique filters remove an arbitrary first match
- C) Style
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Exact targeting.</details>

### Question 5 — Medium
**What is a soft delete?**
- A) Slow delete
- B) Flagging inactive instead of removing
- C) A backup
- D) A transaction

<details><summary>Reveal Answer</summary>**B.** Hide, keep history.</details>

### Question 6 — Hard
**What does soft delete cost?**
- A) Nothing
- B) Perpetual filtering plus complicated uniqueness
- C) Speed only
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Permanent tax.</details>

### Question 7 — Hard
**What guard belongs around `{}` in tooling?**
- A) None
- B) A lint or confirm refusing bare-filter deletes
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Ban the footgun.</details>

### Question 8 — Hard
**When is hard delete required over soft?**
- A) Never
- B) True erasure (privacy deletion) where retention is the violation
- C) Always
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Erasure means gone.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You delete safely. |
| 5-6 | Review preview and counts. |
| < 5 | Re-read the lecture. |
