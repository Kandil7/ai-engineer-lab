# FastAPI 05: Request Body — Quiz

> **Topic Overview**: Pydantic models as request bodies and nesting.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**When does an argument become the request body?**
- A) Always
- B) When it is typed as a Pydantic model (or a dict-like schema)
- C) When it is a string
- D) Never

<details><summary>Reveal Answer</summary>**B.** Model-typed args are bodies.</details>

### Question 2 — Easy
**What content type is the body expected in by default?**
- A) form-data
- B) `application/json`
- C) XML
- D) text

<details><summary>Reveal Answer</summary>**B.** JSON body.</details>

### Question 3 — Medium
**Can you combine a path param, query params, and a body?**
- A) No
- B) Yes; FastAPI infers each from its declaration
- C) Only two
- D) Only with `Body`

<details><summary>Reveal Answer</summary>**B.** Declarations drive binding.</details>

### Question 4 — Medium
**How do you nest a model inside another?**
- A) You cannot
- B) Type a field as another Pydantic model
- C) Use a dict
- D) Use a list

<details><summary>Reveal Answer</summary>**B.** Nested validation.</details>

### Question 5 — Medium
**What happens to extra fields by default?**
- A) They are kept
- B) They are ignored unless the model forbids them
- C) They cause a 500
- D) They are stored

<details><summary>Reveal Answer</summary>**B.** Default model config.</details>

### Question 6 — Hard
**Why use a model instead of a raw `dict`?**
- A) Speed
- B) It validates, documents, and types the body; a dict validates nothing
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Typed contract.</details>

### Question 7 — Hard
**How do you make a body field optional?**
- A) Give it a default or `| None`
- B) Use `Optional`
- C) Add `?`
- D) It is always optional

<details><summary>Reveal Answer</summary>**A.** Defaults mark optional.</details>

### Question 8 — Hard
**What does a 422 on a body mean?**
- A) Not found
- B) The body failed schema/validation
- C) Server error
- D) Unauthorized

<details><summary>Reveal Answer</summary>**B.** Validation failure.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You model request bodies well. |
| 5-6 | Review nesting and optionality. |
| < 5 | Re-read the lecture. |
