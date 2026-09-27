# PostgreSQL 02: Indexes and Queries — Quiz

> **Topic Overview**: B-tree, composite, GIN, and reading the query plan.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 10 |
| Correct Answers | 0 |
| Score | 0% |

---

## Questions

### Question 1 — Easy

**What does an index do?**

- A) Slows reads
- B) Maps values to rows
- C) Deletes rows
- D) Caches rows

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The index is the shortcut to the rows a query needs.

</details>

---

### Question 2 — Easy

**The default index type is:**

- A) GIN
- B) B-tree
- C) Hash
- D) Composite

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: B-tree is sorted, balanced, good for equality and range.

</details>

---

### Question 3 — Easy

**Indexes speed up:**

- A) Writes
- B) Reads
- C) Deletes
- D) Caches

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Reads speed up; writes slow down.

</details>

---

### Question 4 — Medium

**A composite index covers:**

- A) One column
- B) Multiple columns in order
- C) Only JSONB
- D) Only text

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The order must match the query pattern.

</details>

---

### Question 5 — Medium

**GIN serves:**

- A) Equality queries
- B) JSONB and full-text search
- C) Range queries
- D) Only integers

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: GIN indexes JSONB containment and tsvector search.

</details>

---

### Question 6 — Medium

**A sequential scan on a large table signals:**

- A) A good index
- B) A missing index
- C) A fast query
- D) A cache hit

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The database read every row.

</details>

---

### Question 7 — Medium

**EXPLAIN shows:**

- A) The data
- B) The query plan
- C) The cache
- D) The schema

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Index vs sequential scan, rows, and cost.

</details>

---

### Question 8 — Hard

**A query on the second column of a composite index:**

- A) Uses the index
- B) Cannot use the index
- C) Is cached
- D) Is faster

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The leading columns must match in order.

</details>

---

### Question 9 — Hard

**Indexing every column causes:**

- A) Faster writes
- B) Write slowdown
- C) Fewer reads
- D) Fewer indexes

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Every index must be maintained on write.

</details>

---

### Question 10 — Hard**

**For Arabic full-text search, the index must:**

- A) Use any config
- B) Use the same config as the query
- C) Be a B-tree
- D) Be cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A config mismatch makes the index unusable.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Hard |
| 9 | B | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for migrations |
| 7-8 | Proficient | Review composite order |
| 5-6 | Developing | Re-study EXPLAIN |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [01 - Schema Design](01-schema-design-quiz.md) | **Next**: [03 - Migrations](03-migrations-quiz.md)