# FastAPI 48: Docker for FastAPI — Quiz

> **Topic Overview**: Multi-stage builds, layer caching, and non-root images.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why multi-stage builds?**
- A) Speed
- B) Build tools stay in the builder stage; the runtime image stays small and clean
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Slim production image.</details>

### Question 2 — Easy
**What makes layer caching work?**
- A) Luck
- B) Ordering: stable layers (deps) before changing layers (code)
- C) Big layers
- D) Small layers

<details><summary>Reveal Answer</summary>**B.** Deps first, code last.</details>

### Question 3 — Medium
**Slim vs alpine: the tradeoff?**
- A) Alpine always wins
- B) Alpine is smaller but can break wheels and slow builds; slim is the compatible default
- C) Slim is smaller
- D) No difference

<details><summary>Reveal Answer</summary>**B.** Compatibility first.</details>

### Question 4 — Medium
**Why run as non-root?**
- A) Speed
- B) A container breakout or file write lands without root privileges
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Least privilege.</details>

### Question 5 — Medium
**What does `.dockerignore` prevent?**
- A) Builds
- B) Shipping venvs, `.git`, and secrets into the image context
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Lean build context.</details>

### Question 6 — Hard
**Why pin the base image by digest?**
- A) Speed
- B) Tags move; the digest guarantees the exact bits you tested
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Reproducible images.</details>

### Question 7 — Hard
**Why does `COPY . .` before `pip install` destroy caching?**
- A) It does not
- B) Any code change invalidates the dependency layer and reinstalls everything
- C) Speed
- D) Size

<details><summary>Reveal Answer</summary>**B.** Copy lockfiles first.</details>

### Question 8 — Hard
**What healthcheck belongs in the image?**
- A) None
- B) A cheap endpoint probe the orchestrator can poll
- C) The test suite
- D) A shell loop

<details><summary>Reveal Answer</summary>**B.** Observable containers.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You containerize correctly. |
| 5-6 | Review stages, caching, non-root. |
| < 5 | Re-read the lecture. |
