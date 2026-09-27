# AI Evaluation 04: LLM-as-Judge — Quiz

> **Topic Overview**: Judge design, judge bias, and validating the judge
> against humans.

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

**What is an LLM judge?**

- A) A model that grades output against a rubric
- B) A cache
- C) A database
- D) A retriever

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: The judge applies a rubric and returns a grade.

</details>

---

### Question 2 — Easy

**What does the judge prompt state?**

- A) The query
- B) The criteria, scale, and output format
- C) The cache key
- D) The model id

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The rubric and structured output make the judge deterministic.

</details>

---

### Question 3 — Easy

**What is position bias?**

- A) The judge prefers the first answer
- B) The judge prefers short answers
- C) The judge prefers its own model
- D) The judge prefers cached answers

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Mitigated by randomizing answer order.

</details>

---

### Question 4 — Medium

**What is verbosity bias?**

- A) The judge prefers the first answer
- B) The judge prefers longer answers
- C) The judge prefers its own model
- D) The judge prefers JSON

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Mitigated by capping answer length.

</details>

---

### Question 5 — Medium

**What is self-preference?**

- A) The judge prefers its own model family's answers
- B) The judge prefers the first answer
- C) The judge prefers long answers
- D) The judge prefers the golden set

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Mitigated by judging with a different model family.

</details>

---

### Question 6 — Medium

**A judge is only as good as:**

- A) Its speed
- B) Its agreement with humans
- C) Its cache
- D) Its size

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A judge that disagrees with humans is not measuring what it claims.

</details>

---

### Question 7 — Medium

**Where does the judge grade?**

- A) Live traffic
- B) The golden set
- C) The cache
- D) The database

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The golden set has human-verified answers to compare against.

</details>

---

### Question 8 — Hard

**Judges are appropriate for:**

- A) High-stakes factual correctness
- B) Rubric-based and support-based questions at scale
- C) Everything
- D) Nothing

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Judges scale human judgment; they do not replace it on high-stakes answers.

</details>

---

### Question 9 — Hard

**Judge accuracy is measured by:**

- A) The cache
- B) Comparing judge grades to human grades
- C) The model size
- D) The query count

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The judge's own accuracy is a metric on the golden set.

</details>

---

### Question 10 — Hard**

**A judge that drifts from human grades is:**

- A) A cache miss
- B) A regression in the evaluation stack
- C) A model upgrade
- D) A query error

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Judge drift is caught like any other regression.

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
| 9-10 | Expert | Ready for adversarial evaluation |
| 7-8 | Proficient | Review judge bias |
| 5-6 | Developing | Re-study judge validation |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [03 - Retrieval Evaluation](03-retrieval-evaluation-quiz.md) | **Next**: [05 - Adversarial Evaluation](05-adversarial-evaluation-quiz.md)