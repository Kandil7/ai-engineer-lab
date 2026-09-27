# Fine-Tuning 06: RAG vs Fine-Tuning — Quiz

> **Topic Overview**: The knowledge/behavior split, the tradeoffs, and the
> hybrid.

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

**What is RAG good at?**

- A) Behavior
- B) Knowledge at query time
- C) Format
- D) Style

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: RAG supplies facts at query time.

</details>

---

### Question 2 — Easy

**What is fine-tuning good at?**

- A) Knowledge
- B) Behavior at training time
- C) Retrieval
- D) Caching

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Fine-tuning shapes format and style.

</details>

---

### Question 3 — Easy

**RAG is the tool for:**

- A) Facts
- B) Format
- C) Style
- D) Tone

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Knowledge that changes or must be cited.

</details>

---

### Question 4 — Medium

**Fine-tuning is the tool for:**

- A) Facts
- B) Behavior
- C) Retrieval
- D) Caching

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Stable formats and instruction patterns.

</details>

---

### Question 5 — Medium

**RAG costs at:**

- A) Training time
- B) Query time
- C) Release time
- D) Cache time

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Retrieval latency, embedding cost, context budget.

</details>

---

### Question 6 — Medium

**Fine-tuning costs at:**

- A) Query time
- B) Training time
- C) Cache time
- D) Release time

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Data curation, GPU hours, overfitting risk.

</details>

---

### Question 7 — Medium

**RAG is transparent because:**

- A) It is fast
- B) Answers carry citations
- C) It is cached
- D) It is small

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Every answer traces to its source.

</details>

---

### Question 8 — Hard

**The hybrid is:**

- A) RAG for behavior, fine-tuning for facts
- B) RAG for facts, fine-tuning for behavior
- C) Both for facts
- D) Neither

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The standard production shape.

</details>

---

### Question 9 — Hard

**The RAG vs fine-tuning decision is recorded as:**

- A) A cache
- B) An ADR
- C) A model
- D) A quiz

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The ADR is evidence the choice was deliberate.

</details>

---

### Question 10 — Hard**

**Fine-tuning for a fact problem that retrieval solves is:**

- A) Correct
- B) A mistake
- C) Cached
- D) Required

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The tools solve different problems.

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
| 9-10 | Expert | Stage 11 fine-tuning complete |
| 7-8 | Proficient | Review the tradeoffs |
| 5-6 | Developing | Re-study the split |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [05 - Model Registry](05-model-registry-quiz.md)