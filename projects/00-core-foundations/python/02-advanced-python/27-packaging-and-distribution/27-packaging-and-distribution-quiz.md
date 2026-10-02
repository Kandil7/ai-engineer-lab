# Advanced Python 27: Packaging and Distribution — Quiz

> **Topic Overview**: `pyproject.toml`, semver, specifiers, and lockfiles.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is `pyproject.toml`?**
- A) A lockfile
- B) The standard package manifest: build system, metadata, dependencies
- C) A test config
- D) A cache

<details><summary>Reveal Answer</summary>**B.** Project manifest.</details>

### Question 2 — Easy
**What does semantic versioning encode?**
- A) Random numbers
- B) MAJOR.MINOR.PATCH: breaking, additive, and fix changes
- C) Dates
- D) Hashes

<details><summary>Reveal Answer</summary>**B.** Compatibility signal.</details>

### Question 3 — Medium
**What does `>=1.2,<2.0` mean?**
- A) Exactly 1.2
- B) A compatible range: at least 1.2, below 2.0
- C) Any version
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Bounded range.</details>

### Question 4 — Medium
**What is an "extra"?**
- A) A cache
- B) Optional dependency groups (`[project.optional-dependencies]`) installed on request
- C) A lock
- D) A test

<details><summary>Reveal Answer</summary>**B.** Optional features.</details>

### Question 5 — Medium
**What are entry points for?**
- A) Caching
- B) Declaring console scripts and plugin hooks a package exposes
- C) Locking
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Installable commands/plugins.</details>

### Question 6 — Hard
**What does a lockfile pin that a manifest does not?**
- A) Nothing
- B) Exact resolved versions and hashes for reproducible installs
- C) The Python version
- D) The license

<details><summary>Reveal Answer</summary>**B.** Reproducibility.</details>

### Question 7 — Hard
**Why does PEP 440 normalization matter?**
- A) Style
- B) It canonicalizes version strings so comparisons/ranges are consistent
- C) It hashes
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** One canonical form.</details>

### Question 8 — Hard
**Why pin exact versions for an application but ranges for a library?**
- A) No reason
- B) Apps want reproducibility; libraries must stay compatible with a range of host environments
- C) For speed
- D) For hashing

<details><summary>Reveal Answer</summary>**B.** Different goals.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You package projects correctly. |
| 5-6 | Review specifiers and lockfiles. |
| < 5 | Re-read the lecture. |
