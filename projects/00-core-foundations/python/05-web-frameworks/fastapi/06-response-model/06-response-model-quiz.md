# FastAPI 06: Response Model — Quiz

> **Topic Overview**: `response_model`, filtering, and status codes.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `response_model` do?**
- A) Validates the request
- B) Declares and validates/filters the response shape
- C) Routes
- D) Caches

<details><summary>Reveal Answer</summary>**B.** Output contract.</details>

### Question 2 — Easy
**How does it prevent leaking sensitive fields?**
- A) It does not
- B) Extra fields (e.g. a password hash) are dropped because only declared fields serialize
- C) It encrypts
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Output filtering.</details>

### Question 3 — Medium
**How do you set a non-200 status code?**
- A) In the body
- B) `status_code=` on the decorator, or a `Response` parameter
- C) In a header
- D) You cannot

<details><summary>Reveal Answer</summary>**B.** Declared status.</details>

### Question 4 — Medium
**What does `response_model_exclude_unset=True` do?**
- A) Excludes nulls
- B) Omits fields the client did not set, useful for PATCH
- C) Excludes defaults
- D) Excludes all

<details><summary>Reveal Answer</summary>**B.** Unset fields omitted.</details>

### Question 5 — Medium
**Can the response model differ from the request model?**
- A) No
- B) Yes, and it should when the response has derived or hidden fields
- C) Only for POST
- D) Never

<details><summary>Reveal Answer</summary>**B.** Separate input/output contracts.</details>

### Question 6 — Hard
**What happens if the returned data violates `response_model`?**
- A) It is sent anyway
- B) FastAPI raises a response-validation error (500)
- C) It coerces silently
- D) It 404s

<details><summary>Reveal Answer</summary>**B.** Output is validated too.</details>

### Question 7 — Hard
**Why is response validation a correctness feature, not overhead?**
- A) It is not
- B) It guarantees the API contract holds even when internals change
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Contract enforcement.</details>

### Question 8 — Hard
**How do you return a model with computed fields?**
- A) Add them to the model (e.g. `computed_field`) so they serialize
- B) Return a dict
- C) Patch the response
- D) You cannot

<details><summary>Reveal Answer</summary>**A.** Declared computed output.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You control responses well. |
| 5-6 | Review filtering and status codes. |
| < 5 | Re-read the lecture. |
