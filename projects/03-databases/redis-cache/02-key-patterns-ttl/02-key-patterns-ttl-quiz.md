# Redis 02: Key Patterns and TTL — Quiz

> **Topic Overview**: Key patterns, namespaces, TTL, and eviction.

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

**A key is:**

- A) The cache's address
- B) The cache's size
- C) The cache's speed
- D) The cache's policy

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: A string identifying an entry.

</details>

---

### Question 2 — Easy

**The key pattern encodes:**

- A) The cache size
- B) The entry's identity
- C) The eviction policy
- D) The DB load

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: namespace:id.

</details>

---

### Question 3 — Easy

**A namespace:**

- A) Deletes keys
- B) Groups a data type
- C) Caches keys
- D) Evicts keys

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: user:, session:, rate:.

</details>

---

### Question 4 — Medium

**Namespaces prevent:**

- A) Eviction
- B) Collisions
- C) TTLs
- D) Caching

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: user:123 and session:123 never collide.

</details>

---

### Question 5 — Medium

**TTL is set:**

- A) Globally
- B) Per data type
- C) Per eviction
- D) Never

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A profile lives 30 min; a session lives 24 hours.

</details>

---

### Question 6 — Medium

**Eviction happens when:**

- A) The TTL expires
- B) Memory is full
- C) The key is deleted
- D) The DB is down

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The policy decides which entries go.

</details>

---

### Question 7 — Medium

**LRU evicts:**

- A) The least frequently used
- B) The least recently used
- C) The newest
- D) The largest

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Least recently used first.

</details>

---

### Question 8 — Hard

**A flat key space:**

- A) Prevents collisions
- B) Collides
- C) Speeds eviction
- D) Sets TTLs

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Two types can share the same key.

</details>

---

### Question 9 — Hard

**No eviction policy means:**

- A) Faster reads
- B) Writes fail when memory is full
- C) More caching
- D) Fewer keys

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The cache cannot make room.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for keys is:**

- A) They are random
- B) They follow a consistent pattern
- C) They are cached
- D) They are optional

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Consistent, namespaced patterns.

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
| 9-10 | Expert | Ready for rate limiting |
| 7-8 | Proficient | Review eviction |
| 5-6 | Developing | Re-study namespaces |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [01 - Cache Strategies](01-cache-strategies-quiz.md) | **Next**: [03 - Rate Limiting](03-rate-limiting-quiz.md)