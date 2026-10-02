# FastAPI 20: Testing — Quiz

> **Topic Overview**: `TestClient`, dependency overrides, and hermetic tests.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `TestClient` provide?**
- A) A browser
- B) An in-process HTTP client for the app without a real server
- C) A database
- D) A queue

<details><summary>Reveal Answer</summary>**B.** Fast in-process calls.</details>

### Question 2 — Easy
**How do you replace a dependency in tests?**
- A) `app.dependency_overrides[dep] = fake`
- B) Monkeypatch
- C) Restart the app
- D) You cannot

<details><summary>Reveal Answer</summary>**A.** Override map.</details>

### Question 3 — Medium
**What database should tests use?**
- A) Production
- B) A test database or in-memory/transaction-rolled-back instance
- C) Shared staging
- D) Any

<details><summary>Reveal Answer</summary>**B.** Isolated and disposable.</details>

### Question 4 — Medium
**Why roll back or recreate state between tests?**
- A) Speed
- B) To keep tests independent and order-insensitive
- C) For caching
- D) For sorting

<details><summary>Reveal Answer</summary>**B.** Isolation.</details>

### Question 5 — Medium
**What makes a test hermetic?**
- A) It passes
- B) It uses no external network/services and a controlled datastore
- C) It is long
- D) It mocks everything

<details><summary>Reveal Answer</summary>**B.** No external dependencies.</details>

### Question 6 — Hard
**Why test both success and validation-failure paths?**
- A) Coverage only
- B) The error contract (422 shape) is part of the API and can regress
- C) For speed
- D) For caching

<details><summary>Reveal Answer</summary>**B.** Errors are contract too.</details>

### Question 7 — Hard
**Why is `TestClient` not a load test?**
- A) It is
- B) It runs synchronously in-process, measuring none of the server/network behavior
- C) It is slow
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Correctness, not performance.</details>

### Question 8 — Hard
**What is the risk of over-mocking in API tests?**
- A) None
- B) The test verifies mocks, not the real integration, and misses wiring bugs
- C) Slow
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Include integration tests too.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You test FastAPI well. |
| 5-6 | Review overrides and isolation. |
| < 5 | Re-read the lecture. |
