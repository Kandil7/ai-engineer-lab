# MLops 08: Inference Optimization — Quiz

> **Topic Overview**: Making inference faster and cheaper — quantization, batching, and hardware fit.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

---

## Questions

### Question 1 — Easy

**What does quantization do?**

- A) Trains a model
- B) Reduces numeric precision to shrink memory and speed compute
- C) Increases accuracy
- D) Compresses the dataset

<details><summary>Reveal Answer</summary>

**B.** Lower precision trades a little quality for size and speed.

</details>

### Question 2 — Easy

**Why measure quality after quantization, not only memory?**

- A) Memory is enough
- B) Quantization can degrade output quality, especially in another language
- C) It is required
- D) It cannot degrade

<details><summary>Reveal Answer</summary>

**B.** The trade must be measured on the task.

</details>

### Question 3 — Medium

**How does batching improve inference throughput?**

- A) It reduces accuracy
- B) It processes several requests per forward pass, using the hardware better
- C) It increases memory
- D) It reduces latency for one request

<details><summary>Reveal Answer</summary>

**B.** Batching raises throughput.

</details>

### Question 4 — Medium

**What is the KV cache, and why does it matter?**

- A) A dataset cache
- B) Stored attention keys/values so generation does not recompute context; it grows with length and concurrency
- C) A model file
- D) A training trick

<details><summary>Reveal Answer</summary>

**B.** The KV cache is a major memory consumer at inference.

</details>

### Question 5 — Medium

**What is continuous batching?**

- A) Fixed batches
- B) A server technique that batches dynamically as requests arrive and finish
- C) A training loop
- D) A quantization method

<details><summary>Reveal Answer</summary>

**B.** It keeps the accelerator busy under mixed load.

</details>

### Question 6 — Hard

**A model "fits" at rest but OOMs under load. Why?**

- A) The data
- B) The KV cache and activations grow with context length and concurrency, beyond the weights
- C) The network
- D) The CPU

<details><summary>Reveal Answer</summary>

**B.** Budget weights plus KV plus activations plus overhead.

</details>

### Question 7 — Hard

**When is self-hosting cheaper than an API?**

- A) Always
- B) At high, steady volume where the amortized GPU cost beats per-token billing
- C) At low volume
- D) Never

<details><summary>Reveal Answer</summary>

**B.** The break-even depends on volume and utilization.

</details>

### Question 8 — Hard

**Why compare output tokens/second across concurrency levels?**

- A) For accuracy
- B) Throughput collapses under concurrency due to queueing; the curve shows the real capacity
- C) For cost only
- D) It does not change

<details><summary>Reveal Answer</summary>

**B.** Capacity is a curve, not a single number.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can optimize inference. |
| 5-6 | Review quantization and the KV cache. |
| < 5 | Re-read the lecture. |
