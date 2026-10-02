# Advanced Python 20: Patterns — Quiz

> **Topic Overview**: Creational, structural, and behavioral patterns in Python.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What problem does the Singleton pattern address?**
- A) Sorting
- B) Ensuring exactly one instance exists (and a global point of access)
- C) Caching
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** One shared instance.</details>

### Question 2 — Easy
**What does a Factory encapsulate?**
- A) Sorting
- B) Object creation, so callers do not depend on concrete classes
- C) Locking
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Creation indirection.</details>

### Question 3 — Medium
**What is the Observer pattern?**
- A) A cache
- B) Subjects notify registered observers on state change
- C) A lock
- D) A sort

<details><summary>Reveal Answer</summary>**B.** Publish/subscribe.</details>

### Question 4 — Medium
**What does the Strategy pattern let you do?**
- A) Cache
- B) Swap an algorithm at runtime behind a common interface
- C) Lock
- D) Hash

<details><summary>Reveal Answer</summary>**B.** Interchangeable behavior.</details>

### Question 5 — Medium
**What is the Decorator pattern?**
- A) A function decorator only
- B) Wrapping an object to add behavior while keeping the interface
- C) A metaclass
- D) A cache

<details><summary>Reveal Answer</summary>**B.** Composition over inheritance.</details>

### Question 6 — Hard
**Why can Singleton be an anti-pattern?**
- A) It is always good
- B) It hides dependencies and makes testing hard by introducing global state
- C) It is slow
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Prefer dependency injection.</details>

### Question 7 — Hard
**How does Python make many patterns simpler than in Java?**
- A) It does not
- B) First-class functions and duck typing remove boilerplate (e.g. a function is a Strategy)
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Less ceremony.</details>

### Question 8 — Hard
**When should you avoid a pattern?**
- A) Never
- B) When the problem does not require it; patterns are costs paid for flexibility you need
- C) Always
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Do not over-engineer.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You apply patterns judiciously. |
| 5-6 | Review the pattern intents. |
| < 5 | Re-read the lecture. |
