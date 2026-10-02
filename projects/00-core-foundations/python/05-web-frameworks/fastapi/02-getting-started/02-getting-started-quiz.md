# FastAPI 02: Getting Started — Quiz

> **Topic Overview**: The app object, running the dev server, and the first route.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you create an app?**
- A) `app = FastAPI()`
- B) `app = App()`
- C) `app = Server()`
- D) `app = Route()`

<details><summary>Reveal Answer</summary>**A.** One instance per service.</details>

### Question 2 — Easy
**Which command runs the dev server?**
- A) `python app.py`
- B) `uvicorn main:app --reload`
- C) `fastapi run`
- D) `serve app`

<details><summary>Reveal Answer</summary>**B.** Uvicorn hosts the ASGI app.</details>

### Question 3 — Medium
**What does `--reload` do?**
- A) Reloads the database
- B) Restarts the server on code changes (development only)
- C) Reloads the browser
- D) No-op

<details><summary>Reveal Answer</summary>**B.** Dev convenience, not for production.</details>

### Question 4 — Medium
**How is a route declared?**
- A) `@app.get("/")`
- B) `@route("/")`
- C) `@app.url("/")`
- D) `@get("/")`

<details><summary>Reveal Answer</summary>**A.** Decorator per HTTP method.</details>

### Question 5 — Medium
**What does `main:app` mean to uvicorn?**
- A) File `main.py`, attribute `app`
- B) Host `main`
- C) Port
- D) Module version

<details><summary>Reveal Answer</summary>**A.** Module path and app object.</details>

### Question 6 — Hard
**Why use the `--reload` flag only in development?**
- A) It is slow
- B) It watches files and restarts workers, which is wasteful and unsafe under load
- C) It disables docs
- D) It needs a GPU

<details><summary>Reveal Answer</summary>**B.** Dev-only behavior.</details>

### Question 7 — Hard
**Where are the interactive docs served by default?**
- A) `/` and `/api`
- B) `/docs` (Swagger) and `/redoc`
- C) `/openapi`
- D) `/help`

<details><summary>Reveal Answer</summary>**B.** Two built-in UIs.</details>

### Question 8 — Hard
**Why return a dict from a route?**
- A) It is required
- B) FastAPI serializes it to JSON with the correct content type
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Automatic JSON response.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can start a FastAPI app. |
| 5-6 | Review uvicorn and routes. |
| < 5 | Re-read the lecture. |
