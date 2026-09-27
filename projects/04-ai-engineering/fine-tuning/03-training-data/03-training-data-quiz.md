# Fine-Tuning 03: Training Data Preparation — Quiz

> **Topic Overview**: Instruction format, quality filtering,
> deduplication, and the train/eval split.

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

**What does the instruction set contain?**

- A) Raw text
- B) Instruction-answer pairs
- C) Only answers
- D) Only questions

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Each example is an instruction-answer pair for the chat template.

</details>

---

### Question 2 — Easy

**What beats a large noisy set?**

- A) A larger set
- B) A small clean set
- C) A cached set
- D) A random set

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A few hundred clean examples beat thousands of noisy ones.

</details>

---

### Question 3 — Easy

**What does deduplication remove?**

- A) Low-quality answers
- B) Exact and near-duplicate examples
- C) Long answers
- D) Short answers

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Duplicates waste capacity and bias the model.

</details>

---

### Question 4 — Medium

**A mixed instruction format teaches:**

- A) Consistent behavior
- B) Mixed behavior
- C) Faster training
- D) Better caching

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The model learns the format from the data.

</details>

---

### Question 5 — Medium

**Quality filtering is:**

- A) A training task
- B) A data-engineering task
- C) A caching task
- D) A model task

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Cleaning the set happens before training.

</details>

---

### Question 6 — Medium

**The eval set is split:**

- A) By topic
- B) By example
- C) By length
- D) By cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The eval set must represent the same distribution.

</details>

---

### Question 7 — Medium

**The split is:**

- A) Random each run
- B) Fixed and recorded
- C) By model
- D) By cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The same eval set measures every training run.

</details>

---

### Question 8 — Hard

**Near-duplicates need:**

- A) Exact matching
- B) Normalization and similarity comparison
- C) Caching
- D) Random removal

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Near-duplicates differ slightly; similarity finds them.

</details>

---

### Question 9 — Hard

**The audit happens:**

- A) During training
- B) Before training
- C) After training
- D) Never

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A set that fails the audit is fixed before the run.

</details>

---

### Question 10 — Hard**

**The audit covers:**

- A) Only format
- B) Format, length, balance, and eval coverage
- C) Only balance
- D) Only coverage

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The audit is a full report, not a guess.

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
| 9-10 | Expert | Ready for training runs |
| 7-8 | Proficient | Review the split |
| 5-6 | Developing | Re-study deduplication |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [02 - LoRA/QLoRA](02-lora-qlora-quiz.md) | **Next**: [04 - Training Runs](04-training-runs-quiz.md)