# MongoDB 01: Getting Started — Quiz

> **Topic Overview**: The document model, PyMongo, and `ObjectId`.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What are MongoDB's three data levels?**
- A) Tables, rows, columns
- B) Databases, collections, documents
- C) Files, tables, rows
- D) Keys, values, indexes

<details><summary>Reveal Answer</summary>**B.** Database → collection → document.</details>

### Question 2 — Easy
**How do you connect with PyMongo?**
- A) `connect()`
- B) `MongoClient(uri)` once per process
- C) `open()`
- D) `Client()`

<details><summary>Reveal Answer</summary>**B.** One pooled client.</details>

### Question 3 — Medium
**What is `_id`?**
- A) An index
- B) The mandatory unique document key, auto-generated as `ObjectId`
- C) A timestamp
- D) A foreign key

<details><summary>Reveal Answer</summary>**B.** Unique identity.</details>

### Question 4 — Medium
**Why is `ObjectId` not JSON serializable directly?**
- A) It is too big
- B) `json` knows only basic types; use `bson.json_util`
- C) It is encrypted
- D) It is binary only

<details><summary>Reveal Answer</summary>**B.** Serialize at the boundary.</details>

### Question 5 — Medium
**Why prefer `client["db"]["coll"]` over attribute access?**
- A) Speed
- B) Explicit, greppable, and safe for names that are not identifiers
- C) Caching
- D) Style only

<details><summary>Reveal Answer</summary>**B.** Explicit references.</details>

### Question 6 — Hard
**When is a document database the wrong choice?**
- A) Never
- B) For heavily relational data with cross-entity integrity needs
- C) For logs
- D) For catalogs

<details><summary>Reveal Answer</summary>**B.** Relations belong in relational stores.</details>

### Question 7 — Hard
**Why does `MongoClient` connect lazily matter?**
- A) It does not
- B) Constructor success proves nothing; ping at startup to fail fast
- C) Speed
- D) Pooling

<details><summary>Reveal Answer</summary>**B.** Verify connectivity.</details>

### Question 8 — Hard
**What does flexible schema demand in return?**
- A) Nothing
- B) Application-level validation once shapes stabilize
- C) More indexes
- D) Bigger documents

<details><summary>Reveal Answer</summary>**B.** Discipline replaces DDL.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You start with MongoDB correctly. |
| 5-6 | Review the document model and client. |
| < 5 | Re-read the lecture. |
