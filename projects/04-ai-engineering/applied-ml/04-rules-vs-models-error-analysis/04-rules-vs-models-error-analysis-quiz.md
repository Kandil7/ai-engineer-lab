# Applied ML 04: Rules vs Models and Error Analysis — Quiz

> **Topic Overview**: The rules-vs-model decision, the rule baseline, and
> the error analysis loop.

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

**When does a rule beat a model?**

- A) Always
- B) On small, deterministic, explainable problems
- C) Never
- D) On large datasets

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Rules win when the pattern is simple and deterministic; models win on complex, fuzzy patterns.

</details>

---

### Question 2 — Easy

**What is a rule baseline?**

- A) A model
- B) A hand-written heuristic every model must beat
- C) A metric
- D) A dataset

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: If a model cannot beat a simple rule, the model is not earning its complexity.

</details>

---

### Question 3 — Easy

**What is the roadmap exit test for stage 6?**

- A) Train a big model
- B) Know when the rule is better than the model and interpret the confusion matrix
- C) Achieve 99% accuracy
- D) Use PyTorch

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The exit is judgment: when a rule suffices, and reading the confusion matrix.

</details>

---

### Question 4 — Medium

**What is the first step of error analysis?**

- A) Fix the model
- B) Collect the test failures
- C) Add features
- D) Retrain

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Collect failures, then cluster them, find the cause, fix, re-measure.

</details>

---

### Question 5 — Medium

**What is a failure cluster?**

- A) A group of failures sharing a pattern
- B) A crashed process
- C) A slow query
- D) A large model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Clustering failures by pattern is what turns them into a fixable cause.

</details>

---

### Question 6 — Medium

**A data failure means:**

- A) The model is too small
- B) The data is wrong (labels, values, duplicates)
- C) The features miss the signal
- D) The algorithm is wrong

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Wrong data — re-training fixes nothing; fixing the data does.

</details>

---

### Question 7 — Medium

**A feature failure means:**

- A) The data is wrong
- B) The features miss the signal
- C) The model is too small
- D) The threshold is wrong

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The representation is wrong; adding more of the same features fixes nothing.

</details>

---

### Question 8 — Hard

**A model failure means:**

- A) The data is wrong
- B) The model cannot fit the pattern
- C) The features are wrong
- D) The labels are wrong

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Insufficient capacity or the wrong algorithm — more data won't fix it.

</details>

---

### Question 9 — Hard

**The error analysis loop is:**

- A) A single step
- B) Failures → cluster → cause → fix → re-measure
- C) Train → deploy
- D) Collect → report

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Each pass reduces a specific failure cluster; without clustering, fixes are guesses.

</details>

---

### Question 10 — Hard**

**A model that cannot beat a simple rule should:**

- A) Be deployed anyway
- B) Be replaced by the rule
- C) Get more data
- D) Get more features

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The rule is the baseline; if the model loses, ship the rule — less cost, more explainability.

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
| 9-10 | Expert | Stage 6 complete — ready for IR |
| 7-8 | Proficient | Review the failure layers |
| 5-6 | Developing | Re-study the loop |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [03 - Precision/Recall](03-precision-recall-confusion-quiz.md)