# FastAPI 11: Background Tasks — Quiz

> **Topic Overview**: `BackgroundTasks` and when to use a real queue.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `BackgroundTasks` do?**
- A) Runs work after the response is sent, in the same process
- B) Spawns a worker
- C) Blocks the request
- D) Caches

<details><summary>Reveal Answer</summary>**A.** Post-response, in-process.</details>

### Question 2 — Easy
**When is a background task run?**
- A) Before the response
- B) After the response is returned to the client
- C) During routing
- D) Never

<details><summary>Reveal Answer</summary>**B.** After the response.</details>

### Question 3 — Medium
**What happens to in-process background tasks if the worker restarts?**
- A) They resume
- B) They are lost; there is no durability
- C) They duplicate
- D) They retry

<details><summary>Reveal Answer</summary>**B.** No durability.</details>

### Question 4 — Medium
**When do you need a real broker (Celery/RQ)?**
- A) Always
- B) For durable, retryable, long-running work off the request process
- C) Never
- D) For logging

<details><summary>Reveal Answer</summary>**B.** Durable queues.</details>

### Question 5 — Medium
**Why does a background task not survive a crash?**
- A) It does
- B) It lives in the process memory; a crash takes it with the process
- C) It is on disk
- D) It retries

<details><summary>Reveal Answer</summary>**B.** Process-bound.</details>

### Question 6 — Hard
**Why can't a background task report progress to the user directly?**
- A) It can
- B) The response is already sent; progress needs a status endpoint or queue
- C) For speed
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Out-of-band status.</details>

### Question 7 — Hard
**What is the retry story for a broker-based job?**
- A) None
- B) The queue retries with backoff and routes failures to a dead-letter queue
- C) Manual only
- D) It never fails

<details><summary>Reveal Answer</summary>**B.** Managed retries/DLQ.</details>

### Question 8 — Hard
**What is the decision rule?**
- A) Always background tasks
- B) In-process for small fire-and-forget; broker for durable/long/heavy work
- C) Always a broker
- D) Neither

<details><summary>Reveal Answer</summary>**B.** Match durability needs.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You choose the right mechanism. |
| 5-6 | Review durability and retries. |
| < 5 | Re-read the lecture. |
