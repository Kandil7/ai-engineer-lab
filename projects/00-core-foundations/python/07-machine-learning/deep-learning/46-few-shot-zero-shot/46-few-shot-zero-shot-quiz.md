# ML 46: Few-Shot and Zero-Shot Learning — Quiz

> **Topic Overview**: Shared embedding space, zero-shot by description, few-shot
> by prototype, in-context learning, and the cost ladder.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What makes zero-shot classification possible?**
- A) More training data
- B) A shared embedding space where meaning is geometry
- C) A bigger model always
- D) Ensemble methods

<details><summary>Reveal Answer</summary>**B.** Related things are close, so similarity classifies.</details>

### Question 2 — Easy
**What is a prototype in few-shot learning?**
- A) A random example
- B) The mean embedding of the support set
- C) The first example
- D) The label itself

<details><summary>Reveal Answer</summary>**B.** The class center from a few examples.</details>

### Question 3 — Medium
**How does zero-shot differ from few-shot?**
- A) Zero-shot uses no labeled examples; few-shot uses k
- B) They are identical
- C) Zero-shot is slower
- D) Few-shot needs no examples

<details><summary>Reveal Answer</summary>**A.** Zero-shot matches descriptions; few-shot matches prototypes.</details>

### Question 4 — Medium
**What is in-context learning?**
- A) Fine-tuning
- B) LLM few-shot via the prompt, with no weight update
- C) Prototype classification
- D) Cosine similarity

<details><summary>Reveal Answer</summary>**B.** Conditioning, not training.</details>

### Question 5 — Medium
**Why normalize embeddings before cosine?**
- A) It is faster
- B) Cosine on unnormalized vectors is a scaled dot product, not true alignment
- C) It prevents overfitting
- D) It is required by the hardware

<details><summary>Reveal Answer</summary>**B.** Normalization makes cosine measure direction, not magnitude.</details>

### Question 6 — Hard
**What is the correct cost ladder?**
- A) fine-tune -> few-shot -> zero-shot
- B) zero-shot -> few-shot -> fine-tune
- C) few-shot -> zero-shot -> fine-tune
- D) All equal

<details><summary>Reveal Answer</summary>**B.** Escalate cost only as the task demands.</details>

### Question 7 — Hard
**When does zero-shot reliably fail?**
- A) On a niche domain the pretrained space does not align with
- B) On image data
- C) On text data
- D) Never

<details><summary>Reveal Answer</summary>**A.** Similarity only works inside the pretrained space.</details>

### Question 8 — Hard
**Why can a new class be added with no retraining in zero-shot?**
- A) Because it is a new point in the shared space, not a new decision boundary
- B) Because models never retrain
- C) Because classes are hardcoded
- D) Because of gradient descent

<details><summary>Reveal Answer</summary>**A.** A new class is just a new embedding/prototype.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand the similarity regimes. |
| 5-6 | Review zero-shot vs few-shot and in-context. |
| < 5 | Re-read the lecture. |
