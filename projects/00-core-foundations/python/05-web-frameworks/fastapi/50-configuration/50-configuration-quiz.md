# FastAPI 50: Configuration — Quiz

> **Topic Overview**: Typed settings, precedence, secrets, and feature flags.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why typed, validated settings?**
- A) Style
- B) A missing or malformed value fails at startup instead of mid-request
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Fail fast.</details>

### Question 2 — Easy
**What is the precedence chain, highest first?**
- A) Code, env, files
- B) Env/secret store over files over code defaults
- C) Files over env
- D) Random

<details><summary>Reveal Answer</summary>**B.** Explicit overrides implicit.</details>

### Question 3 — Medium
**Where do secrets live?**
- A) The repo
- B) Env vars in dev, a secret manager in production, never git
- C) The docs
- D) The code

<details><summary>Reveal Answer</summary>**B.** Out of version control.</details>

### Question 4 — Medium
**Why per-environment config?**
- A) Style
- B) Dev, staging, and prod differ in hosts, keys, and limits; one settings class reads per-env values
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Environment-specific truth.</details>

### Question 5 — Medium
**What is a feature flag?**
- A) A setting
- B) A runtime toggle keyed per user or percentage, enabling safe rollouts and kills
- C) A cache
- D) A test

<details><summary>Reveal Answer</summary>**B.** Controlled exposure.</details>

### Question 6 — Hard
**Why validate settings at import/startup?**
- A) Style
- B) A bad value discovered on the first request is an outage, not a bug
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Boot-time validation.</details>

### Question 7 — Hard
**What is the risk of boolean env parsing?**
- A) None
- B) The string `"False"` is truthy; parse explicitly or use a settings library
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Strings are not bools.</details>

### Question 8 — Hard
**Why keep secrets out of logs and error messages?**
- A) Size
- B) Logs replicate everywhere and live long; one leak spreads
- C) Speed
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Redact the boundary.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You configure services safely. |
| 5-6 | Review precedence, secrets, flags. |
| < 5 | Re-read the lecture. |
