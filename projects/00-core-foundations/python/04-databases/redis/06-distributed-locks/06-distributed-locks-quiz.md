# Redis 06: Distributed Locks — Quiz

> **Topic Overview**: `SET NX PX`, safe release, fencing, and Redlock.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you take a Redis lock?**
- A) `GET`
- B) `SET key token NX PX ttl`
- C) `INCR`
- D) `LPUSH`

<details><summary>Reveal Answer</summary>**B.** Atomic acquire with expiry.</details>

### Question 2 — Easy
**Why must a lock expire?**
- A) Speed
- B) A crashed holder would otherwise lock forever
- C) Memory
- D) Style

<details><summary>Reveal Answer</summary>**B.** Crash safety.</details>

### Question 3 — Medium
**Why must release check a token?**
- A) Speed
- B) Only the owner may release; an expired lock may now belong to someone else
- C) Style
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Ownership check.</details>

### Question 4 — Medium
**How is safe release implemented?**
- A) `DEL`
- B) A Lua script comparing the token before deleting
- C) `EXPIRE`
- D) `GET`

<details><summary>Reveal Answer</summary>**B.** Atomic compare-and-delete.</details>

### Question 5 — Medium
**What is the fencing-token trap?**
- A) A slow lock
- B) An expired-but-still-running holder writing after losing the lock, corrupting shared state
- C) A deadlock
- D) A cache miss

<details><summary>Reveal Answer</summary>**B.** Stale holder writes.</details>

### Question 6 — Hard
**How do fencing tokens fix it?**
- A) Longer TTL
- B) The resource rejects writes with an older token than it has seen
- C) Redlock
- D) No expiry

<details><summary>Reveal Answer</summary>**B.** Monotonic guard.</details>

### Question 7 — Hard
**What is the Redlock controversy?**
- A) It is perfect
- B) Majority-acquire across instances still has clock and failover edge cases critics reject for safety-critical use
- C) It is slow
- D) It needs Lua

<details><summary>Reveal Answer</summary>**B.** Disputed guarantees.</details>

### Question 8 — Hard
**When do you actually need a distributed lock?**
- A) Always
- B) Rarely: single-flight expensive work or leader election, after simpler designs fail
- C) For caching
- D) For queues

<details><summary>Reveal Answer</summary>**B.** Last resort.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You lock safely. |
| 5-6 | Review expiry, tokens, fencing. |
| < 5 | Re-read the lecture. |
