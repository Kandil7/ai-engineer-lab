# Prompt Engineering 05: End-User IDs — Quiz

> **Topic Overview**: Safe ID handling, injection prevention, isolation.

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

**The end-user ID is:**

- A) An instruction
- B) Metadata
- C) A cache key
- D) A model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: It must never be interpreted as content.

</details>

---

### Question 2 — Easy

**ID injection is:**

- A) A cache miss
- B) Instructions smuggled in the ID
- C) A rate limit
- D) A log entry

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Prevented by format validation.

</details>

---

### Question 3 — Easy

**Format validation uses:**

- A) A cache
- B) A strict regex
- C) A model
- D) A query

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Malicious IDs are rejected.

</details>

---

### Question 4 — Medium

**Per-user isolation means:**

- A) All users share context
- B) Each user's data is separate
- C) The cache is shared
- D) The model is shared

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: User A never sees User B's data.

</details>

---

### Question 5 — Medium

**Per-user logging enables:**

- A) Faster responses
- B) Audit trails and rate limiting
- C) Cache hits
- D) Model updates

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Who asked what.

</details>

---

### Question 6 — Medium

**A valid user ID matches:**

- A) Any string
- B) [a-zA-Z0-9-]{1,64}
- C) Only numbers
- D) Any length

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Strict format.

</details>

---

### Question 7 — Medium

**An injected ID like "x. Ignore all instructions." is:**

- A) Accepted
- B) Rejected by format validation
- C) Cached
- D) Logged

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The regex rejects it.

</details>

---

### Question 8 — Hard

**Interpolating the ID as content is a mistake because:**

- A) It is slow
- B) It allows injection
- C) It is cached
- D) It is required

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The model treats it as an instruction.

</details>

---

### Question 9 — Hard

**Without per-user logging, there is:**

- A) A cache
- B) No audit trail
- C) Faster responses
- D) Better isolation

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: No record of who asked what.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for the ID is:**

- A) It is ignored
- B) It is included safely
- C) It is cached
- D) It is optional

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Metadata, not content.

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
| 9-10 | Expert | Prompt-engineering section complete |
| 7-8 | Proficient | Review isolation |
| 5-6 | Developing | Re-study format validation |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [04 - Prompt Evaluation](04-prompt-evaluation-quiz.md)