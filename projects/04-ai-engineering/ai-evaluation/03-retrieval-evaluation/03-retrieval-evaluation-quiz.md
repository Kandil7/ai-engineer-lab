# AI Evaluation 03: Retrieval Evaluation — Quiz

> **Topic Overview**: Recall@k, precision@k, and MRR against the golden set.

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

**What does recall@k ask?**

- A) How much noise did we show?
- B) Of the relevant passages, how many are in the top k?
- C) How fast is retrieval?
- D) How many queries are cached?

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Recall@k answers "did we find the material?"

</details>

---

### Question 2 — Easy

**What does precision@k ask?**

- A) Of the top k results, how many are relevant?
- B) How many relevant passages exist?
- C) How long is the query?
- D) How big is the cache?

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Precision@k answers "how much noise did we show?"

</details>

---

### Question 3 — Easy

**What does MRR measure?**

- A) The number of relevant passages
- B) How high the first relevant passage ranked
- C) The retrieval speed
- D) The cache hit rate

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: MRR is the reciprocal rank of the first relevant passage.

</details>

---

### Question 4 — Medium

**MRR is 1.0 when:**

- A) All passages are relevant
- B) The first relevant passage is always ranked first
- C) Recall is 1.0
- D) Precision is 1.0

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Reciprocal rank 1 means the answer is always first.

</details>

---

### Question 5 — Medium

**Low recall@k means:**

- A) Too much noise
- B) The retriever misses material
- C) The cache is cold
- D) The model is slow

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Missing relevant passages means the answer cannot be grounded.

</details>

---

### Question 6 — Medium

**High recall, low precision@k means:**

- A) Material is missing
- B) Material is found but noise ranks above it
- C) The cache is broken
- D) The query is bad

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The right passages are buried in noise.

</details>

---

### Question 7 — Medium

**High recall, low MRR means:**

- A) Material is missing
- B) Material is found but not ranked first
- C) Precision is high
- D) The answer is wrong

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The material is grounded but the user sees the wrong passage first.

</details>

---

### Question 8 — Hard

**Which metric is primary for RAG grounding?**

- A) Precision@k
- B) Recall@k
- C) MRR
- D) Latency

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Missing a relevant passage means the answer cannot be grounded.

</details>

---

### Question 9 — Hard

**Why is MRR wrong for multi-answer queries?**

- A) It is slow
- B) It only sees the first relevant passage
- C) It is imprecise
- D) It is cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: MRR rewards only the first hit; multi-answer queries need recall.

</details>

---

### Question 10 — Hard**

**The CI gate threshold comes from:**

- A) A guess
- B) A baseline run
- C) The cache
- D) The model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Thresholds are set from a baseline, then enforced.

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
| 9-10 | Expert | Ready for LLM-as-judge |
| 7-8 | Proficient | Review MRR |
| 5-6 | Developing | Re-study recall@k |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [02 - Faithfulness](02-faithfulness-citation-precision-quiz.md) | **Next**: [04 - LLM-as-Judge](04-llm-as-judge-quiz.md)