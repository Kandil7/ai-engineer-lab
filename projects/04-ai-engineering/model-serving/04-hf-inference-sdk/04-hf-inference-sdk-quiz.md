# Model Serving 04: HF Inference SDK — Quiz

> **Topic Overview**: The SDK, model selection, free-tier limits.

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

**The HF Inference SDK calls:**

- A) Local models
- B) Hosted models on the Hub
- C) The cache
- D) The database

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The Inference API.

</details>

---

### Question 2 — Easy

**Hub models are identified by:**

- A) A number
- B) org/name
- C) A URL
- D) A hash

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: e.g., mistralai/Mistral-7B.

</details>

---

### Question 3 — Easy

**The free tier has:**

- A) No limits
- B) Rate limits and shared capacity
- C) Dedicated capacity
- D) No latency

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: For development, not production.

</details>

---

### Question 4 — Medium

**Inference Endpoints are:**

- A) The free tier
- B) Dedicated, autoscaled deployments
- C) A cache
- D) A local model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The production path.

</details>

---

### Question 5 — Medium

**Hub selection matches on:**

- A) Only the name
- B) Task, language, and size
- C) Only the cost
- D) Only the license

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The three selection axes.

</details>

---

### Question 6 — Medium

**The free tier returns 429 when:**

- A) The model is slow
- B) The rate limit is exceeded
- C) The cache is cold
- D) The query is long

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The request bound.

</details>

---

### Question 7 — Medium

**HF Inference is managed; self-hosting is:**

- A) Also managed
- B) Unmanaged — full control, more work
- C) Free
- D) Cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The infrastructure is yours.

</details>

---

### Question 8 — Hard

**Using the free tier in production is a mistake because:**

- A) It is slow
- B) Rate limits and shared capacity
- C) It is cached
- D) It is free

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Production needs dedicated capacity.

</details>

---

### Question 9 — Hard

**Feature extraction is the task of:**

- A) Text generation
- B) Text to vector
- C) Classification
- D) Translation

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The embedding task.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for the HF SDK is:**

- A) It is ignored
- B) It is used and the comparison is documented
- C) It is cached
- D) It is required

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Including HF vs self-hosting.

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
| 9-10 | Expert | Model-serving section complete |
| 7-8 | Proficient | Review the free tier |
| 5-6 | Developing | Re-study the SDK |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [03 - Inference Serving](03-inference-serving-quiz.md)