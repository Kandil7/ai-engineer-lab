# RAG System 09: Long Context Processing — Quiz

> **Topic Overview**: The budget, truncation, summarization, compaction.

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

**The context budget is:**

- A) The full window
- B) The window minus prompt and output
- C) The cache size
- D) The model size

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: What is left for context.

</details>

---

### Question 2 — Easy

**Truncation drops:**

- A) The highest-ranked material
- B) The lowest-ranked material
- C) The cache
- D) The query

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Fast and lossy.

</details>

---

### Question 3 — Easy

**Summarization:**

- A) Preserves all detail
- B) Compresses but loses detail
- C) Caches
- D) Deletes

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The gist is preserved.

</details>

---

### Question 4 — Medium

**Chunking is a:**

- A) Context-side strategy
- B) Retrieval-side strategy
- C) Cache strategy
- D) Model strategy

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Split before retrieval.

</details>

---

### Question 5 — Medium

**Long conversations are handled by:**

- A) Truncation
- B) Compaction
- C) Caching
- D) Chunking

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Summarize older, keep recent.

</details>

---

### Question 6 — Medium

**Compaction summarizes:**

- A) Recent turns
- B) Older turns
- C) All turns
- D) No turns

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The recent turns are kept.

</details>

---

### Question 7 — Medium

**Budget utilization measures:**

- A) The cache
- B) How much of the budget is used
- C) The model size
- D) The query length

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Ensures the budget is respected.

</details>

---

### Question 8 — Hard

**Summarization costs:**

- A) Nothing
- B) A model call (latency and tokens)
- C) Only time
- D) Only memory

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: It is a model call.

</details>

---

### Question 9 — Hard

**Truncating the highest-ranked material is:**

- A) Correct
- B) A mistake
- C) Faster
- D) Required

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The best material must stay.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for the budget is:**

- A) It is ignored
- B) It is respected
- C) It is cached
- D) It is optional

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The budget is the contract.

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
| 9-10 | Expert | Ready for memory systems |
| 7-8 | Proficient | Review compaction |
| 5-6 | Developing | Re-study the budget |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [08 - Context Security](08-context-security-quiz.md) | **Next**: [10 - Memory Systems](10-memory-systems-quiz.md)