# MLops 07: Model Serving — Quiz

> **Topic Overview**: Exposing a model as a service — API contracts, batching, and latency.

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

**What is model serving?**

- A) Training a model
- B) Exposing a trained model as a service that answers requests
- C) Packaging a model
- D) Monitoring a model

<details><summary>Reveal Answer</summary>

**B.** Serving is the production boundary.

</details>

### Question 2 — Easy

**What is the serving contract?**

- A) The model weights
- B) The stable request and response shapes and error codes
- C) The training config
- D) The dataset

<details><summary>Reveal Answer</summary>

**B.** The contract survives model changes.

</details>

### Question 3 — Medium

**Why batch requests?**

- A) To reduce accuracy
- B) To raise throughput by using the hardware more efficiently
- C) To increase latency
- D) For security

<details><summary>Reveal Answer</summary>

**B.** Batching groups work for the accelerator.

</details>

### Question 4 — Medium

**Which latency metric catches the slow tail?**

- A) The mean
- B) p95 and p99
- C) The minimum
- D) The mode

<details><summary>Reveal Answer</summary>

**B.** Percentiles reveal the tail; the average hides it.

</details>

### Question 5 — Medium

**What is a fallback chain?**

- A) A model version
- B) An ordered set of responses when the primary fails (cheaper model, cache, error)
- C) A training schedule
- D) A batch size

<details><summary>Reveal Answer</summary>

**B.** Availability over consistency, with each fallback recorded.

</details>

### Question 6 — Hard

**Why must the primary fail fast for a fallback to work?**

- A) For accuracy
- B) Otherwise it hangs and the fallback never runs
- C) For security
- D) It does not matter

<details><summary>Reveal Answer</summary>

**B.** A timeout bounds the failure so the fallback can trigger.

</details>

### Question 7 — Hard

**What does time to first token measure, and why does it matter?**

- A) Total cost
- B) How long until output starts streaming; it is what the user feels
- C) Model size
- D) Batch size

<details><summary>Reveal Answer</summary>

**B.** TTFT is the perceived wait.

</details>

### Question 8 — Hard

**Why is an end-to-end serving test required?**

- A) For speed
- B) It catches API drift, latency regressions, and fallback failures unit tests miss
- C) For accuracy
- D) It is optional

<details><summary>Reveal Answer</summary>

**B.** The full path is where those failures live.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can serve a model. |
| 5-6 | Review latency percentiles and fallbacks. |
| < 5 | Re-read the lecture. |
