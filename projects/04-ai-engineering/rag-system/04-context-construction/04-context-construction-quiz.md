# RAG System 04: Context Construction — Quiz

> **Topic Overview**: Assembling the context, ordering, budget, grounding,
> and thin-context detection.

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

**What is the context?**

- A) The model's training data
- B) The material the model reads to answer
- C) The query
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The context is assembled from reranked chunks and is the model's only allowed source.

</details>

---

### Question 2 — Easy

**What decides the answer's quality more than the model?**

- A) The API
- B) The context
- C) The database
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A good model on a bad context answers badly; the context dominates.

</details>

---

### Question 3 — Easy

**What text belongs in the context?**

- A) The normalized form
- B) The original verbatim text
- C) Both
- D) Neither

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The context carries the original quote for display and citation.

</details>

---

### Question 4 — Medium

**How are chunks ordered in the context?**

- A) Arbitrarily
- B) By rerank score, most relevant first
- C) By page number
- D) Alphabetically

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The context is a ranked window; the model reads the best material first.

</details>

---

### Question 5 — Medium

**What happens when the context exceeds the token budget?**

- A) Truncation drops the answer
- B) Nothing
- C) It is faster
- D) It is cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Over-budget contexts get truncated, potentially dropping the material the answer needs.

</details>

---

### Question 6 — Medium

**What does grounding mean?**

- A) Using a database
- B) Answering only from the context, never from memory
- C) Caching
- D) Filtering

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The roadmap exit test: summarize retrieved text, not recall from memory.

</details>

---

### Question 7 — Medium

**What is an evidence id?**

- A) A cache key
- B) The chunk identifier the answer cites
- C) A model id
- D) A tenant id

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Every claim traces to an evidence id in the context.

</details>

---

### Question 8 — Hard

**What signals a thin context?**

- A) Many chunks
- B) No chunk touching the question's key terms
- C) High scores
- D) A large budget

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Thin context means the material to answer is absent.

</details>

---

### Question 9 — Hard

**The correct behavior on thin context is:**

- A) Guess
- B) Abstain
- C) Retry
- D) Cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Abstention is correct when the evidence is absent.

</details>

---

### Question 10 — Hard**

**When over budget, drop:**

- A) The highest-ranked chunks
- B) The lowest-ranked chunks
- C) The middle
- D) Nothing

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Drop the lowest-ranked chunks, never the highest — the context stays a ranked window.

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
| 9-10 | Expert | Ready for abstention and citations |
| 7-8 | Proficient | Review the budget |
| 5-6 | Developing | Re-study grounding |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [03 - Reranking](03-reranking-quiz.md) | **Next**: [05 - Abstention and Citations](05-abstention-citations-quiz.md)