# Advanced Python 40: uv — Quiz

> **Topic Overview**: `pyproject.toml` under uv, the universal `uv.lock`, sync flags, and supply-chain security.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `uv.lock` record that `pyproject.toml` does not?**
- A) The project's license
- B) The exact resolved version of every package plus per-file hashes
- C) The Python interpreter path
- D) The test configuration

<details><summary>Reveal Answer</summary>**B.** The manifest holds ranges; the lock holds the decision, pinned with sha256 hashes for every platform's wheels.</details>

### Question 2 — Easy
**What does a bare `"1.2.3"` mean in `[project] dependencies` under uv?**
- A) `>=1.2.3,<2.0.0`
- B) `>1.2.3`
- C) Exactly 1.2.3
- D) Any 1.2.x

<details><summary>Reveal Answer</summary>**C.** uv reads PEP 508 only; there is no caret syntax anywhere in a uv manifest.</details>

### Question 3 — Medium
**`uv sync --frozen` differs from `uv sync --locked` because `--frozen`:**
- A) Fails when the lockfile is stale
- B) Skips resolution entirely and installs from the existing lock
- C) Downloads without hash verification
- D) Removes the dev group

<details><summary>Reveal Answer</summary>**B.** `--locked` resolves and fails if the lock would change; `--frozen` never resolves, so it will install a stale lock without complaint.</details>

### Question 4 — Medium
**A dependency group differs from an extra because a group:**
- A) Is published in wheel metadata for users
- B) Is developer-only and never ships with the package
- C) Must be marked optional
- D) Can only hold test dependencies

<details><summary>Reveal Answer</summary>**B.** Groups live in `[dependency-groups]` in the repository; extras ship inside the package.</details>

### Question 5 — Medium
**Which group does plain `uv sync` install without any flag?**
- A) Every declared group
- B) Only `main`
- C) `main` plus the `dev` group
- D) Only optional groups

<details><summary>Reveal Answer</summary>**C.** `dev` is the default group under PEP 735 semantics; other groups need `--group` or `--all-groups`.</details>

### Question 6 — Medium
**`uv sync --only-group lint` installs:**
- A) Main dependencies plus lint
- B) Exactly the lint group, excluding main dependencies
- C) Every group except lint
- D) Nothing; the flag only validates

<details><summary>Reveal Answer</summary>**B.** "Only include dependencies from the specified dependency group" — main is excluded, unlike `--group lint`.</details>

### Question 7 — Hard
**Setting `exclude-newer = "2026-06-01T00:00:00Z"` in `[tool.uv]`:**
- A) Pins every dependency to its June 1 version
- B) Makes resolution ignore uploads after June 1, acting as a review cooldown
- C) Deletes newer packages from the cache
- D) Only affects `uv audit`

<details><summary>Reveal Answer</summary>**B.** It is a resolution-time cutoff, not a pin; the lockfile is what actually pins. Per-package opt-out exists via `exclude-newer-package`.</details>

### Question 8 — Hard
**The malware check (`UV_MALWARE_CHECK=1`) must run at sync time rather than as a separate audit because:**
- A) OSV only accepts sync-time queries
- B) PyPI quarantine removes malware from the index but not from object storage, so a lockfile can still point at it
- C) `uv audit` cannot read `uv.lock`
- D) Malware advisories expire after install

<details><summary>Reveal Answer</summary>**B.** Lockfiles reference object storage directly, so index-level removal is invisible at install time; the check must abort before installation.</details>

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can run uv in production. |
| 5-6 | Review the `--locked`/`--frozen` distinction and the security layers. |
| < 5 | Re-read the lecture. |
