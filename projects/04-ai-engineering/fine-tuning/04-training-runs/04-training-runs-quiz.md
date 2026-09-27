# Fine-Tuning 04: Training Runs — Quiz

> **Topic Overview**: The run config, monitoring, checkpointing, and run
> comparison.

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

**What does the run config capture?**

- A) Only the model
- B) Everything the run needs
- C) Only the data
- D) Only the seed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Base model, rank, lr, batch, epochs, split, seed.

</details>

---

### Question 2 — Easy

**A run without its config is:**

- A) Faster
- B) Unreproducible
- C) Cached
- D) Better

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The config is what makes the run reproducible.

</details>

---

### Question 3 — Easy

**The honest training signal is:**

- A) Training loss
- B) Eval loss on the held-out set
- C) The cache
- D) The model size

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Training loss falls even when the model memorizes.

</details>

---

### Question 4 — Medium

**Rising eval loss while training loss falls is:**

- A) Healthy
- B) Overfitting
- C) Cached
- D) Fast

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Stop or reduce epochs.

</details>

---

### Question 5 — Medium

**What does a checkpoint save?**

- A) The full dataset
- B) The adapter state at a step
- C) The cache
- D) The tokenizer

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A run resumes from the last checkpoint.

</details>

---

### Question 6 — Medium

**The checkpoint carries:**

- A) Only the weights
- B) The step and the config hash
- C) Only the step
- D) Only the config

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Resuming with a different config is a different run.

</details>

---

### Question 7 — Medium

**Runs compare on:**

- A) Different eval sets
- B) The same eval set
- C) The cache
- D) The model size

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Cross-set comparison is meaningless.

</details>

---

### Question 8 — Hard

**A changed dataset is:**

- A) The same run
- B) A changed run
- C) A cache miss
- D) An error

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The data version is part of the config.

</details>

---

### Question 9 — Hard

**Reproducibility needs:**

- A) Only the config
- B) Config, seed, and data version
- C) Only the seed
- D) Only the data

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: All three together reproduce the run.

</details>

---

### Question 10 — Hard**

**A candidate improving eval loss but degrading a downstream metric is:**

- A) Hidden
- B) A tradeoff made explicit
- C) A cache win
- D) Ignored

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The comparison is the evidence for the next decision.

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
| 9-10 | Expert | Ready for the model registry |
| 7-8 | Proficient | Review checkpointing |
| 5-6 | Developing | Re-study the config |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [03 - Training Data](03-training-data-quiz.md) | **Next**: [05 - Model Registry](05-model-registry-quiz.md)