# Embeddings 01: Model Selection — Quiz

> **Topic Overview**: The selection axes and the consistency rule.

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

**The embedding model decides:**

- A) The cache size
- B) Retrieval quality
- C) The query count
- D) The corpus size

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The vectors it produces are what retrieval searches.

</details>

---

### Question 2 — Easy

**Higher dimensions:**

- A) Cost less
- B) Capture more but cost more
- C) Are always better
- D) Are always worse

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: More to store and search.

</details>

---

### Question 3 — Easy

**For an Arabic corpus, the model must be:**

- A) Monolingual English
- B) Multilingual
- C) Small
- D) Free

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A monolingual English model embeds Arabic poorly.

</details>

---

### Question 4 — Medium

**The deployment context decides:**

- A) The corpus
- B) The model tier
- C) The query
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Prototype vs production.

</details>

---

### Question 5 — Medium

**A model change requires:**

- A) Nothing
- B) Re-embedding the whole corpus
- C) A cache flush
- D) A query change

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Old and new vectors are incomparable.

</details>

---

### Question 6 — Medium

**The corpus and queries must use:**

- A) Different models
- B) The same model
- C) Any model
- D) A cached model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Consistency across the pipeline.

</details>

---

### Question 7 — Medium

**The choice is re-evaluated:**

- A) Never
- B) When the corpus changes
- C) Every query
- D) Every day

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A growing Arabic corpus may need a better Arabic model.

</details>

---

### Question 8 — Hard

**The re-evaluation is measured on:**

- A) The cache
- B) The golden set
- C) The query log
- D) The model size

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: recall@k, not guesses.

</details>

---

### Question 9 — Hard

**The monolingual trap is:**

- A) A multilingual model on English
- B) An English-only model on Arabic
- C) A small model
- D) A free model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Poor embeddings, poor retrieval.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for the model is:**

- A) It is chosen deliberately
- B) It is the largest
- C) It is the cheapest
- D) It is cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: A deliberate tradeoff, not a default.

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
| 9-10 | Expert | Ready for batch processing |
| 7-8 | Proficient | Review language coverage |
| 5-6 | Developing | Re-study the axes |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [02 - Batch Processing](02-batch-processing-quiz.md)