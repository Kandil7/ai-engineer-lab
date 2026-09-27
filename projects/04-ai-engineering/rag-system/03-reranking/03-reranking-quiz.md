# RAG System 03: Reranking — Quiz

> **Topic Overview**: Bi-encoder vs cross-encoder, rerank depth, and
> measuring the reranker's contribution.

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

**What is a bi-encoder?**

- A) A model scoring pairs jointly
- B) A model embedding query and chunk separately
- C) A lexical ranker
- D) A fusion function

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Bi-encoders embed separately and compare vectors — fast but coarse.

</details>

---

### Question 2 — Easy

**What is a cross-encoder?**

- A) A model embedding separately
- B) A model scoring (query, chunk) jointly
- C) A BM25 ranker
- D) A cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Cross-encoders see the query-chunk interaction — accurate but slow.

</details>

---

### Question 3 — Easy

**What should the reranker rescore?**

- A) The full corpus
- B) Only the fused candidates
- C) Only the query
- D) Nothing

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Reranking the full corpus is too slow; rerank the fused top-N.

</details>

---

### Question 4 — Medium

**Why is a cross-encoder more accurate than a bi-encoder?**

- A) It is bigger
- B) It sees how the query and chunk interact
- C) It is faster
- D) It uses more data

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Joint scoring captures the interaction the separate embeddings miss.

</details>

---

### Question 5 — Medium

**What sets the rerank depth?**

- A) The model size
- B) The latency budget
- C) The corpus size
- D) The query length

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Deeper reranking costs more cross-encoder calls; the budget caps it.

</details>

---

### Question 6 — Medium

**How is the reranker's contribution measured?**

- A) By speed
- B) Recall@k with vs without reranking
- C) By model size
- D) By token count

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Compare recall with and without the reranker on the same golden set.

</details>

---

### Question 7 — Medium

**When does reranking not help?**

- A) When the corpus is small
- B) When the relevant chunk never reached the candidates
- C) When the model is large
- D) When the query is short

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Reranking cannot fix a retrieval miss — the fix is upstream.

</details>

---

### Question 8 — Hard

**A reranker showing no recall gain means:**

- A) The reranker is broken
- B) The problem is upstream in retrieval
- C) The model is too small
- D) The data is bad

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: No gain means the candidates lack the relevant chunk — fix chunking, filters, or fusion.

</details>

---

### Question 9 — Hard

**The correct pipeline order is:**

- A) Rerank, retrieve, generate
- B) Retrieve, rerank, generate
- C) Generate, retrieve, rerank
- D) Rerank, generate, retrieve

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Retrieve candidates, rerank them, then generate grounded on the top-k.

</details>

---

### Question 10 — Hard**

**The roadmap's rerank budget is:**

- A) < 1 s
- B) < 150 ms
- C) < 10 ms
- D) No budget

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The stage budget sets the rerank latency ceiling.

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
| 9-10 | Expert | Ready for context construction |
| 7-8 | Proficient | Review the depth trade |
| 5-6 | Developing | Re-study the encoders |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [02 - Filters](02-hard-filters-retrieval-quiz.md) | **Next**: [04 - Context Construction](04-context-construction-quiz.md)