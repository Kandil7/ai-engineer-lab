# Embeddings 02: Batch Processing — Quiz

> **Topic Overview**: Batching, rate limits, and retries.

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

**A batch of 100 texts is:**

- A) 100 calls
- B) One call
- C) 10 calls
- D) A cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The throughput multiplies.

</details>

---

### Question 2 — Easy

**A 429 means:**

- A) Success
- B) Rate limit exceeded
- C) A cache miss
- D) A sort

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The batch must be retried.

</details>

---

### Question 3 — Easy

**Exponential backoff:**

- A) Retries instantly
- B) Waits, retries, doubles the wait
- C) Never retries
- D) Caches

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Bounded retries, then fail loudly.

</details>

---

### Question 4 — Medium

**The per-item loop is:**

- A) The best practice
- B) The anti-pattern
- C) Required
- D) Cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: One call per text multiplies latency.

</details>

---

### Question 5 — Medium

**Retrying without backoff:**

- A) Is faster
- B) Hammers the API
- C) Is required
- D) Caches

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The retries collide with the limit.

</details>

---

### Question 6 — Medium

**Async processing:**

- A) Blocks ingestion
- B) Runs embedding in the background
- C) Is slower
- D) Is cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The pipeline does not block.

</details>

---

### Question 7 — Medium

**A dropping throughput signals:**

- A) A faster pipeline
- B) A rate-limit or network problem
- C) A cache hit
- D) A sort

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The metrics make it visible.

</details>

---

### Question 8 — Hard

**The retry is bounded to:**

- A) Infinite attempts
- B) A fixed number, then fail loudly
- C) One attempt
- D) Zero attempts

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A persistent failure is not hidden.

</details>

---

### Question 9 — Hard

**The batch size is tuned to:**

- A) The corpus
- B) The API's limit
- C) The cache
- D) The query

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The API's per-request bound.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for embedding is:**

- A) Per-item loops
- B) Texts are embedded in batches
- C) No embedding
- D) Cached embedding

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Batching is the throughput discipline.

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
| 9-10 | Expert | Ready for caching |
| 7-8 | Proficient | Review backoff |
| 5-6 | Developing | Re-study batching |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [01 - Model Selection](01-model-selection-quiz.md) | **Next**: [03 - Caching](03-caching-quiz.md)