# ML 47: Self-Supervised Learning — Quiz

> **Topic Overview**: Pretext tasks, contrastive vs masked, InfoNCE, and
> pretrain-then-fine-tune.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a pretext task?**
- A) The final task
- B) An artificial task whose answer is already in the data
- C) A labeling job
- D) A hyperparameter

<details><summary>Reveal Answer</summary>**B.** SSL invents labels from the data itself.</details>

### Question 2 — Easy
**Which SSL family hides part of the input and reconstructs it?**
- A) Contrastive
- B) Masked modeling
- C) Supervised
- D) Clustering

<details><summary>Reveal Answer</summary>**B.** BERT-style masked prediction.</details>

### Question 3 — Medium
**What is a positive pair in contrastive learning?**
- A) Two different examples
- B) Two views of the same example
- C) Two labels
- D) Two models

<details><summary>Reveal Answer</summary>**B.** Augmented views of one example, pulled together.</details>

### Question 4 — Medium
**What is representation collapse?**
- A) The model diverges
- B) All embeddings drift to one point, making similarity meaningless
- C) The loss becomes NaN
- D) The model overfits

<details><summary>Reveal Answer</summary>**B.** A degenerate contrastive solution.</details>

### Question 5 — Medium
**Which models are contrastive examples?**
- A) BERT, GPT
- B) SimCLR, CLIP
- C) Random forest, SVM
- D) K-means, PCA

<details><summary>Reveal Answer</summary>**B.** CLIP contrasts image and text views.</details>

### Question 6 — Hard
**Why is pretrain-then-fine-tune the production default?**
- A) Unlabeled data is free; SSL moves most learning cost onto it
- B) Labels are free
- C) It is always faster
- D) It never needs a GPU

<details><summary>Reveal Answer</summary>**A.** Inherit the big pretraining, budget only the fine-tune.</details>

### Question 7 — Hard
**For an application engineer, what is SSL's honest role?**
- A) Pretrain from scratch every project
- B) The origin story of every pretrained model you fine-tune
- C) A label annotation tool
- D) A replacement for evaluation

<details><summary>Reveal Answer</summary>**B.** You inherit SSL products; you rarely rerun pretraining.</details>

### Question 8 — Hard
**What should you measure to judge an SSL model's success?**
- A) The pretext task metric
- B) The downstream task metric after fine-tuning
- C) The pretraining loss
- D) The number of epochs

<details><summary>Reveal Answer</summary>**B.** The product is the encoder; measure the real task.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand SSL's role. |
| 5-6 | Review contrastive vs masked and InfoNCE. |
| < 5 | Re-read the lecture. |
