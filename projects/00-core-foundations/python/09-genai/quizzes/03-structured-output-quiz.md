# GenAI 03: Structured Output — Quiz

> **Topic Overview**: Forcing model output into a schema so downstream code can consume it.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why is structured output needed?**
- A) It looks nice
- B) Free text cannot be parsed reliably by code
- C) It is faster
- D) It reduces cost

<details><summary>Reveal Answer</summary>**B.** Code needs a parseable contract.</details>

### Question 2 — Easy
**What is a schema for LLM output?**
- A) The prompt
- B) The declared fields and types the output must satisfy
- C) The model file
- D) The dataset

<details><summary>Reveal Answer</summary>**B.** It is the output contract.</details>

### Question 3 — Medium
**What does Pydantic add over a dict?**
- A) Speed
- B) Type validation and clear errors at the boundary
- C) Encryption
- D) Compression

<details><summary>Reveal Answer</summary>**B.** Validation catches malformed output.</details>

### Question 4 — Medium
**What should happen when the model returns schema-invalid output?**
- A) Use it anyway
- B) Reject it and re-prompt or fail, logging the event
- C) Silently coerce it
- D) Ignore it

<details><summary>Reveal Answer</summary>**B.** Validation is a hard gate.</details>

### Question 5 — Medium
**Why require citations to be an explicit field?**
- A) For style
- B) So grounding can be validated mechanically
- C) For speed
- D) To reduce cost

<details><summary>Reveal Answer</summary>**B.** A field is checkable; prose is not.</details>

### Question 6 — Hard
**A claim without a citation is what, by construction?**
- A) Fine
- B) A hallucination, if the schema requires a citation per claim
- C) A summary
- D) A bug

<details><summary>Reveal Answer</summary>**B.** The schema makes the failure unrepresentable.</details>

### Question 7 — Hard
**Why validate cited ids against the context in the backend?**
- A) For speed
- B) The model can invent plausible ids; only the backend knows the real set
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Fabricated ids are rejected mechanically.</details>

### Question 8 — Hard
**What is the cost of structured output on the prompt?**
- A) None
- B) The schema/spec consumes tokens and constrains generation
- C) It is free
- D) It halves the context

<details><summary>Reveal Answer</summary>**B.** The contract is part of the prompt budget.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can enforce output schemas. |
| 5-6 | Review validation and citation fields. |
| < 5 | Re-read the lecture. |
