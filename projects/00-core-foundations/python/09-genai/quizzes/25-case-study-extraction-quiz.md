# GenAI 25: Case Study — Extraction — Quiz

> **Topic Overview**: Building a structured-extraction service with schema validation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

---

## Questions

### Question 1 — Easy
**What is structured extraction?**
- A) Summarization
- B) Turning free text into fields that satisfy a schema
- C) Translation
- D) Retrieval

<details><summary>Reveal Answer</summary>**B.** Text in, typed fields out.</details>

### Question 2 — Easy
**Why validate extracted fields?**
- A) For style
- B) The model can omit, mistype, or invent values
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Validation is the gate.</details>

### Question 3 — Medium
**What happens on a schema failure?**
- A) Accept it
- B) Reject and re-prompt or fail, logging the failure
- C) Coerce silently
- D) Ignore

<details><summary>Reveal Answer</summary>**B.** Failures must be handled.</details>

### Question 4 — Medium
**Why prefer a small model for extraction when possible?**
- A) It is always better
- B) Extraction is often a fixed mapping; a small model may suffice at lower cost
- C) For speed
- D) It is required

<details><summary>Reveal Answer</summary>**B.** Match model to task.</details>

### Question 5 — Medium
**Why include citations in extraction output?**
- A) For style
- B) So each extracted field traces to its source text
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Grounding per field.</details>

### Question 6 — Hard
**How do you measure extraction quality?**
- A) By reading outputs
- B) Field-level precision/recall against a labeled set
- C) Cost only
- D) It cannot be measured

<details><summary>Reveal Answer</summary>**B.** Per-field metrics.</details>

### Question 7 — Hard
**Why is extraction a good first production LLM task?**
- A) It is easy
- B) Deterministic I/O, measurable, and useful, with no chat ambiguity
- C) It is impressive
- D) It needs no evaluation

<details><summary>Reveal Answer</summary>**B.** Clear contract and measurable target.</details>

### Question 8 — Hard
**The model returns a field not in the source. What is this?**
- A) Fine
- B) A hallucination; output validation and citations must catch it
- C) A summary
- D) A bug

<details><summary>Reveal Answer</summary>**B.** Unsourced fields are hallucinations.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can build extraction. |
| 5-6 | Review validation and metrics. |
| < 5 | Re-read the lecture. |
