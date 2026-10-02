# ML 36: PyTorch Tensors — Quiz

> **Topic Overview**: Tensor creation, dtypes, device, autograd, and shape ops.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a tensor?**
- A) A list
- B) An n-dimensional array with optional GPU and autograd support
- C) A model
- D) A dataset

<details><summary>Reveal Answer</summary>**B.** The core data structure.</details>

### Question 2 — Easy
**What dtype is the deep-learning default?**
- A) float64
- B) float32
- C) int8
- D) bool

<details><summary>Reveal Answer</summary>**B.** The DL default.</details>

### Question 3 — Medium
**What does `.to(device)` do?**
- A) Reshapes
- B) Moves the tensor to CPU/GPU
- C) Casts dtype only
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Device placement.</details>

### Question 4 — Medium
**What does `requires_grad=True` enable?**
- A) Casting
- B) Autograd tracking so gradients are computed for the tensor
- C) Reshaping
- D) Moving

<details><summary>Reveal Answer</summary>**B.** Gradient tracking.</details>

### Question 5 — Medium
**Why do gradients accumulate by default?**
- A) A bug
- B) `backward` adds to `.grad`; you must `zero_grad()` before each step
- C) For speed
- D) For dtype

<details><summary>Reveal Answer</summary>**B.** Explicit zeroing.</details>

### Question 6 — Hard
**When do you use `torch.no_grad()`?**
- A) Training
- B) Inference/feature extraction to save memory and skip graph building
- C) Casting
- D) Moving

<details><summary>Reveal Answer</summary>**B.** No gradients needed.</details>

### Question 7 — Hard
**What is the difference between `reshape` and `view`?**
- A) None
- B) `view` requires contiguous memory; `reshape` copies if needed
- C) `reshape` requires contiguity
- D) They are identical

<details><summary>Reveal Answer</summary>**B.** Contiguity constraint.</details>

### Question 8 — Hard
**Why must a NumPy→tensor→NumPy roundtrip be careful?**
- A) It is always safe
- B) They can share memory; mutating one alters the other
- C) It is slow
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Shared buffer.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You handle tensors well. |
| 5-6 | Review autograd and device/dtype. |
| < 5 | Re-read the lecture. |
