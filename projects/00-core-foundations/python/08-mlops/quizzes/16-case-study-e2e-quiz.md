# MLops 16: End-to-End Case Study — Quiz

> **Topic Overview**: Composing the MLops lifecycle — data, training, registry, deploy, monitor — into one system.

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

**What is the ML lifecycle?**

- A) Only training
- B) Data → train → evaluate → register → deploy → monitor → retrain
- C) Only deployment
- D) Only monitoring

<details><summary>Reveal Answer</summary>

**B.** A cycle, not a one-way path.

</details>

### Question 2 — Easy

**Why is monitoring part of the lifecycle?**

- A) It is optional
- B) Production signals fidelity drive the next retrain (the loop closes)
- C) For storage
- D) For speed

<details><summary>Reveal Answer</summary>

**B.** Monitoring feeds the next iteration.

</details>

### Question 3 — Medium

**What makes the lifecycle reproducible end to end?**

- A) A fast GPU
- B) Versioned data, code, config, and model, with seeds and pinned dependencies
- C) A dashboard
- D) More data

<details><summary>Reveal Answer</summary>

**B.** Every input is identified.

</details>

### Question 4 — Medium

**Where does the eval gate belong?**

- A) Only offline
- B) Before release, enforced in CI, using the golden and adversarial sets
- C) Only online
- D) Nowhere

<details><summary>Reveal Answer</summary>

**B.** The gate blocks a regression from shipping.

</details>

### Question 5 — Medium

**What does the registry provide in the lifecycle?**

- A) Training only
- B) The versioned artifact and its provenance, enabling serving and rollback
- C) Storage only
- D) Nothing

<details><summary>Reveal Answer</summary>

**B.** The registry is the handoff from training to serving.

</details>

### Question 6 — Hard

**A regression reaches production. Which lifecycle stages failed?**

- A) Only deployment
- B) The offline gate missed it and monitoring did not catch it quickly — both stages failed
- C) Only training
- D) None

<details><summary>Reveal Answer</summary>

**B.** Defense in depth means two stages should have caught it.

</details>

### Question 7 — Hard

**How does the case study connect to the 10-week active track?**

- A) It does not
- B) DevMate is the end-to-end vehicle: ingest → RAG eval → deploy → observe, matching the lifecycle
- C) It is the long track
- D) It is separate

<details><summary>Reveal Answer</summary>

**B.** DevMate is the concrete instance of the lifecycle.

</details>

### Question 8 — Hard

**Why is "it works on my machine" insufficient for the lifecycle?**

- A) It is fine
- B) The lifecycle runs across environments; reproducibility and packaging are what make it portable
- C) Only speed matters
- D) It is sufficient

<details><summary>Reveal Answer</summary>

**B.** Portability is a lifecycle requirement.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can compose the ML lifecycle. |
| 5-6 | Review the closed loop and the gate. |
| < 5 | Re-read the lecture. |
