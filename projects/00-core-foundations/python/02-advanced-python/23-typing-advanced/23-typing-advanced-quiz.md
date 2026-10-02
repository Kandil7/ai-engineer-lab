# Advanced Python 23: Typing Advanced — Quiz

> **Topic Overview**: Protocol, generics, TypeVar bounds, ParamSpec, and Literal.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `Protocol` express?**
- A) Inheritance
- B) A structural contract: any type with matching members conforms
- C) Runtime checks
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Structural typing.</details>

### Question 2 — Easy
**What is `TypeVar` for?**
- A) Runtime types
- B) A placeholder tying input and output types in a generic function/class
- C) Hashing
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Preserve type relationships.</details>

### Question 3 — Medium
**What does a bounded `TypeVar` mean?**
- A) It is limited to one value
- B) The type must be a subtype of the bound, giving access to bound methods
- C) It caches
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Constrained type parameter.</details>

### Question 4 — Medium
**What is `ParamSpec` for?**
- A) Caching
- B) Typing decorators so the wrapped function's parameter list is preserved
- C) Locking
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Decorator type preservation.</details>

### Question 5 — Medium
**What does `Literal["a", "b"]` restrict a value to?**
- A) Any string
- B) Exactly the listed literals
- C) A regex
- D) An enum

<details><summary>Reveal Answer</summary>**B.** Closed value set.</details>

### Question 6 — Hard
**What can `runtime_checkable` actually verify?**
- A) Method signatures
- B) Only the presence of members, not their types
- C) Everything
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Shallow structural check.</details>

### Question 7 — Hard
**Why does `TypeGuard` matter?**
- A) It caches
- B) It narrows the type inside a conditional, unlike a plain `bool` return
- C) It hashes
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Informs the checker.</details>

### Question 8 — Hard
**What is true of annotations at runtime by default?**
- A) They are enforced
- B) They are evaluated objects unless deferred; `get_type_hints` resolves them
- C) They are strings always
- D) They are ignored

<details><summary>Reveal Answer</summary>**B.** Types are live objects (unless PEP 563).</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You write precise types. |
| 5-6 | Review generics and ParamSpec. |
| < 5 | Re-read the lecture. |
