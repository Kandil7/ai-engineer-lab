# Qdrant 03: Hybrid Search — Quiz

> **Topic Overview**: Vector + keyword retrieval and the fusion.

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

**Hybrid search combines:**

- A) Two collections
- B) Vector and keyword search
- C) Two models
- D) Two caches

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Semantic and lexical signals fused.

</details>

---

### Question 2 — Easy

**Vector search captures:**

- A) Exact terms
- B) Meaning
- C) Payloads
- D) Point ids

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Semantic similarity, synonyms, paraphrases.

</details>

---

### Question 3 — Easy

**Keyword search captures:**

- A) Meaning
- B) Exact terms
- C) Vectors
- D) Scores

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Rare proper nouns and technical terms.

</details>

---

### Question 4 — Medium

**Fusion combines:**

- A) Two collections
- B) Two ranked lists into one
- C) Two models
- D) Two caches

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The point where the two signals meet.

</details>

---

### Question 5 — Medium

**RRF scores a result by:**

- A) Its vector size
- B) The reciprocal of its rank
- C) Its payload
- D) Its point id

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: 1/(60 + rank) summed across the lists.

</details>

---

### Question 6 — Medium

**A result ranked first in both lists:**

- A) Loses
- B) Wins the fusion
- C) Is cached
- D) Is deleted

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: It scores highest in both signals.

</details>

---

### Question 7 — Medium

**The hybrid weights are:**

- A) Guessed
- B) Tuned on the golden set
- C) Fixed
- D) Cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Evidence-based tuning.

</details>

---

### Question 8 — Hard

**A query with a rare proper noun benefits from:**

- A) Vector search
- B) Keyword search
- C) Neither
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Keyword catches exact terms embeddings dilute.

</details>

---

### Question 9 — Hard

**A query with paraphrased terms benefits from:**

- A) Keyword search
- B) Vector search
- C) Neither
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Vector captures meaning across wording.

</details>

---

### Question 10 — Hard**

**Hybrid is the default because it:**

- A) Is faster
- B) Rarely loses and often wins
- C) Is cached
- D) Is simpler

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Each retriever catches what the other misses.

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
| 9-10 | Expert | Ready for metadata filtering |
| 7-8 | Proficient | Review RRF |
| 5-6 | Developing | Re-study the fusion |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [02 - Vector Search](02-vector-search-quiz.md) | **Next**: [04 - Metadata Filtering](04-metadata-filtering-quiz.md)