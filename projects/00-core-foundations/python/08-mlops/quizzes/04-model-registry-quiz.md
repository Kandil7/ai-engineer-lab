# MLops 04: Model Registry — Quiz

> **Topic Overview**: Versioned model artifacts with provenance, an eval gate, and rollback.

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

**What is a model registry?**

- A) A folder of model files
- B) A versioned catalog of model artifacts with their provenance and metrics
- C) A training script
- D) A GPU driver

<details><summary>Reveal Answer</summary>

**B.** It is the source of truth for released models.

</details>

### Question 2 — Easy

**What does a registry entry record?**

- A) Only the accuracy
- B) Base model, artifact, data/config versions, and eval results
- C) The author's email only
- D) Nothing

<details><summary>Reveal Answer</summary>

**B.** Provenance plus results.

</details>

### Question 3 — Medium

**Why are registered versions immutable?**

- A) For storage
- B) So a released model can always be reproduced and rolled back to
- C) For speed
- D) To save money

<details><summary>Reveal Answer</summary>

**B.** Immutability preserves history and rollback.

</details>

### Question 4 — Medium

**What is the eval gate?**

- A) A payment step
- B) A release is blocked unless the model passes the golden/adversarial sets
- C) A lint check
- D) A GPU check

<details><summary>Reveal Answer</summary>

**B.** Evaluate before release, never after.

</details>

### Question 5 — Medium

**A model improves eval loss but fails faithfulness. What happens?**

- A) Release it
- B) The gate blocks it; improving one metric while failing another is the tradeoff the gate catches
- C) Ignore faithfulness
- D) Lower the threshold

<details><summary>Reveal Answer</summary>

**B.** The gate exists for exactly this.

</details>

### Question 6 — Hard

**Why must an adapter be registered with its base model version?**

- A) For disk space
- B) The adapter is meaningless without its exact base
- C) For speed
- D) It is not needed

<details><summary>Reveal Answer</summary>

**B.** The pair is the artifact.

</details>

### Question 7 — Hard

**What makes rollback mechanical?**

- A) Keeping only the latest model
- B) Keeping prior versions registered with their artifacts available
- C) Git tags
- D) A backup script

<details><summary>Reveal Answer</summary>

**B.** Rollback needs the previous version present.

</details>

### Question 8 — Hard

**Why is rollback itself a recorded decision?**

- A) For storage
- B) It signals the release gate or eval set needs attention, and it has its own tradeoffs
- C) For speed
- D) It is not

<details><summary>Reveal Answer</summary>

**B.** A rollback is a signal and a decision, not a silent action.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can run a registry and gate. |
| 5-6 | Review immutability and the gate. |
| < 5 | Re-read the lecture. |
