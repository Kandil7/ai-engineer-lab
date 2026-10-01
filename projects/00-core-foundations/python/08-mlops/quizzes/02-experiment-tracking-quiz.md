# MLops 02: Experiment Tracking — Quiz

> **Topic Overview**: Recording runs, parameters, metrics, and artifacts so experiments can be compared and reproduced.

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

**What does an experiment tracker record?**

- A) Only the final accuracy
- B) Parameters, metrics, artifacts, and the run's environment
- C) The model weights only
- D) The developer's name

<details><summary>Reveal Answer</summary>

**B.** A run is the full record, not one number.

</details>

### Question 2 — Easy

**Why track experiments at all?**

- A) For compliance only
- B) To compare runs and reproduce the best one
- C) To slow training
- D) To store images

<details><summary>Reveal Answer</summary>

**B.** Tracking turns training into a comparison.

</details>

### Question 3 — Medium

**What is a run?**

- A) A single epoch
- B) One training execution with its parameters, metrics, and artifacts
- C) A dataset
- D) A model file

<details><summary>Reveal Answer</summary>

**B.** The run is the unit of tracking.

</details>

### Question 4 — Medium

**Why log parameters before training starts?**

- A) It is required by law
- B) So a run is self-describing and comparable even if it crashes
- C) To save memory
- D) To speed up training

<details><summary>Reveal Answer</summary>

**B.** A crashed run with parameters is still informative.

</details>

### Question 5 — Medium

**Two runs show the same metric. What else must you check before declaring a tie?**

- A) Nothing
- B) Parameter differences, data version, and seed
- C) The run duration only
- D) The GPU model only

<details><summary>Reveal Answer</summary>

**B.** Same metric on different inputs is not a tie.

</details>

### Question 6 — Hard

**An ablation needs isolating one variable. What does the tracker give you?**

- A) Faster runs
- B) A paired comparison where only one parameter differs, so the delta is attributable
- C) Less storage use
- D) Automatic model choice

<details><summary>Reveal Answer</summary>

**B.** The tracker makes the controlled comparison possible.

</details>

### Question 7 — Hard

**Why log artifact lineages (data, code commit, config) with the run?**

- A) For storage
- B) To reconstruct the exact experiment later
- C) To slow the pipeline
- D) To bill the user

<details><summary>Reveal Answer</summary>

**B.** Lineage is what makes the run reproducible.

</details>

### Question 8 — Hard

**A metric improved but the run is not reproducible. What is the correct status?**

- A) Ship it
- B) Treat it as unverified; a non-reproducible gain is not evidence
- C) Ignore the difference
- D) Average it with other runs

<details><summary>Reveal Answer</summary>

**B.** Evidence requires reproducibility.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can run a tracked experiment. |
| 5-6 | Review what a run records. |
| < 5 | Re-read the lecture. |
