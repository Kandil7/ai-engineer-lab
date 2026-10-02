# FastAPI 04: Query Parameters — Quiz

> **Topic Overview**: Optional/required query params, defaults, and validation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**When does a function argument become a query parameter?**
- A) Always
- B) When it is not part of the path and is a simple type
- C) Only with a decorator
- D) Never

<details><summary>Reveal Answer</summary>**B.** Simple args map to the query string.</details>

### Question 2 — Easy
**How do you make a query parameter optional?**
- A) Give it a default (`q: str | None = None`)
- B) Use `Optional`
- C) Add `?`
- D) It is always optional

<details><summary>Reveal Answer</summary>**A.** Default value.</details>

### Question 3 — Medium
**What does `Query(...)` provide?**
- A) Routing
- B) Extra validation and metadata (`ge`, `le`, `max_length`, description)
- C) Caching
- D) Auth

<details><summary>Reveal Answer</summary>**B.** Declarative constraints.</details>

### Question 4 — Medium
**How are list query parameters passed?**
- A) Comma-separated by default
- B) Repeated keys (`?tag=a&tag=b`) with `list[str]` typed
- C) JSON
- D) Not supported

<details><summary>Reveal Answer</summary>**B.** Multi-value query params.</details>

### Question 5 — Medium
**Why avoid a huge number of query parameters?**
- A) Speed
- B) It signals an unclear resource/endpoint design; consider filters or a search body
- C) They are unsupported
- D) They cannot be validated

<details><summary>Reveal Answer</summary>**B.** Keep endpoints legible.</details>

### Question 6 — Hard
**How do you add an example to a query parameter in the docs?**
- A) A comment
- B) `Query(example=...)` (or `examples=`)
- C) A docstring only
- D) You cannot

<details><summary>Reveal Answer</summary>**B.** Metadata drives docs.</details>

### Question 7 — Hard
**What is the difference between a missing required query param and a wrong-typed one?**
- A) Same
- B) Both are 422, but the error detail differs
- C) Missing is 404
- D) Wrong type is 500

<details><summary>Reveal Answer</summary>**B.** Validation errors with detail.</details>

### Question 8 — Hard
**Why is defaulting a query parameter to a mutable value dangerous?**
- A) It is not
- B) The default is shared across requests, causing cross-request state
- C) It is faster
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Use `None` and build inside.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You use query parameters well. |
| 5-6 | Review defaults and validation. |
| < 5 | Re-read the lecture. |
