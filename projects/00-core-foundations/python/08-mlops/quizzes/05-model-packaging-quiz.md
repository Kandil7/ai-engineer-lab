# MLops 05: Model Packaging — Quiz

> **Topic Overview**: Turning a trained model into a portable, installable artifact.

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

**What is model packaging?**

- A) Compressing a file
- B) Bundling the model, its code, dependencies, and config into a portable artifact
- C) Training a model
- D) Serving a model

<details><summary>Reveal Answer</summary>

**B.** The artifact must run elsewhere.

</details>

### Question 2 — Easy

**Why is a raw weights file insufficient?**

- A) It is too large
- B) It lacks the code, preprocessing, and versions needed to run it
- C) It is encrypted
- D) It is not

<details><summary>Reveal Answer</summary>

**B.** Weights without the surrounding contract are unusable.

</details>

### Question 3 — Medium

**What is the risk of an unpinned environment in a model package?**

- A) Larger size
- B) The model may produce different results under different library versions
- C) Slower training
- D) No risk

<details><summary>Reveal Answer</summary>

**B.** The package must pin its runtime.

</details>

### Question 4 — Medium

**What belongs in a model package besides the weights?**

- A) Nothing
- B) Preprocessing, the inference contract, config, and version metadata
- C) The training data
- D) The GPU driver

<details><summary>Reveal Answer</summary>

**B.** Everything needed to reproduce inference.

</details>

### Question 5 — Medium

**Why record the packaging format version?**

- A) For storage
- B) So a loader knows how to read it and a migration is possible
- C) For speed
- D) It is not needed

<details><summary>Reveal Answer</summary>

**B.** Formats evolve; the version makes it loadable and migratable.

</details>

### Question 6 — Hard

**How do packaging and reproducibility relate?**

- A) They are unrelated
- B) A reproducible package pins what was used, so the model behaves the same everywhere
- C) Packaging removes the need for versions
- D) Packaging improves accuracy

<details><summary>Reveal Answer</summary>

**B.** Packaging is reproducibility made portable.

</details>

### Question 7 — Hard

**A model works locally but fails in the container. First suspect?**

- A) The GPU
- B) A dependency or preprocessing step missing from the package
- C) The network
- D) The data

<details><summary>Reveal Answer</summary>

**B.** Packaging omitted part of the runtime contract.

</details>

### Question 8 — Hard

**Why sign or checksum a model artifact?**

- A) For speed
- B) To detect tampering or corruption and trust the served artifact
- C) For storage
- D) It is optional

<details><summary>Reveal Answer</summary>

**B.** Integrity is part of supply-chain safety.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can package a model. |
| 5-6 | Review the runtime contract. |
| < 5 | Re-read the lecture. |
