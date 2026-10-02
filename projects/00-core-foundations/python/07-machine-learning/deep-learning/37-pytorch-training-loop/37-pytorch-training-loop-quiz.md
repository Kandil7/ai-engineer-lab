# ML 37: PyTorch Training Loop — Quiz

> **Topic Overview**: `nn.Module`, DataLoader, the canonical loop, and train/eval modes.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What two methods must an `nn.Module` implement?**
- A) `fit`/`predict`
- B) `__init__` (layers) and `forward`
- C) `open`/`close`
- D) `run`/`stop`

<details><summary>Reveal Answer</summary>**B.** Define and compute.</details>

### Question 2 — Easy
**What does a DataLoader add over a Dataset?**
- A) Nothing
- B) Batching, shuffling, and parallel loading
- C) Training
- D) Gradients

<details><summary>Reveal Answer</summary>**B.** Batching and shuffling.</details>

### Question 3 — Medium
**What are the canonical loop steps?**
- A) Forward, loss, `zero_grad`, `backward`, `step`
- B) Sort, train, test
- C) Load, save
- D) Shuffle only

<details><summary>Reveal Answer</summary>**A.** The training step.</details>

### Question 4 — Medium
**Why `optimizer.zero_grad()` before `backward()`?**
- A) For speed
- B) To clear accumulated gradients from the previous step
- C) To cast
- D) To shuffle

<details><summary>Reveal Answer</summary>**B.** Avoid accumulation.</details>

### Question 5 — Medium
**What is the "overfit a single batch" trick?**
- A) Regularisation
- B) Train on one batch until loss ≈ 0 to verify the model/loop can learn
- C) Scaling
- D) Inference

<details><summary>Reveal Answer</summary>**B.** Sanity check.</details>

### Question 6 — Hard
**Why call `model.eval()` for evaluation?**
- A) For speed
- B) It disables dropout and uses running batch-norm stats
- C) It frees memory
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Inference behavior.</details>

### Question 7 — Hard
**Why wrap evaluation in `torch.no_grad()`?**
- A) For speed only
- B) To skip graph construction and save memory during inference
- C) To shuffle
- D) To cast

<details><summary>Reveal Answer</summary>**B.** No gradients needed.</details>

### Question 8 — Hard
**What is a common device bug?**
- A) Inputs on CPU while the model is on GPU; move both to the same device
- B) Wrong dtype only
- C) Too many layers
- D) Shuffling

<details><summary>Reveal Answer</summary>**A.** Device mismatch.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You write correct training loops. |
| 5-6 | Review the step order and train/eval modes. |
| < 5 | Re-read the lecture. |
