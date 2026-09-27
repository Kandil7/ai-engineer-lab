# Arabic NLP 05: Hybrid Search and Reranking — Quiz

> **Topic Overview**: Fusing lexical and dense retrieval with RRF, reranking,
> and measuring hybrid against single arms.

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

**What does hybrid search combine?**

- A) Two dense models
- B) Lexical and dense retrieval arms
- C) Two lexical indexes
- D) Query and passage

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Hybrid runs the lexical (BM25) and dense (embedding) arms and fuses their rankings.

</details>

---

### Question 2 — Easy

**What does RRF stand for?**

- A) Ranked Relevance Function
- B) Reciprocal Rank Fusion
- C) Recursive Retrieval Framework
- D) Relative Rank Factor

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Reciprocal Rank Fusion sums 1/(k+rank) per document across arms.

</details>

---

### Question 3 — Easy

**Why does RRF need no score normalization?**

- A) Scores are already normalized
- B) It fuses ranks, not raw scores
- C) It uses only one arm
- D) Normalization is automatic

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: RRF operates on rank positions, which are comparable across arms without scaling.

</details>

---

### Question 4 — Medium

**What does the k=60 constant in RRF do?**

- A) Sets the number of arms
- B) Dampens the top ranks so one arm can't dominate
- C) Limits the corpus size
- D) Sets the rerank depth

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: k dampens the rank contribution, preventing a single arm's top results from overwhelming the fusion.

</details>

---

### Question 5 — Medium

**What is a cross-encoder?**

- A) A model encoding query and passage separately
- B) A model scoring (query, passage) pairs jointly
- C) A lexical ranker
- D) A fusion function

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Cross-encoders score pairs jointly — accurate but slow, so they rerank only fused candidates.

</details>

---

### Question 6 — Medium

**What should the reranker rescore?**

- A) The whole corpus
- B) Only the fused candidates
- C) Only the lexical results
- D) Only the dense results

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Reranking the full corpus is too slow; rerank the fused top-k (e.g., top-50 → top-5).

</details>

---

### Question 7 — Medium

**What is the acceptance test for hybrid search?**

- A) It is faster than either arm
- B) It meets or beats both single arms on recall@k
- C) It uses less memory
- D) It needs no golden set

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Hybrid must not underperform either arm; if it does, fusion or reranking is wrong.

</details>

---

### Question 8 — Hard

**Why does the lexical arm matter on Arabic specifically?**

- A) It is faster
- B) It carries exact-term and name queries the dense arm blurs
- C) It needs no normalization
- D) It replaces embeddings

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Arabic names and exact terms are the lexical arm's strength; the fusion must not let the dense arm drown them.

</details>

---

### Question 9 — Hard

**A document ranked 1 by both arms scores highest under RRF. Why?**

- A) It has the highest raw score
- B) It accumulates 1/(k+1) from each arm
- C) It is the longest
- D) It has the most terms

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Rank 1 contributes 1/(k+1) per arm; agreement across arms compounds the score.

</details>

---

### Question 10 — Hard

**What is the correct tuning order for hybrid search?**

- A) Fusion weights, then arms, then reranker
- B) Measure each arm, then tune fusion, then rerank depth
- C) Rerank depth, then arms
- D) Golden set, then nothing

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Measure each arm on the golden set first, then tune fusion and rerank depth — never tune fusion before knowing the arms.

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
| 9-10 | Expert | Ready for RAG generation |
| 7-8 | Proficient | Review fusion internals |
| 5-6 | Developing | Re-study the arms |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [04 - Embeddings](04-arabic-embeddings-quiz.md)