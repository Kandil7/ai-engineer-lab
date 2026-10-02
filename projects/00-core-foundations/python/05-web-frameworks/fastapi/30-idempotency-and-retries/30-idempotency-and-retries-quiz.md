# FastAPI 30: Idempotency and Retries — Quiz

> **Topic Overview**: Idempotency keys, safe methods, and exactly-once reality.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does an idempotency key do?**
- A) Encrypts the request
- B) Lets the server recognise a retried request and return the stored result
- C) Hashes the body
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Dedup on retry.</details>

### Question 2 — Easy
**Which methods are safe to retry without a key?**
- A) POST
- B) GET, HEAD, PUT, DELETE (idempotent by definition)
- C) All equally
- D) None

<details><summary>Reveal Answer</summary>**B.** Safe/retryable methods.</details>

### Question 3 — Medium
**Why does a timeout not mean failure?**
- A) It does
- B) The server may have completed the work but the response was lost
- C) It is faster
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Unknown outcome.</details>

### Question 4 — Medium
**What does `Retry-After` tell a client?**
- A) To stop forever
- B) How long to wait before retrying
- C) To use another key
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Server-driven backoff.</details>

### Question 5 — Medium
**Why is exactly-once delivery a fiction?**
- A) It is real
- B) Networks can duplicate or drop; design for at-least-once plus a dedup store
- C) It is slow
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Dedup, not delivery guarantees.</details>

### Question 6 — Hard
**Why must the idempotency check be atomic?**
- A) Speed
- B) Concurrent retries could both pass a non-atomic check and duplicate the side effect
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Compare-and-set the key.</details>

### Question 7 — Hard
**What should the dedup store record?**
- A) The key only
- B) The key plus the response, with a TTL, so retries replay the original
- C) The user
- D) The route

<details><summary>Reveal Answer</summary>**B.** Replay stored results.</details>

### Question 8 — Hard
**Who generates the idempotency key?**
- A) The server
- B) The client (e.g. a UUID per logical operation)
- C) The proxy
- D) The database

<details><summary>Reveal Answer</summary>**B.** Client-supplied, server-enforced.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You design idempotent APIs. |
| 5-6 | Review the dedup store and atomicity. |
| < 5 | Re-read the lecture. |
