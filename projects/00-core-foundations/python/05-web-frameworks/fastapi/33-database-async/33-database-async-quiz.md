# FastAPI 33: Async Database — Quiz

> **Topic Overview**: Async drivers, session-per-request, and pool sizing.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why do async handlers need async drivers?**
- A) Style
- B) A sync driver call blocks the loop
- C) For speed
- D) For caching

<details><summary>Reveal Answer</summary>**B.** Keep the loop free.</details>

### Question 2 — Easy
**What is session-per-request?**
- A) One session forever
- B) A DI dependency yielding a fresh session per request and closing it after
- C) A global session
- D) A pool

<details><summary>Reveal Answer</summary>**B.** Request-scoped lifetime.</details>

### Question 3 — Medium
**What is transaction scope?**
- A) A cache
- B) The boundary where multiple writes commit atomically or roll back together
- C) A pool
- D) A route

<details><summary>Reveal Answer</summary>**B.** Atomic unit of work.</details>

### Question 4 — Medium
**Why does a shared global session in async code break?**
- A) It does not
- B) Concurrent requests interleave on one session, corrupting transaction state
- C) For speed
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Sessions are not thread/task safe.</details>

### Question 5 — Medium
**What is the pool-sizing rule?**
- A) Unlimited
- B) Workers × concurrency, bounded by what the database can serve
- C) Always 100
- D) Always 1

<details><summary>Reveal Answer</summary>**B.** Both sides of the pipe.</details>

### Question 6 — Hard
**What are the symptoms of pool exhaustion?**
- A) Fast 500s
- B) Requests queue then time out waiting for a connection
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Queueing, then timeouts.</details>

### Question 7 — Hard
**Why do lazy attributes fail in async handlers?**
- A) They do not
- B) Attribute access triggers implicit sync I/O on the loop
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Eager-load instead.</details>

### Question 8 — Hard
**Why check out a connection late and return it early?**
- A) Style
- B) Shorter hold times raise effective pool capacity
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Hold time is the resource.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You wire async databases well. |
| 5-6 | Review sessions and pool sizing. |
| < 5 | Re-read the lecture. |
