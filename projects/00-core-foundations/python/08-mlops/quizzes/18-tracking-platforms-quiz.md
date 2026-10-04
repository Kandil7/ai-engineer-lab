# MLops 18: Tracking Platforms — Quiz

> **Topic Overview**: MLflow, W&B, Comet, Neptune, Sacred, and choosing a platform without lock-in.

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

**What five fields does a run record hold?**

- A) id, config, metrics, artifacts, provenance
- B) weights, biases, loss
- C) train, val, test
- D) code, data, GPU

<details><summary>Reveal Answer</summary>

**A.** The contract every tracker satisfies.

</details>

### Question 2 — Easy

**Which platform is open-source and self-hosted with a full lifecycle?**

- A) W&B
- B) MLflow
- C) Comet
- D) Sacred

<details><summary>Reveal Answer</summary>

**B.** Tracking, Projects, Models, and a Registry.

</details>

### Question 3 — Medium

**What is the main appeal of W&B?**

- A) Self-hosting
- B) Managed collaboration: dashboards, reports, sweeps
- C) No internet
- D) Free GPUs

<details><summary>Reveal Answer</summary>

**B.** Sharing and collaboration are first-class.

</details>

### Question 4 — Medium

**What is Sacred?**

- A) A managed SaaS
- B) A minimal library for config/seed capture with no server
- C) A registry
- D) A serving system

<details><summary>Reveal Answer</summary>

**B.** Zero infrastructure, config capture only.

</details>

### Question 5 — Medium

**What is the first selection question for a tracker?**

- A) The logo color
- B) Can the data leave your infrastructure (data residency)?
- C) The number of users
- D) The Python version

<details><summary>Reveal Answer</summary>

**B.** Hosting decides before features do.

</details>

### Question 6 — Hard

**Why is a tracker adapter better than direct `wandb.log` calls?**

- A) It is faster
- B) Switching platforms becomes a config change, not a rewrite
- C) It uses less disk
- D) It trains better models

<details><summary>Reveal Answer</summary>

**B.** The contract is yours; the backend is swappable.

</details>

### Question 7 — Hard

**When is Neptune the strongest choice?**

- A) A solo notebook
- B) Many long-running runs with high-frequency logging
- C) A tiny dataset
- D) No metrics

<details><summary>Reveal Answer</summary>

**B.** It is built for large-scale, long-running metadata.

</details>

### Question 8 — Hard

**Why log a reference for large artifacts instead of the blob?**

- A) References are prettier
- B) Pushing gigabytes through a tracking API is a surprise bill and slow
- C) Blobs cannot be stored
- D) It is required by law

<details><summary>Reveal Answer</summary>

**B.** Object storage holds the bytes; the tracker holds the pointer.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can choose and integrate a tracker. |
| 5-6 | Review the contract and the selection order. |
| < 5 | Re-read the lecture. |
