# Data Engineering 07: Parquet and Object Storage — Quiz

> **Topic Overview**: Parquet's columnar design, object-storage principles,
> and partition layout.

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

**What is Parquet?**

- A) A row-oriented text format
- B) A columnar, compressed, schema-enforced binary format
- C) A database
- D) A compression algorithm

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Parquet stores data by column, compressed, with the schema enforced at write time.

</details>

---

### Question 2 — Easy

**Why is Parquet faster for analytics than JSONL?**

- A) It is smaller
- B) Reading one column reads only that column's bytes
- C) It is in memory
- D) It has no schema

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Columnar storage means a column read touches only that column's bytes.

</details>

---

### Question 3 — Easy

**When does JSONL win over Parquet?**

- A) Analytics at scale
- B) Streaming append and human inspection
- C) Large corpora
- D) Schema enforcement

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: JSONL is row-oriented text — good for appends and debugging, poor for analytics.

</details>

---

### Question 4 — Medium

**What is the object-storage immutability principle?**

- A) Files can be edited in place
- B) Write once, never edit; a change is a new object
- C) Files are compressed
- D) Files are encrypted

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Immutability means a new version is a new object, enabling versioning and rollback.

</details>

---

### Question 5 — Medium

**What does object-storage versioning enable?**

- A) Faster reads
- B) Rollback to previous snapshots
- C) Smaller storage
- D) Streaming

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The store keeps object history, so a bad change can be rolled back.

</details>

---

### Question 6 — Medium

**What is the correct partition layout for Athar?**

- A) By passage_id
- B) By book_id then source_version
- C) By page
- D) By content hash

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Partitioning by book then version means a query reads exactly one file.

</details>

---

### Question 7 — Medium

**Why is partitioning by high-cardinality keys bad?**

- A) It is slow
- B) It creates too many tiny files
- C) It loses provenance
- D) It duplicates

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Millions of distinct partition values mean thousands of tiny files — inefficient.

</details>

---

### Question 8 — Hard

**What must the Parquet schema carry?**

- A) Only the text
- B) The same provenance fields as JSONL
- C) Only the page number
- D) Only the book_id

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Provenance survives the format change — a Parquet row is as traceable as a JSONL row.

</details>

---

### Question 9 — Hard

**The pragmatic pattern for a corpus pipeline is:**

- A) Parquet for everything
- B) JSONL for pipeline output, Parquet for the queryable corpus
- C) JSONL for everything
- D) Neither

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: JSONL for inspection and debugging; Parquet for the analytics-grade corpus.

</details>

---

### Question 10 — Hard

**What is the storage-level expression of traceability?**

- A) Compression
- B) Partition keys mirroring provenance fields
- C) Encryption
- D) Replication

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The partition layout (book_id/version) mirrors the provenance fields, making traceability structural.

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
| 9-10 | Expert | Stage 5 data engineering complete |
| 7-8 | Proficient | Review partition layout |
| 5-6 | Developing | Re-study Parquet design |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [06 - Provenance](06-provenance-versioning-quiz.md)