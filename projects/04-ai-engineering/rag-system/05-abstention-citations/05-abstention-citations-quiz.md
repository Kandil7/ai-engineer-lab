# RAG System 05: Abstention and Citations — Quiz

> **Topic Overview**: Abstention on thin context, citation-required answers,
> and rejecting fabricated citations.

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

**What is abstention?**

- A) Guessing
- B) Refusing to answer when evidence is absent
- C) Caching
- D) Filtering

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Abstention is a correctness feature — a confident wrong answer is worse than an honest refusal.

</details>

---

### Question 2 — Easy

**What does every claim in a RAG answer need?**

- A) A model id
- B) A citation to an evidence id
- C) A cache key
- D) A tenant id

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A claim without a citation is a hallucination by construction.

</details>

---

### Question 3 — Easy

**What is a fabricated citation?**

- A) A real evidence id
- B) A cited id not in the context
- C) A cache key
- D) A model id

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The model invented an id the context does not contain.

</details>

---

### Question 4 — Medium

**How is a fabricated citation rejected?**

- A) By the model
- B) By backend validation: cited ids must be in the context
- C) By the cache
- D) By the user

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The mechanical check is `all(c in context_ids for c in cited)`.

</details>

---

### Question 5 — Medium

**The roadmap exit test requires the model to:**

- A) Always answer
- B) Abstain when evidence is absent
- C) Cache answers
- D) Filter queries

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Abstention without evidence is the named exit criterion.

</details>

---

### Question 6 — Medium

**What does a citation resolve to?**

- A) A cache entry
- B) The original text and its provenance
- C) A model
- D) A tenant

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The citation links to the original text with book/page/version.

</details>

---

### Question 7 — Medium

**A claim without a citation is:**

- A) Acceptable
- B) A hallucination by construction
- C) Faster
- D) Cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Requiring citations makes hallucination structurally impossible.

</details>

---

### Question 8 — Hard

**The abstention rule belongs in:**

- A) The cache
- B) The prompt
- C) The database
- D) The UI

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The prompt states: answer only from the context, abstain if absent.

</details>

---

### Question 9 — Hard

**The roadmap exit test "does not accept a fabricated citation id" is enforced by:**

- A) The model
- B) Backend validation
- C) The user
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The backend mechanically validates cited ids against the context.

</details>

---

### Question 10 — Hard**

**Both abstention and citation tests belong in:**

- A) The cache
- B) CI
- C) The UI
- D) The database

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The two named failure modes are regression-tested in CI.

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
| 9-10 | Expert | Ready for caching |
| 7-8 | Proficient | Review citation validation |
| 5-6 | Developing | Re-study abstention |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [04 - Context](04-context-construction-quiz.md) | **Next**: [06 - Caching](06-caching-quiz.md)