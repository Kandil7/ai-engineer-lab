# Advanced Python 08: ABCs — Quiz

> **Topic Overview**: Abstract base classes, template methods, and virtual subclasses.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `ABC` prevent?**
- A) Hashing
- B) Instantiating a class that has unimplemented abstract methods
- C) Inheritance
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Abstract methods must be overridden.</details>

### Question 2 — Easy
**What decorator marks a method abstract?**
- A) `@abstract`
- B) `@abstractmethod`
- C) `@virtual`
- D) `@required`

<details><summary>Reveal Answer</summary>**B.** `@abstractmethod`.</details>

### Question 3 — Medium
**What is the template method pattern?**
- A) A cache
- B) A concrete method defines the skeleton and calls abstract steps subclasses fill in
- C) A decorator
- D) A metaclass

<details><summary>Reveal Answer</summary>**B.** Skeleton in base, steps in subclasses.</details>

### Question 4 — Medium
**What does `register()` do?**
- A) Instantiates
- B) Declares a class a virtual subclass without inheriting from the ABC
- C) Caches
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Virtual subclassing.</details>

### Question 5 — Medium
**Why use an ABC for a plugin architecture?**
- A) Speed
- B) It fixes the contract every plugin must satisfy, checked at instantiation
- C) Memory
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Enforced interface.</details>

### Question 6 — Hard
**What is the cost of `isinstance` against a `register()`-ed ABC?**
- A) None
- B) `isinstance` can return True for a class that never implemented the interface
- C) It is faster
- D) It fails

<details><summary>Reveal Answer</summary>**B.** Virtual subclassing bypasses structure checks.</details>

### Question 7 — Hard
**Can an ABC have concrete methods?**
- A) No
- B) Yes; shared behavior stays in the base, abstract steps are overridden
- C) Only static ones
- D) Only properties

<details><summary>Reveal Answer</summary>**B.** Mix of shared and abstract.</details>

### Question 8 — Hard
**When is `Protocol` preferred over an ABC?**
- A) Always
- B) When you want structural typing without forcing inheritance on implementers
- C) For speed
- D) For state

<details><summary>Reveal Answer</summary>**B.** Decoupled contracts.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand ABCs. |
| 5-6 | Review template method and `register`. |
| < 5 | Re-read the lecture. |
