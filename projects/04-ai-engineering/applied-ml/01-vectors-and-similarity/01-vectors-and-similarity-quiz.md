# Applied ML 01: Vectors and Similarity — Quiz

> **Topic Overview**: Dot product, cosine similarity, Euclidean distance,
> and the unit-vector identity.

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

**What is a vector in ML?**

- A) A single number
- B) An ordered list of numbers representing data
- C) A database row
- D) A function

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Documents, embeddings, and queries are all represented as ordered lists of numbers.

</details>

---

### Question 2 — Easy

**What does cosine similarity measure?**

- A) Magnitude difference
- B) The angle between vectors, ignoring magnitude
- C) Straight-line distance
- D) Term frequency

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Cosine measures direction, not magnitude — the default for text and embeddings.

</details>

---

### Question 3 — Easy

**When does dot product equal cosine similarity?**

- A) Always
- B) When both vectors are unit-normalized
- C) Never
- D) When vectors are large

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: On unit vectors, the norm denominator is 1, so cosine reduces to dot product.

</details>

---

### Question 4 — Medium

**Which metric is magnitude-sensitive?**

- A) Cosine
- B) Euclidean distance
- C) Both
- D) Neither

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Euclidean distance depends on magnitude; cosine ignores it.

</details>

---

### Question 5 — Medium

**Why do vector stores normalize on write?**

- A) To save space
- B) So queries pay one cheap dot product instead of two norms plus a division
- C) To speed up training
- D) To compress vectors

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Normalized vectors make dot product a valid cosine stand-in — cheaper per query.

</details>

---

### Question 6 — Medium

**A long document ranks high by dot product but not by cosine. Why?**

- A) Cosine is broken
- B) Dot product rewards magnitude; cosine rewards direction
- C) The document is too long
- D) Normalization failed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Dot product mixes magnitude into the score; cosine isolates direction.

</details>

---

### Question 7 — Medium

**What is the unit-vector identity?**

- A) All vectors are unit length
- B) cos(a,b) = a·b when both are normalized
- C) Dot equals Euclidean
- D) Cosine is always 1

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: With unit vectors the norm denominator is 1, so cosine equals the dot product.

</details>

---

### Question 8 — Hard

**Which metric should you choose when magnitude is signal?**

- A) Cosine
- B) Dot product or Euclidean
- C) Neither
- D) Always cosine

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: When magnitude carries meaning, dot or Euclidean preserves it; cosine discards it.

</details>

---

### Question 9 — Hard

**What happens if you normalize some vectors but not others?**

- A) Nothing
- B) Rankings become inconsistent — mixed magnitude semantics
- C) It is faster
- D) Cosine breaks

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Partial normalization mixes two metric semantics, corrupting rankings.

</details>

---

### Question 10 — Hard

**The metric choice changes rankings. What must you do?**

- A) Use cosine always
- B) Decide deliberately and record the decision
- C) Use Euclidean always
- D) Avoid metrics

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Metric choice is a design decision with ranking consequences — decide and document it.

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
| 9-10 | Expert | Ready for train/val/test |
| 7-8 | Proficient | Review the identity |
| 5-6 | Developing | Re-study the metrics |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [02 - Train/Validation/Test and Leakage](02-train-val-test-leakage-quiz.md)