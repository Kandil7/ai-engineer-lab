# FastAPI 34: Caching Strategies — Quiz

> **Topic Overview**: Conditional requests, cache keys, and invalidation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does an ETag enable?**
- A) Auth
- B) Conditional requests: the client sends `If-None-Match` and gets 304 if unchanged
- C) Routing
- D) Caching server-side

<details><summary>Reveal Answer</summary>**B.** Bandwidth savings.</details>

### Question 2 — Easy
**What is `Cache-Control: public, max-age=3600`?**
- A) No caching
- B) A shared-cache policy keeping the response for an hour
- C) Auth
- D) Routing

<details><summary>Reveal Answer</summary>**B.** Cache policy.</details>

### Question 3 — Medium
**What is cache-aside?**
- A) Write-through
- B) Read from cache, fall back to the source on a miss, then store
- C) A CDN
- D) A header

<details><summary>Reveal Answer</summary>**B.** Application-managed cache.</details>

### Question 4 — Medium
**What must a cache key encode?**
- A) The path
- B) The full identity: route, params, version, and any tenant/user that changes the answer
- C) The user only
- D) The time

<details><summary>Reveal Answer</summary>**B.** Complete identity.</details>

### Question 5 — Medium
**Why must per-user and shared data never share a cache key space?**
- A) Speed
- B) Cross-user leakage: one user sees another's cached response
- C) Caching is slow
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Tenant boundary.</details>

### Question 6 — Hard
**Why is invalidation the hard part?**
- A) It is trivial
- B) Stale reads persist until TTL or an invalidation event you must emit on every write path
- C) Caching is instant
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Writes must invalidate.</details>

### Question 7 — Hard
**What is the risk of caching an authorized-but-varying response?**
- A) None
- B) Serving user A's private data to user B from the shared cache
- C) Speed
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Same as the key-space rule.</details>

### Question 8 — Hard
**When is `private` required over `public`?**
- A) Always
- B) For per-user responses shared caches must not store
- C) Never
- D) For static assets

<details><summary>Reveal Answer</summary>**B.** Per-user scoping.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You cache correctly. |
| 5-6 | Review keys and invalidation. |
| < 5 | Re-read the lecture. |
