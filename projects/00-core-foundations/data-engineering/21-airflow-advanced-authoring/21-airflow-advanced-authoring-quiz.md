# Data Engineering 21: Airflow Advanced Authoring — Quiz

> **Topic Overview**: Dynamic task mapping, loops and task groups, assets and
> asset-aware scheduling, timetables and event-driven scheduling, deferrable
> operators, params schemas, serialization, and non-Python authoring.

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

**What does `.expand()` do?**

- A) Parses the Dag file faster
- B) Creates one task instance per item in a runtime list
- C) Compiles the Dag to SQL
- D) Deletes duplicate tasks

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Dynamic task mapping fans out at runtime from upstream data; the count is decided when the upstream task runs, not at parse time.

</details>

---

### Question 2 — Easy

**What does `.collect()` do?**

- A) Removes failed tasks
- B) Gathers mapped results into a list for a downstream task
- C) Cancels the run
- D) Stores results in XCom only

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: `.collect()` turns the mapped instances' outputs into a single list that the next task receives as one argument.

</details>

---

### Question 3 — Easy

**What is an asset in Airflow 3?**

- A) A file on disk
- B) A typed dataset with a URI that triggers scheduling
- C) A connection credential
- D) A pool slot

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Assets are typed datasets with URIs; producers emit events and consumer Dags schedule on them, stating the data dependency in code.

</details>

---

### Question 4 — Medium

**When should you schedule on an asset instead of cron?**

- A) Always
- B) When the real trigger is "the data changed"
- C) Never; cron is always better
- D) Only for streaming

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Cron is for "every Tuesday at 03:00"; assets are for "when the data updates". Mixing both (daily fallback plus asset trigger) is common and supported.

</details>

---

### Question 5 — Medium

**What is the difference between `mode='reschedule'` and deferrable?**

- A) None
- B) Reschedule releases the slot between pokes; deferrable suspends and uses the triggerer
- C) Deferrable is deprecated
- D) Reschedule is faster always

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Reschedule suits short waits with frequent checks; deferrable suits long waits and needs the triggerer running and monitored.

</details>

---

### Question 6 — Medium

**What does a params JSON schema buy you?**

- A) Faster parsing
- B) Validation at trigger time and an optional trigger UI form
- C) Encryption
- D) Automatic retries

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A schema validates trigger params (e.g. backfill days 1..30) and can render a form in the UI, preventing bad triggers.

</details>

---

### Question 7 — Medium

**Why must parse-time code in a dynamic Dag be cheap and deterministic?**

- A) It runs on every scheduler cycle
- B) It runs only once
- C) It is cached forever
- D) It uses the network

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: Dynamic Dags are generated at parse time, and parsing happens on every scheduler cycle, so expensive or nondeterministic code multiplies and drifts.

</details>

---

### Question 8 — Hard

**Mapping a single heavy task 500 times without pools leads to...**

- A) Better throughput
- B) A backfill hazard that saturates downstream systems
- C) Automatic retries
- D) Smaller logs

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Fan-out amplifies load; without pools and max_active_tis_per_dag, a backfill can overwhelm Qdrant or the LLM endpoint.

</details>

---

### Question 9 — Hard

**What breaks if an XCom value is not serializable?**

- A) The Dag file fails to parse
- B) It fails at the task boundary at runtime
- C) It is stored in plain text
- D) Nothing; Airflow serializes everything

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Serialization happens when the value crosses a process boundary, so a non-serializable value fails at runtime, not at authoring time.

</details>

---

### Question 10 — Hard

**When are YAML Dags a good fit?**

- A) Complex logic with dynamic generation
- B) Simple, stable pipelines owned by non-Python teams
- C) GPU-heavy ML training
- D) Anything requiring unit tests

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: YAML Dags are declarative and suit simple, stable pipelines; Python Dags win when logic, testing, or dynamic generation matters.

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
| 7 | A | Medium |
| 8 | B | Hard |
| 9 | B | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for Airflow security and platform (topic 22) |
| 7-8 | Proficient | Review assets and dynamic mapping |
| 5-6 | Developing | Re-study the authoring surface |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [22 - Airflow Security and Platform](../22-airflow-security-platform/22-airflow-security-platform-quiz.md)
