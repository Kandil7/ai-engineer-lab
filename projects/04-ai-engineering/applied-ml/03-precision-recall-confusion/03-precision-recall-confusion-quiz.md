# Applied ML 03: Precision/Recall and Confusion Matrix — Quiz

> **Topic Overview**: The confusion matrix, precision, recall, F1, and the
> imbalance trap.

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

**What does the confusion matrix show?**

- A) Model weights
- B) Predicted vs actual outcomes (TP/FP/FN/TN)
- C) Training loss
- D) Feature importance

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The matrix tabulates predictions against actuals in four cells.

</details>

---

### Question 2 — Easy

**What is a false positive?**

- A) Predicted no, actually yes
- B) Predicted yes, actually no
- C) Predicted yes, actually yes
- D) Predicted no, actually no

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A false positive is a false alarm — the model said yes when the answer was no.

</details>

---

### Question 3 — Easy

**What does precision answer?**

- A) Did we catch the yeses?
- B) When we say yes, are we right?
- C) How fast is the model?
- D) How big is the data?

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Precision = TP/(TP+FP): of the yes-predictions, how many were correct.

</details>

---

### Question 4 — Medium

**What does recall answer?**

- A) When we say yes, are we right?
- B) Of the real yeses, how many did we catch?
- C) How accurate is the model?
- D) How many features?

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Recall = TP/(TP+FN): the miss rate inverted.

</details>

---

### Question 5 — Medium

**Why does accuracy lie on imbalanced data?**

- A) It is slow
- B) Predicting the majority class scores high accuracy and zero minority recall
- C) It is biased
- D) It is large

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: On 99% noes, always predicting no scores 99% accuracy and catches nothing.

</details>

---

### Question 6 — Medium

**Which metric matters most for retrieval?**

- A) Precision
- B) Recall
- C) Accuracy
- D) Speed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Missing a relevant passage is worse than a false alarm, so recall leads.

</details>

---

### Question 7 — Medium

**Which metric matters most for spam filtering?**

- A) Recall
- B) Precision
- C) Accuracy
- D) Latency

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A false positive deletes a real email — precision protects against that.

</details>

---

### Question 8 — Hard

**What does F1 penalize?**

- A) Slow training
- B) Imbalance between precision and recall
- C) Large models
- D) Small data

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The harmonic mean drops sharply when either precision or recall is low.

</details>

---

### Question 9 — Hard

**A column with high FP means:**

- A) The model misses that class
- B) The model over-predicts that class
- C) The class is rare
- D) The data is clean

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Many false positives for a class means the model says yes too often for it.

</details>

---

### Question 10 — Hard**

**The roadmap exit test "interpret the confusion matrix" requires:**

- A) Reporting accuracy
- B) Reading which classes get confused with which
- C) Plotting loss
- D) Counting features

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The matrix reveals failure patterns — which classes are confused — driving error analysis.

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
| 9-10 | Expert | Ready for error analysis |
| 7-8 | Proficient | Review the tradeoff |
| 5-6 | Developing | Re-study the matrix |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [02 - Train/Val/Test](02-train-val-test-leakage-quiz.md) | **Next**: [04 - Rules vs Models and Error Analysis](04-rules-vs-models-error-analysis-quiz.md)