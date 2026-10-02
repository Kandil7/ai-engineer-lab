# FastAPI 12: Security — Quiz

> **Topic Overview**: Security schemes, OAuth2 password flow, and the auth stub.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `OAuth2PasswordBearer` do?**
- A) Encrypts passwords
- B) Declares the token URL and extracts the bearer token dependency
- C) Stores users
- D) Hashes

<details><summary>Reveal Answer</summary>**B.** Token extraction + docs.</details>

### Question 2 — Easy
**Where do clients send the token?**
- A) Query string
- B) `Authorization: Bearer <token>`
- C) Body
- D) Cookie always

<details><summary>Reveal Answer</summary>**B.** Bearer header.</details>

### Question 3 — Medium
**What does an auth dependency return?**
- A) The token
- B) The authenticated user (or raises 401)
- C) The password
- D) The session

<details><summary>Reveal Answer</summary>**B.** Current user.</details>

### Question 4 — Medium
**What status for missing/invalid credentials?**
- A) 400
- B) 401 with `WWW-Authenticate: Bearer`
- C) 403
- D) 500

<details><summary>Reveal Answer</summary>**B.** Unauthorized.</details>

### Question 5 — Medium
**Why is security in the OpenAPI docs useful?**
- A) Style
- B) Clients and the Swagger UI know how to authenticate
- C) For caching
- D) It is not

<details><summary>Reveal Answer</summary>**B.** Declared auth scheme.</details>

### Question 6 — Hard
**What is the difference between 401 and 403 here?**
- A) They are the same
- B) 401 = not authenticated; 403 = authenticated but not permitted
- C) 401 = forbidden
- D) 403 = missing token

<details><summary>Reveal Answer</summary>**B.** Identity vs permission.</details>

### Question 7 — Hard
**Why never store raw passwords?**
- A) Speed
- B) A breach exposes them; store a salted slow hash
- C) For caching
- D) It is larger

<details><summary>Reveal Answer</summary>**B.** Hash with salt + slow KDF.</details>

### Question 8 — Hard
**Why is the password flow a stub in the lecture?**
- A) It is complete
- B) It teaches the mechanism; real systems delegate to OIDC/identity providers
- C) It is deprecated
- D) It is insecure only

<details><summary>Reveal Answer</summary>**B.** Mechanism vs production auth.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand FastAPI security. |
| 5-6 | Review bearer auth and status codes. |
| < 5 | Re-read the lecture. |
