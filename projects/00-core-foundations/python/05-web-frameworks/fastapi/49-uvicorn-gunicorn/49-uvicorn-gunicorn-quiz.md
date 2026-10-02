# FastAPI 49: Uvicorn and Gunicorn — Quiz

> **Topic Overview**: Server roles, worker math, and production flags.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What are the two roles?**
- A) Dev/prod
- B) Uvicorn serves ASGI in a worker; Gunicorn manages the worker processes
- C) HTTP/HTTPS
- D) Cache/app

<details><summary>Reveal Answer</summary>**B.** Manager plus servers.</details>

### Question 2 — Easy
**What is the worker-math starting point?**
- A) 100
- B) Roughly `2 × cores + 1` for sync workers, tuned by measurement
- C) 1
- D) Cores × 100

<details><summary>Reveal Answer</summary>**B.** Rule of thumb, then measure.</details>

### Question 3 — Medium
**Why does memory bind before cores?**
- A) It does not
- B) Each worker holds its own app and model memory, so RAM caps workers first
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Memory per worker.</details>

### Question 4 — Medium
**Why is `--reload` dev-only?**
- A) Slow tests
- B) File watching and auto-restart waste CPU and can recycle workers under load
- C) It disables logs
- D) It needs root

<details><summary>Reveal Answer</summary>**B.** Production stability.</details>

### Question 5 — Medium
**Which worker class for async FastAPI?**
- A) `sync`
- B) `uvicorn.workers.UvicornWorker`
- C) `gevent`
- D) `tornado`

<details><summary>Reveal Answer</summary>**B.** Async worker class.</details>

### Question 6 — Hard
**How do timeouts at the server interact with app timeouts?**
- A) They add
- B) The outer timeout must exceed the inner, or the server kills work the app would finish
- C) They are independent
- D) Inner must exceed outer

<details><summary>Reveal Answer</summary>**B.** Nest timeouts outward.</details>

### Question 7 — Hard
**Why does one worker per core fail with a big model?**
- A) It does not
- B) Model memory times workers exceeds RAM; fewer workers or shared loading is needed
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Memory arithmetic.</details>

### Question 8 — Hard
**What does graceful worker restart give you?**
- A) Nothing
- B) Zero-downtime deploys: old workers drain while new ones warm up
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Rolling restarts.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You serve production ASGI. |
| 5-6 | Review roles, workers, timeouts. |
| < 5 | Re-read the lecture. |
