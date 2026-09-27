# Data Engineering 02: Schemas and Contracts — Quiz

> **Topic Overview**: Schema design, boundary validation, structural
> invariants, and schema evolution.

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

**What does a schema declare?**

- A) Only field names
- B) Field set, types, required fields, and constraints
- C) Only data types
- D) Storage location

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A schema declares the full shape: which fields, their types, what is required, and value constraints.

</details>

---

### Question 2 — Easy

**Where should validation happen?**

- A) Deep inside business logic
- B) At the pipeline boundary
- C) Only in the UI
- D) Never

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Reject bad input where it enters the system so downstream code can assume the contract holds.

</details>

---

### Question 3 — Easy

**What is a structural invariant?**

- A) A runtime check
- B) Invalid state made unrepresentable
- C) A database constraint
- D) A log message

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Structural invariants make invalid states impossible to construct — stronger than runtime checks.

</details>

---

### Question 4 — Medium

**Which schema change is safe for consumers?**

- A) Removing a field
- B) Retyping a field
- C) Adding an optional field
- D) Renaming a field

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: Additive changes (new optional fields) are backward-compatible; removing or retyping breaks consumers.

</details>

---

### Question 5 — Medium

**What does source_version enable?**

- A) Faster queries
- B) Old and new data shapes coexisting
- C) Smaller storage
- D) Streaming

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Version tags let consumers know which shape a row holds and let old and new data coexist.

</details>

---

### Question 6 — Medium

**What is the difference between schema and business validation?**

- A) They are the same
- B) Schema checks shape; business checks meaning
- C) Business checks types
- D) Schema checks meaning

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Schema validation is mechanical (types, required, constraints); business validation is domain logic (page in range, source ownership).

</details>

---

### Question 7 — Medium

**Why is `__post_init__` validation stronger than runtime checks?**

- A) It is faster
- B) The invalid state cannot be constructed at all
- C) It runs less often
- D) It logs better

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Construction-time checks make invalid objects unrepresentable, so no downstream code needs to guard against them.

</details>

---

### Question 8 — Hard

**A Passage with an empty original text should be:**

- A) Allowed, it is optional
- B) Impossible to construct
- C) Fixed at query time
- D) Logged and skipped

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The contract requires non-empty original; the invariant is structural.

</details>

---

### Question 9 — Hard

**What is the correct evolution sequence for a schema change?**

- A) Mutate in place
- B) Add a version, migrate, then retire the old
- C) Delete old data
- D) Rename fields

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Version the schema, migrate data, then retire the old shape — never mutate in place.

</details>

---

### Question 10 — Hard

**Which is a business validation, not a schema validation?**

- A) book_id is non-empty
- B) page is within the book's page count
- C) page is an integer
- D) original is non-empty

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Page-in-range depends on the book's domain facts; the others are mechanical shape checks.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | C | Medium |
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
| 9-10 | Expert | Ready for idempotency |
| 7-8 | Proficient | Review evolution rules |
| 5-6 | Developing | Re-study boundary validation |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [01 - ETL](01-etl-fundamentals-quiz.md) | **Next**: [03 - Idempotency](03-idempotency-quiz.md)