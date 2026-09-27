# Arabic NLP 04: Arabic Embeddings — Quiz

> **Topic Overview**: Choosing and evaluating embedding models for Arabic,
> and building the dense retrieval arm.

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

**What does an embedding represent?**

- A) A word's frequency
- B) A text as a vector where distance means similarity
- C) A document's length
- D) A term's IDF

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Embeddings place text in a vector space where semantic nearness is geometric distance.

</details>

---

### Question 2 — Easy

**Why is model choice more important for Arabic than English?**

- A) Arabic has more letters
- B) Multilingual models often tokenize Arabic poorly and skew to English
- C) Arabic needs no embeddings
- D) English models are slower

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Multilingual models are English-heavy and often split Arabic subwords awkwardly, weakening Arabic semantics.

</details>

---

### Question 3 — Easy

**What metric evaluates an embedding model on Arabic retrieval?**

- A) Latency
- B) Recall@k on the golden set
- C) Model size
- D) Token count

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The same labeled set and recall@k that measured BM25 measure the dense arm, making the arms comparable.

</details>

---

### Question 4 — Medium

**What text should be embedded?**

- A) The raw display text
- B) The normalized searchable text
- C) The diacritized original
- D) The translated text

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Embed the same normalized text the lexical index uses, so both arms share one normalization.

</details>

---

### Question 5 — Medium

**What is the dense arm's strength?**

- A) Exact term matching
- B) Matching meaning, including paraphrase and synonyms
- C) Faster than lexical
- D) No index needed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Dense retrieval matches by meaning, catching queries with no shared tokens.

</details>

---

### Question 6 — Medium

**What is the dense arm's weakness?**

- A) It misses paraphrase
- B) It blurs exact terms and names
- C) It requires stemming
- D) It ignores normalization

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Embeddings blur exact strings — the lexical arm covers those.

</details>

---

### Question 7 — Medium

**Which is a suspect when the dense arm misses?**

- A) IDF
- B) Model tokenization of Arabic
- C) Length normalization
- D) b parameter

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Dense misses trace to tokenization, normalization consistency, or model choice.

</details>

---

### Question 8 — Hard

**Why compare arms on the same golden set?**

- A) To save effort
- B) So recall@k is directly comparable before fusion
- C) To avoid normalization
- D) To reduce storage

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Identical evaluation makes the two arms' strengths and weaknesses legible before hybrid fusion.

</details>

---

### Question 9 — Hard

**A dense arm misses an exact-term query. What is the correct conclusion?**

- A) The model is broken
- B) Expected — the lexical arm covers exact terms
- C) Normalization failed
- D) The index is corrupt

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Dense blurring exact terms is its known weakness; the lexical arm exists for exactly that case.

</details>

---

### Question 10 — Hard

**What is the correct candidate set for Arabic embeddings?**

- A) Any multilingual model
- B) Arabic-specialized models or multilingual models with verified Arabic benchmarks
- C) Only English models
- D) The largest model available

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Choose Arabic-specialized or verified multilingual models; the golden set decides between them.

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
| 9-10 | Expert | Ready for hybrid search |
| 7-8 | Proficient | Review model evaluation |
| 5-6 | Developing | Re-study the dense arm |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [03 - Lexical Retrieval](03-arabic-lexical-retrieval-quiz.md) | **Next**: [05 - Hybrid Search](05-arabic-hybrid-search-quiz.md)