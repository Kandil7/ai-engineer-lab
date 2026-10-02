# ML 40: Transformers from Scratch — Quiz

> **Topic Overview**: Attention, multi-head, positional encoding, blocks, and cost.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the core operation of a transformer?**
- A) Convolution
- B) Scaled dot-product attention
- C) Recurrence
- D) Pooling

<details><summary>Reveal Answer</summary>**B.** Attention.</details>

### Question 2 — Easy
**What are Q, K, V?**
- A) Layers
- B) Query, Key, Value projections used to compute attention weights
- C) Losses
- D) Optimizers

<details><summary>Reveal Answer</summary>**B.** Attention triple.</details>

### Question 3 — Medium
**Why scale the dot product by sqrt(d_k)?**
- A) For speed
- B) To keep logits in a stable range so softmax gradients do not vanish
- C) To sort
- D) To cast

<details><summary>Reveal Answer</summary>**B.** Prevent saturation.</details>

### Question 4 — Medium
**Why add positional encoding?**
- A) For speed
- B) Attention is permutation-invariant; order must be injected
- C) To cast
- D) To normalise

<details><summary>Reveal Answer</summary>**B.** Order information.</details>

### Question 5 — Medium
**What does multi-head attention do?**
- A) Repeats one head
- B) Runs several attention projections in parallel subspaces and concatenates
- C) Recurrent
- D) Convolution

<details><summary>Reveal Answer</summary>**B.** Diverse attention patterns.</details>

### Question 6 — Hard
**What components make up a transformer block?**
- A) Only attention
- B) Attention + feed-forward + residual connections (+ norm)
- C) Convolution + pooling
- D) Recurrence

<details><summary>Reveal Answer</summary>**B.** Attention+FFN+residuals.</details>

### Question 7 — Hard
**Why does attention scale quadratically?**
- A) It does not
- B) The attention matrix is O(n²) in sequence length
- C) Because of FFN
- D) Because of positions

<details><summary>Reveal Answer</summary>**B.** Pairwise scores.</details>

### Question 8 — Hard
**How does a transformer become an LLM?**
- A) Add convolution
- B) Stack blocks and train on next-token prediction at scale
- C) Add recurrence
- D) Remove attention

<details><summary>Reveal Answer</summary>**B.** Decoder stack + LM objective.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand transformers. |
| 5-6 | Review attention, scaling, positions. |
| < 5 | Re-read the lecture. |
