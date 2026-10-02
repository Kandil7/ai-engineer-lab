# Advanced Python 03: Context Managers — Quiz

> **Topic Overview**: The `with` protocol, `contextmanager`, and guaranteed cleanup.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Which two methods define the context-manager protocol?**
- A) `__iter__`/`__next__`
- B) `__enter__`/`__exit__`
- C) `__init__`/`__del__`
- D) `__call__`/`__repr__`

<details><summary>Reveal Answer</summary>**B.** Enter and exit.</details>

### Question 2 — Easy
**What is the main guarantee of `with`?**
- A) Speed
- B) `__exit__` runs even if the body raises
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Deterministic cleanup.</details>

### Question 3 — Medium
**How do you return the three `__exit__` arguments?**
- A) They are ignored
- B) `exc_type, exc, tb`; returning `True` suppresses the exception
- C) `self, args, kwargs`
- D) `value, type, trace`

<details><summary>Reveal Answer</summary>**B.** Truthy return swallows the error.</details>

### Question 4 — Medium
**How does `@contextmanager` let you write one?**
- A) A class
- B) A generator that yields once; code before `yield` is setup, after is teardown
- C) A decorator
- D) A metaclass

<details><summary>Reveal Answer</summary>**B.** Generator-based.</details>

### Question 5 — Medium
**What does `contextlib.suppress` do?**
- A) Logs
- B) Silently ignores listed exceptions inside its block
- C) Reraises
- D) Caches

<details><summary>Reveal Answer</summary>**B.** Selective suppression.</details>

### Question 6 — Hard
**Why is `with open(...)` better than manual `open`/`close`?**
- A) It is faster
- B) It closes the file even on exceptions, preventing descriptor leaks
- C) It compresses
- D) It cannot fail

<details><summary>Reveal Answer</summary>**B.** RAII-style safety.</details>

### Question 7 — Hard
**What does `ExitStack` solve?**
- A) Nothing
- B) Entering/leaving a dynamic number of context managers safely
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Dynamic cleanup.</details>

### Question 8 — Hard
**What is a common mistake when teardown itself raises?**
- A) It cannot
- B) An exception in `__exit__` masks the original exception from the body
- C) It is faster
- D) It suppresses

<details><summary>Reveal Answer</summary>**B.** Teardown must be careful.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand context managers. |
| 5-6 | Review `__exit__` and `contextmanager`. |
| < 5 | Re-read the lecture. |
