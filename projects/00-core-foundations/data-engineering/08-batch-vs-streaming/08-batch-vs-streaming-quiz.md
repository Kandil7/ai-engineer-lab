# Data Engineering 08: Batch vs Streaming — Quiz

> **Topic Overview**: Batch vs streaming decision, orchestrators and engines, Lambda
> and Kappa architectures, ordering and exactly-once.

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

**What two facts decide batch versus streaming?**

- A) Team size and budget
- B) Whether the source is bounded and how fresh the result must be
- C) The programming language and the cloud provider
- D) The number of users and the data size

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The decision follows from whether the source is finite and the consumer's latency need.

</details>

---

### Question 2 — Easy

**Which tool is an orchestrator?**

- A) Apache Spark
- B) Apache Flink
- C) Apache Airflow
- D) Apache Kafka

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: Airflow schedules a task DAG; Spark and Flink are compute engines, Kafka is a broker.

</details>

---

### Question 3 — Easy

**What is a broker's central property?**

- A) It computes aggregates
- B) It holds an ordered, durable, replayable log
- C) It schedules jobs
- D) It stores columnar files

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Kafka, Pulsar, and Kinesis all provide an append-only, ordered, replayable event log.

</details>

---

### Question 4 — Medium

**What is the primary cost of Lambda architecture?**

- A) Extra disk space
- B) Two code paths that must stay in sync
- C) Slower queries
- D) Higher network latency

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The batch view and speed view are two implementations of the same logic that must agree at the seam.

</details>

---

### Question 5 — Medium

**How does Kappa architecture recompute results?**

- A) Re-run a separate batch job
- B) Reset the offset and replay the log
- C) Delete and rebuild the database
- D) Add a second speed layer

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Kappa has one stream path; reprocessing is replaying the log from an earlier offset.

</details>

---

### Question 6 — Medium

**Why is the broker's replayable log the foundation of streaming recovery?**

- A) It compresses events
- B) A job can be rebuilt from zero by replaying history
- C) It guarantees ordering across partitions
- D) It removes the need for checkpoints

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Replayability lets a crashed streaming job rebuild its state from the log.

</details>

---

### Question 7 — Medium

**What does a watermark signal in a streaming engine?**

- A) That the log is full
- B) That no event older than a timestamp will arrive
- C) That a consumer is offline
- D) That exactly-once is enabled

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Watermarks let a window close and emit by promising no older events remain.

</details>

---

### Question 8 — Hard

**Which pair of earlier-lecture properties does streaming still require?**

- A) Deduplication and provenance
- B) Idempotency and checkpointing
- C) Parquet and partitioning
- D) ETL and schemas

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A streaming job without checkpoints cannot resume, and a retry without idempotency double-counts.

</details>

---

### Question 9 — Hard

**Under what condition does Kappa architecture fail?**

- A) When the log does not retain enough history for recomputation
- B) When there are two data sources
- C) When the team is small
- D) When queries are read-heavy

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Kappa relies on replaying the log, so the log must hold the full history any recomputation needs.

</details>

---

### Question 10 — Hard

**For the Athar corpus, which choice is correct and why?**

- A) Streaming, because citations need real-time freshness
- B) Batch, because the corpus is bounded and changes rarely
- C) Kappa, to simplify the architecture
- D) Lambda, to merge freshness and correctness

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Books are finite and change rarely, so a batch trigger is simpler and keeps re-runs safe.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | C | Easy |
| 3 | B | Easy |
| 4 | B | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Hard |
| 9 | A | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for ETL vs ELT and CDC |
| 7-8 | Proficient | Review Lambda vs Kappa |
| 5-6 | Developing | Re-study the tooling split |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [09 - ETL vs ELT and CDC](../09-elt-and-cdc/09-elt-and-cdc-quiz.md)
