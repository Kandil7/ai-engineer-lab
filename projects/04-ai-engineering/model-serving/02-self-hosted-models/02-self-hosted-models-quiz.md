# Model Serving 02: Self-Hosted Models — Quiz

> **Topic Overview**: The tradeoff, VRAM budget, OpenAI-compatible API.

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

**Self-hosting trades:**

- A) Speed for cost
- B) API cost for infrastructure work
- C) Quality for speed
- D) License for cost

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: No per-token cost, but you run the hardware.

</details>

---

### Question 2 — Easy

**Ollama is best for:**

- A) Production
- B) Development and single-user
- C) Multi-user
- D) High throughput

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Simplest path, no batching.

</details>

---

### Question 3 — Easy

**vLLM is best for:**

- A) Development
- B) Production serving
- C) Single-user
- D) Testing

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Paged attention and continuous batching.

</details>

---

### Question 4 — Medium

**A 7B model at 4-bit uses about:**

- A) 14 GB
- B) 3.5 GB
- C) 1 GB
- D) 16 GB

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: 7B * 4 bits / 8 = 3.5 GB.

</details>

---

### Question 5 — Medium

**The VRAM budget includes:**

- A) Only weights
- B) Weights, KV cache, and activations
- C) Only the cache
- D) Only activations

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Checked before the run.

</details>

---

### Question 6 — Medium

**OpenAI-compatible means:**

- A) The app must use OpenAI
- B) The app code is identical; only the base URL changes
- C) The API is slow
- D) The API is cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Swap the base URL.

</details>

---

### Question 7 — Medium

**Continuous batching is:**

- A) Ollama's feature
- B) vLLM's throughput optimization
- C) A cache
- D) A quantization method

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Dynamic request batching.

</details>

---

### Question 8 — Hard

**Self-hosting for a low-volume workload is:**

- A) Cheaper
- B) More expensive than the API
- C) Faster
- D) Required

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The infrastructure cost exceeds the API cost.

</details>

---

### Question 9 — Hard

**Ollama for production is a mistake because:**

- A) It is slow
- B) It has no batching
- C) It is cached
- D) It is expensive

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: vLLM handles concurrency.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for self-hosting is:**

- A) It is ignored
- B) The tradeoff is understood
- C) It is cached
- D) It is required

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: When it is worth it.

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
| 9-10 | Expert | Ready for inference serving |
| 7-8 | Proficient | Review the VRAM budget |
| 5-6 | Developing | Re-study the tradeoff |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [01 - Choosing a Model](01-choosing-a-model-quiz.md) | **Next**: [03 - Inference Serving](03-inference-serving-quiz.md)