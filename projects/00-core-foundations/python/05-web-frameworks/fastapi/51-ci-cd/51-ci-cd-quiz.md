# FastAPI 51: CI/CD — Quiz

> **Topic Overview**: The gauntlet, matrices, caching, migrations, and rollback.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What belongs in the CI gauntlet?**
- A) Deploy only
- B) Lint, type-check, unit tests, and a build
- C) Load test only
- D) Docs only

<details><summary>Reveal Answer</summary>**B.** Every change, every time.</details>

### Question 2 — Easy
**What is matrix testing?**
- A) 3D tests
- B) Running the suite across Python/dependency versions
- C) Parallel tests
- D) GUI tests

<details><summary>Reveal Answer</summary>**B.** Compatibility coverage.</details>

### Question 3 — Medium
**What should CI cache?**
- A) Nothing
- B) Dependency installs keyed by lockfile, so unchanged deps skip reinstall
- C) Test results
- D) The database

<details><summary>Reveal Answer</summary>**B.** Fast, deterministic runs.</details>

### Question 4 — Medium
**Why run migrations in the pipeline, not by hand?**
- A) Speed
- B) Deterministic, reviewable, and reversible schema change as code
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Schema as code.</details>

### Question 5 — Medium
**What does a rollout need?**
- A) `kubectl apply` only
- B) Staged traffic, health gates, and an abort path
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Controlled exposure.</details>

### Question 6 — Hard
**What makes rollback one command?**
- A) Luck
- B) Immutable artifacts, previous-ready manifests, and backward-compatible migrations
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Reversibility by design.</details>

### Question 7 — Hard
**Why must migrations be backward compatible during rollout?**
- A) Style
- B) Old and new code run side by side; a breaking migration kills the old half
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Expand then contract.</details>

### Question 8 — Hard
**What proves the pipeline works?**
- A) Green builds
- B) A recent, exercised rollback or game-day, not just green runs
- C) Speed
- D) Coverage

<details><summary>Reveal Answer</summary>**B.** Test the abort path.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You ship with a working pipeline. |
| 5-6 | Review migrations and rollback. |
| < 5 | Re-read the lecture. |
