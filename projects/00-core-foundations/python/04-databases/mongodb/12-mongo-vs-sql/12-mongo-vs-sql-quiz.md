# MongoDB 12: Mongo vs SQL — Quiz

> **Topic Overview**: Embedding vs referencing, flexibility costs, and model choice.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**When do you embed?**
- A) Always
- B) For data read together as a whole, rarely queried alone
- C) Never
- D) For huge lists

<details><summary>Reveal Answer</summary>**B.** Co-read data.</details>

### Question 2 — Easy
**When do you reference?**
- A) Always
- B) For shared, large, or independently queried entities
- C) Never
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Separate lifecycles.</details>

### Question 3 — Medium
**What does referencing cost at read time?**
- A) Nothing
- B) N+1 reads or `$lookup` joins to reassemble
- C) Storage
- D) Indexes

<details><summary>Reveal Answer</summary>**B.** Assembly cost.</details>

### Question 4 — Medium
**What does embedding cost at write time?**
- A) Nothing
- B) Duplicated data must be updated everywhere
- C) Storage only
- D) Indexes

<details><summary>Reveal Answer</summary>**B.** Update fan-out.</details>

### Question 5 — Medium
**What does schema flexibility cost?**
- A) Nothing
- B) Application-owned validation and migration of mixed shapes
- C) Speed
- D) Storage

<details><summary>Reveal Answer</summary>**B.** Discipline moves to code.</details>

### Question 6 — Hard
**When is MongoDB the wrong choice?**
- A) Never
- B) For heavily relational data needing joins and cross-entity integrity
- C) For logs
- D) For catalogs

<details><summary>Reveal Answer</summary>**B.** Relations need relational stores.</details>

### Question 7 — Hard
**What is the document transaction boundary?**
- A) The collection
- B) A single document write is atomic
- C) The database
- D) Nothing is atomic

<details><summary>Reveal Answer</summary>**B.** Document-level atomicity.</details>

### Question 8 — Hard
**How do you decide: embed or reference?**
- A) Always embed
- B) By access pattern: read-together embeds, shared/growing references
- C) Always reference
- D) By size only

<details><summary>Reveal Answer</summary>**B.** Access-driven modeling.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You choose models deliberately. |
| 5-6 | Review embedding vs referencing. |
| < 5 | Re-read the lecture. |
