# AI Evaluation 02: Faithfulness and Citation Precision — Quiz

> **Topic Overview**: Claim-level faithfulness, citation validity vs
> support, and citation precision.

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

**What does faithfulness measure?**

- A) Retrieval quality
- B) Whether the answer is supported by the context
- C) Query speed
- D) Cache hits

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Faithfulness is the answer-side metric: is every claim backed by the context?

</details>

---

### Question 2 — Easy

**What does relevance measure?**

- A) Answer quality
- B) Whether the right passages were retrieved
- C) Model size
- D) Latency

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Relevance is the retrieval-side metric.

</details>

---

### Question 3 — Easy

**What is citation precision?**

- A) The fraction of citations that support their claim
- B) The number of citations
- C) The citation length
- D) The cache size

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Citation precision is supported citations over total citations.

</details>

---

### Question 4 — Medium

**A claim the context does not support is:**

- A) Acceptable if true
- B) A hallucination even if true in the world
- C) A cache hit
- D) A retrieval error

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Faithfulness requires support by the context, not truth in the world.

</details>

---

### Question 5 — Medium

**Citation validity means:**

- A) The passage backs the claim
- B) The cited id exists in the context
- C) The claim is true
- D) The answer is long

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Validity is the mechanical existence check; support is separate.

</details>

---

### Question 6 — Medium

**Citation support means:**

- A) The id exists
- B) The cited passage actually backs the claim
- C) The claim is short
- D) The query is cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Support needs a judge or a human; it is not mechanical.

</details>

---

### Question 7 — Medium

**Why check claims individually?**

- A) It is faster
- B) Whole-answer checks miss partial errors
- C) It is required
- D) It reduces citations

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A claim-level check catches one bad claim in an otherwise good answer.

</details>

---

### Question 8 — Hard

**A system retrieves perfectly but invents the answer. It is:**

- A) Relevant and faithful
- B) Relevant but unfaithful
- C) Unfaithful and irrelevant
- D) Faithful but irrelevant

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Retrieval quality and answer quality are independent.

</details>

---

### Question 9 — Hard

**A change improves recall but drops faithfulness. It is:**

- A) An improvement
- B) A regression
- C) A cache win
- D) Neutral

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The two metrics gate together; retrieval gains do not excuse answer losses.

</details>

---

### Question 10 — Hard**

**Which check runs mechanically in CI?**

- A) Citation support
- B) Citation validity
- C) Claim entailment
- D) Human grading

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Validity is pure validation; support needs a judge or human.

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
| 9-10 | Expert | Ready for retrieval evaluation |
| 7-8 | Proficient | Review validity vs support |
| 5-6 | Developing | Re-study faithfulness |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [01 - Gold Datasets](01-gold-datasets-annotation-quiz.md) | **Next**: [03 - Retrieval Evaluation](03-retrieval-evaluation-quiz.md)