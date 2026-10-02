# Advanced Python 14: Metaclasses — Quiz

> **Topic Overview**: Classes as objects, `type`, `__init_subclass__`, and when not to.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a metaclass?**
- A) A base class
- B) The class of a class, controlling how classes are created
- C) A decorator
- D) A cache

<details><summary>Reveal Answer</summary>**B.** Class factory.</details>

### Question 2 — Easy
**What is the default metaclass?**
- A) `object`
- B) `type`
- C) `ABC`
- D) `super`

<details><summary>Reveal Answer</summary>**B.** `type`.</details>

### Question 3 — Medium
**What does `__init_subclass__` allow?**
- A) Creating classes
- B) A base class to react to subclass creation without a full metaclass
- C) Caching
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Simpler hook for many cases.</details>

### Question 4 — Medium
**What does `__set_name__` do?**
- A) Caches
- B) Tells a descriptor the attribute name and owner when the class is created
- C) Sorts
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Descriptor registration.</details>

### Question 5 — Medium
**Which three methods does a metaclass commonly override?**
- A) `__enter__`/`__exit__`
- B) `__new__`/`__init__`/`__prepare__`
- C) `__iter__`/`__next__`
- D) `__get__`/`__set__`

<details><summary>Reveal Answer</summary>**B.** Class-creation pipeline.</details>

### Question 6 — Hard
**Why is a metaclass often the wrong tool?**
- A) It is slow
- B) It is the most powerful and least understandable option; `__init_subclass__` or a decorator usually suffices
- C) It cannot access members
- D) It is deprecated

<details><summary>Reveal Answer</summary>**B.** Use the weakest tool that works.</details>

### Question 7 — Hard
**What is the conflict risk with multiple metaclasses?**
- A) None
- B) A class cannot have two unrelated metaclasses; inheritance fails
- C) It is faster
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Metaclass conflicts are hard to fix.</details>

### Question 8 — Hard
**What is `__prepare__` for?**
- A) Caching
- B) Providing the namespace mapping used while the class body executes
- C) Hashing
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Order-aware namespaces.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand metaclasses. |
| 5-6 | Review `__init_subclass__` and when to avoid. |
| < 5 | Re-read the lecture. |
