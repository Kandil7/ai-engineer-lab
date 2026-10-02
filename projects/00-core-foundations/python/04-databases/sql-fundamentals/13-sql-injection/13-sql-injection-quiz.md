# SQL Fundamentals 13: SQL Injection — Quiz

> **Topic Overview**: Interpolation, parameters, identifiers, and least privilege.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the injection primitive?**
- A) A slow query
- B) Interpolating user input into SQL text so it becomes code
- C) A missing index
- D) A deadlock

<details><summary>Reveal Answer</summary>**B.** Data becomes code.</details>

### Question 2 — Easy
**What is the fix?**
- A) Escaping by hand
- B) Parameterized queries: values travel separately from the statement
- C) Blacklists
- D) Hashing input

<details><summary>Reveal Answer</summary>**B.** Parameters, never interpolation.</details>

### Question 3 — Medium
**Why can parameters not cover table/column names?**
- A) They can
- B) Placeholders bind values only; identifiers need allowlisting
- C) Speed
- D) They error

<details><summary>Reveal Answer</summary>**B.** Values vs identifiers.</details>

### Question 4 — Medium
**How do you handle dynamic identifiers safely?**
- A) Interpolate
- B) Validate against an allowlist of known names
- C) Escape quotes
- D) Hash them

<details><summary>Reveal Answer</summary>**B.** Allowlist, never raw input.</details>

### Question 5 — Medium
**What is least privilege for the app's DB role?**
- A) Superuser
- B) Only the operations and tables the app needs
- C) Read-only always
- D) No role

<details><summary>Reveal Answer</summary>**B.** Minimal rights.</details>

### Question 6 — Hard
**Do ORMs make injection impossible?**
- A) Yes
- B) No; raw fragments and unvalidated identifiers still inject
- C) They are slower
- D) They error

<details><summary>Reveal Answer</summary>**B.** ORMs help, not magic.</details>

### Question 7 — Hard
**Why is client-side validation not a defense?**
- A) It is
- B) Attackers bypass the client; the server must validate
- C) It is slow
- D) It errors

<details><summary>Reveal Answer</summary>**B.** Server-side is the boundary.</details>

### Question 8 — Hard
**What does defense in depth add beyond parameters?**
- A) Nothing
- B) Least-privilege roles, allowlisted identifiers, and logging, so one failure does not sink the data
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Layered protection.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You prevent injection. |
| 5-6 | Review parameters and identifiers. |
| < 5 | Re-read the lecture. |
