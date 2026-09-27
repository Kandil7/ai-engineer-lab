# Qdrant 02: Vector Search — Quiz

> **Topic Overview**: The query embedding, the score, and the threshold.

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

**The query is embedded with:**

- A) Any model
- B) The same model as the collection
- C) A smaller model
- D) A larger model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A mismatch produces meaningless similarity.

</details>

---

### Question 2 — Easy

**Search returns:**

- A) All points
- B) The top-k points with scores
- C) Only the payload
- D) Only the ids

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Each result carries its similarity score.

</details>

---

### Question 3 — Easy

**The score measures:**

- A) The payload size
- B) Similarity between query and point
- C) The point id
- D) The collection size

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Higher is more similar for cosine.

</details>

---

### Question 4 — Medium

**The limit:**

- A) Sets the vector size
- B) Caps how many points are returned
- C) Changes the metric
- D) Deletes points

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The limit controls the context budget.

</details>

---

### Question 5 — Medium

**The score threshold:**

- A) Caps the results
- B) Drops points below a similarity floor
- C) Changes the metric
- D) Deletes points

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Weak matches stay out of the context.

</details>

---

### Question 6 — Medium

**An embedding mismatch:**

- A) Errors loudly
- B) Fails silently
- C) Is cached
- D) Is fixed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Search returns garbage without error.

</details>

---

### Question 7 — Medium

**A low score means:**

- A) A wrong answer
- B) Weak similarity
- C) A cache miss
- D) A broken collection

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The score is the raw material for the threshold.

</details>

---

### Question 8 — Hard

**The limit and threshold together control:**

- A) The vector size
- B) The context budget
- C) The collection name
- D) The point id

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: How much material reaches the answer.

</details>

---

### Question 9 — Hard

**The roadmap's exit test for the query embedding is:**

- A) Any model works
- B) The same model is used
- C) It is optional
- D) It is cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The query embedding matches the collection.

</details>

---

### Question 10 — Hard**

**Without a score threshold:**

- A) Search is faster
- B) Weak matches flood the context
- C) The metric changes
- D) Points are deleted

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The threshold keeps weak matches out.

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
| 9-10 | Expert | Ready for hybrid search |
| 7-8 | Proficient | Review the threshold |
| 5-6 | Developing | Re-study the score |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [01 - Collections](01-collections-points-quiz.md) | **Next**: [03 - Hybrid Search](03-hybrid-search-quiz.md)