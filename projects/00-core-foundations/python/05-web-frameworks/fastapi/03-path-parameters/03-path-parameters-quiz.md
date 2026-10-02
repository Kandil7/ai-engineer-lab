# FastAPI 03: Path Parameters — Quiz

> **Topic Overview**: Typed path variables and their ordering.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you declare a path parameter?**
- A) In the decorator path as `{name}` and in the function signature
- B) In the query string
- C) In the body
- D) In a header

<details><summary>Reveal Answer</summary>**A.** Path + typed argument.</details>

### Question 2 — Easy
**What happens if the path value does not match the declared type?**
- A) It is coerced silently
- B) FastAPI returns a 422 validation error
- C) It crashes
- D) It returns None

<details><summary>Reveal Answer</summary>**B.** Type validation.</details>

### Question 3 — Medium
**Where is a path parameter documented?**
- A) Nowhere
- B) In the generated OpenAPI operation
- C) In a config file
- D) In the database

<details><summary>Reveal Answer</summary>**B.** Part of the contract.</details>

### Question 4 — Medium
**Why must a fixed route like `/users/me` be declared before `/users/{id}`?**
- A) Style
- B) Routes match in order; otherwise `{id}` captures `me`
- C) For speed
- D) It does not matter

<details><summary>Reveal Answer</summary>**B.** Order matters.</details>

### Question 5 — Medium
**How do you constrain a path parameter?**
- A) You cannot
- B) With `Path(...)` metadata such as `ge`, `le`, `pattern`
- C) With a regex in the URL only
- D) In a middleware

<details><summary>Reveal Answer</summary>**B.** Declarative constraints.</details>

### Question 6 — Hard
**How does a `Enum`-typed path parameter behave?**
- A) Free string
- B) Only the enum's allowed values validate; others 422
- C) It is ignored
- D) It is coerced

<details><summary>Reveal Answer</summary>**B.** Closed value set.</details>

### Question 7 — Hard
**Why is a typed path parameter a contract, not just a variable?**
- A) It is not
- B) It constrains input, documents the API, and types the handler at once
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Validation + docs + types.</details>

### Question 8 — Hard
**What does a 422 response mean here?**
- A) Not found
- B) The request reached validation but the parameter failed
- C) Server error
- D) Unauthorized

<details><summary>Reveal Answer</summary>**B.** Validation error.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You use path parameters well. |
| 5-6 | Review typing and ordering. |
| < 5 | Re-read the lecture. |
