# Advanced Python 04: Async / Await — Quiz

> **Topic Overview**: Coroutines, the event loop, timeouts, and async patterns.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a coroutine?**
- A) A thread
- B) A function defined with `async def` that can be awaited
- C) A process
- D) A lock

<details><summary>Reveal Answer</summary>**B.** Awaitable by the event loop.</details>

### Question 2 — Easy
**What is the event loop?**
- A) A thread pool
- B) The scheduler that runs coroutines and resumes them when I/O completes
- C) A lock
- D) A queue

<details><summary>Reveal Answer</summary>**B.** Cooperative scheduling.</details>

### Question 3 — Medium
**What does `await` do?**
- A) Blocks the thread
- B) Suspends the current coroutine so the loop can run others
- C) Spawns a thread
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Yields control to the loop.</details>

### Question 4 — Medium
**Why is blocking the loop (e.g. `time.sleep` or CPU work) harmful?**
- A) It is not
- B) It stalls every other coroutine, defeating concurrency
- C) It spawns threads
- D) It caches

<details><summary>Reveal Answer</summary>**B.** One thread runs all coroutines.</details>

### Question 5 — Medium
**What does `asyncio.gather` do?**
- A) Sequences calls
- B) Runs awaitables concurrently and collects results
- C) Spawns processes
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Concurrent fan-out.</details>

### Question 6 — Hard
**What is the danger of cancelling a task mid-await?**
- A) None
- B) Cleanup may be skipped; use `finally`/`shield` for work that must finish
- C) It spawns a thread
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Cancellation is an exception at the await point.</details>

### Question 7 — Hard
**What are `async with` and `async for` for?**
- A) Nothing
- B) Async context managers and async iterators that await on entry/next
- C) Threads
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Async protocol variants.</details>

### Question 8 — Hard
**What does an `asyncio.Queue` provide?**
- A) Caching
- B) Backpressure via bounded capacity between producer and consumer coroutines
- C) Locks
- D) Threads

<details><summary>Reveal Answer</summary>**B.** Producer/consumer coordination.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand async/await. |
| 5-6 | Review the loop and cancellation. |
| < 5 | Re-read the lecture. |
