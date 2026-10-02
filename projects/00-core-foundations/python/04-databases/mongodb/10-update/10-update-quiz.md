# MongoDB 10: Update — Quiz

> **Topic Overview**: Operators, atomic counters, and upserts.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is wrong with a bare update document?**
- A) Nothing
- B) It replaces the whole document instead of mutating fields
- C) It is slow
- D) It errors

<details><summary>Reveal Answer</summary>**B.** Replacement, not patch.</details>

### Question 2 — Easy
**What does `$inc` guarantee?**
- A) Speed
- B) Atomic increments safe under concurrency
- C) Sorting
- D) Uniqueness

<details><summary>Reveal Answer</summary>**B.** Race-free counters.</details>

### Question 3 — Medium
**`matched_count` vs `modified_count`?**
- A) Same
- B) Matched found; modified changed — equal values already held differ
- C) Modified is bigger
- D) Matched is bigger always

<details><summary>Reveal Answer</summary>**B.** Found vs changed.</details>

### Question 4 — Medium
**What is an upsert?**
- A) An update only
- B) Update if matched, insert if not
- C) An insert only
- D) A delete

<details><summary>Reveal Answer</summary>**B.** Insert-or-update.</details>

### Question 5 — Medium
**What is `$setOnInsert` for?**
- A) Every write
- B) Creation-only fields in an upsert (created-at vs last-seen)
- C) Sorting
- D) Indexing

<details><summary>Reveal Answer</summary>**B.** Create vs update fields.</details>

### Question 6 — Hard
**Why is read-modify-write wrong for counters?**
- A) Slow
- B) Concurrent readers compute from the same stale value; one increment is lost
- C) Complex
- D) Unindexed

<details><summary>Reveal Answer</summary>**B.** Lost updates.</details>

### Question 7 — Hard
**How does an upsert make retries safe?**
- A) It does not
- B) Re-running with the same filter converges instead of duplicating
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Idempotent writes.</details>

### Question 8 — Hard
**What must you preview before `update_many`?**
- A) Nothing
- B) The filter as a `find`, or the rewrite hits the wrong documents
- C) The operators
- D) The index

<details><summary>Reveal Answer</summary>**B.** Filter first.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You update safely. |
| 5-6 | Review operators and upserts. |
| < 5 | Re-read the lecture. |
