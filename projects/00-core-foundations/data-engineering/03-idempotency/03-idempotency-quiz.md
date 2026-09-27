# Data Engineering 03: Idempotency — Quiz

> **Topic Overview**: Idempotent writes, stable keys, the upsert pattern,
> and the run-twice test.

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

**What does idempotency mean?**

- A) Running once is enough
- B) Twice equals once
- C) Running is fast
- D) Data is compressed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: An idempotent operation applied twice has the same effect as applied once.

</details>

---

### Question 2 — Easy

**Which write is NOT idempotent?**

- A) Upsert
- B) Blind insert
- C) Delete-then-insert
- D) Update by key

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A blind insert duplicates on re-run; the others leave identical state.

</details>

---

### Question 3 — Easy

**What does an upsert do?**

- A) Insert always
- B) Insert if absent, update if present
- C) Delete always
- D) Skip always

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The upsert is the idempotent write primitive, keyed by a stable identifier.

</details>

---

### Question 4 — Medium

**What makes a good stable key?**

- A) Content-derived hash
- B) The same logical row maps to the same key every run
- C) A timestamp
- D) A random id

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The key must identify the same logical row across runs. Content hashes change when text changes.

</details>

---

### Question 5 — Medium

**Why is a content-derived key wrong for upserts?**

- A) It is too long
- B) It changes when the text changes, so the row gets a new identity
- C) It is slow
- D) It is not unique

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A content hash changes with the content, so an edited passage becomes a "new" row instead of updating in place.

</details>

---

### Question 6 — Medium

**What is the risk of delete-then-insert?**

- A) Duplicates
- B) A window where data is missing if the insert fails
- C) Slower reads
- D) Larger storage

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Delete-then-insert is idempotent but risks missing data between the delete and the insert.

</details>

---

### Question 7 — Medium

**How do you test idempotency?**

- A) Run once, check output
- B) Run twice, assert identical state
- C) Check the logs
- D) Measure speed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The run-twice test asserts identical state — the roadmap's exact exit criterion.

</details>

---

### Question 8 — Hard

**What is the difference between idempotent and retry-safe?**

- A) They are identical
- B) Retry-safe may still duplicate if the first attempt succeeded before the failure was reported
- C) Idempotent is faster
- D) Retry-safe needs no key

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Idempotency closes the retry gap: the retry is safe because the operation itself is repeatable.

</details>

---

### Question 9 — Hard

**For Athar, what is the stable key for a passage?**

- A) The page text hash
- B) passage_id (book_id:page:index)
- C) The book title
- D) The file path

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: passage_id identifies the same logical passage across runs, enabling idempotent upserts.

</details>

---

### Question 10 — Hard

**An edited passage re-run should:**

- A) Create a new row
- B) Update the existing row in place
- C) Be skipped
- D) Delete the old row

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The upsert updates the existing row by its stable key — no duplication, no orphan.

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
| 9-10 | Expert | Ready for checkpointing |
| 7-8 | Proficient | Review stable keys |
| 5-6 | Developing | Re-study the upsert |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [02 - Schemas](02-schemas-and-contracts-quiz.md) | **Next**: [04 - Checkpointing](04-checkpointing-quiz.md)