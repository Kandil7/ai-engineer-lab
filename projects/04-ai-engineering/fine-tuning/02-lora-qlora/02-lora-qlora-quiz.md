# Fine-Tuning 02: LoRA and QLoRA — Quiz

> **Topic Overview**: The low-rank update, the rank, and the QLoRA memory
> budget.

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

**What does LoRA freeze?**

- A) The adapter
- B) The base model
- C) The optimizer
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: LoRA trains small adapters; the base weights stay frozen.

</details>

---

### Question 2 — Easy

**What does LoRA train?**

- A) The full model
- B) Small low-rank matrices
- C) The tokenizer
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The adapter is a fraction of the base size.

</details>

---

### Question 3 — Easy

**What does the rank control?**

- A) The model size
- B) The adapter's capacity
- C) The cache size
- D) The token budget

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Higher rank captures more but risks overfitting.

</details>

---

### Question 4 — Medium

**The common rank range is:**

- A) 1 to 4
- B) 8 to 64
- C) 1000 to 2000
- D) 0 to 1

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Rank 8 to 64 is the typical tuning range.

</details>

---

### Question 5 — Medium

**What does QLoRA quantize?**

- A) The adapter
- B) The frozen base model to 4-bit
- C) The optimizer
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The 4-bit base is what makes 7B fine-tuning fit in 16 GB.

</details>

---

### Question 6 — Medium

**A 7B model's weights at 4-bit are about:**

- A) 14 GB
- B) 4 GB
- C) 1 GB
- D) 16 GB

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: 4-bit drops the weights from ~14 GB to ~4 GB.

</details>

---

### Question 7 — Medium

**Gradient checkpointing trades:**

- A) Memory for speed
- B) Compute for memory
- C) Accuracy for speed
- D) Cache for memory

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Activations are recomputed instead of stored.

</details>

---

### Question 8 — Hard

**The memory budget includes:**

- A) Only the weights
- B) Weights, adapters, optimizer state, and activations
- C) Only the adapter
- D) Only the cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The full accounting is checked before the run.

</details>

---

### Question 9 — Hard

**The portable artifact for inference is:**

- A) The full model
- B) The adapter file
- C) The cache
- D) The tokenizer

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The adapter is a few megabytes and merges into the base.

</details>

---

### Question 10 — Hard**

**The merge W' = W + BA is:**

- A) Lossy
- B) Exact and reversible
- C) Approximate
- D) Cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The merged model runs without the adapter machinery.

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
| 9-10 | Expert | Ready for training data |
| 7-8 | Proficient | Review the rank |
| 5-6 | Developing | Re-study the memory budget |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [01 - SFT](01-supervised-fine-tuning-quiz.md) | **Next**: [03 - Training Data](03-training-data-quiz.md)