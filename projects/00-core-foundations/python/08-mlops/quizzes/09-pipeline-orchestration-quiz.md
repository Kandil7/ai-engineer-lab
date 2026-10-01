# MLops 09: Pipeline Orchestration — Quiz

> **Topic Overview**: Scheduling and connecting pipeline stages with dependencies, retries, and backfills.

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

**What is a pipeline orchestrator?**

- A) A training script
- B) A system that schedules stages and enforces their dependencies
- C) A model
- D) A dashboard

<details><summary>Reveal Answer</summary>

**B.** It runs the DAG, not the model.

</details>

### Question 2 — Easy

**What is a DAG in this context?**

- A) A model type
- B) A directed acyclic graph of tasks with dependencies
- C) A dataset
- D) A metric

<details><summary>Reveal Answer</summary>

**B.** Tasks and their order.

</details>

### Question 3 — Medium

**Why must pipeline tasks be idempotent?**

- A) For speed
- B) So a retry or backfill does not duplicate or corrupt results
- C) For security
- D) They need not be

<details><summary>Reveal Answer</summary>

**B.** Retries and backfills are routine.

</details>

### Question 4 — Medium

**What is a backfill?**

- A) A retry
- B) Re-running a pipeline for a past time range after a fix
- C) A schema change
- D) A model update

<details><summary>Reveal Answer</summary>

**B.** Backfills replay history.

</details>

### Question 5 — Medium

**Why record task state?**

- A) For storage
- B) So a failed run resumes where it stopped rather than restarting
- C) For security
- D) It is optional

<details><summary>Reveal Answer</summary>

**B.** State enables resume.

</details>

### Question 6 — Hard

**A downstream task ran on stale upstream data. What was missing?**

- A) A GPU
- B) A dependency edge or a freshness check on the upstream output
- C) A retry
- D) A dashboard

<details><summary>Reveal Answer</summary>

**B.** Dependencies must be explicit and enforced.

</details>

### Question 7 — Hard

**Why separate the scheduler from the compute?**

- A) For cost only
- B) The orchestrator coordinates; the workers scale and fail independently
- C) For security
- D) It is not necessary

<details><summary>Reveal Answer</summary>

**B.** Coordination and execution are different concerns.

</details>

### Question 8 — Hard

**How does orchestration relate to the `devmate`/Athar ingestion?**

- A) Not at all
- B) Ingestion is a multi-stage DAG (parse → normalize → chunk → embed → index) that needs retries and backfills
- C) Only for training
- D) Only for reporting

<details><summary>Reveal Answer</summary>

**B.** The ingestion pipeline is orchestration's workload.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can orchestrate a pipeline. |
| 5-6 | Review idempotency and backfills. |
| < 5 | Re-read the lecture. |
