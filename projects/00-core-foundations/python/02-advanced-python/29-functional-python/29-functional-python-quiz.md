# Advanced Python 29: Functional Python — Quiz

> **Topic Overview**: Pure functions, immutability, composition, and functional core.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a pure function?**
- A) A fast function
- B) Same inputs always give the same output and no side effects
- C) A static method
- D) A cached function

<details><summary>Reveal Answer</summary>**B.** Deterministic, no side effects.</details>

### Question 2 — Easy
**Why are frozen dataclasses functional-friendly?**
- A) Speed
- B) Immutability prevents shared-state bugs and makes equality reliable
- C) Hashing only
- D) They sort

<details><summary>Reveal Answer</summary>**B.** Values, not mutable state.</details>

### Question 3 — Medium
**When is a comprehension preferred over `map`/`filter`?**
- A) Never
- B) When it is clearer; comprehensions are the Pythonic default for simple transforms
- C) Always
- D) For `reduce`

<details><summary>Reveal Answer</summary>**B.** Readability first.</details>

### Question 4 — Medium
**What is currying/partial application?**
- A) Caching
- B) Fixing some arguments to produce a more specific function
- C) Sorting
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Specialisation via `partial`.</details>

### Question 5 — Medium
**Why does Python limit recursion depth?**
- A) For speed
- B) Each call uses C stack; deep recursion overflows, unlike a lazily-evaluated functional language
- C) It caches
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** No tail-call optimisation.</details>

### Question 6 — Hard
**What does "functional core, imperative shell" mean?**
- A) All code pure
- B) Pure, testable logic in the core; I/O and mutation confined to a thin shell
- C) No functions
- D) Only classes

<details><summary>Reveal Answer</summary>**B.** Push side effects to the edges.</details>

### Question 7 — Hard
**Why is composition powerful?**
- A) It is fast
- B) Small pure functions combine into pipelines without hidden state
- C) It caches
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Build complex from simple.</details>

### Question 8 — Hard
**What is referential transparency?**
- A) Caching
- B) An expression can be replaced by its value without changing behavior
- C) Hashing
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Substitutability from purity.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You apply functional Python well. |
| 5-6 | Review purity and composition. |
| < 5 | Re-read the lecture. |
