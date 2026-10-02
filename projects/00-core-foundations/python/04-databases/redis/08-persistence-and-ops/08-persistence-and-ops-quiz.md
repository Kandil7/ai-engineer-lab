# Redis 08: Persistence and Ops — Quiz

> **Topic Overview**: RDB vs AOF, eviction, `SCAN`, and clustering.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**RDB vs AOF?**
- A) Same
- B) RDB snapshots point-in-time; AOF logs every write for finer recovery
- C) AOF is faster to restart
- D) RDB logs writes

<details><summary>Reveal Answer</summary>**B.** Snapshot vs log.</details>

### Question 2 — Easy
**What does `maxmemory` trigger?**
- A) An error always
- B) The eviction policy, or write errors with `noeviction`
- C) A restart
- D) A backup

<details><summary>Reveal Answer</summary>**B.** Policy or refusal.</details>

### Question 3 — Medium
**Why do volatile policies protect TTL-less keys?**
- A) They do not
- B) Only keys with a TTL are eviction candidates, so persistent config survives
- C) Speed
- D) Size

<details><summary>Reveal Answer</summary>**B.** Sacred persistent keys.</details>

### Question 4 — Medium
**What does `INFO memory` tell you?**
- A) Hit rate
- B) Used, peak, fragmentation, and eviction pressure
- C) Keys
- D) Clients

<details><summary>Reveal Answer</summary>**B.** Memory posture.</details>

### Question 5 — Medium
**Why `SCAN` and never `KEYS`?**
- A) Style
- B) `SCAN` iterates in small steps without blocking the single thread
- C) `KEYS` is faster
- D) `SCAN` deletes

<details><summary>Reveal Answer</summary>**B.** Non-blocking iteration.</details>

### Question 6 — Hard
**What are hash slots?**
- A) Buckets in RAM
- B) The 16384 partitions keys hash into, assigned to cluster nodes
- C) Locks
- D) TTLs

<details><summary>Reveal Answer</summary>**B.** Sharding unit.</details>

### Question 7 — Hard
**What are hash tags for?**
- A) TTL
- B) `{tag}` forces related keys onto the same slot for multi-key operations
- C) Speed
- D) Size

<details><summary>Reveal Answer</summary>**B.** Co-located keys.</details>

### Question 8 — Hard
**Why is multi-key code cluster-unsafe by default?**
- A) It is not
- B) Keys may live on different nodes; only same-slot (tagged) multi-key ops work
- C) Speed
- D) Size

<details><summary>Reveal Answer</summary>**B.** Slot locality.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You operate Redis well. |
| 5-6 | Review persistence, eviction, slots. |
| < 5 | Re-read the lecture. |
