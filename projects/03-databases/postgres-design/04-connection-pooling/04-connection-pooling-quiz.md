# PostgreSQL 04: Connection Pooling — Quiz

> **Topic Overview**: The pool, borrow/return, and leaks.

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

**Why pool connections?**

- A) They are free
- B) Opening one is expensive
- C) They are cached
- D) They are fast

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The pool reuses connections instead of reopening them.

</details>

---

### Question 2 — Easy

**A connection is:**

- A) Borrowed, used, and returned
- B) Opened per request
- C) Never returned
- D) Cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Return makes it available for the next request.

</details>

---

### Question 3 — Easy

**A leak is:**

- A) A returned connection
- B) A connection never returned
- C) A cached connection
- D) A closed connection

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Leaks exhaust the pool.

</details>

---

### Question 4 — Medium

**The max connections setting:**

- A) Speeds queries
- B) Caps the database load
- C) Caches data
- D) Deletes data

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The upper bound of the pool.

</details>

---

### Question 5 — Medium

**The min connections setting:**

- A) Caps load
- B) Keeps connections ready
- C) Caches data
- D) Deletes data

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The always-ready floor.

</details>

---

### Question 6 — Medium

**A timeout:**

- A) Hangs forever
- B) Fails fast
- C) Caches
- D) Deletes

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Timeouts prevent runaway waits.

</details>

---

### Question 7 — Medium

**A pool that runs dry causes:**

- A) Faster queries
- B) Requests to hang
- C) Cached data
- D) Deleted data

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: No connections are available.

</details>

---

### Question 8 — Hard

**The fix for leaks is:**

- A) A bigger pool
- B) Discipline: always return, even on error
- C) No pool
- D) Caching

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Context managers or try/finally guarantee the return.

</details>

---

### Question 9 — Hard

**Pool settings are:**

- A) Guessed
- B) Tuned to the workload
- C) Cached
- D) Fixed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tuned, not guessed.

</details>

---

### Question 10 — Hard**

**The roadmap's rule for connections is:**

- A) Open per request
- B) Use the pool, return the connections
- C) Never pool
- D) Cache them

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The pool plus the discipline.

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
| 9-10 | Expert | PostgreSQL section complete |
| 7-8 | Proficient | Review leaks |
| 5-6 | Developing | Re-study the pool |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [03 - Migrations](03-migrations-quiz.md)