# Redis 01: Cache Strategies — Quiz

> **Topic Overview**: Cache-aside, write-through, write-behind, and TTL.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 10 |
| Correct Answers | 0 |
| Score | 0% |

---

## Questions

### Question 1 — Easy

**Cache-aside is:**

- A) Write to cache and DB together
- B) Load on demand, store on miss
- C) Write async
- D) Never cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The default for read-heavy data.

</details>

---

### Question 2 — Easy

**A cache hit means:**

- A) The value is loaded from the DB
- B) The value is in the cache
- C) The cache is empty
- D) The DB is down

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Returned without touching the database.

</details>

---

### Question 3 — Easy

**A cache miss means:**

- A) The value is in the cache
- B) Load from the DB and store
- C) The cache is full
- D) The DB is down

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The miss path populates the cache.

</details>

---

### Question 4 — Medium

**Write-through:**

- A) Writes to cache only
- B) Writes to cache and DB together
- C) Writes async
- D) Never writes

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Both are always in sync.

</details>

---

### Question 5 — Medium

**Write-behind risks:**

- A) Stale reads
- B) Data loss if the cache dies before the flush
- C) Slow writes
- D) Cache misses

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The flush is asynchronous.

</details>

---

### Question 6 — Medium

**Write-behind is right for:**

- A) Critical data
- B) Non-critical counters and metrics
- C) Sessions
- D) User profiles

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Loss-tolerant data.

</details>

---

### Question 7 — Medium

**TTL bounds:**

- A) The cache size
- B) Staleness
- C) The DB load
- D) The key count

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: How old a cached value can get.

</details>

---

### Question 8 — Hard

**A TTL too long:**

- A) Defeats the cache
- B) Serves stale data
- C) Speeds writes
- D) Caches more

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Staleness grows with the TTL.

</details>

---

### Question 9 — Hard

**A TTL too short:**

- A) Serves stale data
- B) Defeats the cache
- C) Speeds writes
- D) Caches more

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Entries expire before they are reused.

</details>

---

### Question 10 — Hard**

**The strategy choice is a:**

- A) Speed decision
- B) Consistency decision
- C) Cache decision
- D) Key decision

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The data's consistency needs decide the strategy.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Hard |
| 9 | B | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for key patterns |
| 7-8 | Proficient | Review write-behind |
| 5-6 | Developing | Re-study cache-aside |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [02 - Key Patterns and TTL](02-key-patterns-ttl-quiz.md)