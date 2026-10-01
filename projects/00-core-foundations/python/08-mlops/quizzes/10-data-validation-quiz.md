# MLops 10: Data Validation — Quiz

> **Topic Overview**: Checking data against expectations at pipeline boundaries so bad data fails loudly.

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

**What is data validation?**

- A) Training a model
- B) Checking data against expected schema and statistical properties before use
- C) Storing data
- D) Deleting data

<details><summary>Reveal Answer</summary>

**B.** Validation is a boundary check.

</details>

### Question 2 — Easy

**Where should validation run?**

- A) Only in production
- B) At the pipeline boundary, before the data is consumed
- C) In the dashboard
- D) Never

<details><summary>Reveal Answer</summary>

**B.** Reject bad data once, at entry.

</details>

### Question 3 — Medium

**Give an example of a schema expectation.**

- A) The file is large
- B) A required column is present and typed; a null rate is within bounds
- C) The GPU is idle
- D) The model is small

<details><summary>Reveal Answer</summary>

**B.** Schema plus statistical checks.

</details>

### Question 4 — Medium

**What is a distribution expectation?**

- A) A file size
- B) A feature's range, mean, or category set staying within a known band
- C) A model metric
- D) A GPU count

<details><summary>Reveal Answer</summary>

**B.** It catches silent data drift.

</details>

### Question 5 — Medium

**What is quarantine?**

- A) Deleting bad data
- B) Diverting failed records for review instead of letting them flow
- C) Encoding data
- D) Compressing data

<details><summary>Reveal Answer</summary>

**B.** Failing records are set aside, not silently dropped or passed.

</details>

### Question 6 — Hard

**Why fail the pipeline on a validation breach rather than warn?**

- A) To slow it down
- B) Bad data downstream corrupts models and answers, often silently
- C) For storage
- D) Warnings suffice

<details><summary>Reveal Answer</summary>

**B.** A loud failure at the boundary prevents silent corruption.

</details>

### Question 7 — Hard

**A model degrades but no code changed. Where does validation help?**

- A) Retraining
- B) It flags the input drift that changed the data distribution under the model
- C) It improves accuracy
- D) It does not

<details><summary>Reveal Answer</summary>

**B.** Input drift is a data-validation catch.

</details>

### Question 8 — Hard

**Why log rejected and missing record counts?**

- A) For storage
- B) So a silent partial ingest is visible as a number, not discovered later
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>

**B.** Counts make silent loss loud.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can validate a pipeline. |
| 5-6 | Review schema vs distribution checks. |
| < 5 | Re-read the lecture. |
