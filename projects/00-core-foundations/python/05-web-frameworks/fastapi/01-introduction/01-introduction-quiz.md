# FastAPI 01: Introduction — Quiz

> **Topic Overview**: What FastAPI is, ASGI, and automatic docs.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is FastAPI?**
- A) A database
- B) A modern async Python web framework built on Starlette and Pydantic
- C) A JS runtime
- D) A template engine

<details><summary>Reveal Answer</summary>**B.** Async framework with typed validation.</details>

### Question 2 — Easy
**What does ASGI provide over WSGI?**
- A) Nothing
- B) Async support and long-lived connections (websockets, streaming)
- C) Templates
- D) ORM

<details><summary>Reveal Answer</summary>**B.** Asynchronous server gateway.</details>

### Question 3 — Medium
**Where do automatic OpenAPI docs come from?**
- A) A plugin
- B) FastAPI introspects routes and Pydantic types to generate the schema
- C) A config file
- D) The database

<details><summary>Reveal Answer</summary>**B.** Types drive the schema.</details>

### Question 4 — Medium
**What role does Pydantic play?**
- A) Routing
- B) Request/response validation and serialization
- C) Templating
- D) Serving

<details><summary>Reveal Answer</summary>**B.** Data contracts.</details>

### Question 5 — Medium
**What does the `/docs` endpoint show?**
- A) Source code
- B) Interactive Swagger UI generated from the OpenAPI schema
- C) Logs
- D) Metrics

<details><summary>Reveal Answer</summary>**B.** Generated documentation.</details>

### Question 6 — Hard
**Why is type-hint-driven validation valuable?**
- A) It is faster
- B) The same annotation validates input, documents the API, and types the editor
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** One source of truth.</details>

### Question 7 — Hard
**What is the main performance claim of FastAPI?**
- A) Fastest database
- B) On par with Node/Go for I/O-bound APIs, thanks to ASGI and async
- C) Fastest templating
- D) GPU acceleration

<details><summary>Reveal Answer</summary>**B.** Async I/O throughput.</details>

### Question 8 — Hard
**When is FastAPI a poor fit?**
- A) Never
- B) CPU-bound batch work where a worker/queue is the right tool
- C) For APIs
- D) For async

<details><summary>Reveal Answer</summary>**B.** Match the tool to the workload.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand FastAPI's role. |
| 5-6 | Review ASGI and Pydantic. |
| < 5 | Re-read the lecture. |
