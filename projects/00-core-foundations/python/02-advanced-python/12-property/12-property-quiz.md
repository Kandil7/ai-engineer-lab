# Advanced Python 12: Property — Quiz

> **Topic Overview**: Computed attributes, setters, and controlled mutation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `@property` turn a method into?**
- A) A class method
- B) An attribute-style accessor that runs code on read
- C) A static method
- D) A cache

<details><summary>Reveal Answer</summary>**B.** Computed attribute.</details>

### Question 2 — Easy
**How do you add validation on assignment?**
- A) `@setter`
- B) `@<name>.setter`
- C) `@getter`
- D) `@deleter`

<details><summary>Reveal Answer</summary>**B.** Paired setter.</details>

### Question 3 — Medium
**Why use a property instead of an eager attribute?**
- A) For speed
- B) To compute lazily or validate/transform on access without changing the public API
- C) Hashing
- D) Memory

<details><summary>Reveal Answer</summary>**B.** Encapsulation with attribute syntax.</details>

### Question 4 — Medium
**What makes a read-only property?**
- A) No setter defined (assignment raises `AttributeError`)
- B) `@frozen`
- C) `@property(readonly=True)`
- D) `__slots__`

<details><summary>Reveal Answer</summary>**A.** Absence of a setter.</details>

### Question 5 — Medium
**How do you expose a property's docstring?**
- A) Set it on the getter, before defining the setter
- B) You cannot
- C) Set it on the setter
- D) With a comment

<details><summary>Reveal Answer</summary>**A.** The getter owns the doc.</details>

### Question 6 — Hard
**What is the cost of a property vs a plain attribute?**
- A) None
- B) A method call per access, so hot loops can be slower
- C) It is faster
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Measure in hot paths.</details>

### Question 7 — Hard
**Why is a property a poor fit for `__init__` assignment during subclassing?**
- A) It is not
- B) If a subclass overrides the property, setup order can call the override before it is ready
- C) It sorts
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Virtual dispatch during construction.</details>

### Question 8 — Hard
**What does `@cached_property` combine?**
- A) Property and cache
- B) Lazy computation with per-instance storage after the first access
- C) Slots
- D) Validation

<details><summary>Reveal Answer</summary>**B.** Compute once, then cache.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand properties. |
| 5-6 | Review setters and `cached_property`. |
| < 5 | Re-read the lecture. |
