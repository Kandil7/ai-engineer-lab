# GenAI 01: LLM Fundamentals — Quiz

> **Topic Overview**: Tokens, context windows, sampling, and the limits of an LLM.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a token?**
- A) A word
- B) A subword unit the model reads and predicts
- C) A file
- D) A GPU

<details><summary>Reveal Answer</summary>**B.** Text is split into tokens, not words.</details>

### Question 2 — Easy
**What is the context window?**
- A) The training time
- B) The maximum tokens the model can read and produce at once
- C) The number of GPUs
- D) The batch size

<details><summary>Reveal Answer</summary>**B.** Input plus output share the window.</details>

### Question 3 — Medium
**What does temperature control?**
- A) Speed
- B) The randomness of sampling: low is focused, high is varied
- C) Memory
- D) Cost only

<details><summary>Reveal Answer</summary>**B.** Temperature trades determinism for diversity.</details>

### Question 4 — Medium
**Why can an LLM hallucinate?**
- A) It is broken
- B) It predicts plausible tokens, not verified facts
- C) It lacks a GPU
- D) It is encrypted

<details><summary>Reveal Answer</summary>**B.** Plausibility is not truth.</details>

### Question 5 — Medium
**Why does a long prompt raise time to first token?**
- A) It does not
- B) Prefill processes the whole prompt before the first output token
- C) It raises cost only
- D) It reduces quality

<details><summary>Reveal Answer</summary>**B.** Prefill cost scales with prompt length.</details>

### Question 6 — Hard
**A fact absent from pretraining and from the prompt: what will the model do?**
- A) Refuse
- B) Produce a plausible fabrication
- C) Error
- D) Search the web

<details><summary>Reveal Answer</summary>**B.** Absent knowledge becomes a plausible guess.</details>

### Question 7 — Hard
**Why is "LLM told X" not evidence that X is true?**
- A) It is evidence
- B) The model optimizes plausibility under its training, not correctness
- C) X is always false
- D) The model is small

<details><summary>Reveal Answer</summary>**B.** Grounding or verification is required.</details>

### Question 8 — Hard
**Why ground answers in retrieved context?**
- A) For speed
- B) It gives the model the facts and a citation handle, reducing fabrication
- C) For cost
- D) It improves sampling

<details><summary>Reveal Answer</summary>**B.** Grounding replaces recall with supplied evidence.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | Solid on LLM fundamentals. |
| 5-6 | Review tokens, context, and hallucination. |
| < 5 | Re-read the lecture. |
