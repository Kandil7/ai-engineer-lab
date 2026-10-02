# Data Engineering 10: Lakehouse — Iceberg and Delta Lake — Quiz

> **Topic Overview**: Lake vs warehouse vs lakehouse, table formats, ACID,
> time travel, Iceberg vs Delta Lake, schema and partition evolution.

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

**What does a table format add to a directory of bare Parquet files?**

- A) More compression
- B) Metadata, ACID transactions, and time travel
- C) Faster networking
- D) A second copy of the data

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The table format is a metadata layer that turns files into a versioned, transactional table.

</details>

---

### Question 2 — Easy

**Which two table formats are the leading lakehouse options?**

- A) Parquet and ORC
- B) Iceberg and Delta Lake
- C) Kafka and Flink
- D) PostgreSQL and MySQL

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Iceberg and Delta Lake are the table formats; Parquet and ORC are file formats.

</details>

---

### Question 3 — Easy

**What is time travel in a lakehouse table?**

- A) Reading data in the future
- B) Querying the table at a past snapshot
- C) Moving data between clusters
- D) Replaying a log

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Every write is a retained snapshot, so any past state remains queryable.

</details>

---

### Question 4 — Medium

**What is the defining feature of Iceberg's hidden partitioning?**

- A) It hides the data entirely
- B) The physical layout is decoupled from the logical partition column
- C) It removes the need for indexes
- D) It encrypts partitions

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Queries use the logical column while the metadata maps it to the physical layout.

</details>

---

### Question 5 — Medium

**How does Delta Lake record what changed?**

- A) In a `_delta_log` of ordered JSON commits
- B) In a single manifest file
- C) In the database WAL
- D) In a Kafka topic

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Delta Lake appends commits to a JSON transaction log over Parquet data files.

</details>

---

### Question 6 — Medium

**Why does time travel make old citations resolvable?**

- A) It stores citations separately
- B) The snapshot that existed when the passage was written remains queryable
- C) It compresses old data
- D) It blocks new writes

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Old snapshots are not overwritten, so a citation can resolve against its original state.

</details>

---

### Question 7 — Medium

**What does schema evolution let you do without rewriting data?**

- A) Drop columns
- B) Add a column additively
- C) Delete rows
- D) Rename the table

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Adding a column is backward-compatible; old files read the new column as null.

</details>

---

### Question 8 — Hard

**Which is the primary emphasis difference between Iceberg and Delta Lake?**

- A) Iceberg is engine-neutral; Delta Lake is Spark-centric
- B) Iceberg is faster; Delta Lake is cheaper
- C) Iceberg is for streaming; Delta Lake is for batch
- D) There is no difference

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Iceberg targets multi-engine reads and partition evolution; Delta Lake is deeply integrated with Spark.

</details>

---

### Question 9 — Hard

**Why is editing a data file in place a mistake in a lakehouse?**

- A) It costs more
- B) It breaks every snapshot that referenced that file
- C) It requires a schema change
- D) It is slower than appending

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Snapshots reference files immutably; mutating a file corrupts the history that references it.

</details>

---

### Question 10 — Hard

**How does a lakehouse turn a re-ingest into a transaction?**

- A) It locks the database
- B) Each write commits a new snapshot atomically; readers see old or new, never partial
- C) It batches all writes monthly
- D) It copies the whole table

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: ACID semantics mean a re-ingest either commits or does not; no partial snapshot is visible.

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
| 8 | A | Hard |
| 9 | B | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for data quality frameworks |
| 7-8 | Proficient | Review Iceberg vs Delta |
| 5-6 | Developing | Re-study the table format |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [11 - Data Quality Frameworks](../11-data-quality/11-data-quality-quiz.md)
