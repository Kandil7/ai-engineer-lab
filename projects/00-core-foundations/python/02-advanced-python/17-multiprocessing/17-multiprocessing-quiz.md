# Advanced Python 17: Multiprocessing — Quiz

> **Topic Overview**: Process pools, pickling, shared state, and the CPU escape hatch.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is multiprocessing best for?**
- A) I/O
- B) CPU-bound work that the GIL otherwise serializes
- C) Hashing
- D) Networking

<details><summary>Reveal Answer</summary>**B.** Real parallel CPU execution.</details>

### Question 2 — Easy
**Why does it bypass the GIL?**
- A) It does not
- B) Each process has its own interpreter and its own GIL
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Separate interpreters.</details>

### Question 3 — Medium
**What is the main overhead of processes?**
- A) Memory only
- B) Startup cost and inter-process communication serialization
- C) Hashing
- D) Networking

<details><summary>Reveal Answer</summary>**B.** IPC is not free.</details>

### Question 4 — Medium
**What is pickling required for?**
- A) Caching
- B) Sending arguments/results between processes
- C) Locking
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Serialization at the boundary.</details>

### Question 5 — Medium
**Why are globals not shared between processes?**
- A) They are
- B) Each process has its own memory space
- C) The GIL copies them
- D) They are pickled

<details><summary>Reveal Answer</summary>**B.** Isolated memory.</details>

### Question 6 — Hard
**What is the Windows-specific hazard?**
- A) None
- B) The spawn start method requires an `if __name__ == "__main__":` guard or child processes re-run the script
- C) No processes
- D) It is faster

<details><summary>Reveal Answer</summary>**B.** Spawn, not fork.</details>

### Question 7 — Hard
**Why can IPC erase CPU gains?**
- A) It cannot
- B) Large data transfers dominate; chunk work and keep payloads small
- C) It hashes
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Send less, compute more.</details>

### Question 8 — Hard
**What is a use case that mixes processes and threads?**
- A) Nothing
- B) A process pool for CPU plus a thread pool for the I/O of fetching each chunk
- C) Only threads
- D) Only processes

<details><summary>Reveal Answer</summary>**B.** Match each pool to its workload.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand multiprocessing. |
| 5-6 | Review pickling, spawn, and IPC cost. |
| < 5 | Re-read the lecture. |
