# FastAPI 09: Dependency Injection — Quiz

> **Topic Overview**: `Depends`, sub-dependencies, and shared resources.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you inject a dependency?**
- A) `x: T = Depends(fn)`
- B) `x = fn()`
- C) `@inject`
- D) `x: T`

<details><summary>Reveal Answer</summary>**A.** `Depends` resolves it.</details>

### Question 2 — Easy
**What is a common use of DI?**
- A) Routing
- B) Sharing a DB session, auth context, or config across handlers
- C) Templating
- D) Serving

<details><summary>Reveal Answer</summary>**B.** Per-request resources.</details>

### Question 3 — Medium
**Can dependencies depend on other dependencies?**
- A) No
- B) Yes; they compose into a dependency graph
- C) Only one level
- D) Only for auth

<details><summary>Reveal Answer</summary>**B.** Nested dependencies.</details>

### Question 4 — Medium
**How do you make a dependency with cleanup?**
- A) `yield` in a generator dependency; code after runs at teardown
- B) `finally`
- C) A middleware
- D) You cannot

<details><summary>Reveal Answer</summary>**A.** Generator-based DI.</details>

### Question 5 — Medium
**Why is DI good for testing?**
- A) Speed
- B) `app.dependency_overrides` swaps the real dependency for a fake
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Override in tests.</details>

### Question 6 — Hard
**When are generator dependencies torn down relative to the response?**
- A) Before
- B) After the response is sent (with `yield`), which matters for streaming
- C) Never
- D) During

<details><summary>Reveal Answer</summary>**B.** Teardown timing.</details>

### Question 7 — Hard
**Why is caching a dependency by default per-request?**
- A) For speed only
- B) The same dependency used by several sub-dependencies resolves once per request unless configured otherwise
- C) It is not
- D) It caches forever

<details><summary>Reveal Answer</summary>**B.** Request-scoped caching.</details>

### Question 8 — Hard
**What is a DI security use case?**
- A) None
- B) A dependency validates the token and returns the current user, rejecting early
- C) Caching
- D) Templating

<details><summary>Reveal Answer</summary>**B.** Auth as a dependency.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You use DI well. |
| 5-6 | Review yield dependencies and overrides. |
| < 5 | Re-read the lecture. |
