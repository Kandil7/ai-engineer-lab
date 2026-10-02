# Advanced Python 09: functools — Quiz

> **Topic Overview**: `partial`, caching, `wraps`, `reduce`, and `singledispatch`.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `functools.partial` do?**
- A) Sorts
- B) Binds some arguments now, producing a callable that needs the rest
- C) Caches
- D) Hashes

<details><summary>Reveal Answer</summary>**B.** Partial application.</details>

### Question 2 — Easy
**What does `functools.wraps` do?**
- A) Caches
- B) Copies `__name__`/`__doc__`/metadata from the wrapped function onto the wrapper
- C) Sorts
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Preserve metadata.</details>

### Question 3 — Medium
**What must a key be for `lru_cache`?**
- A) Any
- B) Hashable
- C) Sortable
- D) A string

<details><summary>Reveal Answer</summary>**B.** It keys a dict internally.</details>

### Question 4 — Medium
**What is the difference between `cache` and `lru_cache`?**
- A) None
- B) `cache` is the unbounded version of `lru_cache` with no max size
- C) `cache` is smaller
- D) `cache` is slower

<details><summary>Reveal Answer</summary>**B.** Unbounded convenience.</details>

### Question 5 — Medium
**What does `functools.reduce` do?**
- A) Caches
- B) Folds a sequence into one value with a binary function
- C) Sorts
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Left fold.</details>

### Question 6 — Hard
**Why can an unbounded `cache` leak memory?**
- A) It cannot
- B) Distinct arguments accumulate forever; use `lru_cache(maxsize=...)` for long-running processes
- C) It is faster
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Bounded cache needed for production.</details>

### Question 7 — Hard
**What does `singledispatch` enable?**
- A) Hashing
- B) Function overloading by the first argument's type
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Runtime type dispatch.</details>

### Question 8 — Hard
**What is `cached_property` for?**
- A) Class attributes
- B) A property computed once per instance and then stored
- C) Caching across processes
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Per-instance lazy cache.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You use functools well. |
| 5-6 | Review caching and dispatch. |
| < 5 | Re-read the lecture. |
