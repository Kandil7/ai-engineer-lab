# Advanced Python 22: asyncio Advanced — Quiz

> **Topic Overview**: TaskGroup, cancellation, shielding, timeouts, and backpressure.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `TaskGroup` add over `gather`?**
- A) Nothing
- B) Structured concurrency: it cancels siblings when one fails and cannot be left un-awaited
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Safer lifetime management.</details>

### Question 2 — Easy
**What is `asyncio.timeout` for?**
- A) Caching
- B) Cancelling a block that exceeds a deadline
- C) Locking
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Deadlines as code.</details>

### Question 3 — Medium
**What does `asyncio.shield` do?**
- A) Cancels
- B) Protects an awaitable from being cancelled by the outer cancellation
- C) Caches
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Must-finish work.</details>

### Question 4 — Medium
**Why run `run_in_executor` for blocking calls?**
- A) For speed
- B) To move blocking sync code off the event loop so it does not stall other coroutines
- C) To cache
- D) To lock

<details><summary>Reveal Answer</summary>**B.** Offload blocking work.</details>

### Question 5 — Medium
**What do bounded queues give you?**
- A) Sorting
- B) Backpressure: producers block when the queue is full
- C) Caching
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Flow control.</details>

### Question 6 — Hard
**How is cancellation delivered to a coroutine?**
- A) A signal
- B) A `CancelledError` raised at the next `await`
- C) A thread
- D) A cache

<details><summary>Reveal Answer</summary>**B.** Exception at suspension point.</details>

### Question 7 — Hard
**Why is a `Semaphore` useful for rate limiting?**
- A) It caches
- B) It caps concurrent holders, making the in-flight count observable and bounded
- C) It sorts
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Bounded concurrency.</details>

### Question 8 — Hard
**What is the cost of blocking the loop?**
- A) None
- B) Every other task stalls for the duration; one bad `time.sleep` serializes everything
- C) It is faster
- D) It caches

<details><summary>Reveal Answer</summary>**B.** One thread runs all tasks.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You write structured async code. |
| 5-6 | Review cancellation and TaskGroup. |
| < 5 | Re-read the lecture. |
