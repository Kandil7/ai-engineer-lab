# FastAPI 39: OAuth2 and OIDC — Quiz

> **Topic Overview**: Code+PKCE, scopes vs claims, and key rotation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does the authorization code + PKCE flow protect?**
- A) Passwords
- B) Token interception on untrusted redirects for public clients
- C) Databases
- D) Templates

<details><summary>Reveal Answer</summary>**B.** Verifier-bound exchange.</details>

### Question 2 — Easy
**What is a scope?**
- A) A user
- B) A named permission the client requests and the user grants
- C) A claim
- D) A key

<details><summary>Reveal Answer</summary>**B.** Requested access.</details>

### Question 3 — Medium
**What is a claim?**
- A) A permission
- B) A statement about the subject carried in a token
- C) A scope
- D) A key

<details><summary>Reveal Answer</summary>**B.** Token-carried fact.</details>

### Question 4 — Medium
**How does an ID token differ from an access token?**
- A) They are identical
- B) The ID token asserts identity for the client; the access token authorizes API calls
- C) The access token is longer
- D) The ID token is secret

<details><summary>Reveal Answer</summary>**B.** Authentication vs authorization.</details>

### Question 5 — Medium
**What is JWKS for?**
- A) User storage
- B) Publishing the rotating public keys so anyone can verify signatures
- C) Refresh tokens
- D) Scopes

<details><summary>Reveal Answer</summary>**B.** Key discovery.</details>

### Question 6 — Hard
**How should key rotation be handled?**
- A) Swap instantly
- B) Publish the new key with an overlap window and retire the old one after TTL
- C) Never rotate
- D) Rotate per request

<details><summary>Reveal Answer</summary>**B.** Overlap avoids outages.</details>

### Question 7 — Hard
**Why validate `aud` and `iss`?**
- A) Style
- B) An otherwise valid token minted for someone else, or by someone else, must be rejected
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Intended audience and issuer.</details>

### Question 8 — Hard
**Why is the resource server's clock a security input?**
- A) It is not
- B) Skewed clocks widen the `exp`/`nbf` window an attacker can abuse
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Time is a trust input.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You wire OAuth2/OIDC correctly. |
| 5-6 | Review tokens, claims, and rotation. |
| < 5 | Re-read the lecture. |
