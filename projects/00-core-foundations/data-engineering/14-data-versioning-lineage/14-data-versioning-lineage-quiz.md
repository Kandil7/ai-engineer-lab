# Data Engineering 14: Data Versioning and Lineage — Quiz

> **Topic Overview**: Data versioning, DVC, data catalogs, column-level lineage,
> impact analysis, audit trails.

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

**What does DVC store in Git?**

- A) The full data bytes
- B) Hashes and pointer files
- C) Nothing
- D) The database

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: DVC stores small pointer files with hashes in Git; the data bytes live in remote storage.

</details>

---

### Question 2 — Easy

**What property does a content hash give reproducibility?**

- A) Faster downloads
- B) It changes exactly when the data changes
- C) Smaller files
- D) Better compression

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Two files with the same hash are the same data, making "which version" checkable.

</details>

---

### Question 3 — Easy

**What is lineage?**

- A) A log of errors
- B) A directed graph of "derived from" edges across data assets
- C) A list of tables
- D) A schedule

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Lineage records how data flows from source to derived tables, features, and models.

</details>

---

### Question 4 — Medium

**What does `dvc repro` do?**

- A) Deletes old data
- B) Re-runs only the stages whose inputs changed
- C) Backs up the repo
- D) Uploads data to S3

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Using hashes and the dependency graph, DVC recomputes only what an input change affected.

</details>

---

### Question 5 — Medium

**What is the primary difference between Amundsen and DataHub?**

- A) Amundsen is discovery-first; DataHub is a metadata graph with queryable lineage
- B) DataHub is discovery-first; Amundsen is a notebook
- C) They are the same tool
- D) Amundsen is for streaming only

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Amundsen emphasizes search and discovery; DataHub models metadata as a graph where lineage is a first-class edge.

</details>

---

### Question 6 — Medium

**Why is column-level lineage more useful than table-level?**

- A) It is smaller
- B) It scopes impact to the columns that actually changed, avoiding full recomputes
- C) It is faster to compute
- D) It needs less storage

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: If only `original` changes, column-level lineage flags `searchable` and its embedding, not the whole table.

</details>

---

### Question 7 — Medium

**What does impact analysis answer?**

- A) Where data came from
- B) Which downstream nodes a change affects
- C) How fast a pipeline is
- D) Who owns a table

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Impact analysis traverses lineage forward from a change to the affected downstream set.

</details>

---

### Question 8 — Hard

**Which of the roadmap's "catalog tools" is miscategorized?**

- A) Amundsen
- B) DataHub
- C) Marimo — it is a reactive notebook, not a catalog
- D) None of them

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: Marimo is a reactive Python notebook; a catalog is for discovery and lineage, a notebook for computation.

</details>

---

### Question 9 — Hard

**What do provenance, content hashing, and the audit trail compose into?**

- A) Faster queries
- B) Complete traceability: origin, verifiability, and attributable history
- C) A smaller database
- D) A caching layer

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Provenance names the origin, hashing makes it checkable, and the audit trail makes changes attributable.

</details>

---

### Question 10 — Hard

**Why is storing data directly in Git a mistake?**

- A) Git has no hashing
- B) Data is large and mutable; versioning data and code are different jobs
- C) Git cannot compress
- D) Git is too slow for text

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Large, mutable datasets bloat the repo; DVC keeps pointers in Git and bytes in remote storage.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Medium |
| 5 | A | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | C | Hard |
| 9 | B | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for storage and databases |
| 7-8 | Proficient | Review impact analysis |
| 5-6 | Developing | Re-study lineage granularity |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [15 - Storage Systems and Database Selection](../15-storage-and-databases/15-storage-and-databases-quiz.md)
