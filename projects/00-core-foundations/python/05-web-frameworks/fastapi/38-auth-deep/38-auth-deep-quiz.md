# FastAPI 38: Auth Deep — Quiz

> **Topic Overview**: Sessions vs tokens, JWT structure, and refresh rotation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the core tradeoff of sessions vs tokens?**
- A) Speed
- B) Server-side sessions are revocable but stateful; tokens are stateless but hard to revoke
- C) Cost
- D) None

<details><summary>Reveal Answer</summary>**B.** Revocability vs statelessness.</details>

### Question 2 — Easy
**What are JWT's three parts?**
- A) User, pass, hash
- B) Header, payload, signature
- C) Key, value, index
- D) Get, post, put

<details><summary>Reveal Answer</summary>**B.** Signed segments.</details>

### Question 3 — Medium
**What are JWTs bad at?**
- A) Everything
- B) Revocation, large payloads, and secrecy (they are readable)
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Stateless limits.</details>

### Question 4 — Medium
**How does refresh rotation work?**
- A) Refresh tokens never change
- B) Each use issues a new access token and a new refresh token, retiring the old one
- C) Refresh tokens are long access tokens
- D) Rotation is not needed

<details><summary>Reveal Answer</summary>**B.** One-time refresh tokens.</details>

### Question 5 — Medium
**Why hash passwords with bcrypt?**
- A) Speed
- B) Slow, salted hashing resists brute force after a breach
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Breach-resistant storage.</details>

### Question 6 — Hard
**Why use a timing-safe compare for secrets?**
- A) Style
- B) Early-exit string compare leaks the matching prefix through timing
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Close the timing side channel.</details>

### Question 7 — Hard
**Where do short access tokens plus rotation pay off?**
- A) Nowhere
- B) A stolen access token dies fast while refresh stays usable legitimately
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Small blast radius.</details>

### Question 8 — Hard
**What belongs in the `sub` claim?**
- A) The email
- B) A stable, opaque user id, not PII
- C) The password
- D) The whole profile

<details><summary>Reveal Answer</summary>**B.** Opaque identity.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You authenticate securely. |
| 5-6 | Review sessions vs tokens and rotation. |
| < 5 | Re-read the lecture. |
