# FastAPI 14: OAuth2 — Quiz

> **Topic Overview**: Grant types, tokens, and scopes.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does OAuth2 authorize?**
- A) Passwords
- B) Delegated access via tokens, without sharing credentials
- C) Encryption
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Delegated authorization.</details>

### Question 2 — Easy
**Which flow suits server-to-server?**
- A) Authorization code with PKCE
- B) Client credentials
- C) Implicit
- D) Password

<details><summary>Reveal Answer</summary>**B.** Machine-to-machine.</details>

### Question 3 — Medium
**Which flow is recommended for user-facing apps?**
- A) Implicit
- B) Authorization code + PKCE
- C) Password grant
- D) Client credentials

<details><summary>Reveal Answer</summary>**B.** Best current practice.</details>

### Question 4 — Medium
**What is a scope?**
- A) A token
- B) A named permission the client requests
- C) A user
- D) A secret

<details><summary>Reveal Answer</summary>**B.** Requested permission.</details>

### Question 5 — Medium
**What is an access token for?**
- A) Identifying the user
- B) Authorizing API calls
- C) Refresh
- D) Encryption

<details><summary>Reveal Answer</summary>**B.** Bearer credential.</details>

### Question 6 — Hard
**Why is the implicit flow discouraged?**
- A) Slow
- B) Tokens leak via the URL fragment and it lacks PKCE
- C) It uses secrets
- D) It is newer

<details><summary>Reveal Answer</summary>**B.** Deprecated in favor of code+PKCE.</details>

### Question 7 — Hard
**What does PKCE add to the code flow?**
- A) Encryption
- B) A code verifier/challenge preventing authorization-code interception
- C) Hashing
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Public-client protection.</details>

### Question 8 — Hard
**Why is OAuth2 not authentication by itself?**
- A) It is
- B) It grants access; identity needs OpenID Connect's ID token
- C) It encrypts
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Authz vs authentication.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand OAuth2. |
| 5-6 | Review flows, scopes, PKCE. |
| < 5 | Re-read the lecture. |
