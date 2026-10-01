# GenAI 19: Guardrails and Safety — Quiz

> **Topic Overview**: Input/output guardrails, injection defense, and safe behavior.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a guardrail?**
- A) A model
- B) A check that constrains input or output for safety or correctness
- C) A cache
- D) A chunk

<details><summary>Reveal Answer</summary>**B.** A boundary control.</details>

### Question 2 — Easy
**Where can prompt injection arrive in a RAG system?**
- A) Only the query
- B) The query and the retrieved content
- C) The model weights
- D) The cache

<details><summary>Reveal Answer</summary>**B.** Retrieved content is untrusted input.</details>

### Question 3 — Medium
**Why is retrieved content treated as data, not instructions?**
- A) For speed
- B) The model will otherwise follow instructions hidden in a passage
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Context is data to summarize.</details>

### Question 4 — Medium
**What is an output guardrail?**
- A) An input filter
- B) A check on the generated answer (PII, schema, citations) before it is returned
- C) A cache
- D) A chunker

<details><summary>Reveal Answer</summary>**B.** Output is validated too.</details>

### Question 5 — Medium
**Why is the model not a security boundary?**
- A) It is
- B) It reads what it is given and may follow injected instructions
- C) It is too small
- D) It is encrypted

<details><summary>Reveal Answer</summary>**B.** The pipeline enforces the boundary.</details>

### Question 6 — Hard
**Why layer defenses (filter, provenance, marker scan, output validation, abstention)?**
- A) For speed
- B) No single check catches everything
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Layering covers what each misses.</details>

### Question 7 — Hard
**Why test guardrails in CI as a rate?**
- A) For speed
- B) Resistance is a rate that must stay at target, tested against a growing adversarial set
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Security is measured continuously.</details>

### Question 8 — Hard
**What is the correct behavior on untrusted or thin context?**
- A) Answer anyway
- B) Abstain or refuse, never fabricate
- C) Guess
- D) Ignore the guardrail

<details><summary>Reveal Answer</summary>**B.** Honesty beats a confident wrong answer.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can design guardrails. |
| 5-6 | Review injection and layering. |
| < 5 | Re-read the lecture. |
