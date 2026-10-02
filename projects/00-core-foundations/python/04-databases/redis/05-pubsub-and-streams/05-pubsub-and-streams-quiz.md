# Redis 05: Pub/Sub and Streams — Quiz

> **Topic Overview**: Fan-out vs durable logs, consumer groups, and backpressure.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is Pub/Sub?**
- A) A queue
- B) Live fan-out to current subscribers, nothing stored
- C) A log
- D) A stream

<details><summary>Reveal Answer</summary>**B.** Ephemeral broadcast.</details>

### Question 2 — Easy
**What happens to a message with no subscribers?**
- A) It queues
- B) It is dropped
- C) It persists
- D) It retries

<details><summary>Reveal Answer</summary>**B.** No storage.</details>

### Question 3 — Medium
**What do Streams add?**
- A) Speed
- B) A durable, replayable log with consumer groups
- C) Fan-out only
- D) TTL

<details><summary>Reveal Answer</summary>**B.** Persistent log.</details>

### Question 4 — Medium
**What does a consumer group guarantee?**
- A) Every worker gets every message
- B) One delivery per message across the group's workers
- C) Ordering globally
- D) Exactly-once

<details><summary>Reveal Answer</summary>**B.** Partitioned consumption.</details>

### Question 5 — Medium
**What does at-least-once mean here?**
- A) No duplicates
- B) A message can redeliver after a worker crash, so consumers must be idempotent
- C) No loss ever
- D) Ordered

<details><summary>Reveal Answer</summary>**B.** Duplicates possible.</details>

### Question 6 — Hard
**What happens when consumers are slower than producers?**
- A) Nothing
- B) The log grows unbounded (or drops, by policy) — backpressure must exist
- C) Producers slow automatically
- D) Messages compress

<details><summary>Reveal Answer</summary>**B.** Lag is the signal.</details>

### Question 7 — Hard
**When is Pub/Sub correct over Streams?**
- A) Always
- B) For live presence/chat ticks where only current listeners matter
- C) Never
- D) For job queues

<details><summary>Reveal Answer</summary>**B.** Ephemeral fan-out.</details>

### Question 8 — Hard
**What must a stream consumer track?**
- A) Nothing
- B) Its last-delivered id (and pending list) to resume without loss or full replay
- C) The group name only
- D) The TTL

<details><summary>Reveal Answer</summary>**B.** Offset management.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You choose messaging primitives well. |
| 5-6 | Review groups and delivery guarantees. |
| < 5 | Re-read the lecture. |
