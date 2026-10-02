# Redis 02: Data Structures — Quiz

> **Topic Overview**: Strings, hashes, lists, sets, and sorted sets.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**When is a hash better than many string keys?**
- A) Never
- B) For one object with many fields, fetched and expired together
- C) For queues
- D) For rankings

<details><summary>Reveal Answer</summary>**B.** Grouped fields.</details>

### Question 2 — Easy
**What are lists good for?**
- A) Rankings
- B) Queues and stacks with `LPUSH`/`RPOP`
- C) Membership
- D) Expiry

<details><summary>Reveal Answer</summary>**B.** Ordered ends.</details>

### Question 3 — Medium
**What do sets guarantee?**
- A) Order
- B) Unique membership with O(1) add/remove/test
- C) Scores
- D) TTL

<details><summary>Reveal Answer</summary>**B.** Dedup plus membership.</details>

### Question 4 — Medium
**What do sorted sets add over sets?**
- A) Nothing
- B) A score per member enabling rankings and ranges
- C) Expiry
- D) Hashes

<details><summary>Reveal Answer</summary>**B.** Ordered by score.</details>

### Question 5 — Medium
**How do you model a leaderboard?**
- A) A list
- B) A sorted set scored by points, read with `ZRANGE`/`ZREVRANGE`
- C) A hash
- D) Strings

<details><summary>Reveal Answer</summary>**B.** Score-ordered set.</details>

### Question 6 — Hard
**Why can one big hash beat many keys?**
- A) It cannot
- B) Fewer keys means less per-key overhead and one TTL for the object
- C) Speed of one command
- D) Replication

<details><summary>Reveal Answer</summary>**B.** Grouped lifecycle.</details>

### Question 7 — Hard
**What is the type-selection rule?**
- A) Always strings
- B) Match the access pattern: fields→hash, order→list, membership→set, rank→zset
- C) Always hashes
- D) Always zsets

<details><summary>Reveal Answer</summary>**B.** Pattern drives type.</details>

### Question 8 — Hard
**Why are huge values in any type a problem?**
- A) They are not
- B) Single-threaded commands on megabytes block everything
- C) They do not expire
- D) They do not replicate

<details><summary>Reveal Answer</summary>**B.** Big values block the loop.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You pick Redis types well. |
| 5-6 | Review hashes, sets, zsets. |
| < 5 | Re-read the lecture. |
