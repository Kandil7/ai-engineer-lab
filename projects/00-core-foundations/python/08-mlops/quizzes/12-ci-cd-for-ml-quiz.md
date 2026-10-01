# MLops 12: CI/CD for ML — Quiz

> **Topic Overview**: Extending CI/CD to ML — data and model tests, eval gates, and safe deployment.

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

**How does CI/CD for ML differ from software CI/CD?**

- A) It does not
- B) It also tests data and models, not only code
- C) It skips tests
- D) It has no pipeline

<details><summary>Reveal Answer</summary>

**B.** Data and models are first-class artifacts.

</details>

### Question 2 — Easy

**What is an eval gate in CI?**

- A) A payment step
- B) A build that fails when model metrics drop below a baseline
- C) A lint check
- D) A GPU check

<details><summary>Reveal Answer</summary>

**B.** The regression guard for models.

</details>

### Question 3 — Medium

**Why test data in CI?**

- A) For speed
- B) A schema or distribution break should fail before training, not after
- C) It is required
- D) Data cannot be tested

<details><summary>Reveal Answer</summary>

**B.** Fail early, cheaply.

</details>

### Question 4 — Medium

**Why is a model release gated rather than automatic?**

- A) For cost
- B) A model that fails the golden/adversarial set must not ship
- C) For speed
- D) It is automatic

<details><summary>Reveal Answer</summary>

**B.** Evaluate before release.

</details>

### Question 5 — Medium

**What is a smoke test after deployment?**

- A) A load test
- B) A minimal check that the deployed service responds correctly
- C) A unit test
- D) A lint

<details><summary>Reveal Answer</summary>

**B.** The first post-deploy confidence check.

</details>

### Question 6 — Hard

**Why is rollback part of CD for ML?**

- A) For cost
- B) A model can regress in production; the pipeline must revert to a prior version
- C) For speed
- D) It is not

<details><summary>Reveal Answer</summary>

**B.** Reversibility is a deployment property.

</details>

### Question 7 — Hard

**What belongs in the artifact the CD pipeline ships?**

- A) Only the weights
- B) The model, its runtime contract, the config, and the data/model versions
- C) The training data
- D) The GPU driver

<details><summary>Reveal Answer</summary>

**B.** Everything needed to run and to reproduce.

</details>

### Question 8 — Hard

**A prompt change is merged. Why must it run the eval gate too?**

- A) It should not
- B) A prompt is part of the system; its change can regress quality like any code change
- C) For speed
- D) Prompts are irrelevant

<details><summary>Reveal Answer</summary>

**B.** Prompts are versioned assets under the same gate.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can set up ML CI/CD. |
| 5-6 | Review the eval gate and rollback. |
| < 5 | Re-read the lecture. |
