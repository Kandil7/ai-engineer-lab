# Data Engineering 15: Storage Systems and Database Selection — Quiz

> **Topic Overview**: Object storage practices, Parquet/ORC/Avro, partitioning,
> database families and the selection rubric, the polyglot principle.

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

**Which format is columnar, compressed, and schema-enforced?**

- A) Avro
- B) Parquet
- C) JSON
- D) CSV

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Parquet is the columnar, compressed, schema-enforced analytics format.

</details>

---

### Question 2 — Easy

**Which format carries its schema with the data and evolves additively?**

- A) Parquet
- B) ORC
- C) Avro
- D) CSV

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: Avro embeds the schema in the data, enabling row-based serialization and schema evolution.

</details>

---

### Question 3 — Easy

**What is PostgreSQL's `pgvector` extension for?**

- A) Graph traversal
- B) Vector search alongside relational metadata
- C) Time-series retention
- D) Document storage

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: `pgvector` adds vector search to Postgres, so one database can hold metadata and embeddings.

</details>

---

### Question 4 — Medium

**Why is partitioning by a high-cardinality key an anti-pattern?**

- A) It is too slow to query
- B) It produces many tiny files, slow to list and wasteful
- C) It loses data
- D) It needs more RAM

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Partitioning per-passage or per-second scatters data into millions of tiny files.

</details>

---

### Question 5 — Medium

**What does data skipping rely on?**

- A) Column min/max and bloom filters to skip files outside the filter range
- B) Dropping unused columns
- C) Reading only headers
- D) Indexing every row

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Per-column statistics let the engine skip files whose value range excludes the filter.

</details>

---

### Question 6 — Medium

**Which database family wins for append-only, time-ordered metrics?**

- A) Graph
- B) Document
- C) Time-series (InfluxDB, TimescaleDB)
- D) Relational

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: Time-series stores are built for timestamp-ordered, range-queried, downsampled metrics.

</details>

---

### Question 7 — Medium

**When should you choose NoSQL over relational?**

- A) When the access pattern is fixed and known (key lookup, write-heavy)
- B) Whenever the data is large
- C) When you need arbitrary joins
- D) When you need ACID everywhere

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: NoSQL pays for its scale with ad-hoc query loss; it wins only when the access pattern is known.

</details>

---

### Question 8 — Hard

**Which query shape tips a dataset from PostgreSQL into Neo4j?**

- A) Aggregations
- B) Multi-hop traversal over relationships
- C) Single-key lookups
- D) Time-range scans

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Graph stores excel at traversal that relational joins handle poorly at depth.

</details>

---

### Question 9 — Hard

**What is the polyglot principle?**

- A) One store for all data
- B) The right store per data shape, chosen by a rubric
- C) Only relational databases
- D) Only NoSQL databases

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Different data types (corpus, vectors, metadata, telemetry, graphs) belong in different stores.

</details>

---

### Question 10 — Hard

**What five questions make up the storage-selection rubric?**

- A) Price, brand, age, size, color
- B) Access pattern, consistency, latency, scale, operational cost
- C) Language, framework, team, budget, deadline
- D) CPU, RAM, disk, network, GPU

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The rubric matches a store to its workload, guarantees, latency, scale, and ops burden.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | C | Easy |
| 3 | B | Easy |
| 4 | B | Medium |
| 5 | A | Medium |
| 6 | C | Medium |
| 7 | A | Medium |
| 8 | B | Hard |
| 9 | B | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Data engineering fundamentals complete |
| 7-8 | Proficient | Review the database families |
| 5-6 | Developing | Re-study the file formats |
| 0-4 | Novice | Restart the lecture |

---

**Back to start**: [01 - ETL Fundamentals](../01-etl-fundamentals/01-etl-fundamentals-quiz.md)
