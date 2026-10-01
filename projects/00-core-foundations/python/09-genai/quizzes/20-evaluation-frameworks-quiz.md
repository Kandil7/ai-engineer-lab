# GenAI 20: Evaluation Frameworks — Quiz

> **Topic Overview**: Structuring evaluation — golden sets, metrics, and regression gates.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a golden set?**
- A) Training data
- B) A fixed, curated set of queries with verified answers
- C) A model
- D) A cache

<details><summary>Reveal Answer</summary>**B.** The fixed yardstick.</details>

### Question 2 — Easy
**Why must the golden set be fixed?**
- A) For speed
- B) So a change is attributable to the system, not the test set
- C) For cost
- D) It need not be

<details><summary>Reveal Answer</summary>**B.** A moving yardstick measures nothing.</details>

### Question 3 — Medium
**Why separate retrieval metrics from answer metrics?**
- A) They are the same
- B) Each isolates a different failure
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Diagnose at the layer.</details>

### Question 4 — Medium
**What is a regression gate?**
- A) A model
- B) A CI check that fails when metrics drop below a baseline
- C) A cache
- D) A chunker

<details><summary>Reveal Answer</summary>**B.** It guards against silent regressions.</details>

### Question 5 — Medium
**Why validate an LLM judge against human labels?**
- A) It is optional
- B) An unvalidated judge measures itself, not quality
- C) For speed
- D) It is always right

<details><summary>Reveal Answer</summary>**B.** Judge accuracy is a metric.</details>

### Question 6 — Hard
**Why run a small eval per PR and a larger one before release?**
- A) For cost only
- B) Fast feedback per change, thorough coverage at the release boundary
- C) For speed
- D) It is arbitrary

<details><summary>Reveal Answer</summary>**B.** Tiered gates match cost to risk.</details>

### Question 7 — Hard
**Why is a reproducible eval report an artifact?**
- A) For storage
- B) It records what changed and by how much, so decisions are reviewable
- C) For style
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** The report is the evidence.</details>

### Question 8 — Hard
**A change improves one category and regresses another. What is required?**
- A) Ship it
- B) An explicit, recorded tradeoff decision with the numbers
- C) Ignore the regression
- D) Lower the threshold

<details><summary>Reveal Answer</summary>**B.** Tradeoffs are explicit, never silent.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can structure evaluation. |
| 5-6 | Review gates and judge validation. |
| < 5 | Re-read the lecture. |
