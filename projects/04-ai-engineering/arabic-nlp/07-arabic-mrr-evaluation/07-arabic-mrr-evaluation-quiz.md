# Arabic NLP 07: MRR Evaluation — Quiz

> **Topic Overview**: MRR, recall@k, and the Arabic golden set.

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

**MRR rewards:**

- A) Finding any passage
- B) Ranking the first relevant passage high
- C) Speed
- D) Cache hits

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The reciprocal rank of the first relevant passage.

</details>

---

### Question 2 — Easy

**MRR is 1.0 when:**

- A) All passages are relevant
- B) The first relevant passage is ranked first
- C) Recall is 1.0
- D) The query is cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Reciprocal rank 1.

</details>

---

### Question 3 — Easy

**Recall@k asks:**

- A) How fast is retrieval?
- B) Are the relevant passages in the top k?
- C) How many queries are cached?
- D) How big is the corpus?

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Did we find the material?

</details>

---

### Question 4 — Medium

**High recall, low MRR means:**

- A) Material is missing
- B) Material is found but not ranked first
- C) The cache is cold
- D) The query is bad

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The answer is grounded but the user sees the wrong passage first.

</details>

---

### Question 5 — Medium

**Low recall means:**

- A) Too much noise
- B) The material is missing
- C) The cache is cold
- D) The query is bad

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Fix the retriever.

</details>

---

### Question 6 — Medium

**The Arabic golden set contains:**

- A) Only verse queries
- B) Verse, hadith, fiqh, and unanswerable queries
- C) Only hadith queries
- D) Random queries

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Coverage of the corpus's question types.

</details>

---

### Question 7 — Medium

**An unanswerable query tests:**

- A) Speed
- B) Abstention
- C) Caching
- D) Ranking

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A query with no relevant passage.

</details>

---

### Question 8 — Hard

**The thresholds come from:**

- A) A guess
- B) A baseline run
- C) The cache
- D) The model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Then enforced in CI.

</details>

---

### Question 9 — Hard

**The metrics gate:**

- A) Nothing
- B) Changes in CI
- C) The cache
- D) The model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A drop below the baseline fails CI.

</details>

---

### Question 10 — Hard**

**A golden set that changes under the system is:**

- A) Fine
- B) A broken yardstick
- C) Faster
- D) Cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The set must be fixed to measure regressions.

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
| 9-10 | Expert | Stage 7 IR complete |
| 7-8 | Proficient | Review recall@k |
| 5-6 | Developing | Re-study MRR |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [06 - ANN Search](06-arabic-ann-search-quiz.md)