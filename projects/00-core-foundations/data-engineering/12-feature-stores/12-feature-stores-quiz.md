# Data Engineering 12: Feature Stores — Quiz

> **Topic Overview**: Training-serving skew, the four components, offline/online/on-demand
> features, Feast/Tecton/Feathr, point-in-time correctness, feature versioning.

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

**What is training-serving skew?**

- A) A hardware mismatch
- B) The same-named feature differs between training and serving paths
- C) A slow inference server
- D) A version mismatch in Git

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Skew is the gap between feature values in training versus serving, caused by two code paths.

</details>

---

### Question 2 — Easy

**Which component is the single source of truth for feature definitions?**

- A) Online store
- B) Registry
- C) Serving API
- D) Offline store

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The registry holds the definitions; both paths derive their logic from it.

</details>

---

### Question 3 — Easy

**What is the online store used for?**

- A) Long-term archival
- B) Low-latency feature reads at inference
- C) Training data joins
- D) Batch aggregation

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The online store (Redis/DynamoDB) serves the latest values fast for inference.

</details>

---

### Question 4 — Medium

**Why does a naive "as of now" feature join leak data into training?**

- A) It is too slow
- B) A feature value that depends on future data ends up in the training row
- C) It drops rows
- D) It uses the wrong schema

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Joining as-of-now lets the model see data created after the label, inflating training metrics.

</details>

---

### Question 5 — Medium

**What does point-in-time correctness require?**

- A) Joining features as they existed at the label's timestamp
- B) Using the newest value always
- C) Training only on recent data
- D) Randomizing timestamps

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Each feature is joined as of the label's creation time, never later.

</details>

---

### Question 6 — Medium

**Which feature store is the self-hosted, warehouse-first option?**

- A) Tecton
- B) Feast
- C) Databand
- D) DVC

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Feast is open source, using your warehouse as offline store and Redis/DynamoDB as online store.

</details>

---

### Question 7 — Medium

**What is materialization in a feature store?**

- A) Deleting old features
- B) Copying computed features from the offline to the online store
- C) Training a model
- D) Versioning a feature

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Materialization fills the online store so inference can read features fast.

</details>

---

### Question 8 — Hard

**Which feature store is the managed, streaming-first option?**

- A) Feast
- B) Tecton
- C) Feathr
- D) Great Expectations

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tecton is the managed platform with built-in batch, streaming, and real-time features.

</details>

---

### Question 9 — Hard

**How does a feature store prevent skew by construction?**

- A) It retrains the model daily
- B) One definition in the registry, one computation, served to both paths
- C) It logs every prediction
- D) It drops unused features

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Both paths read the same materialized value from the same definition, so drift is impossible.

</details>

---

### Question 10 — Hard

**How does feature versioning connect to the cache-key discipline?**

- A) It is unrelated
- B) The feature version appears in the cache key, so a redefinition invalidates downstream artifacts
- C) It clears the model registry
- D) It shortens the cache TTL

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A feature-version bump keys invalidation, mirroring the source_version discipline from topic 06.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Medium |
| 5 | A | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Hard |
| 9 | B | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for feature pipelines |
| 7-8 | Proficient | Review point-in-time joins |
| 5-6 | Developing | Re-study the components |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [13 - Feature Pipelines](../13-feature-pipelines/13-feature-pipelines-quiz.md)
