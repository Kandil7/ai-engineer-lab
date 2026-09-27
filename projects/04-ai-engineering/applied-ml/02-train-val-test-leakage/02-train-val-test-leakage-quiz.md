# Applied ML 02: Train/Validation/Test and Leakage — Quiz

> **Topic Overview**: The three-way split, leakage patterns, and group
> splitting.

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

**What does the train set do?**

- A) Tunes hyperparameters
- B) Fits the model
- C) Measures final performance
- D) Validates

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The train set is where the model learns its parameters.

</details>

---

### Question 2 — Easy

**What does the validation set do?**

- A) Fits the model
- B) Tunes hyperparameters and selects candidates
- C) Measures final performance
- D) Leaks

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Validation is for tuning so the test set stays untouched.

</details>

---

### Question 3 — Easy

**How often should the test set be evaluated?**

- A) Every iteration
- B) Once, at the end
- C) Twice
- D) Never

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Test is the honest referee — measured once, any influence corrupts it.

</details>

---

### Question 4 — Medium

**What is target leakage?**

- A) Training on future data
- B) The label leaking into the features
- C) Same source in train and test
- D) A slow model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A feature computed from the answer lets the model cheat.

</details>

---

### Question 5 — Medium

**What is temporal leakage?**

- A) The label in features
- B) Training on data from after the test period
- C) Same source both sides
- D) A timestamp feature

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Time-series data must be split by time, not randomly.

</details>

---

### Question 6 — Medium

**What is group leakage?**

- A) The label in features
- B) Same source appearing in both train and test
- C) Future data in training
- D) A large group

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The model recognizes the source instead of generalizing.

</details>

---

### Question 7 — Medium

**For Athar, how should passages be split?**

- A) Randomly by passage
- B) By book_id
- C) By page
- D) By text length

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Passages share a book; splitting by book prevents group leakage.

</details>

---

### Question 8 — Hard

**What is the first symptom of leakage?**

- A) Slow training
- B) A suspiciously high score
- C) A large model
- D) A long test

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Scores too good to be true usually mean the model saw the answer.

</details>

---

### Question 9 — Hard

**Why must test never influence decisions?**

- A) It is slow
- B) Every look at test leaks it into the model
- C) It is small
- D) It is unlabeled

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tuning against test corrupts the honest measurement.

</details>

---

### Question 10 — Hard**

**The leakage diagnosis is:**

- A) A single test
- B) A checklist: label in features, future in training, source straddling
- C) A model comparison
- D) A metric

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Check target, temporal, and group leakage; the fix is usually a re-split.

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
| 9-10 | Expert | Ready for precision/recall |
| 7-8 | Proficient | Review leakage patterns |
| 5-6 | Developing | Re-study the split |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [01 - Vectors](01-vectors-and-similarity-quiz.md) | **Next**: [03 - Precision/Recall](03-precision-recall-confusion-quiz.md)