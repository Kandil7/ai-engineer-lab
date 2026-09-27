# Fine-Tuning 01: Supervised Fine-Tuning (SFT) — Quiz

> **Topic Overview**: What SFT changes, the chat template, answer-token
> loss, and overfitting.

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

**What does SFT change?**

- A) The model's knowledge
- B) The model's behavior
- C) The corpus
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: SFT teaches format and behavior; it does not reliably add facts.

</details>

---

### Question 2 — Easy

**What is the chat template?**

- A) A cache key
- B) The system/user/assistant format
- C) A model id
- D) A token budget

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The template is the training-inference contract.

</details>

---

### Question 3 — Easy

**Where is the loss computed?**

- A) On the prompt tokens
- B) On the answer tokens only
- C) On all tokens
- D) On the cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The model learns to produce answers, not to predict questions.

</details>

---

### Question 4 — Medium

**How are prompt tokens masked?**

- A) With 0
- B) With -100
- C) With 1
- D) With None

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: -100 is the standard mask that excludes tokens from the loss.

</details>

---

### Question 5 — Medium

**A template mismatch between training and inference:**

- A) Is fine
- B) Degrades the model
- C) Speeds it up
- D) Caches it

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The template is the contract; a mismatch breaks it.

</details>

---

### Question 6 — Medium

**Overfitting shows as:**

- A) Eval loss near zero
- B) Train loss near zero while eval loss rises
- C) High train loss
- D) A cache miss

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Memorization looks perfect on training, fails on evaluation.

</details>

---

### Question 7 — Medium

**The fix for invisible overfitting is:**

- A) More training
- B) A held-out evaluation set
- C) A bigger cache
- D) A faster model

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Held-out examples make overfitting visible during training.

</details>

---

### Question 8 — Hard

**A model that never saw a fact in pretraining will:**

- A) Learn it from a few hundred examples
- B) Not reliably learn it from a few hundred examples
- C) Cache it
- D) Retrieve it

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: SFT is not a reliable way to add new facts.

</details>

---

### Question 9 — Hard

**SFT is right when the task is:**

- A) Factual
- B) Behavioral
- C) Retrieval
- D) Caching

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Format, style, and instruction-following are behavioral.

</details>

---

### Question 10 — Hard**

**The roadmap's split is:**

- A) SFT for knowledge, RAG for behavior
- B) RAG for knowledge, SFT for behavior
- C) Both for knowledge
- D) Neither

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Retrieval supplies facts; fine-tuning shapes behavior.

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
| 9-10 | Expert | Ready for LoRA/QLoRA |
| 7-8 | Proficient | Review the loss |
| 5-6 | Developing | Re-study the template |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [02 - LoRA and QLoRA](02-lora-qlora-quiz.md)