# FastAPI 47: Resilience Patterns — Quiz

> **Topic Overview**: Timeouts, retries, breakers, bulkheads, and degradation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the first resilience rule?**
- A) Retry everything
- B) Always set a timeout
- C) Add workers
- D) Cache everything

<details><summary>Reveal Answer</summary>**B.** Bound every wait.</details>

### Question 2 — Easy
**Why retry with backoff and jitter?**
- A) Speed
- B) Backoff gives the dependency room; jitter stops synchronized retry storms
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Patient, desynchronized retries.</details>

### Question 3 — Medium
**What does a circuit breaker do?**
- A) Caches
- B) Trips open after failures, fails fast, and probes recovery before closing
- C) Restarts
- D) Logs

<details><summary>Reveal Answer</summary>**B.** Stop feeding a dead dependency.</details>

### Question 4 — Medium
**What is a bulkhead?**
- A) A wall
- B) Isolated resource pools per dependency so one slow service cannot drain all capacity
- C) A cache
- D) A retry

<details><summary>Reveal Answer</summary>**B.** Fault containment.</details>

### Question 5 — Medium
**What is graceful degradation?**
- A) Crashing
- B) Serving a reduced but correct answer (cached, default) when a dependency fails
- C) Retrying
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Partial beats down.</details>

### Question 6 — Hard
**Which failures should not be retried?**
- A) Timeouts
- B) Non-idempotent side effects without a dedup key, and 4xx client errors
- C) 503s
- D) DNS

<details><summary>Reveal Answer</summary>**B.** Retry only what is safe.</details>

### Question 7 — Hard
**Why is a timeout without a deadline on the caller still a leak?**
- A) It is not
- B) Threads/coroutines pile up waiting even if the dependency call eventually returns
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Bound the whole wait.</details>

### Question 8 — Hard
**What orders these patterns: timeout → retry → breaker → bulkhead → fallback?**
- A) Alphabetical
- B) From containing one call to containing the system: stop, retry, give up, isolate, degrade
- C) Random
- D) Speed

<details><summary>Reveal Answer</summary>**B.** Escalating containment.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You build resilient services. |
| 5-6 | Review breakers, bulkheads, fallbacks. |
| < 5 | Re-read the lecture. |
