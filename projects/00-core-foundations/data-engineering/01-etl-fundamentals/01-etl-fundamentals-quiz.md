# Data Engineering 01: ETL Fundamentals — Quiz

> **Topic Overview**: Extract, transform, load decomposition, determinism,
> and idempotency.

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

**What does ETL stand for?**

- A) Extract, Transform, Load
- B) Evaluate, Test, Launch
- C) Extract, Test, Log
- D) Encode, Transform, Load

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: ETL is extract, transform, load — the pipeline turning raw source material into queryable data.

</details>

---

### Question 2 — Easy

**What property must the extract stage have?**

- A) Destructive
- B) Read-only and resumable
- C) Idempotent
- D) Streaming

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Extract reads the source without modifying it and can resume from where it stopped.

</details>

---

### Question 3 — Easy

**What makes a pipeline deterministic?**

- A) It runs fast
- B) Identical input produces identical output
- C) It uses timestamps
- D) It streams

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Determinism means no timestamps in output, no unseeded randomness, no iteration-order dependence.

</details>

---

### Question 4 — Medium

**What does idempotency guarantee?**

- A) Faster runs
- B) Re-running leaves identical state
- C) Smaller output
- D) Streaming

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: An idempotent load can run twice and leave the same state — no duplicates.

</details>

---

### Question 5 — Medium

**Which pipeline is right for a finite corpus that changes rarely?**

- A) Stream
- B) Batch
- C) Real-time
- D) Event-driven

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Batch processes bounded chunks on a schedule — right for books that change rarely.

</details>

---

### Question 6 — Medium

**Why does every stage need row counts logged?**

- A) For billing
- B) So failures are attributable to a stage
- C) For storage
- D) For speed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Per-stage counts tell you which stage lost a row when a passage goes missing.

</details>

---

### Question 7 — Medium

**What should the transform stage be?**

- A) Destructive
- B) Pure where possible
- C) Streaming
- D) Random

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Transform applies business logic and should be pure — same input, same output.

</details>

---

### Question 8 — Hard

**What breaks determinism?**

- A) Fixed seeds
- B) Timestamps in output
- C) Sorted iteration
- D) Pure functions

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Timestamps in output make re-runs differ — the pipeline is no longer a function.

</details>

---

### Question 9 — Hard

**The roadmap exit test requires "running twice does not duplicate data." Which property delivers that?**

- A) Determinism alone
- B) Idempotent load
- C) Streaming
- D) Observability

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: An idempotent load upserts by key, so a second run updates instead of duplicating.

</details>

---

### Question 10 — Hard

**What is the correct order of the Athar pipeline stages?**

- A) Load, transform, extract
- B) Extract pages, transform to passages, load with provenance
- C) Transform, extract, load
- D) Load, extract, transform

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Read pages, apply cleaning and normalization, then write passages with book_id/page/source_version.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | A | Easy |
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
| 9-10 | Expert | Ready for schemas and contracts |
| 7-8 | Proficient | Review idempotency |
| 5-6 | Developing | Re-study the stages |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [02 - Schemas and Contracts](02-schemas-and-contracts-quiz.md)