# Redis 04: Rate Limiting — Quiz

> **Topic Overview**: Fixed/sliding windows, token buckets, and atomicity.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How does fixed-window limiting work?**
- A) `INCR` a counter keyed by window, `EXPIRE` it
- B) A sorted set
- C) A token bucket
- D) A lock

<details><summary>Reveal Answer</summary>**B.** Count per window.</details>

### Question 2 — Easy
**What is the fixed-window edge flaw?**
- A) None
- B) A burst can straddle two windows, doubling the effective rate
- C) It is slow
- D) It needs Lua

<details><summary>Reveal Answer</summary>**B.** Boundary burst.</details>

### Question 3 — Medium
**How does a sliding window fix it?**
- A) Bigger windows
- B) Timestamped entries in a sorted set, trimming older than the window
- C) Token bucket
- D) Fixed counters

<details><summary>Reveal Answer</summary>**B.** True trailing window.</details>

### Question 4 — Medium
**What does a token bucket smooth?**
- A) Nothing
- B) Bursts: tokens refill over time and each request spends one
- C) Windows
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Burst-tolerant rate.</details>

### Question 5 — Medium
**Why must check-then-act be atomic?**
- A) Speed
- B) Concurrent requests can all pass the check before any increments
- C) Style
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Race on the counter.</details>

### Question 6 — Hard
**How do you make it atomic?**
- A) Two commands
- B) A Lua script or a single conditional command
- C) A lock
- D) Trust

<details><summary>Reveal Answer</summary>**B.** Server-side atomicity.</details>

### Question 7 — Hard
**Why Redis for distributed limits?**
- A) Speed only
- B) One shared, atomic counter store all workers see
- C) Persistence
- D) Size

<details><summary>Reveal Answer</summary>**B.** Shared truth.</details>

### Question 8 — Hard
**What key should a per-user limiter use?**
- A) The route
- B) `ratelimit:{user}:{window}` so users do not share budget
- C) A global key
- D) The IP only

<details><summary>Reveal Answer</summary>**B.** Per-actor keys.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You limit correctly. |
| 5-6 | Review windows and atomicity. |
| < 5 | Re-read the lecture. |
