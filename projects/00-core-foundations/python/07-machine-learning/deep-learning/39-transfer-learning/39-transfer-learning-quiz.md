# ML 39: Transfer Learning — Quiz

> **Topic Overview**: Frozen backbones, head swapping, fine-tuning, and schedules.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is transfer learning?**
- A) Training from scratch
- B) Reusing a model trained on one task for another
- C) Clustering
- D) Scaling

<details><summary>Reveal Answer</summary>**B.** Reuse learned features.</details>

### Question 2 — Easy
**What does freezing the backbone mean?**
- A) Deleting it
- B) Keeping its weights fixed while training a new head
- C) Casting
- D) Shuffling

<details><summary>Reveal Answer</summary>**B.** No backbone updates.</details>

### Question 3 — Medium
**Why does transfer beat from-scratch on small data?**
- A) Faster only
- B) The pretrained features already capture general structure, needing less data
- C) Less memory
- D) No gradients

<details><summary>Reveal Answer</summary>**B.** Prior knowledge.</details>

### Question 4 — Medium
**What is fine-tuning vs feature extraction?**
- A) The same
- B) Fine-tuning unfreezes (some) backbone layers with a small LR; extraction freezes all and trains only the head
- C) Extraction updates more
- D) Fine-tuning freezes all

<details><summary>Reveal Answer</summary>**B.** How much is updated.</details>

### Question 5 — Medium
**Why a small learning rate when unfreezing?**
- A) For speed
- B) To avoid destroying the pretrained weights with large updates
- C) To cast
- D) To shuffle

<details><summary>Reveal Answer</summary>**B.** Preserve learned features.</details>

### Question 6 — Hard
**When is freezing all layers insufficient?**
- A) Never
- B) When the target domain differs enough that the features must adapt
- C) Always
- D) For tabular

<details><summary>Reveal Answer</summary>**B.** Domain gap.</details>

### Question 7 — Hard
**How are pretrained embeddings used as features?**
- A) They are not
- B) Run frozen and use the vectors (e.g. for retrieval or a shallow head)
- C) Fine-tuned first
- D) Deleted

<details><summary>Reveal Answer</summary>**B.** Frozen feature vectors.</details>

### Question 8 — Hard
**What is a common LR-schedule strategy for fine-tuning?**
- A) Constant high LR
- B) Warmup + decay, sometimes discriminative (lower LR for earlier layers)
- C) Random
- D) None

<details><summary>Reveal Answer</summary>**B.** Gentle, staged updates.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You transfer and fine-tune well. |
| 5-6 | Review freezing, fine-tuning, schedules. |
| < 5 | Re-read the lecture. |
