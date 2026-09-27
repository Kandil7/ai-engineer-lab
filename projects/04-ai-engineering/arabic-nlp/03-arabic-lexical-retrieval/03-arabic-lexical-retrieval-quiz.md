# Arabic NLP 03: Lexical Retrieval — Quiz

> **Topic Overview**: Inverted index, BM25 scoring, and Arabic-aware lexical
> retrieval.

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

**What does an inverted index map?**

- A) Documents to terms
- B) Terms to documents
- C) Queries to scores
- D) Passages to lengths

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: An inverted index maps each term to the documents containing it (the postings list).

</details>

---

### Question 2 — Easy

**What does IDF do in BM25?**

- A) Rewards common terms
- B) Down-weights terms appearing in many documents
- C) Normalizes document length
- D) Caps term frequency

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: IDF gives rare terms more weight — a term in every document carries little signal.

</details>

---

### Question 3 — Easy

**What does length normalization prevent?**

- A) Short documents winning
- B) Long documents winning by volume
- C) Term frequency saturation
- D) Index bloat

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Without length normalization, long documents accumulate more term matches and dominate unfairly.

</details>

---

### Question 4 — Medium

**Why must normalization run at index time?**

- A) To save storage
- B) So the index matches the normalized query terms
- C) To speed up scoring
- D) To avoid stemming

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The query is normalized too; the index must use the same normalized terms or matches fail.

</details>

---

### Question 5 — Medium

**What does term frequency saturation do?**

- A) Rewards unlimited repetition
- B) Caps the reward for a term appearing many times
- C) Removes rare terms
- D) Normalizes length

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Saturation (k1) stops repetition from rewarding without bound — a term appearing 10 times is not 10x better than once.

</details>

---

### Question 6 — Medium

**Which stage failure explains a query missing a passage that shares no normalized term?**

- A) Scoring
- B) Normalization or tokenization
- C) Length normalization
- D) IDF

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: If query and passage share no normalized form, the failure is upstream of scoring — in normalization or tokenization.

</details>

---

### Question 7 — Medium

**What is the role of the b parameter in BM25?**

- A) Term saturation
- B) Length normalization strength
- C) IDF scaling
- D) Query expansion

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: b controls how strongly document length is normalized; it often needs tuning on code or mixed corpora.

</details>

---

### Question 8 — Hard

**Which passage should rank first for the query "الكتاب" given the index is normalized and stemmed?**

- A) "المكتبة مفتوحة"
- B) "الكتاب على المكتب"
- C) "البيت كبير"
- D) "الكاتب يكتب"

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: "الكتاب" normalizes and stems to "كتاب", which appears in the book-on-desk passage — the exact match ranks first.

</details>

---

### Question 9 — Hard

**Why is lexical search still needed alongside embeddings?**

- A) It is faster
- B) It matches exact terms, names, and codes that embeddings blur
- C) It requires no index
- D) It replaces embeddings entirely

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Lexical search matches exact strings; embeddings match meaning. Hybrid uses both because they fail in opposite directions.

</details>

---

### Question 10 — Hard

**What is the correct diagnosis order for a recall miss?**

- A) Scoring, tokenization, normalization
- B) Normalization, tokenization, scoring
- C) Length, IDF, saturation
- D) Index, query, passage

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Check normalization first (shared normalized form), then tokenization (stemmer split), then scoring (right passage ranked below k).

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
| 9-10 | Expert | Ready for embeddings and hybrid |
| 7-8 | Proficient | Review BM25 internals |
| 5-6 | Developing | Re-study the index |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [02 - Normalization](02-arabic-normalization-tokenization-quiz.md) | **Next**: [04 - Embeddings](04-arabic-embeddings-quiz.md)