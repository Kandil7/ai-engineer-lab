# FastAPI 32: Async Endpoints Deep — Quiz

> **Topic Overview**: Handler kinds, the single-threaded loop, and measured costs.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What are the two handler kinds?**
- A) GET/POST
- B) `async def` (runs on the loop) and plain `def` (runs in a threadpool)
- C) Public/private
- D) Cached/uncached

<details><summary>Reveal Answer</summary>**B.** Two execution models.</details>

### Question 2 — Easy
**What is true of the event loop?**
- A) It is multi-threaded
- B) It is single-threaded, so one blocking call stalls everything
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** One loop, no blocking.</details>

### Question 3 — Medium
**Why does `time.sleep` in an `async def` handler hurt?**
- A) It is slow
- B) It blocks the loop, serializing all concurrent requests
- C) It caches
- D) It errors

<details><summary>Reveal Answer</summary>**B.** Use `asyncio.sleep` or offload.</details>

### Question 4 — Medium
**When is plain `def` correct?**
- A) Never
- B) For handlers calling blocking libraries you cannot replace
- C) Always
- D) For LLM calls

<details><summary>Reveal Answer</summary>**B.** Threadpool escape.</details>

### Question 5 — Medium
**What does `run_in_threadpool` do inside async code?**
- A) Caches
- B) Runs a blocking callable in a worker thread and awaits it
- C) Sorts
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Escape hatch.</details>

### Question 6 — Hard
**How was "blocking serializes" measured?**
- A) Guessed
- B) A blocking call under concurrency inflates p99 of unrelated requests
- C) By logs
- D) It was not

<details><summary>Reveal Answer</summary>**B.** Cross-request interference.</details>

### Question 7 — Hard
**Why is `async def` with only CPU work a mistake?**
- A) It is not
- B) It adds context-switch overhead with no I/O overlap and still occupies the loop
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** No I/O, no benefit.</details>

### Question 8 — Hard
**What is the decision rule for choosing a handler kind?**
- A) Always async
- B) Async for async I/O; sync for blocking/CPU work the pool absorbs
- C) Always sync
- D) Flip a coin

<details><summary>Reveal Answer</summary>**B.** Match the execution model.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You choose handler kinds correctly. |
| 5-6 | Review the loop and the threadpool. |
| < 5 | Re-read the lecture. |
