# ML 50: Pruning — Quiz

> **Topic Overview**: Structured vs unstructured, magnitude pruning, global
> pruning, lottery ticket, and prune-then-fine-tune.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does unstructured pruning do?**
- A) Removes whole channels
- B) Zeros individual weights -> sparse matrix
- C) Removes layers
- D) Shrinks the batch

<details><summary>Reveal Answer</summary>**B.** Individual weights become zero.</details>

### Question 2 — Easy
**What is the default pruning criterion?**
- A) Random
- B) Magnitude (smallest |w| first)
- C) Largest |w| first
- D) Alphabetical

<details><summary>Reveal Answer</summary>**B.** Small weights contribute least.</details>

### Question 3 — Medium
**Why might sparsity not equal speedup?**
- A) Sparse matrices need sparse-kernel support to run faster
- B) Sparsity is always faster
- C) Sparsity is imaginary
- D) Speedup is unrelated to size

<details><summary>Reveal Answer</summary>**A.** Unstructured sparsity compresses but may not accelerate.</details>

### Question 4 — Medium
**Which pruning gives a real, hardware-friendly speedup?**
- A) Unstructured
- B) Structured (whole channels removed)
- C) Neither
- D) Both equally

<details><summary>Reveal Answer</summary>**B.** A smaller dense model runs faster.</details>

### Question 5 — Medium
**What is the lottery-ticket hypothesis?**
- A) Random weights win
- B) A sparse subnetwork matches the dense net's accuracy
- C) Pruning always helps
- D) Bigger is always better

<details><summary>Reveal Answer</summary>**B.** Efficient subnetworks hide inside dense nets.</details>

### Question 6 — Hard
**What is the standard remedy for pruning's accuracy drop?**
- A) Nothing
- B) A short fine-tuning pass after pruning
- C) More pruning
- D) A larger batch

<details><summary>Reveal Answer</summary>**B.** Surviving weights adapt to the smaller structure.</details>

### Question 7 — Hard
**Why is global pruning often better than uniform per-layer pruning?**
- A) It respects per-layer sensitivity by finding least-important weights anywhere
- B) It is faster to run
- C) It removes more weights
- D) It needs no fine-tuning

<details><summary>Reveal Answer</summary>**A.** Uniform pruning over-prunes critical layers.</details>

### Question 8 — Hard
**What should you report instead of sparsity alone?**
- A) Latency, memory, and accuracy
- B) Only the sparsity percentage
- C) Only the model name
- D) Only the epoch count

<details><summary>Reveal Answer</summary>**A.** Sparsity is a number, not the goal.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You prune for real speedup. |
| 5-6 | Review structured vs unstructured. |
| < 5 | Re-read the lecture. |
