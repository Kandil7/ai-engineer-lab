# MongoDB 08: Limit and Skip — Quiz

> **Topic Overview**: Bounding reads, skip cost, and keyset pagination.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `limit(10)` do?**
- A) Skips 10
- B) Returns at most 10 documents
- C) Sorts 10
- D) Counts 10

<details><summary>Reveal Answer</summary>**B.** Result bound.</details>

### Question 2 — Easy
**What does `skip(20)` do?**
- A) Limits to 20
- B) Walks past the first 20 documents
- C) Sorts 20
- D) Deletes 20

<details><summary>Reveal Answer</summary>**B.** Offset walk.</details>

### Question 3 — Medium
**Why does deep skip cost grow?**
- A) It does not
- B) Every page rescans all skipped documents
- C) Locking
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Rescan cost.</details>

### Question 4 — Medium
**How does keyset pagination replace skip?**
- A) Bigger pages
- B) A ranged filter from the last seen `_id` plus `limit`
- C) Caching
- D) Sorting only

<details><summary>Reveal Answer</summary>**B.** Continue from a key.</details>

### Question 5 — Medium
**Why must keyset pages sort deterministically?**
- A) Style
- B) Ties and reorderings skip or repeat rows
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Stable continuation.</details>

### Question 6 — Hard
**When is skip acceptable?**
- A) Never
- B) Small, cold, administrative listings with capped page numbers
- C) Always
- D) For feeds

<details><summary>Reveal Answer</summary>**B.** Bounded convenience.</details>

### Question 7 — Hard
**What guard belongs on a skip endpoint?**
- A) None
- B) A max page/depth returning 400 beyond it
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Depth cap.</details>

### Question 8 — Hard
**Why is `limit` a safety device?**
- A) It is not
- B) Unbounded reads OOM; every consumer-facing read needs a bound
- C) Speed
- D) Style

<details><summary>Reveal Answer</summary>**B.** Bound every read.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You page safely. |
| 5-6 | Review skip cost and keyset. |
| < 5 | Re-read the lecture. |
