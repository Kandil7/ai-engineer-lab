# GenAI 21: Fine-Tuning — Quiz

> **Topic Overview**: When and how to adapt a model — behavior versus knowledge, LoRA.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does fine-tuning change?**
- A) Knowledge reliably
- B) Behavior: format, tone, instruction-following
- C) The tokenizer
- D) The GPU

<details><summary>Reveal Answer</summary>**B.** Behavior, not knowledge.</details>

### Question 2 — Easy
**What tool supplies knowledge?**
- A) Fine-tuning
- B) Retrieval (RAG)
- C) Quantization
- D) Caching

<details><summary>Reveal Answer</summary>**B.** RAG for facts.</details>

### Question 3 — Medium
**What is LoRA?**
- A) Full fine-tuning
- B) Training small low-rank adapters with the base frozen
- C) A cache
- D) A chunker

<details><summary>Reveal Answer</summary>**B.** Parameter-efficient adaptation.</details>

### Question 4 — Medium
**What does the rank control in LoRA?**
- A) Speed
- B) The adapter's capacity (higher captures more, risks overfitting)
- C) Memory only
- D) Cost

<details><summary>Reveal Answer</summary>**B.** A tuned hyperparameter.</details>

### Question 5 — Medium
**Why does QLoRA fit a large model on a small GPU?**
- A) It trains faster
- B) The frozen base is quantized to 4-bit, cutting weight memory
- C) It shrinks the dataset
- D) It is smaller

<details><summary>Reveal Answer</summary>**B.** Quantized base plus small adapters.</details>

### Question 6 — Hard
**Why must the training chat template match inference?**
- A) For style
- B) A mismatch degrades the model's behavior silently
- C) For speed
- D) It need not

<details><summary>Reveal Answer</summary>**B.** The template is a training-inference contract.</details>

### Question 7 — Hard
**Why is data quality more important than quantity for SFT?**
- A) Quantity always wins
- B) The model imitates the data, so noise is imitated too
- C) For speed
- D) It is not

<details><summary>Reveal Answer</summary>**B.** Clean examples beat many noisy ones.</details>

### Question 8 — Hard
**What is the RAG-vs-fine-tuning decision?**
- A) Always fine-tune
- B) RAG for knowledge, fine-tuning for behavior, often hybrid
- C) Always RAG
- D) It is arbitrary

<details><summary>Reveal Answer</summary>**B.** Match tool to problem.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand fine-tuning. |
| 5-6 | Review behavior vs knowledge and LoRA. |
| < 5 | Re-read the lecture. |
