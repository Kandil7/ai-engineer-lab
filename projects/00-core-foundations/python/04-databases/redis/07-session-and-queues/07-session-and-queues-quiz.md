# Redis 07: Sessions and Queues — Quiz

> **Topic Overview**: Session hashes, FIFO/priority queues, delays, and recovery.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How do you store a session?**
- A) A string
- B) A hash keyed by session id with a TTL, renewed on activity
- C) A list
- D) A set

<details><summary>Reveal Answer</summary>**B.** Hash plus sliding expiry.</details>

### Question 2 — Easy
**How do you build a FIFO queue?**
- A) A set
- B) `LPUSH` plus `BRPOP` on a list
- C) A hash
- D) Pub/Sub

<details><summary>Reveal Answer</summary>**B.** Blocking list pop.</details>

### Question 3 — Medium
**How do you build a priority queue?**
- A) Multiple lists
- B) A sorted set scored by priority, popped from the top
- C) A hash
- D) Pub/Sub

<details><summary>Reveal Answer</summary>**B.** Score-ordered work.</details>

### Question 4 — Medium
**How do you delay a job?**
- A) `SLEEP`
- B) A sorted set scored by run-at time, moved to ready when due
- C) TTL
- D) Pub/Sub

<details><summary>Reveal Answer</summary>**B.** Time-scored scheduling.</details>

### Question 5 — Medium
**What makes a queue reliable?**
- A) Speed
- B) Lease plus heartbeat: a crashed worker's job returns to ready after timeout
- C) Bigger lists
- D) Pub/Sub

<details><summary>Reveal Answer</summary>**B.** Lease recovery.</details>

### Question 6 — Hard
**Why can `BRPOPLPUSH` lose or duplicate?**
- A) It cannot
- B) A crash between pop and ack needs the processing-list pattern to recover
- C) Speed
- D) Size

<details><summary>Reveal Answer</summary>**B.** Reliable-queue pattern.</details>

### Question 7 — Hard
**Why must jobs be idempotent?**
- A) Style
- B) Recovery redelivers; a twice-run job must be safe
- C) Speed
- D) Size

<details><summary>Reveal Answer</summary>**B.** At-least-once reality.</details>

### Question 8 — Hard
**Session sliding renewal vs fixed TTL?**
- A) Same
- B) Sliding extends on activity (active users stay logged in); fixed logs out on schedule
- C) Fixed is safer always
- D) Sliding is unsafe always

<details><summary>Reveal Answer</summary>**B.** Activity-based expiry.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You build sessions and queues well. |
| 5-6 | Review leases and priority/delay patterns. |
| < 5 | Re-read the lecture. |
