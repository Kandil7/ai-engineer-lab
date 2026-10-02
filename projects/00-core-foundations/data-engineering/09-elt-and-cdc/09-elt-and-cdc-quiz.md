# Data Engineering 09: ETL vs ELT and CDC — Quiz

> **Topic Overview**: ETL vs ELT, transform-late, Change Data Capture, Debezium
> and Flink CDC, applying change records downstream.

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

**What does ELT stand for?**

- A) Extract, Load, Transform
- B) Extract, Transform, Load
- C) Evaluate, Load, Test
- D) Encode, Load, Transform

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: ELT extracts, loads raw into the destination, then transforms inside the warehouse.

</details>

---

### Question 2 — Easy

**What does CDC stand for?**

- A) Change Data Capture
- B) Central Data Cache
- C) Column Data Compression
- D) Continuous Data Compute

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: CDC captures row-level insert/update/delete events from a transactional source.

</details>

---

### Question 3 — Easy

**What is the main advantage of ELT over ETL?**

- A) It needs less storage
- B) Raw data is kept, so the transform can be re-run without re-reading the source
- C) It runs faster in every case
- D) It does not need a warehouse

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Keeping the raw layer makes re-transformation possible, at the cost of storage.

</details>

---

### Question 4 — Medium

**Why can query-based CDC not reliably capture deletes?**

- A) Deletes have no updated_at timestamp to poll
- B) Deletes are too fast
- C) Deletes are rare
- D) Deletes happen in another table

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Polling `WHERE updated_at > ?` sees inserts and updates but not removed rows.

</details>

---

### Question 5 — Medium

**What does log-based CDC read?**

- A) The table's indexes
- B) The database's write-ahead log (binlog/WAL)
- C) A nightly snapshot
- D) The application's logs

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Reading the database's own log sees every change exactly once, in order, including deletes.

</details>

---

### Question 6 — Medium

**Which tool reads a database's binlog and publishes change records to Kafka?**

- A) Apache Spark
- B) Debezium
- C) Airflow
- D) Great Expectations

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Debezium is the log-based CDC connector that publishes binlog/WAL changes to Kafka.

</details>

---

### Question 7 — Medium

**What does Flink CDC add over Debezium alone?**

- A) Query-based polling
- B) A processing engine for stateful aggregation and exactly-once sinks
- C) A columnar storage format
- D) A scheduler

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Flink CDC combines Debezium's capture connectors with Flink's stream-processing engine.

</details>

---

### Question 8 — Hard

**What is the before image in a change record used for?**

- A) To compress the record
- B) To apply deletes and some updates
- C) To sort the log
- D) To identify the partition

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A delete needs the prior row key (before image); without it the downstream key is unknown.

</details>

---

### Question 9 — Hard

**Why must changes for one row apply in log order?**

- A) To save space
- B) A stale update could overwrite a newer one
- C) To match the batch schedule
- D) To satisfy SQL constraints

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Ordering per key preserves correctness; reordering the same key risks applying stale state.

</details>

---

### Question 10 — Hard

**Why is an upsert-based CDC sink safe to replay?**

- A) It is naturally idempotent: the operation, not the count, determines the state
- B) It drops duplicates automatically
- C) It is backed up
- D) It uses exactly-once checkpoints only

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Replaying an upsert leaves the same state, which is the idempotency principle from topic 03.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | A | Easy |
| 2 | A | Easy |
| 3 | B | Easy |
| 4 | A | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Hard |
| 9 | B | Hard |
| 10 | A | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for the lakehouse |
| 7-8 | Proficient | Review CDC record shape |
| 5-6 | Developing | Re-study ELT vs ETL |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [10 - Lakehouse: Iceberg and Delta Lake](../10-lakehouse/10-lakehouse-quiz.md)
