# Model Serving 03: Inference Serving — Quiz

> **Topic Overview**: The API contract, metrics, fallback chain.

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

**The serving API is:**

- A) The model
- B) The request/response contract
- C) The cache
- D) The GPU

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Stable across model changes.

</details>

---

### Question 2 — Easy

**Batching is handled by:**

- A) The application
- B) The server
- C) The cache
- D) The query

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: vLLM, TGI handle batching.

</details>

---

### Question 3 — Easy

**Latency measures:**

- A) Cost
- B) Time to first token and total time
- C) Cache hits
- D) Model size

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The responsiveness metric.

</details>

---

### Question 4 — Medium

**Throughput measures:**

- A) Latency
- B) Tokens per second
- C) Cost
- D) Cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The volume metric.

</details>

---

### Question 5 — Medium

**A fallback chain routes to:**

- A) The cache
- B) A backup model on primary failure
- C) The database
- D) The user

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Preserves availability.

</details>

---

### Question 6 — Medium

**p95 latency captures:**

- A) The average
- B) The tail (slow requests)
- C) The fastest
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The 95th percentile.

</details>

---

### Question 7 — Medium

**Without a fallback chain:**

- A) The system is faster
- B) There is a single point of failure
- C) The cache is warm
- D) The model is better

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Primary failure takes the system down.

</details>

---

### Question 8 — Hard

**The API contract is stable because:**

- A) The model never changes
- B) The model behind it can change
- C) It is cached
- D) It is required

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The contract is the boundary.

</details>

---

### Question 9 — Hard

**An end-to-end test checks:**

- A) Only the cache
- B) Request, response, and metric
- C) Only the model
- D) Only the GPU

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The full serving path.

</details>

---

### Question 10 — Hard**

**Batching in the application is a mistake because:**

- A) It is faster
- B) The server handles it
- C) It is cached
- D) It is required

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The server optimizes batching.

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
| 9-10 | Expert | Ready for HF inference SDK |
| 7-8 | Proficient | Review the fallback chain |
| 5-6 | Developing | Re-study the API |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [02 - Self-Hosted Models](02-self-hosted-models-quiz.md) | **Next**: [04 - HF Inference SDK](04-hf-inference-sdk-quiz.md)