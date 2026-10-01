# GenAI 06: Embeddings — Quiz

> **Topic Overview**: Turning text into vectors and measuring similarity for retrieval.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is an embedding?**
- A) A keyword
- B) A dense vector representing meaning
- C) A file
- D) A token

<details><summary>Reveal Answer</summary>**B.** Meaning becomes geometry.</details>

### Question 2 — Easy
**Which metric is the usual default for text?**
- A) Euclidean distance
- B) Cosine similarity
- C) Manhattan distance
- D) Hamming distance

<details><summary>Reveal Answer</summary>**B.** Cosine ignores length.</details>

### Question 3 — Medium
**Why must the query and corpus use the same model?**
- A) For speed
- B) Different models define different vector spaces
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Cross-space similarity is meaningless.</details>

### Question 4 — Medium
**Why normalize vectors on write?**
- A) For accuracy
- B) On unit vectors cosine equals dot, so queries pay one dot product
- C) For storage
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Normalization enables the cheap metric.</details>

### Question 5 — Medium
**What does a high cosine mean?**
- A) Long vector
- B) High semantic similarity
- C) High cost
- D) Low quality

<details><summary>Reveal Answer</summary>**B.** Cosine measures similarity.</details>

### Question 6 — Hard
**A model that never saw Arabic embeds it poorly. Why?**
- A) It is broken
- B) Its tokenizer and training skew toward other languages, so Arabic meaning is weak
- C) Arabic is unembeddable
- D) It lacks a GPU

<details><summary>Reveal Answer</summary>**B.** Coverage is a measured property.</details>

### Question 7 — Hard
**Why evaluate the embedding model on your own golden set?**
- A) For speed
- B) Leaderboard quality may not transfer to your task/language
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Measure on your data.</details>

### Question 8 — Hard
**Why embed the normalized text, not the raw display text?**
- A) For style
- B) Diacritics/variants would split the space for no benefit
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Consistent normalization keeps the space coherent.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | Solid on embeddings. |
| 5-6 | Review metrics and consistency. |
| < 5 | Re-read the lecture. |
