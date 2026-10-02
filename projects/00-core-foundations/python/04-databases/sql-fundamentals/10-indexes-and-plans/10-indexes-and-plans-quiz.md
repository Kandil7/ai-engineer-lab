# SQL Fundamentals 10: Indexes and Plans — Quiz

> **Topic Overview**: Scans, B-trees, selectivity, composites, and write cost.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does an index speed up?**
- A) Writes
- B) Lookups and ordered access on the indexed columns
- C) Backups
- D) `SELECT *`

<details><summary>Reveal Answer</summary>**B.** Fast access paths.</details>

### Question 2 — Easy
**What is a sequential scan?**
- A) An index lookup
- B) Reading every row, the cost of having no usable index
- C) A plan
- D) A cache

<details><summary>Reveal Answer</summary>**B.** Full read.</details>

### Question 3 — Medium
**What is selectivity?**
- A) Column count
- B) The fraction of rows a predicate matches; low selectivity means the index may be skipped
- C) Index size
- D) Write speed

<details><summary>Reveal Answer</summary>**B.** Match fraction.</details>

### Question 4 — Medium
**Why does column order matter in a composite index?**
- A) Style
- B) The index serves leftmost-prefix predicates; a wrong order leaves it unused
- C) Speed only
- D) It does not

<details><summary>Reveal Answer</summary>**B.** Prefix rule.</details>

### Question 5 — Medium
**What does every index cost on write?**
- A) Nothing
- B) Each `INSERT`/`UPDATE`/`DELETE` must maintain every index
- C) Reads
- D) Plans

<details><summary>Reveal Answer</summary>**B.** Write tax.</details>

### Question 6 — Hard
**What is a covering index?**
- A) A big index
- B) An index containing all columns the query needs, so the table is never read
- C) A primary key
- D) A partial index

<details><summary>Reveal Answer</summary>**B.** Index-only scan.</details>

### Question 7 — Hard
**How do you prove an index helped?**
- A) The query is fast
- B) `EXPLAIN` shows the index scan and the measured cost/rows drop
- C) Trust
- D) Row counts

<details><summary>Reveal Answer</summary>**B.** Read the plan.</details>

### Question 8 — Hard
**Why can an unused index be worse than none?**
- A) It cannot
- B) It taxes every write while helping no read
- C) It uses cache
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Pure cost.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You index with evidence. |
| 5-6 | Review selectivity and covering indexes. |
| < 5 | Re-read the lecture. |
