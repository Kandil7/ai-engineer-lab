# MongoDB 03: Collections — Quiz

> **Topic Overview**: Creation, capped collections, and shape discipline.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What creates a collection?**
- A) `CREATE TABLE`
- B) First insert, or explicit `create_collection`
- C) A migration
- D) An index

<details><summary>Reveal Answer</summary>**B.** Lazy or explicit.</details>

### Question 2 — Easy
**When must creation be explicit?**
- A) Always
- B) When options like capped or validation rules are needed
- C) Never
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Options require it.</details>

### Question 3 — Medium
**What is a capped collection?**
- A) Indexed
- B) Fixed-size, insertion-ordered, self-evicting
- C) Encrypted
- D) Replicated

<details><summary>Reveal Answer</summary>**B.** Bounded log.</details>

### Question 4 — Medium
**What can capped collections not do?**
- A) Insert
- B) Grow documents on update or shard by default
- C) Delete
- D) Query

<details><summary>Reveal Answer</summary>**B.** Fixed allocation.</details>

### Question 5 — Medium
**How do you list collections?**
- A) `SHOW TABLES`
- B) `db.list_collection_names()`
- C) `find()`
- D) `ls`

<details><summary>Reveal Answer</summary>**B.** List call.</details>

### Question 6 — Hard
**Where does shape discipline live?**
- A) Nowhere
- B) In `$jsonSchema` validation rules once shapes stabilize
- C) In indexes
- D) In the driver

<details><summary>Reveal Answer</summary>**B.** Opt-in validation.</details>

### Question 7 — Hard
**Why is dropping a collection a migration, not a query?**
- A) It is fast
- B) It is final and affects all readers; review and back up first
- C) It locks
- D) It is slow

<details><summary>Reveal Answer</summary>**B.** Reviewed removal.</details>

### Question 8 — Hard
**Collection vs table: the core difference?**
- A) Speed
- B) No enforced schema per row; shape by convention plus validation
- C) Size
- D) Indexes

<details><summary>Reveal Answer</summary>**B.** Flexible membership.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You manage collections well. |
| 5-6 | Review capped and validation. |
| < 5 | Re-read the lecture. |
