# FastAPI 13: JWT Auth — Quiz

> **Topic Overview**: Signing, verifying, and expiry of JSON Web Tokens.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a JWT composed of?**
- A) Header, payload, signature (three base64url parts)
- B) A cookie
- C) A hash
- D) A session id

<details><summary>Reveal Answer</summary>**A.** Three dot-separated parts.</details>

### Question 2 — Easy
**What makes a JWT trustworthy?**
- A) It is encrypted
- B) The signature, verified with the secret/public key
- C) Its size
- D) Its expiry

<details><summary>Reveal Answer</summary>**B.** Signed, not necessarily encrypted.</details>

### Question 3 — Medium
**What standard field carries expiry?**
- A) `sub`
- B) `exp`
- C) `iat`
- D) `aud`

<details><summary>Reveal Answer</summary>**B.** `exp`.</details>

### Question 4 — Medium
**Why must you always verify the signature before trusting claims?**
- A) For speed
- B) An unverified token is attacker-controlled data
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Signature is the only trust anchor.</details>

### Question 5 — Medium
**Can the payload be read by anyone?**
- A) No
- B) Yes; JWT payloads are base64url, not encrypted
- C) Only with 2FA
- D) Only the server

<details><summary>Reveal Answer</summary>**B.** Do not put secrets in claims.</details>

### Question 6 — Hard
**Why is long-lived access-token expiry a risk?**
- A) It is not
- B) A stolen token is valid until expiry; short lives plus refresh reduce the window
- C) It is faster
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Minimize the blast radius.</details>

### Question 7 — Hard
**Why can't you revoke a JWT by deleting it server-side?**
- A) You can
- B) It is stateless; revocation needs a denylist or short expiry
- C) It is encrypted
- D) It is signed

<details><summary>Reveal Answer</summary>**B.** Stateless tradeoff.</details>

### Question 8 — Hard
**What does refresh-token rotation protect against?**
- A) None
- B) Replay of a stolen refresh token, by invalidating the old one on each use
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** One-time refresh tokens.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You handle JWTs correctly. |
| 5-6 | Review signing, expiry, revocation. |
| < 5 | Re-read the lecture. |
