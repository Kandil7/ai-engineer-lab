# Qdrant 04: Metadata Filtering — Quiz

> **Topic Overview**: Payload filters and tenant isolation.

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

**A filter selects points by:**

- A) Vector size
- B) Payload
- C) Point id
- D) Collection name

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Book, page, language — the payload fields.

</details>

---

### Question 2 — Easy

**must means:**

- A) Any condition holds
- B) All conditions must hold
- C) No conditions hold
- D) Conditions are cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The query's scope.

</details>

---

### Question 3 — Easy

**must_not means:**

- A) All conditions hold
- B) None of the conditions may hold
- C) Any condition holds
- D) Conditions are cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Excludes points.

</details>

---

### Question 4 — Medium

**Pre-filtering:**

- A) Scores all, drops after
- B) Narrows candidates before scoring
- C) Caches results
- D) Deletes points

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Faster on large collections.

</details>

---

### Question 5 — Medium

**Post-filtering:**

- A) Narrows before scoring
- B) Scores all, drops after
- C) Caches results
- D) Deletes points

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Can return fewer results with strict filters.

</details>

---

### Question 6 — Medium

**Tenant isolation is enforced by:**

- A) The cache
- B) A filter on every query
- C) The collection name
- D) The vector size

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The tenant filter is the correctness boundary.

</details>

---

### Question 7 — Medium

**A missing tenant filter is:**

- A) A cache miss
- B) A data leak
- C) A speed win
- D) An error

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Another tenant's data becomes visible.

</details>

---

### Question 8 — Hard

**A filter works only on fields:**

- A) In the cache
- B) In the payload schema
- C) In the vector
- D) In the point id

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: An unindexed field cannot be filtered.

</details>

---

### Question 9 — Hard

**Adding a filter field means:**

- A) Only a filter change
- B) Adding it to the schema and re-ingesting
- C) A cache change
- D) A vector change

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Filters and schema evolve together.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for filters is:**

- A) They are optional
- B) They match the payload schema
- C) They are cached
- D) They are guessed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Alignment with the schema.

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
| 9-10 | Expert | Qdrant section complete |
| 7-8 | Proficient | Review pre/post filtering |
| 5-6 | Developing | Re-study tenant isolation |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [03 - Hybrid Search](03-hybrid-search-quiz.md)