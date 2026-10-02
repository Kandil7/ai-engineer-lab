# FastAPI 17: Static Files — Quiz

> **Topic Overview**: Mounting static assets and caching.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you serve static files?**
- A) `app.mount("/static", StaticFiles(directory="static"))`
- B) `app.get("/static")`
- C) `app.files(...)`
- D) `app.serve(...)`

<details><summary>Reveal Answer</summary>**A.** Mount a sub-app.</details>

### Question 2 — Easy
**What does mounting do?**
- A) Copies files
- B) Delegates a path prefix to another ASGI app
- C) Caches
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Prefix delegation.</details>

### Question 3 — Medium
**Why should production static assets usually be served by a CDN/proxy?**
- A) Style
- B) Offloads the app workers and adds caching/edge delivery
- C) It is required
- D) For sorting

<details><summary>Reveal Answer</summary>**B.** Keep the app for APIs.</details>

### Question 4 — Medium
**What caching header helps static assets?**
- A) `Cache-Control: no-store`
- B) Long `max-age` with content-hashed filenames
- C) `Pragma`
- D) None

<details><summary>Reveal Answer</summary>**B.** Immutable cacheable assets.</details>

### Question 5 — Medium
**Why content-hash filenames?**
- A) For style
- B) So a change produces a new URL and caches never serve stale bytes
- C) For speed
- D) For sorting

<details><summary>Reveal Answer</summary>**B.** Cache-busting by construction.</details>

### Question 6 — Hard
**What is the risk of serving a user-uploaded directory as static?**
- A) None
- B) Stored XSS or content exposure if files are untrusted
- C) Slow
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Separate untrusted uploads.</details>

### Question 7 — Hard
**Why might mounting static before routes matter?**
- A) It does not
- B) Route matching order can intercept the prefix if not mounted appropriately
- C) For speed
- D) For caching

<details><summary>Reveal Answer</summary>**B.** Ordering matters.</details>

### Question 8 — Hard
**What is directory traversal here?**
- A) A network path
- B) A request escaping the static root via `../`; the server must confine paths
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Confine to the root.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You serve static files well. |
| 5-6 | Review caching and traversal. |
| < 5 | Re-read the lecture. |
