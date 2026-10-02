# FastAPI 28: Pagination and Filtering — Quiz

> **Topic Overview**: Offset vs keyset, sorting, and the count trap.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is offset pagination?**
- A) Cursor-based
- B) `?limit=&offset=` into a result set
- C) A cache
- D) A sort

<details><summary>Reveal Answer</summary>**B.** Skip/take.</details>

### Question 2 — Easy
**What is keyset (cursor) pagination?**
- A) Offset-based
- B) Continue from the last seen key rather than a numeric offset
- C) A cache
- D) A sort

<details><summary>Reveal Answer</summary>**B.** Stable continuation.</details>

### Question 3 — Medium
**Why does offset break at scale?**
- A) It is slow to type
- B) Large offsets scan and discard rows, and concurrent writes shift the window
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Cost + instability.</details>

### Question 4 — Medium
**When is keyset pagination required?**
- A) Never
- B) For large, changing datasets where consistent pages matter
- C) Always
- D) For tiny tables

<details><summary>Reveal Answer</summary>**B.** Scale and correctness.</details>

### Question 5 — Medium
**Why does a total count cost more than a page?**
- A) It does not
- B) `COUNT(*)` over a large filtered set can be as expensive as the data scan
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** The total-count trap.</details>

### Question 6 — Hard
**What must a composite cursor encode?**
- A) Just the id
- B) All sort keys plus a tiebreaker, so pages do not skip or repeat
- C) The offset
- D) The user

<details><summary>Reveal Answer</summary>**B.** Stable ordering key.</details>

### Question 7 — Hard
**Why is an unbounded `limit` a resource risk?**
- A) It is not
- B) A client can request the whole table, exhausting memory and the DB
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Cap page size.</details>

### Question 8 — Hard
**Why prefer explicit filter parameters over an open query DSL?**
- A) Style
- B) Explicit params are safe, indexable, and documented; a DSL invites injection and unbounded queries
- C) Caching
- D) Speed

<details><summary>Reveal Answer</summary>**B.** Controlled surface.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You paginate correctly. |
| 5-6 | Review keyset and the count trap. |
| < 5 | Re-read the lecture. |
