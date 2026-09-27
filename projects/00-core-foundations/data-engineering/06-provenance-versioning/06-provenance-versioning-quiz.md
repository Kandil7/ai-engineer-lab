# Data Engineering 06: Provenance and Versioning — Quiz

> **Topic Overview**: Provenance fields, source versioning, tracing, and
> stale-passage detection.

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

**What does provenance answer?**

- A) How fast data loads
- B) Where data came from
- C) How big data is
- D) Who queried it

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Provenance records the origin of every passage.

</details>

---

### Question 2 — Easy

**Which fields make a passage traceable?**

- A) passage_id only
- B) book_id, page, source_version, path
- C) text only
- D) timestamp only

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The provenance fields identify the book, location, source version, and original file.

</details>

---

### Question 3 — Easy

**What does a source version identify?**

- A) The pipeline version
- B) A specific snapshot of the source
- C) The database version
- D) The model version

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A source version identifies a specific snapshot of the source material.

</details>

---

### Question 4 — Medium

**What makes re-ingests attributable?**

- A) Timestamps
- B) Source versioning
- C) Content hashing alone
- D) Random ids

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: New passages carry the new version, so re-ingests are traceable to their snapshot.

</details>

---

### Question 5 — Medium

**How should tracing behave when a link is missing?**

- A) Return a guess
- B) Fail loudly
- C) Skip the passage
- D) Log and continue

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A passage that cannot be traced is an integrity failure — it must fail loudly, never guess.

</details>

---

### Question 6 — Medium

**What is a stale passage?**

- A) An old passage_id
- B) A passage whose source changed but was not refreshed
- C) A slow passage
- D) A duplicate passage

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The source moved to a new version but the passage still carries the old one.

</details>

---

### Question 7 — Medium

**How is a stale passage detected?**

- A) By length
- B) Version comparison or content-hash mismatch
- C) By timestamp
- D) By query count

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: If the passage's version is behind the current source version, it is stale.

</details>

---

### Question 8 — Hard**

**Why is provenance mandatory, not optional?**

- A) It is faster
- B) Optional provenance means untraceable passages exist
- C) It saves storage
- D) It is required by the schema

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: If provenance is optional, some passages cannot be traced — the integrity guarantee is broken.

</details>

---

### Question 9 — Hard

**What does the audit trail enable?**

- A) Faster queries
- B) Stating which source version produced any passage
- C) Smaller storage
- D) Streaming

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Provenance plus versioning lets you state the exact source version behind any passage.

</details>

---

### Question 10 — Hard

**The roadmap exit test "every passage can be traced to its origin" requires:**

- A) Content hashing only
- B) Mandatory provenance fields plus versioned sources
- C) A database index
- D) A log file

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Mandatory provenance fields plus versioned sources make every passage traceable in one lookup.

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
| 9-10 | Expert | Ready for Parquet and storage |
| 7-8 | Proficient | Review tracing |
| 5-6 | Developing | Re-study provenance fields |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [05 - Deduplication](05-deduplication-quiz.md) | **Next**: [07 - Parquet and Object Storage](07-parquet-object-storage-quiz.md)