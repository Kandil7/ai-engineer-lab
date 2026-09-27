# Data Engineering 05: Deduplication — Quiz

> **Topic Overview**: Exact and content-based deduplication, edit detection,
> and the two-half dedup test.

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

**Why do duplicates corrupt retrieval?**

- A) They slow queries
- B) They split relevance and pollute citations
- C) They use storage
- D) They break the schema

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A passage indexed twice splits its relevance across rows and pollutes citation attribution.

</details>

---

### Question 2 — Easy

**What is the exact-dedup tool?**

- A) Content hash
- B) Stable key (passage_id)
- C) Timestamp
- D) Random id

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Two rows with the same stable key are the same passage.

</details>

---

### Question 3 — Easy

**What does a content hash detect?**

- A) Near-duplicates
- B) Exact duplicates and edited pages
- C) Schema violations
- D) Slow queries

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Identical content maps to the same hash; changed content changes the hash.

</details>

---

### Question 4 — Medium

**When does key-based dedup miss a duplicate?**

- A) When the key is stable
- B) When the same content arrives under different keys
- C) When content is identical
- D) When the key is unique

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Re-ingested content under a different key escapes key-based dedup; content hashing catches it.

</details>

---

### Question 5 — Medium

**What is the roadmap's "a single edited page is detected" check?**

- A) Key comparison
- B) Same key, different content hash
- C) Length comparison
- D) Timestamp comparison

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: An edited page keeps its key but its content hash changes — that is the detection signal.

</details>

---

### Question 6 — Medium

**How should near-duplicates be handled?**

- A) Automatic delete
- B) A human review queue
- C) Ignored
- D) Merged blindly

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Near-dedup risks deleting distinct content; a human decides true redundancy.

</details>

---

### Question 7 — Medium

**Which dedup is cheaper?**

- A) Cleanup
- B) Ingest-time
- C) Near-dedup
- D) Manual

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Ingest-time dedup prevents duplicates from existing; cleanup repairs them after the fact.

</details>

---

### Question 8 — Hard

**What are the two halves of the dedup test?**

- A) Fast and slow
- B) Duplicates removed AND distinct passages kept
- C) Exact and fuzzy
- D) Ingest and cleanup

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The test proves duplicates are removed and distinct content survives — the second half catches over-aggressive dedup.

</details>

---

### Question 9 — Hard

**Why is automatic near-dedup risky?**

- A) It is slow
- B) It can delete distinct passages that merely look similar
- C) It needs a key
- D) It duplicates

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Similarity-based auto-delete can remove genuinely distinct content; humans judge true redundancy.

</details>

---

### Question 10 — Hard

**What is the correct dedup strategy for Athar?**

- A) Cleanup only
- B) Ingest-time upsert by key plus content-hash edit detection
- C) Near-dedup auto-delete
- D) No dedup

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Upsert by passage_id prevents duplicates; content hashing detects edited pages for re-indexing.

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
| 9-10 | Expert | Ready for provenance |
| 7-8 | Proficient | Review content hashing |
| 5-6 | Developing | Re-study the two halves |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [04 - Checkpointing](04-checkpointing-quiz.md) | **Next**: [06 - Provenance](06-provenance-versioning-quiz.md)