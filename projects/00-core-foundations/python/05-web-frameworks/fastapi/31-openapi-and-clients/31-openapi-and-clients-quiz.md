# FastAPI 31: OpenAPI and Clients — Quiz

> **Topic Overview**: The schema as contract, tags, examples, and client generation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is OpenAPI?**
- A) A testing tool
- B) A machine-readable contract describing the API surface
- C) A proxy
- D) A database

<details><summary>Reveal Answer</summary>**B.** The schema contract.</details>

### Question 2 — Easy
**What do `tags` do?**
- A) Auth
- B) Group operations in the docs UI
- C) Cache
- D) Route

<details><summary>Reveal Answer</summary>**B.** Documentation grouping.</details>

### Question 3 — Medium
**Why set a stable `operation_id`?**
- A) Style
- B) Generated clients use it for method names, so churn breaks consumers
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Stable client codegen.</details>

### Question 4 — Medium
**Why add examples to the schema?**
- A) Style
- B) Concrete payloads make the contract usable and catch misunderstandings
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Ground the contract.</details>

### Question 5 — Medium
**How do security schemes appear in OpenAPI?**
- A) They do not
- B) As declared components clients and the docs UI honor
- C) In comments
- D) In headers only

<details><summary>Reveal Answer</summary>**B.** Auth in the contract.</details>

### Question 6 — Hard
**What is contract testing?**
- A) Unit testing
- B) Verifying responses actually match the published schema
- C) Load testing
- D) Fuzzing

<details><summary>Reveal Answer</summary>**B.** Schema conformance.</details>

### Question 7 — Hard
**Why does code drift invalidate generated clients?**
- A) It does not
- B) If the implementation changes without updating the schema, clients follow a lie
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Schema from code stays honest.</details>

### Question 8 — Hard
**When should you hand-write parts of the schema?**
- A) Always
- B) Rarely; prefer generated schema plus curated examples and descriptions
- C) Never
- D) For auth

<details><summary>Reveal Answer</summary>**B.** Generate, then annotate.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You publish honest contracts. |
| 5-6 | Review operation_id and contract testing. |
| < 5 | Re-read the lecture. |
