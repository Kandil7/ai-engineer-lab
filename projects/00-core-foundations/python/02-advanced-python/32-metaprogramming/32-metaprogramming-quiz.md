# Advanced Python 32: Metaprogramming — Quiz

> **Topic Overview**: Registration hooks, signature-driven tool schemas, and dynamic import.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How does `__init_subclass__` enable registration?**
- A) It creates classes
- B) The base class runs it for each subclass, where you can record it in a registry
- C) It caches
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Hook on subclass creation.</details>

### Question 2 — Easy
**What does `inspect.signature` give you?**
- A) The source
- B) A function's parameters, names, and defaults
- C) The docstring
- D) The hash

<details><summary>Reveal Answer</summary>**B.** The function's shape.</details>

### Question 3 — Medium
**What is the `@tool` pattern?**
- A) A cache
- B) Deriving a tool's JSON schema from its signature/annotations at registration time
- C) A lock
- D) A sort

<details><summary>Reveal Answer</summary>**B.** Schema from code, not duplication.</details>

### Question 4 — Medium
**How does `importlib` support plugins?**
- A) It caches
- B) It imports a module by string name at runtime for dynamic loading
- C) It hashes
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Dynamic import.</details>

### Question 5 — Medium
**Why prefer `getattr(obj, name, default)` over `obj.name`?**
- A) It is faster
- B) It handles a missing attribute safely without raising
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Safe access.</details>

### Question 6 — Hard
**Why avoid `exec`/`eval` on untrusted input?**
- A) They are slow
- B) They execute arbitrary code; there is no safe sandbox
- C) They hash
- D) They sort

<details><summary>Reveal Answer</summary>**B.** Code execution.</details>

### Question 7 — Hard
**Why is `ast` safer than `eval` for analyzing code?**
- A) It is faster
- B) It parses to data you can inspect without executing
- C) It caches
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Parse, do not run.</details>

### Question 8 — Hard
**What is the cost of monkey-patching?**
- A) None
- B) It changes behavior globally and invisibly, making bugs hard to trace
- C) It is slow
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Hidden global mutation.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You metaprogram safely. |
| 5-6 | Review hooks, signatures, and dynamic import. |
| < 5 | Re-read the lecture. |
