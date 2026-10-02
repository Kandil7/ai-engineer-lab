# SQLAlchemy 07: Async SQLAlchemy — Quiz

> **Topic Overview**: `AsyncEngine`, `AsyncSession`, and per-request async sessions.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What must be awaited in `AsyncSession`?**
- A) Nothing
- B) Add, commit, and reads — the session boundary is async
- C) Only commits
- D) Only reads

<details><summary>Reveal Answer</summary>**B.** Await the session.</details>

### Question 2 — Easy
**What is `async_sessionmaker`?**
- A) A pool
- B) The factory producing `AsyncSession` instances
- C) An engine
- D) A migration

<details><summary>Reveal Answer</summary>**B.** Session factory.</details>

### Question 3 — Medium
**What is `run_sync` for?**
- A) Speed
- B) Running sync-style code (migrations, DDL) inside the async engine via a greenlet bridge
- C) Caching
- D) Pooling

<details><summary>Reveal Answer</summary>**B.** Sync bridge.</details>

### Question 4 — Medium
**How do you wire async session-per-request in FastAPI?**
- A) Global session
- B) An async DI dependency yielding a session and closing after
- C) Sync session
- D) A pool directly

<details><summary>Reveal Answer</summary>**B.** Request-scoped async.</details>

### Question 5 — Medium
**Why does lazy loading fail in async?**
- A) It does not
- B) Attribute access triggers sync I/O with no await point
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** No implicit I/O.</details>

### Question 6 — Hard
**What does the batch async ingest pattern combine?**
- A) Sync inserts
- B) Chunked Core inserts with `await` and bounded concurrency
- C) Caching
- D) Migrations

<details><summary>Reveal Answer</summary>**B.** Bounded async bulk.</details>

### Question 7 — Hard
**Why must the async driver match the sync URL?**
- A) Style
- B) `postgresql+asyncpg://` vs `postgresql://` select different drivers; a mismatch fails
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Driver scheme matters.</details>

### Question 8 — Hard
**What happens sharing one `AsyncSession` across tasks?**
- A) Nothing
- B) Interleaved unit-of-work state corrupts both
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** One session, one task flow.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You run async SQLAlchemy well. |
| 5-6 | Review sessions and lazy loading. |
| < 5 | Re-read the lecture. |
