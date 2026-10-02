# Advanced Python 05: Type Hints — Quiz

> **Topic Overview**: Annotations, generics, Protocol, and static checking.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**When do type hints take effect at runtime?**
- A) Always
- B) They do not enforce anything; they are for readers and checkers
- C) Only in functions
- D) Only in classes

<details><summary>Reveal Answer</summary>**B.** Static, not runtime, enforcement.</details>

### Question 2 — Easy
**Which tool statically checks type hints?**
- A) pytest
- B) mypy / pyright
- C) ruff only
- D) black

<details><summary>Reveal Answer</summary>**B.** Static analyzers.</details>

### Question 3 — Medium
**What does `Optional[int]` mean?**
- A) An int
- B) `int | None`
- C) A missing key
- D) Any

<details><summary>Reveal Answer</summary>**B.** May be absent.</details>

### Question 4 — Medium
**What is `Protocol` for?**
- A) Inheritance
- B) Structural subtyping: any type with the right methods fits
- C) Runtime checks
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Duck typing, statically checked.</details>

### Question 5 — Medium
**What is a common mistake with mutable defaults in annotations-adjacent code?**
- A) Using `list[int]`
- B) `def f(x=[])` — the default is shared across calls
- C) Annotating return types
- D) Using `None`

<details><summary>Reveal Answer</summary>**B.** Use `None` as the sentinel.</details>

### Question 6 — Hard
**Why can `str` and `bytes` not be used interchangeably despite both being sequences?**
- A) They can
- B) They are different types with different element types; `Sequence[str]` rejects bytes
- C) For speed
- D) Because of the GIL

<details><summary>Reveal Answer</summary>**B.** Element types differ.</details>

### Question 7 — Hard
**What does `From __future__ import annotations` change?**
- A) Enforces types
- B) Defers annotation evaluation to strings, allowing forward references
- C) Speeds up code
- D) None

<details><summary>Reveal Answer</summary>**B.** PEP 563 semantics.</details>

### Question 8 — Hard
**Why annotate decorators with `ParamSpec`/`TypeVar`?**
- A) For speed
- B) So the checker preserves the wrapped function's signature instead of `*args, **kwargs`
- C) For runtime
- D) It is required

<details><summary>Reveal Answer</summary>**B.** Keeps the type contract honest.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You use type hints well. |
| 5-6 | Review generics, Protocol, and Optional. |
| < 5 | Re-read the lecture. |
