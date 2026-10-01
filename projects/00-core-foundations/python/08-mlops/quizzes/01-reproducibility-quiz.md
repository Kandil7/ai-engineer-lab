# MLops 01: Reproducibility — Quiz

> **Topic Overview**: Making an ML run reproducible — seeds, pinned dependencies, recorded configs, and deterministic pipelines.

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

**What makes an experiment reproducible?**

- A) A fast GPU
- B) A recorded config, pinned dependencies, and a fixed seed
- C) A large dataset
- D) More epochs

<details><summary>Reveal Answer</summary>

**B.** Reproducibility needs the same code, data, and randomness controls.

</details>

### Question 2 — Easy

**Why pin dependency versions?**

- A) To save disk space
- B) Because a library update can change results silently
- C) To speed up installs
- D) To avoid GPUs

<details><summary>Reveal Answer</summary>

**B.** Floating versions mean the environment changes under the experiment.

</details>

### Question 3 — Medium

**What is the role of the random seed?**

- A) It makes training faster
- B) It fixes the stochastic choices (shuffling, init, dropout) so a re-run matches
- C) It improves accuracy
- D) It reduces memory

<details><summary>Reveal Answer</summary>

**B.** Without a fixed seed, every run samples differently.

</details>

### Question 4 — Medium

**A run has no recorded config but "the same code". Is it reproducible?**

- A) Yes, code is enough
- B) No; hyperparameters, data version, and seed are also inputs
- C) Only if the GPU matches
- D) Only if it is small

<details><summary>Reveal Answer</summary>

**B.** The config is part of the experiment's inputs.

</details>

### Question 5 — Medium

**Why record the data version in the config?**

- A) To save space
- B) A different dataset is a different experiment
- C) For licensing
- D) It is optional

<details><summary>Reveal Answer</summary>

**B.** Data is an input; changing it changes the run.

</details>

### Question 6 — Hard

**GPU nondeterminism can make two "identical" runs differ slightly. What is the practical response?**

- A) Ignore it; it never matters
- B) Accept a tolerance, record the environment, and re-run to measure the variance
- C) Buy a bigger GPU
- D) Remove the seed

<details><summary>Reveal Answer</summary>

**B.** Some nondeterminism is unavoidable; characterize it rather than pretend it is absent.

</details>

### Question 7 — Hard

**A result cannot be reproduced. Rank the first three things to check.**

- A) GPU, network, cost
- B) Seed, dependency versions, data version
- C) Learning rate, batch size, epochs
- D) File names, comments, README

<details><summary>Reveal Answer</summary>

**B.** The usual culprits are the randomness and environment inputs.

</details>

### Question 8 — Hard

**Why is a lockfile a reproducibility tool?**

- A) It compiles faster
- B) It pins the exact resolved dependency graph, so the environment is identical across machines
- C) It shrinks the model
- D) It encrypts data

<details><summary>Reveal Answer</summary>

**B.** Versions resolved once can be reinstalled exactly elsewhere.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can make a run reproducible. |
| 5-6 | Review seeds and dependency pinning. |
| < 5 | Re-read the lecture. |
