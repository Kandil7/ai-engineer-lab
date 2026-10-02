# FastAPI 21: Async — Quiz

> **Topic Overview**: Async handlers, sync fallback, and the threadpool.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `async def` on a route enable?**
- A) Threads
- B) The handler runs on the event loop and can await I/O
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Cooperative concurrency.</details>

### Question 2 — Easy
**What happens to a plain `def` handler with blocking I/O?**
- A) It blocks everything
- B) FastAPI runs it in a threadpool so the loop is not blocked
- C) It errors
- D) It is slower always

<details><summary>Reveal Answer</summary>**B.** Threadpool escape.</details>

### Question 3 — Medium
**Why is a blocking call inside an `async def` handler worse than in `def`?**
- A) It is not
- B) There is no threadpool escape; it stalls the whole event loop
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** `async def` must not block.</details>

### Question 4 — Medium
**What should you use for a blocking library inside async code?**
- A) Nothing
- B) `await run_in_threadpool(...)` or an async client
- C) `time.sleep`
- D) A lock

<details><summary>Reveal Answer</summary>**B.** Offload blocking work.</details>

### Question 5 — Medium
**When is sync correct?**
- A) Never
- B) For quick CPU-light handlers or when using a blocking DB driver you cannot replace
- C) Always
- D) For LLM calls

<details><summary>Reveal Answer</summary>**B.** Pragmatic choice.</details>

### Question 6 — Hard
**What is the threadpool default size risk?**
- A) None
- B) A small pool under many blocking calls becomes a queue, serializing throughput
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Size the pool to the workload.</details>

### Question 7 — Hard
**Why can CPU-bound work in async handlers be worse than in sync?**
- A) It is not
- B) It holds the loop for the whole computation, blocking all requests
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** No parallelism on one loop.</details>

### Question 8 — Hard
**What is the golden rule for async endpoints?**
- A) Use async always
- B) Never block the loop; await async I/O or offload blocking calls
- C) Use threads always
- D) Use sync always

<details><summary>Reveal Answer</summary>**B.** Loop discipline.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You write safe async handlers. |
| 5-6 | Review the threadpool and blocking. |
| < 5 | Re-read the lecture. |
