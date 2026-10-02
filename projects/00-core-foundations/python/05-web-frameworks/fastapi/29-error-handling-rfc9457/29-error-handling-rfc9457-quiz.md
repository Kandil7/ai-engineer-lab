# FastAPI 29: Error Handling (RFC 9457) — Quiz

> **Topic Overview**: The problem-details envelope and client-actionable errors.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What fields does an RFC 9457 problem object carry?**
- A) `{"error": ...}`
- B) `type`, `title`, `status`, plus optional `detail` and `instance`
- C) A stack trace
- D) The route name

<details><summary>Reveal Answer</summary>**B.** The standard envelope.</details>

### Question 2 — Easy
**Why use one envelope for every error?**
- A) Style
- B) Clients can parse any failure uniformly instead of branching per endpoint
- C) For speed
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Uniform client handling.</details>

### Question 3 — Medium
**What makes a 422 actionable?**
- A) The status code
- B) Pointing at the failing field with the rule violated
- C) The stack trace
- D) The request id

<details><summary>Reveal Answer</summary>**B.** Field-level detail.</details>

### Question 4 — Medium
**What should a 500 return?**
- A) The exception message
- B) A generic problem object with a logged correlation id, never internals
- C) The stack trace
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Generic to clients, details in logs.</details>

### Question 5 — Medium
**What makes a 404 actionable?**
- A) The path
- B) Naming the missing resource and the identifier, plus what exists
- C) The stack trace
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Client can fix the call.</details>

### Question 6 — Hard
**Why add an extension member like `errors[]`?**
- A) Required by the RFC
- B) Standard envelope plus structured per-field failures machines can act on
- C) For speed
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Machine-readable detail.</details>

### Question 7 — Hard
**What is the risk of echoing request input in an error?**
- A) None
- B) Reflected content can enable XSS when errors render in a browser
- C) For speed
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Treat input as untrusted in output too.</details>

### Question 8 — Hard
**Why return a stable `type` URI per error kind?**
- A) Required
- B) Clients can branch on a stable code instead of fragile message text
- C) For speed
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Codes, not prose.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You shape errors correctly. |
| 5-6 | Review the envelope and 5xx secrecy. |
| < 5 | Re-read the lecture. |
