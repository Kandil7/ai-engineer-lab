# RAG System 07: Context Failure Modes — Quiz

> **Topic Overview**: Missing, noisy, stale, and contradictory material.

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

**What are the four context failure modes?**

- A) Missing, noisy, stale, contradictory
- B) Slow, fast, cached, uncached
- C) Long, short, wide, narrow
- D) True, false, maybe, unknown

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Each has a retrieval cause and a guard.

</details>

---

### Question 2 — Easy

**Missing material means:**

- A) Too many passages
- B) The relevant passage is not in the context
- C) The cache is cold
- D) The query is too long

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The answer is wrong or an abstention.

</details>

---

### Question 3 — Easy

**Noisy material means:**

- A) The passage is missing
- B) Irrelevant passages crowd the context
- C) The cache is stale
- D) The query is ambiguous

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Low precision in retrieval.

</details>

---

### Question 4 — Medium

**Stale material is caught by:**

- A) The score threshold
- B) The provenance version
- C) The cache key
- D) The query embedding

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A version mismatch means the material is outdated.

</details>

---

### Question 5 — Medium

**Contradictory material causes:**

- A) A faster answer
- B) The model synthesizes a lie or picks one
- C) A cache hit
- D) A retrieval error

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The abstention rule guards against it.

</details>

---

### Question 6 — Medium

**Noisy material is guarded by:**

- A) The provenance version
- B) The score threshold and reranker
- C) The cache
- D) The query

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Weak matches are dropped.

</details>

---

### Question 7 — Medium

**The context quality log records:**

- A) Only the query
- B) The query, context ids, scores, and answer
- C) Only the answer
- D) Only the cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The diagnosis tool for failures.

</details>

---

### Question 8 — Hard

**Missing material is caused by:**

- A) Low precision
- B) Low recall or wrong filters
- C) A stale cache
- D) A contradictory corpus

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The retriever did not find the passage.

</details>

---

### Question 9 — Hard

**Stale material is caused by:**

- A) Low recall
- B) A cache serving old content or an un-reindexed corpus
- C) Low precision
- D) A contradictory corpus

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The version mismatch reveals it.

</details>

---

### Question 10 — Hard**

**Without logging, context failures are:**

- A) Obvious
- B) Undiagnosable
- C) Cached
- D) Impossible

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The log is the diagnosis tool.

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
| 9-10 | Expert | Ready for context security |
| 7-8 | Proficient | Review stale material |
| 5-6 | Developing | Re-study the four modes |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [06 - Caching](06-caching-quiz.md) | **Next**: [08 - Context Security](08-context-security-quiz.md)