# Redis 03: Rate Limiting — Quiz

> **Topic Overview**: The sliding window, the counter, and the rejection.

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

**The sliding window counts:**

- A) All requests ever
- B) Requests in the last N seconds
- C) Only today's requests
- D) Only failed requests

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The window slides with time.

</details>

---

### Question 2 — Easy

**The counter is stored in:**

- A) A string
- B) A sorted set
- C) A list
- D) A hash

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Timestamps in a sorted set.

</details>

---

### Question 3 — Easy

**An over-limit request is:**

- A) Allowed
- B) Rejected
- C) Cached
- D) Retried

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Rejected with a 429 and a retry hint.

</details>

---

### Question 4 — Medium

**The count operations are:**

- A) Race-prone
- B) Atomic
- C) Cached
- D) Optional

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Executed in a pipeline, race-free.

</details>

---

### Question 5 — Medium

**Limits are set:**

- A) Globally
- B) Per endpoint
- C) Per user
- D) Never

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Auth is strict; general API is loose.

</details>

---

### Question 6 — Medium

**The counter's TTL:**

- A) Clears idle counters
- B) Speeds counting
- C) Caches counts
- D) Deletes limits

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Without it, counters accumulate forever.

</details>

---

### Question 7 — Medium

**The rejection includes:**

- A) The cache
- B) A retry-after hint
- C) The DB
- D) The key

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The client knows when to retry.

</details>

---

### Question 8 — Hard

**Expired timestamps are:**

- A) Kept
- B) Removed before counting
- C) Cached
- D) Counted

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The window only counts the recent rate.

</details>

---

### Question 9 — Hard

**The limit is part of:**

- A) The cache
- B) The key
- C) The DB
- D) The window

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: rate:{ip}:{endpoint}.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for the counter is:**

- A) It is optional
- B) It is atomic
- C) It is cached
- D) It is slow

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Race-free counting.

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
| 9-10 | Expert | Ready for Pub/Sub |
| 7-8 | Proficient | Review the window |
| 5-6 | Developing | Re-study the counter |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [02 - Key Patterns](02-key-patterns-ttl-quiz.md) | **Next**: [04 - Pub/Sub and Streams](04-pubsub-streams-quiz.md)