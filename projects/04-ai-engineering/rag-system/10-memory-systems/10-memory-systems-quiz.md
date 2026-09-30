# RAG System 10: Memory Systems — Quiz

> **Topic Overview**: The three memory types, write/read paths, coherence.

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

**The three memory types are:**

- A) Cache, database, file
- B) Conversation, semantic, episodic
- C) Short, medium, long
- D) Read, write, delete

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Each serves a different purpose.

</details>

---

### Question 2 — Easy

**Conversation memory holds:**

- A) Facts
- B) The current session's turns
- C) Past episodes
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Recent context.

</details>

---

### Question 3 — Easy

**Semantic memory holds:**

- A) Turns
- B) Facts extracted from past interactions
- C) Episodes
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Stored separately.

</details>

---

### Question 4 — Medium

**Episodic memory holds:**

- A) Turns
- B) Facts
- C) Past interactions as retrievable events
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Similar past sessions.

</details>

---

### Question 5 — Medium

**The write path is:**

- A) Synchronous
- B) Asynchronous
- C) Cached
- D) Blocked

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The user's response is not blocked.

</details>

---

### Question 6 — Medium

**The read path assembles:**

- A) The cache
- B) The context from memory
- C) The query
- D) The model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Recent turns + facts + episodes.

</details>

---

### Question 7 — Medium

**Memory growth is bounded by:**

- A) The cache
- B) TTL, size cap, and retention window
- C) The model
- D) The query

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Without bounds, memory grows forever.

</details>

---

### Question 8 — Hard

**Memory coherence means:**

- A) The memory is fast
- B) The system does not contradict its own memory
- C) The memory is cached
- D) The memory is small

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tested across sessions.

</details>

---

### Question 9 — Hard

**Without a read path, memory is:**

- A) Useful
- B) Written but never read
- C) Cached
- D) Coherent

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The write is pointless without the read.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for memory is:**

- A) It is ignored
- B) The three types are distinguished
- C) It is cached
- D) It is optional

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Conversation, semantic, episodic.

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
| 9-10 | Expert | RAG-system section complete |
| 7-8 | Proficient | Review coherence |
| 5-6 | Developing | Re-study the three types |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [09 - Long Context](09-long-context-processing-quiz.md)