# Redis 01: Introduction — Quiz

> **Topic Overview**: In-memory store, single-threaded execution, TTL, and eviction.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is Redis fundamentally?**
- A) A disk database
- B) An in-memory data-structure server
- C) A queue only
- D) A cache only

<details><summary>Reveal Answer</summary>**B.** Memory-first structures.</details>

### Question 2 — Easy
**Why is single-threaded execution a feature?**
- A) It is slow
- B) Commands are atomic without locks; no race conditions inside one command
- C) It uses less RAM
- D) It scales writes

<details><summary>Reveal Answer</summary>**B.** Atomic by design.</details>

### Question 3 — Medium
**What does a TTL do?**
- A) Locks a key
- B) Expires the key automatically after N seconds
- C) Backs up
- D) Replicates

<details><summary>Reveal Answer</summary>**B.** Self-expiring keys.</details>

### Question 4 — Medium
**`SET NX` vs `SET XX`?**
- A) Same
- B) `NX` sets only if absent; `XX` only if present
- C) `NX` is faster
- D) `XX` deletes

<details><summary>Reveal Answer</summary>**B.** Conditional writes.</details>

### Question 5 — Medium
**Why namespace keys (`app:entity:id`)?**
- A) Style
- B) So `SCAN`, eviction, and debugging operate per domain instead of globally
- C) Speed
- D) Replication

<details><summary>Reveal Answer</summary>**B.** Scoped keyspace.</details>

### Question 6 — Hard
**What happens at `maxmemory`?**
- A) Writes fail always
- B) The eviction policy decides which keys die to make room
- C) Reads fail
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Policy-driven eviction.</details>

### Question 7 — Hard
**Why can `KEYS *` take down production?**
- A) It is slow to type
- B) It blocks the single thread scanning the whole keyspace; use `SCAN`
- C) It deletes keys
- D) It replicates

<details><summary>Reveal Answer</summary>**B.** Blocking scan.</details>

### Question 8 — Hard
**When is Redis the wrong store?**
- A) Never
- B) For data that must survive restarts cheaply or exceed RAM comfortably
- C) For caching
- D) For queues

<details><summary>Reveal Answer</summary>**B.** Memory economics.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand Redis basics. |
| 5-6 | Review TTL, NX/XX, eviction. |
| < 5 | Re-read the lecture. |
