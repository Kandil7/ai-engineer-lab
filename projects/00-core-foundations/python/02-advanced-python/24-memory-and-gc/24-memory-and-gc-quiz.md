# Advanced Python 24: Memory and GC — Quiz

> **Topic Overview**: Refcounts, cycles, weak references, and allocation profiling.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is CPython's primary memory strategy?**
- A) Tracing GC only
- B) Reference counting, with a cycle collector as backup
- C) Manual free
- D) Arena only

<details><summary>Reveal Answer</summary>**B.** Refcounts plus cycle GC.</details>

### Question 2 — Easy
**When is an object freed under refcounting?**
- A) At program end
- B) When its reference count drops to zero
- C) After a GC pause
- D) Never

<details><summary>Reveal Answer</summary>**B.** Deterministic for acyclic data.</details>

### Question 3 — Medium
**What can refcounting not reclaim?**
- A) Lists
- B) Reference cycles
- C) Strings
- D) Dicts

<details><summary>Reveal Answer</summary>**B.** The cycle collector handles those.</details>

### Question 4 — Medium
**What is a weak reference for?**
- A) Locking
- B) Referring to an object without keeping it alive (caches that self-evict)
- C) Sorting
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Non-owning references.</details>

### Question 5 — Medium
**What does `tracemalloc` help with?**
- A) Locking
- B) Naming the allocation site behind a memory growth
- C) Sorting
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Allocation attribution.</details>

### Question 6 — Hard
**Why can a long-lived cache leak memory?**
- A) It cannot
- B) Every distinct key holds a strong reference forever unless bounded or weakly referenced
- C) It is faster
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Unbounded growth.</details>

### Question 7 — Hard
**What does `sys.getrefcount` reveal during debugging?**
- A) The size
- B) How many references exist (including the temporary from the call itself)
- C) The GC generation
- D) The hash

<details><summary>Reveal Answer</summary>**B.** Reference accounting.</details>

### Question 8 — Hard
**Why does `__slots__` reduce memory?**
- A) It caches
- B) It removes the per-instance `__dict__`, storing fields in fixed slots
- C) It hashes
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** No dict overhead.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand Python memory. |
| 5-6 | Review cycles, weakrefs, and tracemalloc. |
| < 5 | Re-read the lecture. |
