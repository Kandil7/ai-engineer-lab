# Advanced Python 21: Concurrency Comparison — Quiz

> **Topic Overview**: GIL, threads vs processes vs async, and choosing by workload.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Which tool for I/O-bound work with many concurrent waits?**
- A) Processes
- B) Threads or async
- C) Neither
- D) Multiprocessing only

<details><summary>Reveal Answer</summary>**B.** Concurrency for waits.</details>

### Question 2 — Easy
**Which tool for CPU-bound work?**
- A) Threads
- B) Processes
- C) Async
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Bypass the GIL.</details>

### Question 3 — Medium
**What does the GIL prevent?**
- A) I/O
- B) Multiple threads executing Python bytecode simultaneously
- C) Processes
- D) Async

<details><summary>Reveal Answer</summary>**B.** One bytecode thread at a time.</details>

### Question 4 — Medium
**Why can async be lighter than threads for many I/O tasks?**
- A) It uses processes
- B) One thread with cooperative scheduling avoids per-thread memory and context-switch cost
- C) It bypasses the GIL
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Cheaper concurrency per task.</details>

### Question 5 — Medium
**What is `concurrent.futures` for?**
- A) Locking
- B) One API (`ThreadPoolExecutor` / `ProcessPoolExecutor`) over both strategies
- C) Sorting
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Uniform executor interface.</details>

### Question 6 — Hard
**Why do threads not speed up CPU-bound work?**
- A) They do
- B) The GIL serializes bytecode, so they add switching overhead without parallel compute
- C) Too much memory
- D) They cache

<details><summary>Reveal Answer</summary>**B.** No true parallelism.</details>

### Question 7 — Hard
**What is the fourth dimension often ignored when comparing strategies?**
- A) Speed
- B) Memory per task (each thread/process has overhead)
- C) Sorting
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Memory cost.</details>

### Question 8 — Hard
**What does the decision flowchart key on first?**
- A) Language
- B) Whether the workload is I/O-bound or CPU-bound
- C) Memory
- D) Code length

<details><summary>Reveal Answer</summary>**B.** Workload family first.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You choose the right concurrency tool. |
| 5-6 | Review GIL and the decision flowchart. |
| < 5 | Re-read the lecture. |
