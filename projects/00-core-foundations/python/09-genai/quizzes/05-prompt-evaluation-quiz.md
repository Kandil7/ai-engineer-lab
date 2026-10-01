# GenAI 05: Prompt Evaluation — Quiz

> **Topic Overview**: Measuring prompt quality against fixed cases and comparing variants.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why evaluate a prompt?**
- A) To speed it up
- B) A prompt is a hypothesis until measured
- C) It is required
- D) To reduce tokens

<details><summary>Reveal Answer</summary>**B.** Evidence, not taste, decides.</details>

### Question 2 — Easy
**What are prompt test cases?**
- A) Random inputs
- B) Fixed inputs with expected behavior
- C) The prompt itself
- D) The model weights

<details><summary>Reveal Answer</summary>**B.** A fixed set makes variants comparable.</details>

### Question 3 — Medium
**Why compare variants on the same cases?**
- A) For speed
- B) Otherwise the difference is the inputs, not the prompt
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Control the variables.</details>

### Question 4 — Medium
**How do you score a subjective metric?**
- A) Guess
- B) A judge model validated against human labels
- C) Ignore it
- D) Use accuracy only

<details><summary>Reveal Answer</summary>**B.** Calibrated judges scale human judgment.</details>

### Question 5 — Medium
**Why change only one thing between variants?**
- A) For speed
- B) So the delta is attributable
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** One variable at a time.</details>

### Question 6 — Hard
**Why run each variant more than once?**
- A) For speed
- B) Output is stochastic; one sample may be noise
- C) For cost
- D) It is unnecessary

<details><summary>Reveal Answer</summary>**B.** Compare aggregates.</details>

### Question 7 — Hard
**A prompt reads better but scores lower. Which do you ship?**
- A) The better-reading one
- B) The higher-scoring one (or neither, if the score is within noise)
- C) Both
- D) Neither

<details><summary>Reveal Answer</summary>**B.** Score decides close calls.</details>

### Question 8 — Hard
**Why gate prompt changes in CI?**
- A) For speed
- B) A prompt change can regress quality like any code change
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Prompts are under the eval gate.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can evaluate prompts. |
| 5-6 | Review test cases and noise. |
| < 5 | Re-read the lecture. |
