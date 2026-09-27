# Data Engineering 04: Checkpointing — Quiz

> **Topic Overview**: Durable checkpoints, atomic writes, resume, and the
> checkpoint-plus-idempotency combination.

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

**Why do long pipelines need checkpoints?**

- A) To run faster
- B) So a failure resumes instead of restarting from zero
- C) To save storage
- D) To compress data

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Checkpoints record completed work so a failed run continues from there.

</details>

---

### Question 2 — Easy

**What does a checkpoint record?**

- A) The whole dataset
- B) The position of completed work
- C) The pipeline code
- D) The logs

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A checkpoint answers "what is done?" — the last committed unit.

</details>

---

### Question 3 — Easy

**What is an atomic checkpoint write?**

- A) A fast write
- B) A whole-or-nothing write with no torn records
- C) A compressed write
- D) A logged write

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Atomic means either the whole checkpoint is written or none of it is.

</details>

---

### Question 4 — Medium

**How do you write a checkpoint atomically on most filesystems?**

- A) Append to the file
- B) Write a temp file, then rename
- C) Write twice
- D) Write in place

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Write to a temp file then `os.replace` — atomic on most filesystems.

</details>

---

### Question 5 — Medium

**What is a torn write?**

- A) A slow write
- B) A half-written record from a crash mid-write
- C) A duplicate write
- D) A compressed write

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A crash mid-write leaves a torn record that corrupts the resume position.

</details>

---

### Question 6 — Medium

**What must resume do?**

- A) Redo everything
- B) Continue after the last committed unit
- C) Skip everything
- D) Restart from zero

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Resume continues after the last committed unit — no redoing, no skipping.

</details>

---

### Question 7 — Medium

**Why is a stale checkpoint safe with idempotent loads?**

- A) It is always accurate
- B) Re-processing a committed unit is harmless
- C) It never happens
- D) Idempotency skips everything

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: If the checkpoint is slightly behind, idempotent loads absorb the re-processing.

</details>

---

### Question 8 — Hard

**What is the commit unit?**

- A) The whole job
- B) The smallest unit of completed work a checkpoint records
- C) The pipeline version
- D) The source file

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The commit unit is the granularity of resume — one page, one batch.

</details>

---

### Question 9 — Hard

**What is the risk of appending to a checkpoint file?**

- A) It is slow
- B) A crash mid-append leaves a torn record
- C) It duplicates
- D) It is not durable

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Appending is not atomic; a crash mid-append corrupts the checkpoint.

</details>

---

### Question 10 — Hard

**Checkpointing plus idempotency together enable:**

- A) Faster pipelines
- B) Safe crash-and-resume
- C) Smaller checkpoints
- D) Streaming

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Checkpointing says resume here; idempotency says even a stale resume is safe.

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
| 9-10 | Expert | Ready for deduplication |
| 7-8 | Proficient | Review atomic writes |
| 5-6 | Developing | Re-study resume |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [03 - Idempotency](03-idempotency-quiz.md) | **Next**: [05 - Deduplication](05-deduplication-quiz.md)