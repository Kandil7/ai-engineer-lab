# Advanced Python 26: Advanced Design Patterns — Quiz

> **Topic Overview**: Adapter, dependency injection, Command, Registry, and Strategy.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does the Adapter pattern do?**
- A) Caches
- B) Converts one interface to another expected by the client
- C) Locks
- D) Hashes

<details><summary>Reveal Answer</summary>**B.** Interface translation.</details>

### Question 2 — Easy
**What is dependency injection?**
- A) Global singletons
- B) Passing collaborators in rather than constructing them inside
- C) Caching
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Invert the construction.</details>

### Question 3 — Medium
**Why does DI make tests easier?**
- A) It is faster
- B) You can inject a fake in place of the real dependency
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Replace boundaries with fakes.</details>

### Question 4 — Medium
**What is the Command pattern?**
- A) A cache
- B) An operation packaged as an object, enabling queueing/undo/logging
- C) A lock
- D) A sort

<details><summary>Reveal Answer</summary>**B.** Encapsulated action.</details>

### Question 5 — Medium
**What does a Registry give you?**
- A) Caching
- B) Declarative discovery: components register under keys to be looked up later
- C) Locking
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Name-to-implementation map.</details>

### Question 6 — Hard
**How does Strategy differ from a plain `if/elif`?**
- A) It is faster
- B) Behavior is encapsulated and swappable without editing the caller
- C) It caches
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Open/closed extension.</details>

### Question 7 — Hard
**Why are fakes "honest"?**
- A) They are real services
- B) They implement the same contract as the real dependency, so the test exercises the real code path
- C) They skip tests
- D) They cache

<details><summary>Reveal Answer</summary>**B.** Same interface, controlled behavior.</details>

### Question 8 — Hard
**When is a pattern overkill?**
- A) Never
- B) When a single function or direct call is enough; patterns add indirection
- C) Always
- D) For tests

<details><summary>Reveal Answer</summary>**B.** Match complexity to need.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You apply advanced patterns well. |
| 5-6 | Review DI, Command, Registry. |
| < 5 | Re-read the lecture. |
