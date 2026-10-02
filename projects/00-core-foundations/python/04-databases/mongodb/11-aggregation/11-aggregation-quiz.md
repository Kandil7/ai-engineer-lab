# MongoDB 11: Aggregation — Quiz

> **Topic Overview**: Stages, accumulators, ordering, and `$lookup`.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a pipeline?**
- A) An index
- B) Ordered stages where each stage's output feeds the next
- C) A single query
- D) A transaction

<details><summary>Reveal Answer</summary>**B.** Stream of stages.</details>

### Question 2 — Easy
**Why does `$match` go first?**
- A) Style
- B) Early filtering shrinks the stream and can use indexes
- C) Speed of typing
- D) It is required

<details><summary>Reveal Answer</summary>**B.** Filter early.</details>

### Question 3 — Medium
**What does `_id` mean inside `$group`?**
- A) Document id
- B) The group key
- C) An index
- D) A counter

<details><summary>Reveal Answer</summary>**B.** Grouping key.</details>

### Question 4 — Medium
**Name three accumulators.**
- A) `$match/$sort/$limit`
- B) `$sum/$avg/$push` (also `$min/$max`)
- C) `$and/$or/$not`
- D) `$gt/$lt/$eq`

<details><summary>Reveal Answer</summary>**B.** Aggregation functions.</details>

### Question 5 — Medium
**What does `$project` do?**
- A) Filters rows
- B) Shapes output fields and computes derived values
- C) Groups
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Output shaping.</details>

### Question 6 — Hard
**What breaks with unbounded `$push`?**
- A) Nothing
- B) Group documents can exceed the 16 MB limit
- C) Speed
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Size cap.</details>

### Question 7 — Hard
**When is `$lookup` appropriate?**
- A) Always
- B) For genuinely separate entities; read-hot relations should be embedded
- C) Never
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Join escape hatch.</details>

### Question 8 — Hard
**How do you group an entire collection into one result?**
- A) Omit `$group`
- B) Group by a constant (`_id: None`)
- C) `$match` all
- D) `$sort` all

<details><summary>Reveal Answer</summary>**B.** Constant key.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You pipeline well. |
| 5-6 | Review stages and ordering. |
| < 5 | Re-read the lecture. |
