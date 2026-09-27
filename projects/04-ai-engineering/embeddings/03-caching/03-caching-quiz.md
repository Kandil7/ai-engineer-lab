# Embeddings 03: Caching — Quiz

> **Topic Overview**: The cache key, cache-aside, and invalidation.

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

**The cache key carries:**

- A) Only the text
- B) The model and the content hash
- C) Only the model
- D) Only the hash

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A different model produces a different vector.

</details>

---

### Question 2 — Easy

**The content hash is of:**

- A) The raw text
- B) The normalized text
- C) The vector
- D) The model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Same text, same key.

</details>

---

### Question 3 — Easy

**L1 memory is:**

- A) Slow, persistent
- B) Fastest, lost on restart
- C) The vector store
- D) Redis

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Process memory.

</details>

---

### Question 4 — Medium

**L2 Redis:**

- A) Is lost on restart
- B) Survives restarts, TTL-bounded
- C) Is the vector store
- D) Is the fastest

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The middle layer.

</details>

---

### Question 5 — Medium

**L3 is:**

- A) Process memory
- B) The stored vector in the vector store
- C) Redis
- D) The cache key

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A stored point never needs re-embedding.

</details>

---

### Question 6 — Medium

**Cache-aside on a miss:**

- A) Returns nothing
- B) Embeds and stores
- C) Caches the key
- D) Deletes the key

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Then returns.

</details>

---

### Question 7 — Medium

**A model change invalidates because:**

- A) The cache is flushed
- B) The key carries the model
- C) The hash changes
- D) The text changes

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The old key naturally misses.

</details>

---

### Question 8 — Hard

**Hashing unnormalized text causes:**

- A) Fewer keys
- B) Same text, different keys
- C) Faster lookups
- D) A cache flush

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The same text misses the cache.

</details>

---

### Question 9 — Hard

**The hit rate is:**

- A) A cache setting
- B) The cost lever
- C) A model setting
- D) A hash

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A high rate means few API calls.

</details>

---

### Question 10 — Hard**

**A dropping hit rate signals:**

- A) A faster pipeline
- B) A changing corpus or broken key
- C) A cache flush
- D) A sort

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tracked per model and corpus.

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
| 9-10 | Expert | Ready for quality evaluation |
| 7-8 | Proficient | Review the layers |
| 5-6 | Developing | Re-study the key |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [02 - Batch Processing](02-batch-processing-quiz.md) | **Next**: [04 - Quality Evaluation](04-quality-evaluation-quiz.md)