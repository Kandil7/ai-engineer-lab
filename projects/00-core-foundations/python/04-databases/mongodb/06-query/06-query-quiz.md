# MongoDB 06: Query Operators — Quiz

> **Topic Overview**: Comparison, logical, element, and regex operators.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you express a range on one field?**
- A) Two filters
- B) `{"age": {"$gte": 18, "$lt": 65}}`
- C) `$and`
- D) `$or`

<details><summary>Reveal Answer</summary>**B.** Operator nesting.</details>

### Question 2 — Easy
**When is explicit `$and` needed?**
- A) Always
- B) When the same field needs two same-key constraints that would collide
- C) Never
- D) For `$or`

<details><summary>Reveal Answer</summary>**B.** Key collision.</details>

### Question 3 — Medium
**How do you test "has a real value"?**
- A) `{"f": {"$ne": None}}`
- B) `{"f": {"$exists": True, "$ne": None}}`
- C) `{"f": True}`
- D) `$type`

<details><summary>Reveal Answer</summary>**B.** Presence plus value.</details>

### Question 4 — Medium
**Why is `$ne` expensive?**
- A) It is not
- B) "Everything but X" rarely uses an index well
- C) It locks
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Anti-selective.</details>

### Question 5 — Medium
**Which regex shape uses an index?**
- A) `.*foo`
- B) Anchored `^foo`
- C) Case-insensitive always
- D) None do

<details><summary>Reveal Answer</summary>**B.** Prefix serves the index.</details>

### Question 6 — Hard
**Why avoid `$where` JavaScript?**
- A) Slow to type
- B) Unindexed, slow, and a code-injection surface
- C) It errors
- D) It locks

<details><summary>Reveal Answer</summary>**B.** No place in app queries.</details>

### Question 7 — Hard
**What leads a compound filter?**
- A) Any order
- B) The selective, indexed predicate
- C) `$or` always
- D) `$ne` always

<details><summary>Reveal Answer</summary>**B.** Selective first.</details>

### Question 8 — Hard
**Why does `$ne: None` match missing fields?**
- A) A bug
- B) Missing is not equal to null, so the predicate passes
- C) It errors
- D) Indexes

<details><summary>Reveal Answer</summary>**B.** Missing passes `$ne`.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You filter precisely. |
| 5-6 | Review presence tests and index use. |
| < 5 | Re-read the lecture. |
