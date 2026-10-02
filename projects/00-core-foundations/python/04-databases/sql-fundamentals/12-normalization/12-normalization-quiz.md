# SQL Fundamentals 12: Normalization — Quiz

> **Topic Overview**: 1NF–3NF, denormalization, and key choice.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What problem does normalization solve?**
- A) Slow queries
- B) Update/insert/delete anomalies from redundant storage
- C) Missing indexes
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Redundancy anomalies.</details>

### Question 2 — Easy
**What does 1NF require?**
- A) A primary key
- B) Atomic cells: one value per cell, no repeating groups
- C) No partial dependencies
- D) No transitive dependencies

<details><summary>Reveal Answer</summary>**B.** Atomic values.</details>

### Question 3 — Medium
**What does 2NF remove?**
- A) Redundant rows
- B) Partial dependencies: non-key columns must depend on the whole key
- C) Transitive dependencies
- D) Duplicates

<details><summary>Reveal Answer</summary>**B.** Full-key dependence.</details>

### Question 4 — Medium
**What does 3NF remove?**
- A) Partial dependencies
- B) Transitive dependencies: non-key columns must depend only on the key
- C) Repeating groups
- D) Surrogate keys

<details><summary>Reveal Answer</summary>**B.** No chained dependence.</details>

### Question 5 — Medium
**When is denormalization correct?**
- A) Never
- B) Deliberately, for read-heavy paths where join cost exceeds staleness risk
- C) Always
- D) For writes

<details><summary>Reveal Answer</summary>**B.** Measured tradeoff.</details>

### Question 6 — Hard
**Surrogate vs natural keys?**
- A) Same
- B) Surrogates are stable system ids; naturals are meaningful but can change
- C) Naturals are always better
- D) Surrogates break joins

<details><summary>Reveal Answer</summary>**B.** Stability vs meaning.</details>

### Question 7 — Hard
**Why can over-normalization hurt reads?**
- A) It cannot
- B) Reassembling a view needs many joins, each a cost
- C) It locks
- D) It duplicates

<details><summary>Reveal Answer</summary>**B.** Join tax.</details>

### Question 8 — Hard
**How do normalized schemas reassemble a view?**
- A) Views only
- B) Joins along the foreign-key paths
- C) Denormalization
- D) CTEs only

<details><summary>Reveal Answer</summary>**B.** Joins rebuild.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You normalize deliberately. |
| 5-6 | Review 1NF–3NF and denormalization. |
| < 5 | Re-read the lecture. |
