# Data Engineering 11: Data Quality Frameworks — Quiz

> **Topic Overview**: Six dimensions, Pydantic and Great Expectations, checkpoints
> and data docs, Databand, anomaly detection, the quality gate.

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

**Which is NOT one of the six data-quality dimensions?**

- A) Completeness
- B) Uniqueness
- C) Velocity
- D) Timeliness

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: The six are completeness, validity, uniqueness, consistency, timeliness, and accuracy. Velocity is a "big data V", not a quality dimension.

</details>

---

### Question 2 — Easy

**What does Pydantic validate?**

- A) The whole batch
- B) A single record at the boundary
- C) The pipeline's runtime
- D) The storage format

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Pydantic checks one record as it enters, using typed fields and constraints.

</details>

---

### Question 3 — Easy

**What is an "expectation" in Great Expectations?**

- A) A SQL query
- B) A declarative assertion about a column or table
- C) A scheduled task
- D) A data file

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: An expectation is a named check like `expect_column_values_to_not_be_null`.

</details>

---

### Question 4 — Medium

**What does a Great Expectations checkpoint produce?**

- A) A new table
- B) A validation result listing passed and failed expectations
- C) A trained model
- D) A dashboard

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Running a suite against a batch yields a result with per-expectation pass/fail and samples.

</details>

---

### Question 5 — Medium

**What can a batch-level expectation catch that Pydantic cannot?**

- A) A single invalid field
- B) Duplicate keys across the whole dataset
- C) A wrong type
- D) A missing import

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Uniqueness and distributions are dataset properties, invisible to a record-level validator.

</details>

---

### Question 6 — Medium

**What layer does Databand observe?**

- A) Only the data values
- B) The pipeline: durations, volumes, and dependency health
- C) Only the schema
- D) Only the storage cost

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Databand watches the pipeline's behavior and trends, not just the data's static validity.

</details>

---

### Question 7 — Medium

**Why is a volume anomaly detector needed even when static checks pass?**

- A) Static checks are slow
- B) A run can be valid yet half the usual size, signaling a broken extract
- C) It saves storage
- D) It replaces the schema

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Rows can all be individually valid while the source silently truncated the batch.

</details>

---

### Question 8 — Hard

**Where in the pipeline should the quality gate sit?**

- A) After load
- B) Between transform and load
- C) Before extract
- D) Only at the end of the week

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The gate validates transformed rows before load, so bad data never reaches the destination.

</details>

---

### Question 9 — Hard

**Why must quality failures be loud rather than silent?**

- A) To reduce logs
- B) A silent failure lets bad data propagate into the index and cited answers
- C) To satisfy auditors only
- D) To speed up the pipeline

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A failing check that neither stops the pipeline nor alerts is noise; the error still lands downstream.

</details>

---

### Question 10 — Hard

**What is the smallest useful quality floor?**

- A) A record schema, a uniqueness check on the key, and a volume anomaly check
- B) Every expectation imaginable
- C) Only a dashboard
- D) Only periodic spot checks

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Those three layers — record, key uniqueness, temporal volume — catch most real failures at trivial cost.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | C | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Hard |
| 9 | B | Hard |
| 10 | A | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for feature stores |
| 7-8 | Proficient | Review the anomaly layer |
| 5-6 | Developing | Re-study the six dimensions |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [12 - Feature Stores](../12-feature-stores/12-feature-stores-quiz.md)
