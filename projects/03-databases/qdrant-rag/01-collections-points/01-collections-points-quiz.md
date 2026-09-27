# Qdrant 01: Collections and Points — Quiz

> **Topic Overview**: The collection, the point, and the payload.

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

**What is a collection?**

- A) A cache
- B) A named set of points with a fixed vector size
- C) A query
- D) A connection

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The vector size is fixed at creation.

</details>

---

### Question 2 — Easy

**What is a point?**

- A) A vector plus its payload
- B) A cache entry
- C) A query
- D) A connection

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: The vector is the embedding; the payload is the metadata.

</details>

---

### Question 3 — Easy

**What is the payload?**

- A) The vector
- B) The filterable metadata
- C) The point id
- D) The collection

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Book, page, language — what makes retrieval filterable.

</details>

---

### Question 4 — Medium

**The vector size must match:**

- A) The collection name
- B) The embedding model
- C) The payload
- D) The point id

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Every vector in the collection has the same dimensionality.

</details>

---

### Question 5 — Medium

**The distance metric decides:**

- A) The vector size
- B) How similarity is measured
- C) The payload
- D) The point id

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Cosine, dot, or euclidean.

</details>

---

### Question 6 — Medium

**The point id is:**

- A) Random
- B) Deterministic from the source
- C) The payload
- D) The vector

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Re-ingestion updates the same point instead of duplicating.

</details>

---

### Question 7 — Medium

**The point id is the target of:**

- A) The cache
- B) Citations
- C) The collection
- D) The metric

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The evidence id the answer cites.

</details>

---

### Question 8 — Hard

**The payload schema is designed:**

- A) After ingestion
- B) Before ingestion
- C) Never
- D) During search

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Which fields are filters, display, and provenance.

</details>

---

### Question 9 — Hard

**Random point ids cause:**

- A) Faster search
- B) Duplicates on re-ingestion
- C) Smaller payloads
- D) Fewer points

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The same source becomes multiple points.

</details>

---

### Question 10 — Hard**

**Updates and deletes are idempotent because:**

- A) They are cached
- B) The same id gives the same result
- C) They are fast
- D) They are optional

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The id is the identity.

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
| 9-10 | Expert | Ready for vector search |
| 7-8 | Proficient | Review the payload |
| 5-6 | Developing | Re-study point ids |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [02 - Vector Search](02-vector-search-quiz.md)