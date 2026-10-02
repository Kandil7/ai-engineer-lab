# Advanced Python 01: Decorators — Quiz

> **Topic Overview**: Wrapping functions, decorator factories, and class-based decorators.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What must a decorator be able to accept?**
- A) Only classes
- B) A function (first-class functions make this possible)
- C) Only strings
- D) Only methods

<details><summary>Reveal Answer</summary>**B.** Functions are first-class values.</details>

### Question 2 — Easy
**What does `functools.wraps` preserve?**
- A) The cache
- B) The wrapped function's name, docstring, and metadata
- C) The return type
- D) The decorator's arguments

<details><summary>Reveal Answer</summary>**B.** Without it, introspection breaks.</details>

### Question 3 — Medium
**How do you write a decorator that takes arguments?**
- A) Add a parameter to the inner function
- B) A factory: the outer function takes the config and returns the real decorator
- C) Use a class only
- D) You cannot

<details><summary>Reveal Answer</summary>**B.** One extra layer of nesting.</details>

### Question 4 — Medium
**What is the order of application when decorators are stacked?**
- A) Bottom-up wraps first, top-down calls first
- B) Top-down
- C) Random
- D) Alphabetical

<details><summary>Reveal Answer</summary>**A.** The decorator nearest the function applies first.</details>

### Question 5 — Medium
**What does a class-based decorator need to be callable?**
- A) `__iter__`
- B) `__call__`
- C) `__enter__`
- D) `__get__`

<details><summary>Reveal Answer</summary>**B.** Instances must be callable.</details>

### Question 6 — Hard
**Why does a decorator without `wraps` break frameworks?**
- A) It is slower
- B) They read `__name__`/`__doc__`/signatures, which now describe the wrapper
- C) It changes the return value
- D) It cannot be called

<details><summary>Reveal Answer</summary>**B.** Metadata points to the wrapper.</details>

### Question 7 — Hard
**When is a class-based decorator preferable?**
- A) Never
- B) When it must carry state across calls, which instance attributes hold naturally
- C) For speed
- D) For static methods

<details><summary>Reveal Answer</summary>**B.** State lives on the instance.</details>

### Question 8 — Hard
**What is a common mistake in a decorator factory?**
- A) Forgetting to call the factory, or mixing the config and the function arguments
- B) Using `wraps`
- C) Returning a function
- D) Using `*args, **kwargs`

<details><summary>Reveal Answer</summary>**A.** Three nesting levels must stay straight.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can write decorators. |
| 5-6 | Review factories and `wraps`. |
| < 5 | Re-read the lecture. |
