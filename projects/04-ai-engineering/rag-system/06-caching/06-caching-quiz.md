# RAG System 06: Caching — Quiz

> **Topic Overview**: Version-keyed cache keys, semantic caching,
> invalidation, and the never-cache-bad-answers rule.

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

**What does a cache key carry?**

- A) Only the query
- B) Query + prompt version + corpus version
- C) Only the answer
- D) Only the model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A cache entry is valid only for the exact configuration that produced it.

</details>

---

### Question 2 — Easy

**What is semantic caching?**

- A) Caching by exact query
- B) Returning cached answers for similar queries
- C) Caching by tenant
- D) Caching by model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Semantic caching reuses an answer when a new query is similar enough to a cached one.

</details>

---

### Question 3 — Easy

**What is the hit rate?**

- A) The model's accuracy
- B) The fraction of queries served from cache
- C) The cache size
- D) The query count

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The hit rate is a cost lever — a 30% hit rate cuts a third of LLM spend.

</details>

---

### Question 4 — Medium

**What happens when the corpus changes?**

- A) Nothing
- B) The cache invalidates; old entries miss
- C) The cache grows
- D) The cache is faster

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The version-keyed cache naturally misses after a corpus change.

</details>

---

### Question 5 — Medium

**What is the semantic threshold?**

- A) A cache size
- B) The precision-recall dial for semantic caching
- C) A model parameter
- D) A token limit

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Too low serves wrong answers; too high misses savings.

</details>

---

### Question 6 — Medium

**What should never be cached?**

- A) Good answers
- B) Abstained or malformed answers
- C) Grounded answers
- D) Cited answers

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Caching a refusal locks it in; caching malformed output amplifies the error.

</details>

---

### Question 7 — Medium

**A dropping hit rate means:**

- A) The cache is working
- B) The cache is rotting
- C) The model is better
- D) The corpus is smaller

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Queries diverging, threshold too strict, or invalidation too aggressive.

</details>

---

### Question 8 — Hard

**Why does the cache key carry the prompt version?**

- A) It is faster
- B) A prompt change produces different answers; old entries are stale
- C) It saves space
- D) It is required

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The same query under a new prompt yields a different answer — the old cache entry is stale.

</details>

---

### Question 9 — Hard

**The validate-before-cache rule requires:**

- A) Caching everything
- B) Schema-valid, grounded, non-abstained answers only
- C) Caching abstentions
- D) Caching malformed output

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Only good answers enter the cache.

</details>

---

### Question 10 — Hard**

**The roadmap treats cache hit rate as:**

- A) A nice-to-have
- B) A first-class cost metric
- C) A model metric
- D) A UI metric

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Hit rate is a cost lever tracked on the dashboard.

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
| 9-10 | Expert | Stage 9 RAG complete |
| 7-8 | Proficient | Review invalidation |
| 5-6 | Developing | Re-study cache keys |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [05 - Abstention and Citations](05-abstention-citations-quiz.md)