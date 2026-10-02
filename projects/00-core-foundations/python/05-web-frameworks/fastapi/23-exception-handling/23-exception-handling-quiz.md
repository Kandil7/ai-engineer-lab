# FastAPI 23: Exception Handling — Quiz

> **Topic Overview**: `HTTPException` and custom exception handlers.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you return an error status from a handler?**
- A) `raise HTTPException(status_code=..., detail=...)`
- B) `return None`
- C) `print`
- D) `abort`

<details><summary>Reveal Answer</summary>**A.** Raise an HTTP error.</details>

### Question 2 — Easy
**What does the default error body look like?**
- A) Empty
- B) `{"detail": ...}`
- C) HTML
- D) Plain text

<details><summary>Reveal Answer</summary>**B.** Default envelope.</details>

### Question 3 — Medium
**What does `@app.exception_handler(Foo)` do?**
- A) Logs
- B) Registers a handler translating an exception into a response
- C) Caches
- D) Routes

<details><summary>Reveal Answer</summary>**B.** Centralized translation.</details>

### Question 4 — Medium
**Why is catching broad exceptions in handlers risky?**
- A) Slow
- B) It hides real bugs and can leak internals in the response
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Masking and leakage.</details>

### Question 5 — Medium
**What status for a validation error?**
- A) 400
- B) 422
- C) 500
- D) 404

<details><summary>Reveal Answer</summary>**B.** 422.</details>

### Question 6 — Hard
**Why must a 500 never leak a stack trace?**
- A) Style
- B) It exposes internals and paths useful to an attacker
- C) For speed
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Log internally, return generic.</details>

### Question 7 — Hard
**How do you attach an error code for clients?**
- A) A custom envelope/handler with a stable code, not just the message
- B) In the status only
- C) In a header only
- D) You cannot

<details><summary>Reveal Answer</summary>**A.** Stable machine-readable codes.</details>

### Question 8 — Hard
**Why prefer raising over returning error sentinels?**
- A) Style
- B) Exceptions propagate correctly through dependencies and middleware and centralize handling
- C) Caching
- D) Speed

<details><summary>Reveal Answer</summary>**B.** Clean control flow.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You handle errors well. |
| 5-6 | Review handlers and status codes. |
| < 5 | Re-read the lecture. |
