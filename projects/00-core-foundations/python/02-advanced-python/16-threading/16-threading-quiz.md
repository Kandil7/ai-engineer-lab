# Advanced Python 16: Threading — Quiz

> **Topic Overview**: The GIL, I/O-bound work, locks, and thread safety.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is threading best for?**
- A) CPU-bound math
- B) I/O-bound work that releases the GIL (network, disk)
- C) Video encoding
- D) Sorting large lists

<details><summary>Reveal Answer</summary>**B.** I/O concurrency.</details>

### Question 2 — Easy
**What does the GIL allow only one thread to do at a time?**
- A) Any operation
- B) Execute Python bytecode
- C) Access files
- D) Use sockets

<details><summary>Reveal Answer</summary>**B.** One bytecode thread at a time.</details>

### Question 3 — Medium
**Why can threading still speed up I/O?**
- A) It removes the GIL
- B) Blocking I/O releases the GIL, letting other threads run
- C) It uses processes
- D) It caches

<details><summary>Reveal Answer</summary>**B.** GIL is released during I/O.</details>

### Question 4 — Medium
**What does a `Lock` prevent?**
- A) Crashes
- B) Race conditions from concurrent mutation of shared state
- C) Hashing
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Mutual exclusion.</details>

### Question 5 — Medium
**When should you use `ThreadPoolExecutor`?**
- A) CPU work
- B) To run many I/O tasks concurrently with a bounded worker pool
- C) For hashing
- D) For sorting

<details><summary>Reveal Answer</summary>**B.** Convenient pool API.</details>

### Question 6 — Hard
**Why is `x += 1` not atomic?**
- A) It is atomic
- B) It is load-add-store; a context switch between steps loses updates
- C) The GIL prevents it
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Compound operations interleave.</details>

### Question 7 — Hard
**What is a deadlock?**
- A) A slow thread
- B) Two threads each waiting for a lock the other holds
- C) A crash
- D) A cache miss

<details><summary>Reveal Answer</summary>**B.** Circular waiting.</details>

### Question 8 — Hard
**Why is shared mutable state the central hazard?**
- A) It is not
- B) Interleaved reads/writes produce undefined results; prefer immutable data or locks
- C) It is faster
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Concurrency plus mutation is the danger.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand threading. |
| 5-6 | Review the GIL and locking. |
| < 5 | Re-read the lecture. |
