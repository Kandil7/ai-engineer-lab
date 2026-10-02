# FastAPI 22: CORS — Quiz

> **Topic Overview**: Cross-origin policy and correct configuration.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does CORS control?**
- A) Authentication
- B) Whether a browser lets a page call a different origin
- C) Caching
- D) Routing

<details><summary>Reveal Answer</summary>**B.** Browser same-origin policy exception.</details>

### Question 2 — Easy
**What does a preflight request use?**
- A) `GET`
- B) `OPTIONS`
- C) `HEAD`
- D) `POST`

<details><summary>Reveal Answer</summary>**B.** Preflight `OPTIONS`.</details>

### Question 3 — Medium
**Why is `allow_origins=["*"]` wrong with credentials?**
- A) It is fine
- B) Browsers reject wildcard origin when credentials are included; you must list origins
- C) For speed
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Explicit origins required.</details>

### Question 4 — Medium
**What generates CORS headers?**
- A) The browser
- B) The server, via `CORSMiddleware`
- C) The proxy only
- D) The database

<details><summary>Reveal Answer</summary>**B.** Server sets them.</details>

### Question 5 — Medium
**What is the most common misconfiguration?**
- A) Too few methods
- B) Too permissive (wildcard origin) or missing headers on error responses
- C) Wrong port
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Over-permission and error-path gaps.</details>

### Question 6 — Hard
**Why do you list allowed methods/headers rather than allow all?**
- A) Speed
- B) Least privilege: only what the frontend needs
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Minimal surface.</details>

### Question 7 — Hard
**Why can CORS errors look like network failures?**
- A) They are
- B) The browser hides the response when headers are missing, so the real error is obscured
- C) They cache
- D) They sort

<details><summary>Reveal Answer</summary>**B.** Opaque failure.</details>

### Question 8 — Hard
**Is CORS a server security control?**
- A) Yes
- B) No; it is a browser control; the server must still authenticate and authorize
- C) It encrypts
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Browser policy, not authz.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You configure CORS correctly. |
| 5-6 | Review preflight and credentials. |
| < 5 | Re-read the lecture. |
