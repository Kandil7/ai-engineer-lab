# Data Engineering 13: Feature Pipelines — Quiz

> **Topic Overview**: Windows and real-time aggregation, caching strategies,
> invalidation rules, feature versioning and lineage, freshness vs latency.

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

**Which window is fixed and non-overlapping?**

- A) Sliding
- B) Session
- C) Tumbling
- D) Hopping

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: Tumbling windows are fixed and non-overlapping; each event belongs to exactly one.

</details>

---

### Question 2 — Easy

**What is the cache-aside pattern?**

- A) Cache everything eagerly
- B) Check cache, compute on miss, store, invalidate on write
- C) Write-through only
- D) Never cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Cache-aside reads the cache first, computes on a miss, and invalidates on writes.

</details>

---

### Question 3 — Easy

**What does LRU stand for?**

- A) Least Recently Used
- B) Last Retrieved Unit
- C) Linear Read Utility
- D) Low Resource Usage

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: LRU evicts the least-recently-used entries to bound the cache size.

</details>

---

### Question 4 — Medium

**Why is window choice a correctness decision?**

- A) Different windows answer different questions
- B) Windows affect disk space
- C) Windows are hard to code
- D) Windows slow the pipeline

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Tumbling answers "per minute"; sliding answers "last N over M"; picking the wrong one gives a right number for the wrong question.

</details>

---

### Question 5 — Medium

**What happens to a counter that is not exactly-once?**

- A) It becomes faster
- B) A retried event inflates the count
- C) It drops all events
- D) It sorts events

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Without exactly-once state, a crash-and-retry double-counts the retried events.

</details>

---

### Question 6 — Medium

**What is the thundering-herd problem?**

- A) Too much disk usage
- B) A hot key expires and many requests recompute at once
- C) A slow network
- D) A full cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: When a hot key expires, all concurrent misses trigger simultaneous recomputation, spiking the backend.

</details>

---

### Question 7 — Medium

**Why is a TTL the wrong staleness bound for a citation corpus?**

- A) TTLs are too short
- B) A citation cache must never serve a superseded source; versioned keys bound staleness by correctness
- C) TTLs are too long
- D) TTLs cost more

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A versioned key guarantees the cache is never older than its source version, not merely younger than a fixed age.

</details>

---

### Question 8 — Hard

**How do feature versioning and the cache key form a self-healing loop?**

- A) They do not interact
- B) A version bump is in the key, so it invalidates the cache, forcing recomputation of the new value
- C) The key encrypts the version
- D) The version shortens the TTL

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Because the version is part of the key, a redefinition changes the key and old entries are simply never read.

</details>

---

### Question 9 — Hard

**Which cache should serve a shared, multi-instance hot path?**

- A) Local dict
- B) Redis
- C) In-process LRU only
- D) A file on disk

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Redis provides one shared value across instances; a local cache is per-instance and inconsistent.

</details>

---

### Question 10 — Hard

**What is the pragmatic floor for DevMate's scale?**

- A) Full streaming with exactly-once windows everywhere
- B) An LRU keyed by model version plus a tumbling batch aggregation for stats
- C) No caching at all
- D) Only TTLs

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Versioned-key caching and batch aggregation capture most correctness at none of the streaming ops cost, matching the batch-first default.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | C | Easy |
| 2 | B | Easy |
| 3 | A | Easy |
| 4 | A | Medium |
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
| 9-10 | Expert | Ready for versioning and lineage |
| 7-8 | Proficient | Review invalidation rules |
| 5-6 | Developing | Re-study the window types |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [14 - Data Versioning and Lineage](../14-data-versioning-lineage/14-data-versioning-lineage-quiz.md)
