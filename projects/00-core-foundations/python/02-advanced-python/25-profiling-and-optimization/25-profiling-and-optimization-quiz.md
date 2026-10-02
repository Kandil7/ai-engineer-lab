# Advanced Python 25: Profiling and Optimization — Quiz

> **Topic Overview**: `timeit`, `cProfile`, memoization, and vectorization.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the first rule of optimization?**
- A) Rewrite in C
- B) Measure first; never guess the bottleneck
- C) Add caches
- D) Use threads

<details><summary>Reveal Answer</summary>**B.** Evidence before action.</details>

### Question 2 — Easy
**What does `timeit` measure?**
- A) Memory
- B) The runtime of a small snippet, repeated to average out noise
- C) Allocations
- D) CPU %

<details><summary>Reveal Answer</summary>**B.** Micro-benchmarks.</details>

### Question 3 — Medium
**What does `cProfile` give you?**
- A) Memory
- B) Per-function call counts and cumulative time
- C) CPU %
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Whole-program hot paths.</details>

### Question 4 — Medium
**When does memoization help most?**
- A) Always
- B) When the same inputs recur (e.g. overlapping recursion), turning exponential work into linear
- C) Never
- D) For I/O

<details><summary>Reveal Answer</summary>**B.** Cache repeated results.</details>

### Question 5 — Medium
**Why is NumPy vectorization 100x faster than a Python loop?**
- A) It uses threads
- B) Operations run in compiled C over contiguous buffers, avoiding per-element interpreter overhead
- C) It caches
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Compiled bulk operations.</details>

### Question 6 — Hard
**Why is `+=` string concatenation in a loop slow?**
- A) It is not
- B) Strings are immutable; each `+=` copies the growing buffer, giving O(n²)
- C) It hashes
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Use `''.join`.</details>

### Question 7 — Hard
**When is a complexity refactor better than a constant-factor tweak?**
- A) Always
- B) When the algorithm class is wrong (e.g. O(n²) → O(n log n)); no micro-tweak rescues it
- C) Never
- D) For small n

<details><summary>Reveal Answer</summary>**B.** Fix the growth class first.</details>

### Question 8 — Hard
**What does an optimization without a benchmark risk?**
- A) Nothing
- B) Making the code more complex for no measured gain (or a regression)
- C) Hashing
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Unmeasured changes are guesses.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You optimize with evidence. |
| 5-6 | Review profiling tools and vectorization. |
| < 5 | Re-read the lecture. |
