# Advanced Python 15: Descriptors — Quiz

> **Topic Overview**: `__get__`/`__set__`, data vs non-data, and the mechanism behind properties.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a descriptor?**
- A) A decorator
- B) An object defining `__get__`, and optionally `__set__`/`__delete__`, used as a class attribute
- C) A cache
- D) A metaclass

<details><summary>Reveal Answer</summary>**B.** Attribute access protocol.</details>

### Question 2 — Easy
**What is `@property` implemented with?**
- A) A metaclass
- B) A data descriptor
- C) A decorator
- D) `__slots__`

<details><summary>Reveal Answer</summary>**B.** Properties are descriptors.</details>

### Question 3 — Medium
**What distinguishes a data descriptor from a non-data one?**
- A) Size
- B) Whether it defines `__set__` (and/or `__delete__`)
- C) Hashing
- D) Speed

<details><summary>Reveal Answer</summary>**B.** Data descriptors take precedence over instance `__dict__`.</details>

### Question 4 — Medium
**Which wins on lookup when a data descriptor and an instance attribute share a name?**
- A) Instance attribute
- B) Data descriptor
- C) Random
- D) Neither

<details><summary>Reveal Answer</summary>**B.** Descriptor precedence.</details>

### Question 5 — Medium
**What is the lookup order for `obj.attr`?**
- A) Instance dict first
- B) Data descriptor, then instance dict, then non-data descriptor/class attr
- C) Class first
- D) Metaclass first

<details><summary>Reveal Answer</summary>**B.** The MRO plus descriptor precedence.</details>

### Question 6 — Hard
**What does a non-data descriptor (only `__get__`) enable?**
- A) Validation
- B) Lazy per-instance values that are then shadowed by the instance dict on first write
- C) Sorting
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Caching descriptors.</details>

### Question 7 — Hard
**Why do methods work as descriptors?**
- A) They are properties
- B) Functions implement `__get__`, returning a bound method
- C) They are slots
- D) They are metaclasses

<details><summary>Reveal Answer</summary>**B.** Binding happens on access.</details>

### Question 8 — Hard
**When would you write a custom descriptor?**
- A) Never
- B) For reusable validation or computed attributes shared across many classes
- C) For speed
- D) For hashing

<details><summary>Reveal Answer</summary>**B.** Reusable attribute behavior.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand descriptors. |
| 5-6 | Review data vs non-data precedence. |
| < 5 | Re-read the lecture. |
