# RAG System 08: Context Security — Quiz

> **Topic Overview**: Context injection, tenant isolation, provenance.

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

**The context is:**

- A) Safe
- B) An attack surface
- C) A cache
- D) A database

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Injected instructions, poisoned passages, and leakage arrive through it.

</details>

---

### Question 2 — Easy

**Context injection arrives:**

- A) Only through the query
- B) Through a retrieved passage
- C) Through the cache
- D) Through the database

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A passage can carry an instruction.

</details>

---

### Question 3 — Easy

**A poisoned passage is:**

- A) A clean source
- B) A fabricated or corrupted source
- C) A cached source
- D) A vetted source

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The defense is provenance.

</details>

---

### Question 4 — Medium

**Cross-tenant leakage is caused by:**

- A) A stale cache
- B) A missing tenant filter
- C) A slow query
- D) A large context

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Another tenant's data becomes visible.

</details>

---

### Question 5 — Medium

**Provenance validation checks:**

- A) Only the source
- B) Source, version, and content hash
- C) Only the version
- D) Only the hash

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: All three before admission.

</details>

---

### Question 6 — Medium

**The tenant filter is applied:**

- A) Occasionally
- B) On every query
- C) Only on writes
- D) Only on reads

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The correctness boundary.

</details>

---

### Question 7 — Medium

**Context security is tested:**

- A) Never
- B) In CI like other behaviors
- C) Only manually
- D) Only in production

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The adversarial set includes context-injection cases.

</details>

---

### Question 8 — Hard

**A passage failing provenance validation is:**

- A) Admitted
- B) Dropped
- C) Cached
- D) Logged

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Only vetted, current, un-tampered passages enter.

</details>

---

### Question 9 — Hard

**The model does not filter bad context because:**

- A) It is slow
- B) It is trained to follow the context
- C) It is cached
- D) It is small

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The defense is upstream of the model.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for context security is:**

- A) It is ignored
- B) The context resists injection and leakage
- C) It is cached
- D) It is optional

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tested and gated.

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
| 9-10 | Expert | Ready for long context |
| 7-8 | Proficient | Review provenance |
| 5-6 | Developing | Re-study injection |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [07 - Context Failure Modes](07-context-failure-modes-quiz.md) | **Next**: [09 - Long Context Processing](09-long-context-processing-quiz.md)