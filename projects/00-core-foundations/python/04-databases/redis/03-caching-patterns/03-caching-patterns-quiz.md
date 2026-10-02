# Redis 03: Caching Patterns — Quiz

> **Topic Overview**: Cache-aside, write policies, stampedes, and hit-rate math.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is cache-aside?**
- A) Write-through
- B) Read from cache, fall back to source on miss, then store
- C) A CDN
- D) Write-back

<details><summary>Reveal Answer</summary>**B.** Lazy loading.</details>

### Question 2 — Easy
**What is write-through?**
- A) Lazy loading
- B) Every write goes to cache and source together
- C) Async writes
- D) No writes

<details><summary>Reveal Answer</summary>**B.** Synchronous coherence.</details>

### Question 3 — Medium
**Why is write-back rare?**
- A) It is slow
- B) Acknowledged writes live only in cache until flushed — a crash loses them
- C) It is complex
- D) It needs TTL

<details><summary>Reveal Answer</summary>**B.** Durability risk.</details>

### Question 4 — Medium
**What is a cache stampede?**
- A) Fast hits
- B) A hot key expiring lets every request hit the source at once
- C) A slow query
- D) A full cache

<details><summary>Reveal Answer</summary>**B.** Thundering herd.</details>

### Question 5 — Medium
**How do you prevent stampedes?**
- A) Longer TTL only
- B) Request coalescing, probabilistic early refresh, or a lock around recompute
- C) Bigger cache
- D) No cache

<details><summary>Reveal Answer</summary>**B.** Single-flight recompute.</details>

### Question 6 — Hard
**What is cache penetration?**
- A) High hit rate
- B) Queries for nonexistent keys bypass the cache every time
- C) Slow writes
- D) Full memory

<details><summary>Reveal Answer</summary>**B.** Miss flood.</details>

### Question 7 — Hard
**How do you stop penetration?**
- A) Bigger TTL
- B) Negative caching (store the miss briefly) or a Bloom prefilter
- C) More RAM
- D) No cache

<details><summary>Reveal Answer</summary>**B.** Cache the absence.</details>

### Question 8 — Hard
**What does hit-rate math decide?**
- A) Nothing
- B) Whether the cache earns its complexity: hits must dominate the workload
- C) TTL
- D) Size

<details><summary>Reveal Answer</summary>**B.** Measure the win.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You design caches well. |
| 5-6 | Review stampede and penetration. |
| < 5 | Re-read the lecture. |
