# MLops 19: Resource and Performance Metrics — Quiz

> **Topic Overview**: Latency percentiles, throughput, utilization, efficiency, and gating promotion on resources.

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

**Why do SLOs use p95/p99 instead of the mean?**

- A) The mean is faster to compute
- B) Users experience the tail; the mean hides it
- C) Percentiles are cheaper
- D) The mean is always zero

<details><summary>Reveal Answer</summary>

**B.** A fast mean with a slow tail still violates the SLO.

</details>

### Question 2 — Easy

**What does throughput measure?**

- A) Accuracy
- B) Requests served per second
- C) Memory size
- D) Training epochs

<details><summary>Reveal Answer</summary>

**B.** It rises with batching and falls with latency.

</details>

### Question 3 — Medium

**GPU is idle while CPU is at 100%. What is the bottleneck?**

- A) The model
- B) The data pipeline (loading/preprocessing)
- C) VRAM
- D) The network

<details><summary>Reveal Answer</summary>

**B.** The saturated resource names the fix.

</details>

### Question 4 — Medium

**What three terms make up the VRAM budget?**

- A) Weights, KV cache, activations
- B) CPU, RAM, disk
- C) Data, labels, seeds
- D) Train, val, test

<details><summary>Reveal Answer</summary>

**A.** Weights + KV cache + activations must fit the card.

</details>

### Question 5 — Medium

**Why does maximizing throughput usually hurt per-request latency?**

- A) Larger batches parallelize work but make each request wait
- B) It does not
- C) Throughput is latency
- D) Batches are slower to train

<details><summary>Reveal Answer</summary>

**A.** Fast and high-throughput are different goals.

</details>

### Question 6 — Hard

**What does the efficiency ratio let you do?**

- A) Train faster
- B) Compare models fairly across sizes: quality per ms, per GB, per dollar
- C) Skip profiling
- D) Remove the SLO

<details><summary>Reveal Answer</summary>

**B.** It is the number behind "should we ship the bigger model".

</details>

### Question 7 — Hard

**Why must a promotion gate check resources, not just accuracy?**

- A) Accuracy is irrelevant
- B) A model that regresses p95 or exceeds VRAM must not ship, even if accurate
- C) Gates only check code
- D) Resources never change

<details><summary>Reveal Answer</summary>

**B.** Deployability is four budgets, not one.

</details>

### Question 8 — Hard

**Low GPU utilization with high latency points at what?**

- A) A slow model
- B) A data-pipeline bottleneck: the GPU waits on loading/CPU
- C) Too much VRAM
- D) A fast network

<details><summary>Reveal Answer</summary>

**B.** Profile the loader, not the model.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can size and gate a model for production. |
| 5-6 | Review percentiles and the bottleneck rule. |
| < 5 | Re-read the lecture. |
