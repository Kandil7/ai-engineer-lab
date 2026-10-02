# ML 34: Ensembling — Quiz

> **Topic Overview**: Voting, stacking, blending, and the role of diversity.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why do ensembles usually beat a single model?**
- A) Always more accurate per member
- B) Averaging decorrelated errors cancels noise
- C) They are faster
- D) They need less data

<details><summary>Reveal Answer</summary>**B.** Error cancellation.</details>

### Question 2 — Easy
**What is hard voting?**
- A) Average probabilities
- B) Majority label wins
- C) Weighted into a meta-model
- D) A single model

<details><summary>Reveal Answer</summary>**B.** Majority vote.</details>

### Question 3 — Medium
**What is soft voting?**
- A) Majority label
- B) Average predicted probabilities, then argmax
- C) Meta-model
- D) A single model

<details><summary>Reveal Answer</summary>**B.** Uses confidence.</details>

### Question 4 — Medium
**What is stacking?**
- A) Majority vote
- B) A meta-model is trained on base models' out-of-fold predictions
- C) Blending
- D) A single model

<details><summary>Reveal Answer</summary>**B.** Learned combiner.</details>

### Question 5 — Medium
**What is blending?**
- A) A meta-model
- B) A hand-weighted average of base predictions on a holdout set
- C) Majority vote
- D) A single model

<details><summary>Reveal Answer</summary>**B.** Simple weighted average.</details>

### Question 6 — Hard
**Why is diversity the key to ensemble gain?**
- A) It is not
- B) Identical models make identical errors; averaging changes nothing
- C) It is faster
- D) It reduces data

<details><summary>Reveal Answer</summary>**B.** Decorrelated errors.</details>

### Question 7 — Hard
**When should you NOT ensemble?**
- A) Never
- B) When a single model meets the requirement; ensembles add cost and complexity
- C) Always
- D) For tabular

<details><summary>Reveal Answer</summary>**B.** Cost/benefit.</details>

### Question 8 — Hard
**Why must stacking use out-of-fold predictions?**
- A) For speed
- B) In-sample base predictions leak, letting the meta-model overfit
- C) To scale
- D) To sort

<details><summary>Reveal Answer</summary>**B.** Honest meta-features.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You ensemble well. |
| 5-6 | Review voting vs stacking vs blending. |
| < 5 | Re-read the lecture. |
