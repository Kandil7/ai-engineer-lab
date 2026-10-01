# Applied ML 05: Baseline Intent Classifier — Quiz

> **Topic Overview**: The non-LLM baseline exit artifact — a keyword rule, a Naive
> Bayes model, a leakage-aware group split, per-class metrics, and an error report.

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

**Why is a keyword rule a useful baseline for intent classification?**

- A) It is always more accurate than a model
- B) It is cheap, explainable, and the bar every model must beat
- C) It needs no data at all
- D) It generalizes to unseen phrasings

<details>
<summary>Reveal Answer</summary>

**B.** A baseline is the cheapest reasonable approach; a model must beat it to be worth
its complexity.

</details>

### Question 2 — Easy

**What does "split by source" mean here?**

- A) Randomly split rows
- B) Split so one `source` appears in both train and test
- C) Split so every `source` is entirely in train or entirely in test
- D) Sort by source and take the first half

<details>
<summary>Reveal Answer</summary>

**C.** The group key keeps a source on one side, preventing group leakage.

</details>

### Question 3 — Medium

**A split is leakage-free but the test set contains only `other` examples. What is the
problem?**

- A) Nothing; it is leakage-free
- B) The test set does not represent the label distribution, so recall for other classes is
  structurally zero
- C) The model will overfit
- D) The rule will fail

<details>
<summary>Reveal Answer</summary>

**B.** A leakage-free split can still be a bad split; the test set must represent the
labels.

</details>

### Question 4 — Medium

**What does Laplace smoothing prevent in Naive Bayes?**

- A) Slow training
- B) A token unseen in a class zeroing that class's probability
- C) Overfitting to the majority class
- D) Group leakage

<details>
<summary>Reveal Answer</summary>

**B.** Adding 1 to counts keeps unseen tokens from assigning probability zero.

</details>

### Question 5 — Medium

**Why assert that the model beats the majority baseline?**

- A) To prove the model is fast
- B) Because a model that does not beat always-predict-the-majority has learned nothing
- C) To size the model
- D) To avoid group leakage

<details>
<summary>Reveal Answer</summary>

**B.** The majority baseline is the floor; not beating it means the model added nothing.

</details>

### Question 6 — Medium

**What does macro-F1 add over accuracy?**

- A) Nothing
- B) It weights each class equally, so a rare class is not ignored
- C) It is faster to compute
- D) It measures latency

<details>
<summary>Reveal Answer</summary>

**B.** Macro-F1 averages per-class F1, so an ignored rare class lowers the score.

</details>

### Question 7 — Hard

**A model misclassifies every `other` question that begins with a question word as `how`.
What is the failure layer, and the fix?**

- A) Data; relabel
- B) Features/model boundary; the `other` class is under-represented or its features are
  weak — fix features or the label definition, not more epochs
- C) Model capacity; use a bigger model
- D) Split; re-split

<details>
<summary>Reveal Answer</summary>

**B.** Clustering the failures points at a specific class boundary, which is a
feature/data fix, not a capacity fix.

</details>

### Question 8 — Hard

**Why is Naive Bayes the right complexity for this comparison?**

- A) It is the most accurate
- B) It is small and fast; if it cannot beat the rule, a larger model probably will not
  either, and the rule is the better ship
- C) It needs no smoothing
- D) It handles group leakage

<details>
<summary>Reveal Answer</summary>

**B.** Complexity must be earned; the simple model is the honest first comparison.

</details>

### Question 9 — Hard

**What makes this script the "exit artifact" for the ML-foundations axis?**

- A) It uses PyTorch
- B) It is an Arabic intent classifier with a non-LLM baseline, a leakage-free split, and
  an error report
- C) It trains a large model
- D) It measures latency

<details>
<summary>Reveal Answer</summary>

**B.** Those three properties are exactly the axis's exit test.

</details>

### Question 10 — Hard

**The full report shows rule macro-F1 = 1.00 and model macro-F1 = 1.00. What is the
engineered decision?**

- A) Ship the model because it is learned
- B) Ship the rule, because it matches the model on this data at lower complexity and cost
- C) Train a bigger model
- D) Add more data and re-run

<details>
<summary>Reveal Answer</summary>

**B.** When the rule ties the model, the rule wins on cost, explainability, and
maintenance. This is the "know when the rule is better" exit test.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 9-10 | You can build and defend a baseline comparison. |
| 7-8 | Solid; review macro-F1 and the failure-layer routing. |
| 5-6 | Re-read the split and error-analysis sections. |
| < 5 | Re-read the lecture and rerun the script's `--verify`. |
