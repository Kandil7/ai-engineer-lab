# FastAPI 41: API Security — Quiz

> **Topic Overview**: Rate limits, CORS allowlists, headers, size caps, SSRF, secrets.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What do rate limits protect?**
- A) Accuracy
- B) Availability and cost against abuse and floods
- C) Sorting
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Throttle, not trust.</details>

### Question 2 — Easy
**Per what should limits be keyed?**
- A) Path only
- B) Identity (user, API key) or IP, not just the route
- C) Method
- D) Time

<details><summary>Reveal Answer</summary>**B.** Per-actor buckets.</details>

### Question 3 — Medium
**Why is CORS `*` wrong for credentialed APIs?**
- A) Style
- B) Browsers reject wildcard origins with credentials; enumerate the real origins
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Explicit allowlist.</details>

### Question 4 — Medium
**Why cap request size?**
- A) Speed
- B) Unbounded bodies exhaust memory and workers
- C) Sorting
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Size is an attack input.</details>

### Question 5 — Medium
**What is SSRF?**
- A) A cache bug
- B) The server fetching attacker-chosen URLs, reaching internal services
- C) A slow query
- D) A header

<details><summary>Reveal Answer</summary>**B.** Validate and restrict outbound targets.</details>

### Question 6 — Hard
**How should secrets reach the app?**
- A) Hardcoded
- B) Env vars or a secret manager, never the repo
- C) The docs
- D) The database

<details><summary>Reveal Answer</summary>**B.** No secrets in code.</details>

### Question 7 — Hard
**Why set CSRF protection with cookie auth?**
- A) Style
- B) Browsers attach cookies automatically, so forged cross-site requests ride them
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** SameSite plus tokens.</details>

### Question 8 — Hard
**What makes security headers defense in depth?**
- A) Nothing
- B) Each narrows one abuse path (framing, sniffing, XSS) independent of app bugs
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Layered narrowing.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You harden APIs. |
| 5-6 | Review limits, CORS, SSRF, secrets. |
| < 5 | Re-read the lecture. |
