# Advanced Python 39: Poetry — Quiz

> **Topic Overview**: `pyproject.toml` under Poetry 2.x, constraints, groups, and lockfile freshness.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `poetry.lock` record that `pyproject.toml` does not?**
- A) The project's license
- B) The exact resolved version of every package plus file hashes
- C) The Python interpreter path
- D) The test configuration

<details><summary>Reveal Answer</summary>**B.** The manifest holds ranges; the lock holds the decision, pinned with hashes.</details>

### Question 2 — Easy
**What does a bare `"1.2.3"` mean in `[tool.poetry.dependencies]`?**
- A) `>=1.2.3,<2.0.0`
- B) `>1.2.3`
- C) Exactly 1.2.3
- D) Any 1.2.x

<details><summary>Reveal Answer</summary>**C.** A bare version is exact; you must write `^1.2.3` for a caret range.</details>

### Question 3 — Medium
**`^0.2.3` expands to:**
- A) `>=0.2.3,<0.3.0`
- B) `>=0.2.3,<1.0.0`
- C) `>=0.0.0,<0.2.3`
- D) `==0.2.3`

<details><summary>Reveal Answer</summary>**A.** The leftmost non-zero digit is the minor, so it may only reach `0.3.0`.</details>

### Question 4 — Medium
**A dependency group differs from an extra because a group:**
- A) Is published in wheel metadata for users
- B) Is developer-only and never ships with the package
- C) Must be marked optional
- D) Can only hold test dependencies

<details><summary>Reveal Answer</summary>**B.** Groups live in the repository; extras ship inside the package.</details>

### Question 5 — Medium
**`poetry check --lock` fails when:**
- A) The README is missing
- B) The lockfile is absent, or its content hash no longer matches the manifest
- C) A dependency has a pre-release version
- D) The virtualenv has extra packages

<details><summary>Reveal Answer</summary>**B.** It compares the recomputed hash with the stored one and also requires the file to exist.</details>

### Question 6 — Medium
**`poetry install --only main` installs:**
- A) Every group including optional ones
- B) Only runtime dependencies, skipping all development groups
- C) Only the root package
- D) The main and dev groups

<details><summary>Reveal Answer</summary>**B.** `--only` overrides `--with`/`--without`; `main` is the shipped dependency set.</details>

### Question 7 — Hard
**Editing `[tool.ruff]` in `pyproject.toml` makes the lockfile:**
- A) Stale, because any edit changes the hash
- B) Still fresh, because tool configuration is not part of the hashed content
- C) Invalid, because Poetry forbids that table
- D) Automatically regenerated

<details><summary>Reveal Answer</summary>**B.** Only resolution-relevant fields are hashed: dependencies, groups, `requires-python`, sources.</details>

### Question 8 — Hard
**Since Poetry 2.0, running `poetry export` requires:**
- A) Nothing, it is built in
- B) Installing `poetry-plugin-export`
- C) Downgrading to Poetry 1.8
- D) The `--regenerate` flag

<details><summary>Reveal Answer</summary>**B.** `export` and `shell` moved out of the core; install plugins with `poetry self add`.</details>

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can run Poetry in production. |
| 5-6 | Review constraint expansion and the content hash. |
| < 5 | Re-read the lecture. |
