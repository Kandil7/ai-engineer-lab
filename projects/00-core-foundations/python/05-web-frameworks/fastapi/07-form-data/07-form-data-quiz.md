# FastAPI 07: Form Data — Quiz

> **Topic Overview**: `Form` fields and form vs JSON.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Which package must be installed for form parsing?**
- A) `python-multipart`
- B) `jinja2`
- C) `httpx`
- D) `uvicorn`

<details><summary>Reveal Answer</summary>**A.** Multipart/form-urlencoded parser.</details>

### Question 2 — Easy
**How do you declare a form field?**
- A) `Form(...)`
- B) `Query(...)`
- C) `Body(...)`
- D) `Path(...)`

<details><summary>Reveal Answer</summary>**A.** `Form` marks the source.</details>

### Question 3 — Medium
**What content type do HTML forms submit by default?**
- A) JSON
- B) `application/x-www-form-urlencoded`
- C) XML
- D) text

<details><summary>Reveal Answer</summary>**B.** Standard form encoding.</details>

### Question 4 — Medium
**Why does FastAPI need to distinguish `Form` from body models?**
- A) For speed
- B) They use different media types; declaring the source binds correctly
- C) It does not
- D) For docs only

<details><summary>Reveal Answer</summary>**B.** Source drives parsing.</details>

### Question 5 — Medium
**Can form fields be validated?**
- A) No
- B) Yes, with the same `Form(...)` constraints as `Query`
- C) Only strings
- D) Only required

<details><summary>Reveal Answer</summary>**B.** Same constraint system.</details>

### Question 6 — Hard
**Why prefer JSON bodies for APIs but forms for HTML login pages?**
- A) No reason
- B) Browsers post forms; APIs speak JSON; match the client
- C) For speed
- D) It is required

<details><summary>Reveal Answer</summary>**B.** Match the consumer.</details>

### Question 7 — Hard
**What is the 422 response for a missing form field?**
- A) 404
- B) 422 validation error
- C) 500
- D) 401

<details><summary>Reveal Answer</summary>**B.** Validation failure.</details>

### Question 8 — Hard
**Why is CSRF a concern with form posts?**
- A) It is not
- B) Browsers attach cookies automatically, so cross-site forms can act as the user
- C) Forms are encrypted
- D) For speed

<details><summary>Reveal Answer</summary>**B.** Cookie-auth form posts need CSRF protection.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You handle form data. |
| 5-6 | Review form vs JSON and CSRF. |
| < 5 | Re-read the lecture. |
