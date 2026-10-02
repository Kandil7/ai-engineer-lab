# FastAPI 26: Pydantic v2 Deep — Quiz

> **Topic Overview**: Validators, computed fields, strict mode, and aliases.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `field_validator` do?**
- A) Cross-field checks
- B) Per-field validation logic
- C) Serialization
- D) Routing

<details><summary>Reveal Answer</summary>**B.** Field-level logic.</details>

### Question 2 — Easy
**What does `model_validator` add?**
- A) Nothing
- B) Cross-field invariants over the whole model
- C) Only one field
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Model-level rules.</details>

### Question 3 — Medium
**What does `computed_field` do?**
- A) Validates
- B) Derives an output value included in serialization
- C) Caches
- D) Sorts

<details><summary>Reveal Answer</summary>**B.** Derived output.</details>

### Question 4 — Medium
**What does strict mode change?**
- A) Speed
- B) It disables silent type coercion, so `"1"` is rejected for an int
- C) Caching
- D) Routing

<details><summary>Reveal Answer</summary>**B.** No coercion.</details>

### Question 5 — Medium
**What is `TypeAdapter` for?**
- A) Models only
- B) Validating/serializing a standalone type without a model class
- C) Routing
- D) Auth

<details><summary>Reveal Answer</summary>**B.** Types outside models.</details>

### Question 6 — Hard
**Why use serialization aliases?**
- A) Style
- B) JSON field names can differ from Python attributes (e.g. camelCase vs snake_case)
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Wire vs code naming.</details>

### Question 7 — Hard
**What is a common validator pitfall?**
- A) Using types
- B) Mutating input in place instead of returning a validated value
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Return, do not mutate.</details>

### Question 8 — Hard
**Why prefer `Field` constraints over hand-written checks?**
- A) Style
- B) They are declarative, documented, and consistently enforced
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Declarative validation.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You use Pydantic v2 deeply. |
| 5-6 | Review validators and aliases. |
| < 5 | Re-read the lecture. |
