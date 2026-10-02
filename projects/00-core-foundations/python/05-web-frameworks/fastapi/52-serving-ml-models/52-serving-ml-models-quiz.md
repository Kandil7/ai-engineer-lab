# FastAPI 52: Serving ML Models — Quiz

> **Topic Overview**: Load-once startup, warmup, batching, and the predict contract.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**When should the model load?**
- A) Per request
- B) Once at startup, shared by handlers
- C) Per user
- D) Lazily per batch

<details><summary>Reveal Answer</summary>**B.** Amortize load cost.</details>

### Question 2 — Easy
**What is warmup?**
- A) Scaling
- B) Running a few inferences at startup so caches, kernels, and pools are hot
- C) Logging
- D) Caching inputs

<details><summary>Reveal Answer</summary>**B.** Hot-first-request.</details>

### Question 3 — Medium
**What does the `/predict` contract include?**
- A) The model
- B) Versioned input/output schemas plus an error envelope
- C) The weights
- D) The logs

<details><summary>Reveal Answer</summary>**B.** Stable inference interface.</details>

### Question 4 — Medium
**Why batch inference requests?**
- A) Accuracy
- B) Amortized model cost per item raises throughput
- C) Speed per single request
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Efficiency at volume.</details>

### Question 5 — Medium
**What bounds memory per worker?**
- A) Nothing
- B) Model size × workers plus per-request buffers against available RAM
- C) CPU
- D) Disk

<details><summary>Reveal Answer</summary>**B.** Worker memory math.</details>

### Question 6 — Hard
**When is GPU serving worth it?**
- A) Always
- B) When batchable compute dominates and utilization justifies the instance cost
- C) Never
- D) For small models

<details><summary>Reveal Answer</summary>**B.** Break-even arithmetic.</details>

### Question 7 — Hard
**Why version the model behind the endpoint?**
- A) Style
- B) Roll back a bad model and A/B a new one without redeploying the API
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Model lifecycle independent of code.</details>

### Question 8 — Hard
**What must the readiness probe check for a model server?**
- A) The port
- B) Model loaded, warmed, and reachable dependencies
- C) The git hash
- D) The logs

<details><summary>Reveal Answer</summary>**B.** Serve only when truly ready.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You serve models in production. |
| 5-6 | Review startup, batching, memory. |
| < 5 | Re-read the lecture. |
