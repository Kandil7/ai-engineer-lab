# Fine-Tuning 05: Model Registry and Release — Quiz

> **Topic Overview**: The registry entry, the model card, the eval gate,
> and rollback.

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

**What does a registry entry record?**

- A) Only the model id
- B) The artifact and its full provenance
- C) Only the eval
- D) Only the base

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Base, adapter, config, data, and eval all recorded.

</details>

---

### Question 2 — Easy

**What does the model card document?**

- A) Only the base model
- B) What, how, and how well
- C) Only the eval
- D) Only the limits

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Base, training data, eval results, failure modes, intended use.

</details>

---

### Question 3 — Easy

**When is the model card written?**

- A) After release
- B) At release
- C) Never
- D) During training

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The card is written at release, not after.

</details>

---

### Question 4 — Medium

**The eval gate requires passing:**

- A) Only eval loss
- B) The golden and adversarial sets
- C) Only faithfulness
- D) Only speed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The same sets that gate the RAG system.

</details>

---

### Question 5 — Medium

**A model improving eval loss but failing faithfulness is:**

- A) Released
- B) Not released
- C) Cached
- D) Ignored

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The eval gate blocks it.

</details>

---

### Question 6 — Medium

**Versions are:**

- A) Editable
- B) Immutable
- C) Cached
- D) Optional

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A change is a new version, never an edit.

</details>

---

### Question 7 — Medium

**The adapter is meaningless without:**

- A) The cache
- B) Its base model version
- C) The tokenizer
- D) The seed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Both base and adapter versions are recorded.

</details>

---

### Question 8 — Hard

**Rollback is mechanical only if:**

- A) The cache is warm
- B) The previous version is still registered
- C) The model is small
- D) The eval passed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The registry is the safety net.

</details>

---

### Question 9 — Hard

**A model without a card is:**

- A) An artifact without a story
- B) Faster
- C) Cached
- D) Better

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: The card is the documentation of the artifact.

</details>

---

### Question 10 — Hard**

**The registry entry is the:**

- A) Cache
- B) Single source of truth for the model
- C) Tokenizer
- D) Seed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: What the model is and how it was made.

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
| 9-10 | Expert | Ready for RAG vs fine-tuning |
| 7-8 | Proficient | Review the eval gate |
| 5-6 | Developing | Re-study versioning |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [04 - Training Runs](04-training-runs-quiz.md) | **Next**: [06 - RAG vs Fine-Tuning](06-rag-vs-fine-tuning-quiz.md)