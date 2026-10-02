# FastAPI 25: Events — Quiz

> **Topic Overview**: Startup/shutdown and the lifespan context.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the modern way to manage startup/shutdown?**
- A) `@app.on_event`
- B) The `lifespan` async context manager
- C) Middleware
- D) A dependency

<details><summary>Reveal Answer</summary>**B.** Lifespan is preferred.</details>

### Question 2 — Easy
**What belongs in startup?**
- A) Requests
- B) Connecting pools, loading models, validating config
- C) Templating
- D) Routing

<details><summary>Reveal Answer</summary>**B.** Heavy shared resources.</details>

### Question 3 — Medium
**Why load a model at startup rather than per request?**
- A) Speed only
- B) Loading is expensive; per-request loading destroys latency and memory
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Amortize the cost.</details>

### Question 4 — Medium
**What belongs in shutdown?**
- A) Nothing
- B) Closing pools/connections and flushing buffers for a clean exit
- C) Requests
- D) Routing

<details><summary>Reveal Answer</summary>**B.** Graceful teardown.</details>

### Question 5 — Medium
**Why are events not for per-request work?**
- A) They are
- B) They run once per process, not per request
- C) They cache
- D) They sort

<details><summary>Reveal Answer</summary>**B.** Process lifecycle.</details>

### Question 6 — Hard
**Why does a startup exception prevent the app from serving?**
- A) It does not
- B) A failed lifespan startup aborts the worker, surfacing as crash loops
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Fail fast on bad config.</details>

### Question 7 — Hard
**What is the interaction with multiple workers?**
- A) Events run once total
- B) Startup/shutdown run per worker process, so resources are per worker
- C) Once per worker
- D) Never

<details><summary>Reveal Answer</summary>**B.** Per-process lifecycle.</details>

### Question 8 — Hard
**Why validate configuration at startup?**
- A) Style
- B) A missing secret should fail immediately, not on the first request
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Fail fast.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You manage lifecycle well. |
| 5-6 | Review lifespan and per-worker scope. |
| < 5 | Re-read the lecture. |
