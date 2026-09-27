# AI Evaluation 01: Gold Datasets and Annotation — Quiz

> **Topic Overview**: Building the golden set, annotation guidelines, and
> inter-annotator agreement.

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

**What is a gold dataset?**

- A) A sample of user traffic
- B) A fixed, curated set of queries with verified answers
- C) The training data
- D) A cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The golden set is a fixed yardstick, not training data and not a traffic sample.

</details>

---

### Question 2 — Easy

**What does a golden query carry?**

- A) Only the query
- B) The query, relevant passages, and a verified answer
- C) Only the answer
- D) Only the model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Each golden query has relevant passage ids and a verified answer.

</details>

---

### Question 3 — Easy

**What beats size in a golden set?**

- A) Randomness
- B) Coverage of the query space
- C) Speed
- D) Caching

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Fifty well-chosen queries beat five hundred random ones.

</details>

---

### Question 4 — Medium

**Why do annotation guidelines matter?**

- A) They are required
- B) They make labels reproducible across annotators
- C) They speed up labeling
- D) They reduce queries

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Without guidelines, the golden set measures the annotators, not the system.

</details>

---

### Question 5 — Medium

**What does Cohen's kappa correct for?**

- A) Speed
- B) Chance agreement
- C) Query count
- D) Model size

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Kappa subtracts the agreement expected by chance.

</details>

---

### Question 6 — Medium

**A kappa below 0.7 means:**

- A) The system is good
- B) The guidelines are ambiguous
- C) The queries are good
- D) The model is fast

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Low agreement means the labels are not trustworthy.

</details>

---

### Question 7 — Medium

**Which query type belongs in the golden set?**

- A) Only easy ones
- B) Unanswerable queries (abstention cases)
- C) Only verse questions
- D) Only hadith questions

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Coverage includes the hard cases and the abstention cases.

</details>

---

### Question 8 — Hard

**Why is the golden set not a sample of user traffic?**

- A) It is faster
- B) It must be a fixed yardstick, not a moving sample
- C) It is cheaper
- D) It is required

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A fixed set makes regressions visible; a traffic sample moves under the system.

</details>

---

### Question 9 — Hard

**The golden set runs in CI as:**

- A) A cache
- B) A regression gate
- C) A model
- D) A database

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A retrieval change that drops golden-set recall@5 is caught before it ships.

</details>

---

### Question 10 — Hard**

**Two annotators agree 96% on a 90%-majority label. Kappa will be:**

- A) 0.96
- B) Below 0.96, corrected for chance
- C) 1.0
- D) 0.0

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: High raw agreement on a skewed label hides chance agreement; kappa corrects it.

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
| 9-10 | Expert | Ready for faithfulness |
| 7-8 | Proficient | Review kappa |
| 5-6 | Developing | Re-study coverage |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [02 - Faithfulness and Citation Precision](02-faithfulness-citation-precision-quiz.md)