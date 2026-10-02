# Advanced Python 31: Concurrency Patterns — Quiz

> **Topic Overview**: Deadlock fixes, pools, backoff, circuit breakers, and bulkheads.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What prevents a producer from outrunning consumers in a queue design?**
- A) A lock
- B) A bounded queue, which applies backpressure
- C) A cache
- D) A sort

<details><summary>Reveal Answer</summary>**B.** Bounded capacity.</details>

### Question 2 — Easy
**What is a worker pool?**
- A) A lock
- B) A fixed set of workers consuming from a shared work queue
- C) A cache
- D) A sort

<details><summary>Reveal Answer</summary>**B.** Bounded concurrency.</details>

### Question 3 — Medium
**What is fan-out/fan-in?**
- A) Sorting
- B) Split work to many workers (fan-out) and collect results (fan-in)
- C) Locking
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Parallel map-reduce shape.</details>

### Question 4 — Medium
**Why add jitter to retry backoff?**
- A) For speed
- B) Without it, many clients retry in lockstep (thundering herd), re-crashing the service
- C) It hashes
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Desynchronize retries.</details>

### Question 5 — Medium
**What does a circuit breaker do?**
- A) Caches
- B) Fails fast when a dependency is unhealthy, then probes to recover
- C) Locks
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Stop hammering a dead dependency.</details>

### Question 6 — Hard
**What is the difference between deadlock, livelock, and starvation?**
- A) They are the same
- B) Deadlock: no progress; livelock: busy but no progress; starvation: some task never gets a turn
- C) All are crashes
- D) All are fast

<details><summary>Reveal Answer</summary>**B.** Three distinct failure modes.</details>

### Question 7 — Hard
**What does a bulkhead isolate?**
- A) Caches
- B) Failure: per-dependency resource pools stop one slow dependency draining everything
- C) Locks
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Fault containment.</details>

### Question 8 — Hard
**What is a token bucket for?**
- A) Sorting
- B) Rate limiting: tokens refill over time and each request consumes one
- C) Caching
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Smooth rate control.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can design resilient concurrency. |
| 5-6 | Review backoff, breaker, and bulkhead. |
| < 5 | Re-read the lecture. |
