# Embeddings 04: Quality Evaluation — Quiz

> **Topic Overview**: Golden pairs, similarity, and consistency.

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

**Golden pairs are:**

- A) Random text pairs
- B) Hand-verified pairs with expected similarity
- C) Cached pairs
- D) Sorted pairs

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Positive and negative pairs.

</details>

---

### Question 2 — Easy

**A positive pair is:**

- A) Different concepts
- B) Same concept, different wording
- C) Identical text
- D) A cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Should embed close.

</details>

---

### Question 3 — Easy

**A negative pair is:**

- A) Same concept
- B) Different concepts, similar wording
- C) Identical text
- D) A cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The control that proves separation.

</details>

---

### Question 4 — Medium

**The similarity is measured with:**

- A) Euclidean distance
- B) Cosine similarity
- C) A hash
- D) A sort

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Compared to the expected value.

</details>

---

### Question 5 — Medium

**Retrieval accuracy is:**

- A) A similarity check
- B) The end-to-end test
- C) A cache test
- D) A sort test

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Embeddings plus search.

</details>

---

### Question 6 — Medium

**Consistency means:**

- A) Different texts, same vector
- B) Same text, same vector
- C) Same text, different vectors
- D) A cache hit

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Nondeterminism breaks the cache.

</details>

---

### Question 7 — Medium

**A positive pair scoring below its target signals:**

- A) A fast model
- B) A weak model
- C) A cache miss
- D) A sort

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The model does not capture the relation.

</details>

---

### Question 8 — Hard

**The metrics run on:**

- A) Nothing
- B) Every embedding change
- C) Every query
- D) Every day

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A model swap or normalization change.

</details>

---

### Question 9 — Hard

**A drop in retrieval accuracy is:**

- A) An improvement
- B) A regression
- C) A cache win
- D) Neutral

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The gate catches it.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for consistency is:**

- A) 50%
- B) 100%
- C) 0%
- D) Optional

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Same text, same vector, always.

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
| 9-10 | Expert | Embeddings section complete |
| 7-8 | Proficient | Review the pairs |
| 5-6 | Developing | Re-study consistency |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [03 - Caching](03-caching-quiz.md)