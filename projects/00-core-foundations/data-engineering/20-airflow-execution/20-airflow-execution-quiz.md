# Data Engineering 20: Airflow Execution and Operations — Quiz

> **Topic Overview**: Architecture and components, executors, concurrency (pools,
> parallelism, priorities), retries/timeout/SLA, deferrable operators, production
> deployment and monitoring, security, and the Airflow 3 deltas.

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

**Where does Airflow keep all its state?**

- A) In the scheduler's memory
- B) In the metadata database
- C) In the Dag files
- D) In the workers

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Every Dag run, task instance, and XCom is a row in the metadata database, which is why components can restart without losing state.

</details>

---

### Question 2 — Easy

**Which executor gives each task its own pod?**

- A) LocalExecutor
- B) CeleryExecutor
- C) KubernetesExecutor
- D) SequentialExecutor

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: KubernetesExecutor runs each task instance in its own pod with its own image and resources, for maximum isolation.

</details>

---

### Question 3 — Easy

**What parses Dag files into the metadata database?**

- A) The scheduler itself, inline
- B) The dag processor
- C) The triggerer
- D) The workers

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The dag processor parses Dag files into serialized form in the database, decoupling parsing from scheduling.

</details>

---

### Question 4 — Medium

**What protects Qdrant from a fifty-task backfill?**

- A) parallelism
- B) A pool with limited slots
- C) Priority weights
- D) SLA

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A pool is a named slot limit shared across Dags; it throttles how many tasks may touch the resource at once, whatever Dag they belong to.

</details>

---

### Question 5 — Medium

**Why pair every retry with an execution_timeout?**

- A) Retries need logs
- B) A task that can hang must not retry into another indefinite hang
- C) Timeouts speed up retries
- D) The UI requires both

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Without a timeout, one hung call holds a worker slot forever; a retry without a timeout just queues a second indefinite hold.

</details>

---

### Question 6 — Medium

**Retries should be zero on tasks whose failures are...**

- A) Network blips
- B) Service warm-ups
- C) Logic bugs
- D) Timeouts

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: A retry on a logic error re-executes the same bug; zero retries makes the crash immediate and attributable.

</details>

---

### Question 7 — Medium

**What is an SLA?**

- A) A retry policy
- B) A deadline alert, separate from task failure
- C) A pool limit
- D) A Dag version

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: An SLA fires when a task misses its deadline even if it eventually succeeds; late-but-successful is still an operational event.

</details>

---

### Question 8 — Hard

**The triggerer dies. What happens?**

- A) All tasks fail immediately
- B) Nothing; workers take over
- C) Deferred tasks stall silently
- D) The scheduler restarts it

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: Deferrable tasks hand their wait conditions to the triggerer; if it dies, they stall quietly, which is why it needs scheduler-grade monitoring.

</details>

---

### Question 9 — Hard

**Why is SQLite wrong as a production metadata database?**

- A) It cannot store XComs
- B) It cannot take concurrent scheduler writes
- C) It has no encryption
- D) It is not open source

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Production runs multiple concurrent components writing state; SQLite's write model cannot sustain that, so Postgres is the standard.

</details>

---

### Question 10 — Hard

**What makes Dag-file write access equivalent to production access?**

- A) Dags are stored encrypted
- B) Dag files execute arbitrary Python with scheduler privileges
- C) The UI renders Dag code
- D) Dags are versioned

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The dag processor executes Dag files as Python; whoever can write them runs code with the scheduler's privileges, so access is gated like a deploy.

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
| 6 | C | Medium |
| 7 | B | Medium |
| 8 | C | Hard |
| 9 | B | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for the data-engineering capstone |
| 7-8 | Proficient | Review pools and failure semantics |
| 5-6 | Developing | Re-study the architecture |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [19 - DAG Orchestration](../19-dag-orchestration/19-dag-orchestration-quiz.md)
