# GenAI 11: Advanced Retrieval — Quiz

> **Topic Overview**: Hybrid search, fusion, and query transformation beyond a single dense arm.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why combine lexical and dense retrieval?**
- A) For speed
- B) They fail in opposite directions, so hybrid covers more
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Complementary strengths.</details>

### Question 2 — Easy
**What is reciprocal rank fusion?**
- A) Adding scores
- B) Combining ranked lists by summing 1/(k+rank)
- C) Training a model
- D) A chunking method

<details><summary>Reveal Answer</summary>**B.** RRF needs no score normalization.</details>

### Question 3 — Medium
**Why fuse ranks rather than raw scores?**
- A) Ranks are prettier
- B) Lexical and dense scores are on incomparable scales
- C) For speed
- D) It is arbitrary

<details><summary>Reveal Answer</summary>**B.** Ranks are comparable across arms.</details>

### Question 4 — Medium
**What does query rewriting do?**
- A) Changes the model
- B) Reformulates the query to improve retrieval (expansion, decomposition)
- C) Compresses the index
- D) Reduces cost

<details><summary>Reveal Answer</summary>**B.** A better query retrieves better passages.</details>

### Question 5 — Medium
**When should you add an advanced retrieval step?**
- A) Always
- B) Only after a baseline comparison shows it helps
- C) Never
- D) To reduce cost

<details><summary>Reveal Answer</summary>**B.** Complexity must earn its place.</details>

### Question 6 — Hard
**Hybrid underperforms one arm. What is a likely cause?**
- A) The model is broken
- B) The fusion weights or RRF constant are wrong
- C) The GPU
- D) The dataset

<details><summary>Reveal Answer</summary>**B.** The fusion config is a tuning variable.</details>

### Question 7 — Hard
**Why is hard filtering a correctness concern in hybrid?**
- A) It is not
- B) Both arms must honor the same filters, or the fusion leaks
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Safety is the weaker arm's safety.</details>

### Question 8 — Hard
**What is hierarchical retrieval?**
- A) One flat index
- B) Retrieving at multiple granularities (summary then detail)
- C) A model
- D) A cache

<details><summary>Reveal Answer</summary>**B.** Coarse-to-fine retrieval.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can design hybrid retrieval. |
| 5-6 | Review RRF and when to add steps. |
| < 5 | Re-read the lecture. |
