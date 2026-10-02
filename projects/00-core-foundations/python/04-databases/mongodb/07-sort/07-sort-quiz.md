# MongoDB 07: Sort — Quiz

> **Topic Overview**: Direction, compound sorts, top-N, and index-backed order.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you sort descending?**
- A) `sort("age", "desc")`
- B) `sort("age", -1)`
- C) `rsort("age")`
- D) `order(-1)`

<details><summary>Reveal Answer</summary>**B.** `-1`.</details>

### Question 2 — Easy
**How do you sort by two fields?**
- A) Two sorts
- B) `sort([("age", 1), ("name", -1)])`
- C) One string
- D) You cannot

<details><summary>Reveal Answer</summary>**B.** Pair list.</details>

### Question 3 — Medium
**What is the leaderboard sort shape?**
- A) `(score, _id)`
- B) `(score DESC, _id ASC)`
- C) `(_id, score)`
- D) `(score)` only

<details><summary>Reveal Answer</summary>**B.** Score then tiebreaker.</details>

### Question 4 — Medium
**Why end sorts with `_id`?**
- A) Style
- B) Ties otherwise reorder across queries and pages
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Deterministic order.</details>

### Question 5 — Medium
**How do you get top-N efficiently?**
- A) Sort all, slice in Python
- B) Sort + `limit(N)` on a supporting index
- C) `skip`
- D) Aggregate only

<details><summary>Reveal Answer</summary>**B.** Index-backed top-N.</details>

### Question 6 — Hard
**What happens sorting past 32 MB without an index?**
- A) It spills automatically
- B) It fails; the sort must fit or be indexed
- C) It is slow but works
- D) It uses disk always

<details><summary>Reveal Answer</summary>**B.** Memory cap.</details>

### Question 7 — Hard
**How does `explain()` reveal an unindexed sort?**
- A) Timing
- B) A `SORT` stage instead of an index scan
- C) Row counts
- D) It does not

<details><summary>Reveal Answer</summary>**B.** Stage inspection.</details>

### Question 8 — Hard
**Why is `$natural` order not a contract?**
- A) It is
- B) Storage order changes with moves and deletes
- C) It is slow
- D) It locks

<details><summary>Reveal Answer</summary>**B.** No order guarantee.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You sort deterministically. |
| 5-6 | Review tiebreakers and indexes. |
| < 5 | Re-read the lecture. |
