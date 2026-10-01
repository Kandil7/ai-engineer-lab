# GenAI 12: Reranking — Quiz

> **Topic Overview**: Reordering retrieved candidates with a cross-encoder.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does a reranker do?**
- A) Trains the model
- B) Reorders the retrieved candidates by a stronger model
- C) Chunks documents
- D) Caches answers

<details><summary>Reveal Answer</summary>**B.** Retrieval finds; reranking reorders.</details>

### Question 2 — Easy
**Why is the reranker only run on candidates?**
- A) It is lazy
- B) A cross-encoder is too slow to scan the corpus
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** It is an accuracy layer on a narrow set.</details>

### Question 3 — Medium
**Bi-encoder vs cross-encoder: the key difference?**
- A) Speed only
- B) The bi-encoder embeds separately (coarse); the cross-encoder scores the pair jointly (accurate)
- C) Language
- D) Size

<details><summary>Reveal Answer</summary>**B.** Joint scoring sees the interaction.</details>

### Question 4 — Medium
**What is rerank depth?**
- A) The model depth
- B) How many candidates go to the reranker
- C) The chunk size
- D) The batch size

<details><summary>Reveal Answer</summary>**B.** A latency-quality trade.</details>

### Question 5 — Medium
**How do you know the reranker helps?**
- A) It sounds better
- B) Measure recall/MRR with and without it on the golden set
- C) It is always helpful
- D) You cannot

<details><summary>Reveal Answer</summary>**B.** Measure its contribution.</details>

### Question 6 — Hard
**A reranker shows no recall gain. What is the likely cause?**
- A) The reranker is broken
- B) Retrieval never found the relevant passage, so reordering cannot help
- C) The GPU
- D) The dataset

<details><summary>Reveal Answer</summary>**B.** The fix is upstream.</details>

### Question 7 — Hard
**Where does reranking sit in the pipeline?**
- A) Before ingestion
- B) Between fusion and context construction
- C) After generation
- D) In the cache

<details><summary>Reveal Answer</summary>**B.** The last quality lever before the answer.</details>

### Question 8 — Hard
**Why is reranking cost part of the per-query budget?**
- A) It is free
- B) It is a model call with its own latency and cost
- C) For accuracy
- D) It is not

<details><summary>Reveal Answer</summary>**B.** It is an inference cost.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand reranking. |
| 5-6 | Review cross-encoder and depth. |
| < 5 | Re-read the lecture. |
