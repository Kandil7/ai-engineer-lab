# Data Engineering 19: DAG Orchestration — Quiz

> **Topic Overview**: The Dag model, TaskFlow, sensors, XCom, variables and params,
> connections, scheduling with cron and assets, catchup and backfill, and testing.

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

**What does a Dag file do when the scheduler parses it?**

- A) Executes every task in order
- B) Builds the workflow model, executes nothing
- C) Runs only the first task
- D) Starts a Dag run

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A Dag file is a definition, not a program. Parsing builds the model; the scheduler decides what runs and when.

</details>

---

### Question 2 — Easy

**What does the TaskFlow `@task` decorator do?**

- A) Runs the function immediately at parse time
- B) Turns a plain function into a task with inferred dependencies
- C) Replaces operators entirely
- D) Stores the function in the UI

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: TaskFlow turns functions into tasks, infers dependencies from argument passing, and makes the function testable with pytest.

</details>

---

### Question 3 — Easy

**What is a Dag run?**

- A) One execution of a Dag over one interval
- B) The Dag file itself
- C) A single task
- D) A backfill only

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Each schedule interval gets a Dag run with its own state, logs, and logical date.

</details>

---

### Question 4 — Medium

**What belongs in XCom?**

- A) The transformed passages dataframe
- B) Small metadata: a row count or an index path
- C) The raw book corpus
- D) Credentials

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: XCom lives in the metadata database and is metadata only; large data flows through storage with the reference in XCom.

</details>

---

### Question 5 — Medium

**A sensor waits three hours for a file. Which mode costs no worker slot while waiting?**

- A) Poke
- B) Reschedule
- C) Deferrable
- D) Stream

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: A deferrable sensor suspends the task; the triggerer watches the condition, holding no worker slot.

</details>

---

### Question 6 — Medium

**What is the difference between a variable and a param?**

- A) None; synonyms
- B) Variables configure the deployment, params configure the run
- C) Params configure the deployment, variables configure the run
- D) Variables are only for connections

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Variables are global deployment configuration; params are passed per Dag run at trigger time, optionally schema-validated.

</details>

---

### Question 7 — Medium

**Why is `catchup=False` right for DevMate's repo-ingest Dag?**

- A) Catchup is deprecated
- B) Re-ingesting old repo snapshots adds nothing; the latest state is the value
- C) Catchup breaks cron
- D) The Dag is too small

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Catchup replays missed intervals. For an invoice pipeline each interval is real money; for a repo re-ingest, only the latest state matters.

</details>

---

### Question 8 — Hard

**An asset-scheduled Dag runs when...**

- A) The clock hits the cron time
- B) The upstream asset emits an update event
- C) The user clicks trigger
- D) The worker is idle

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Assets state the data dependency in code: the Dag runs when the producer emits the asset event, regardless of wall-clock time.

</details>

---

### Question 9 — Hard

**Backfilling a non-idempotent ingest three times yields...**

- A) Three identical results
- B) One result, two runs skipped
- C) Tripled data
- D) A parse error

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: Backfill is safe only on an idempotent pipeline; otherwise each replay duplicates the data. Idempotency (topic 03) is the precondition.

</details>

---

### Question 10 — Hard

**What is the cheapest Dag bug to catch in CI?**

- A) A slow task
- B) A wrong row count
- C) An import error that breaks parsing
- D) A lost XCom

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: A Dag file that fails to parse fails every future run, so import errors are caught in CI before any 3 a.m. run can see them.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | A | Easy |
| 4 | B | Medium |
| 5 | C | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Hard |
| 9 | C | Hard |
| 10 | C | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for execution and operations (topic 20) |
| 7-8 | Proficient | Review scheduling and catchup |
| 5-6 | Developing | Re-study the Dag model |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [20 - Airflow Execution and Operations](../20-airflow-execution/20-airflow-execution-quiz.md)
