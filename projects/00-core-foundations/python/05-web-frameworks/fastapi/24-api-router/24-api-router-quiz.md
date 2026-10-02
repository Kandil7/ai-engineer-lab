# FastAPI 24: API Router — Quiz

> **Topic Overview**: Splitting routes into modules.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is `APIRouter` for?**
- A) Serving
- B) Grouping related routes into a module
- C) Caching
- D) Auth

<details><summary>Reveal Answer</summary>**B.** Modular routing.</details>

### Question 2 — Easy
**How do you include a router?**
- A) `app.include_router(router, prefix="/x")`
- B) `app.add(router)`
- C) `app.route(router)`
- D) You cannot

<details><summary>Reveal Answer</summary>**A.** Include with optional prefix/tags.</details>

### Question 3 — Medium
**Why split routes into routers?**
- A) Speed
- B) Large apps stay navigable; each domain lives in its own file
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Maintainability.</details>

### Question 4 — Medium
**What do `tags` on a router do?**
- A) Auth
- B) Group operations in the docs UI
- C) Cache
- D) Route

<details><summary>Reveal Answer</summary>**B.** Documentation grouping.</details>

### Question 5 — Medium
**Can a router have its own dependencies?**
- A) No
- B) Yes; `dependencies=[...]` apply to all routes in it
- C) Only auth
- D) Only one

<details><summary>Reveal Answer</summary>**B.** Shared dependencies.</details>

### Question 6 — Hard
**Why apply an auth dependency at the router level?**
- A) Speed
- B) It enforces authz across a whole domain without repeating it per route
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Centralized enforcement.</details>

### Question 7 — Hard
**What is a common prefix trap?**
- A) None
- B) Double prefixes (`/api/api/...`) from nested includes; keep prefixes unique
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Prefix composition.</details>

### Question 8 — Hard
**Why keep routers thin and services separate?**
- A) Style
- B) Routing/transport vs business logic; testable and swappable
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Separation of concerns.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You structure APIs with routers. |
| 5-6 | Review prefixes and dependencies. |
| < 5 | Re-read the lecture. |
