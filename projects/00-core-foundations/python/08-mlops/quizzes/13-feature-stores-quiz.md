# MLops 13: Feature Stores — Quiz

> **Topic Overview**: A shared store of features that keeps training and serving consistent.

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

**What problem does a feature store solve?**

- A) Model accuracy
- B) Feature reuse and training/serving consistency
- C) GPU cost
- D) Storage size

<details><summary>Reveal Answer</summary>

**B.** One definition used in both paths.

</details>

### Question 2 — Easy

**What is training/serving skew?**

- A) Different GPUs
- B) A feature computed differently in training than in serving
- C) A data version
- D) A model change

<details><summary>Reveal Answer</summary>

**B.** The two paths diverge and the model misbehaves.

</details>

### Question 3 — Medium

**What is a point-in-time correct join?**

- A) A normal join
- B) Joining features as they were at the prediction time, preventing future leakage
- C) A cross join
- D) An outer join

<details><summary>Reveal Answer</summary>

**B.** It prevents temporal leakage.

</details>

### Question 4 — Medium

**Why are online and offline stores separate?**

- A) For cost only
- B) Online needs low-latency lookup; offline needs batch scans over history
- C) For security
- D) They are the same

<details><summary>Reveal Answer</summary>

**B.** Different access patterns, same definitions.

</details>

### Question 5 — Medium

**What does a feature store share?**

- A) The model
- B) Feature definitions computed identically in both paths
- C) The dataset
- D) The GPU

<details><summary>Reveal Answer</summary>

**B.** Shared definitions remove skew.

</details>

### Question 6 — Hard

**A model is great offline and poor online. First suspect?**

- A) The GPU
- B) Feature skew between the offline and online computation
- C) The network
- D) The user

<details><summary>Reveal Answer</summary>

**B.** Offline/online divergence is the classic cause.

</details>

### Question 7 — Hard

**Why does the feature store prevent leakage at training time?**

- A) It encrypts data
- B) The point-in-time join returns only features known before the label
- C) It compresses data
- D) It does not

<details><summary>Reveal Answer</summary>

**B.** Temporal correctness is built in.

</details>

### Question 8 — Hard

**When is a feature store overkill?**

- A) Never
- B) For a single model with no reuse and no real-time path, a plain table suffices
- C) Always
- D) When you have a GPU

<details><summary>Reveal Answer</summary>

**B.** Adopt it when reuse and consistency justify the operational cost.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You understand feature stores. |
| 5-6 | Review skew and point-in-time joins. |
| < 5 | Re-read the lecture. |
