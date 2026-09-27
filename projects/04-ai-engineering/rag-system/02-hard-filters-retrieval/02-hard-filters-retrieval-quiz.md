# RAG System 02: Hard Filters and Retrieval — Quiz

> **Topic Overview**: Filter types, pre- vs post-filtering, and tenant
> isolation.

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

**What is a hard filter?**

- A) A slow query
- B) A predicate constraining retrieval before ranking
- C) A database index
- D) A cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Hard filters constrain which chunks can be retrieved.

</details>

---

### Question 2 — Easy

**What decides pre- vs post-filtering?**

- A) The model
- B) Selectivity
- C) The database
- D) The query length

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Low selectivity (few eligible rows) favors pre-filtering.

</details>

---

### Question 3 — Easy

**What is tenant isolation?**

- A) A performance optimization
- B) A mandatory per-tenant filter, never optional
- C) A cache
- D) A model choice

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Isolation is a correctness guarantee — a leak is a security incident.

</details>

---

### Question 4 — Medium

**What is the risk of post-filtering?**

- A) It is slow
- B) It wastes vector work and can return fewer than k results
- C) It leaks
- D) It duplicates

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Post-filtering ranks everything then discards — wasted work, broken k guarantee.

</details>

---

### Question 5 — Medium

**When is pre-filtering correct?**

- A) Always
- B) At low selectivity, with index support
- C) Never
- D) At high selectivity

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Pre-filtering searches only the eligible subset — right when that subset is small.

</details>

---

### Question 6 — Medium

**What is a hybrid leak?**

- A) A slow query
- B) One retrieval arm ignoring the filter
- C) A duplicate
- D) A cache miss

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: If one arm ignores the filter, the fused result crosses the boundary.

</details>

---

### Question 7 — Medium

**When is a payload attribute designed?**

- A) At query time
- B) At ingest time
- C) At runtime
- D) Never

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A filterable attribute missing from the payload is a re-ingest, not a query fix.

</details>

---

### Question 8 — Hard

**The roadmap's "no leakage between permissions" exit test is:**

- A) A performance test
- B) Asserting no result crosses the tenant boundary
- C) A load test
- D) A model test

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The test asserts every result belongs to the caller's tenant.

</details>

---

### Question 9 — Hard

**Where is the tenant filter enforced?**

- A) In the UI
- B) Below the API layer, mandatory
- C) In the model
- D) In the cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Isolation is enforced at the retrieval boundary, never optional.

</details>

---

### Question 10 — Hard**

**OWASP treats tenant isolation as:**

- A) An audit finding
- B) An ingestion-and-retrieval control
- C) A model concern
- D) A UI concern

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Isolation is designed into ingestion and retrieval, not discovered in audits.

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
| 9-10 | Expert | Ready for reranking |
| 7-8 | Proficient | Review selectivity |
| 5-6 | Developing | Re-study isolation |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [01 - Chunking](01-chunking-by-structure-quiz.md) | **Next**: [03 - Reranking](03-reranking-quiz.md)