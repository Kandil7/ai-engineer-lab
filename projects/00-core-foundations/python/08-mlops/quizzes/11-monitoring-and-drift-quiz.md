# MLops 11: Monitoring and Drift — Quiz

> **Topic Overview**: Watching a model in production for data drift, concept drift, and quality decay.

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

**What is model monitoring?**

- A) Training a model
- B) Tracking a deployed model's inputs, outputs, and performance over time
- C) Packaging a model
- D) Deleting a model

<details><summary>Reveal Answer</summary>

**B.** Production behavior, not training.

</details>

### Question 2 — Easy

**Why monitor a model after deployment?**

- A) For cost only
- B) The world changes; quality degrades without retraining
- C) It is required by law
- D) To slow the system

<details><summary>Reveal Answer</summary>

**B.** Deployment is the start of drift.

</details>

### Question 3 — Medium

**What is data drift?**

- A) The model changes
- B) The input distribution shifts away from training
- C) The code changes
- D) The labels change

<details><summary>Reveal Answer</summary>

**B.** Inputs change; the model did not.

</details>

### Question 4 — Medium

**What is concept drift?**

- A) The inputs change
- B) The relationship between inputs and outputs changes
- C) The code changes
- D) The GPU changes

<details><summary>Reveal Answer</summary>

**B.** The mapping the model learned no longer holds.

</details>

### Question 5 — Medium

**Why is quality drift hard to detect?**

- A) It happens instantly
- B) It is gradual, so each day looks like the last until the aggregate has moved a lot
- C) It never happens
- D) It is always loud

<details><summary>Reveal Answer</summary>

**B.** Slow slides are invisible without a rolling baseline.

</details>

### Question 6 — Hard

**How do you detect quality drift without immediate labels?**

- A) Wait for labels
- B) Monitor proxy signals (input drift, output distribution, confidence, abstention) against a baseline
- C) Only retrain
- D) You cannot

<details><summary>Reveal Answer</summary>

**B.** Proxies give an early warning before labels arrive.

</details>

### Question 7 — Hard

**Which check fires when the live input distribution moves away from training?**

- A) A code lint
- B) A data-drift check on feature distributions
- C) A cost alert
- D) A GPU alert

<details><summary>Reveal Answer</summary>

**B.** Distribution comparison against a reference.

</details>

### Question 8 — Hard

**What does a rising abstention rate signal in a RAG system?**

- A) Better answers
- B) Retrieval degrading, so fewer queries have supporting evidence
- C) Lower cost
- D) Nothing

<details><summary>Reveal Answer</summary>

**B.** Abstention is an AI-specific drift signal.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can monitor for drift. |
| 5-6 | Review data vs concept drift. |
| < 5 | Re-read the lecture. |
