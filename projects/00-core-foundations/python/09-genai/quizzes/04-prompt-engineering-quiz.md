# GenAI 04: Prompt Engineering — Quiz

> **Topic Overview**: Designing prompts for reliability — structure, examples, and constraints.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What are the core sections of a structured prompt?**
- A) Only a question
- B) Role, context, task, constraints, output format
- C) Random text
- D) A URL

<details><summary>Reveal Answer</summary>**B.** Explicit sections make behavior reliable.</details>

### Question 2 — Easy
**Why state the output format explicitly?**
- A) For style
- B) So the output is parseable and consistent
- C) For speed
- D) To reduce cost

<details><summary>Reveal Answer</summary>**B.** The format is a contract.</details>

### Question 3 — Medium
**When do few-shot examples help?**
- A) Always
- B) When the model needs to see the pattern, not just be told it
- C) Never
- D) Only for translation

<details><summary>Reveal Answer</summary>**B.** Examples teach by imitation.</details>

### Question 4 — Medium
**Why keep a prompt versioned?**
- A) For storage
- B) So a quality change is attributable and rollback is possible
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Prompts are versioned assets.</details>

### Question 5 — Medium
**What is the risk of a long prompt?**
- A) It is free
- B) It consumes the context budget and raises cost/latency
- C) It improves accuracy
- D) It is encrypted

<details><summary>Reveal Answer</summary>**B.** Tokens cost money and attention.</details>

### Question 6 — Hard
**A prompt works in testing and fails on new inputs. What is missing?**
- A) A bigger model
- B) Constraints and coverage (the prompt over-fits the examples)
- C) More temperature
- D) A GPU

<details><summary>Reveal Answer</summary>**B.** Constraints generalize; examples can narrow.</details>

### Question 7 — Hard
**Why measure prompt variants rather than read them?**
- A) Reading is enough
- B) Close calls are invisible by reading; only scores decide
- C) For speed
- D) Measurement is optional

<details><summary>Reveal Answer</summary>**B.** Evidence decides.</details>

### Question 8 — Hard
**Why state anti-hallucination rules ("answer only from context")?**
- A) For style
- B) To constrain generation to the supplied evidence
- C) For speed
- D) It is decorative

<details><summary>Reveal Answer</summary>**B.** The rule reduces fabrication.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can design prompts. |
| 5-6 | Review structure and constraints. |
| < 5 | Re-read the lecture. |
