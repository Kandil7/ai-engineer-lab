# FastAPI 10: Middleware — Quiz

> **Topic Overview**: Request/response middleware and ordering.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is middleware?**
- A) A route
- B) A function wrapping every request/response
- C) A dependency
- D) A template

<details><summary>Reveal Answer</summary>**B.** Cross-cutting around requests.</details>

### Question 2 — Easy
**Give a use for middleware.**
- A) Business logic
- B) Logging, CORS, request IDs, timing
- C) Templating
- D) ORM

<details><summary>Reveal Answer</summary>**B.** Cross-cutting concerns.</details>

### Question 3 — Medium
**How does execution order work for stacked middleware?**
- A) Random
- B) The last added is the outermost, entering first
- C) First added is outermost
- D) Alphabetical

<details><summary>Reveal Answer</summary>**B.** Add order reverses around the request.</details>

### Question 4 — Medium
**Where is `@app.middleware("http")` written?**
- A) On the app with an `async def (request, call_next)`
- B) On a route
- C) In a dependency
- D) In a template

<details><summary>Reveal Answer</summary>**A.** HTTP middleware hook.</details>

### Question 5 — Medium
**What does `call_next(request)` do?**
- A) Retries
- B) Passes the request to the next layer and returns the response
- C) Caches
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Chain continuation.</details>

### Question 6 — Hard
**Why must middleware not block the event loop?**
- A) It can
- B) It wraps every request; blocking there stalls all traffic
- C) For speed
- D) It cannot block

<details><summary>Reveal Answer</summary>**B.** Global path.</details>

### Question 7 — Hard
**Why add a request ID in middleware?**
- A) Style
- B) To correlate logs and traces for one request across services
- C) For caching
- D) For sorting

<details><summary>Reveal Answer</summary>**B.** Correlation.</details>

### Question 8 — Hard
**What is a pitfall with CORS middleware and error responses?**
- A) None
- B) Errors raised outside the middleware chain can lack CORS headers, so the browser hides the real error
- C) It is faster
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Order matters for error paths.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You use middleware well. |
| 5-6 | Review ordering and blocking. |
| < 5 | Re-read the lecture. |
