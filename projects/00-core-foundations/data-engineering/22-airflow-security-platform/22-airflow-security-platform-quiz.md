# Data Engineering 22: Airflow Security and Platform — Quiz

> **Topic Overview**: Security model (auth manager, RBAC, multi-team), secrets
> backends, lineage and listeners, plugins, object storage and state stores,
> installation and upgrades, UI, best practices, and troubleshooting.

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

**What is the Dag-file trust boundary?**

- A) Dag files are read-only in production
- B) Dag files execute arbitrary Python with scheduler privileges
- C) Dag files are encrypted at rest
- D) Dag files cannot import modules

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The dag processor executes Dag files as Python, so write access to the bundle is production access.

</details>

---

### Question 2 — Easy

**Where should production credentials live?**

- A) In the Dag file
- B) In an environment variable baked into the image
- C) In a secrets backend or connection
- D) In a committed config file

<details>
<summary>Reveal Answer</summary>

**Correct Answer: C**

**Explanation**: Connections encrypt at rest in the metadata DB; secrets backends move credentials out entirely. The other options leak secrets.

</details>

---

### Question 3 — Easy

**What does a listener do?**

- A) Executes tasks
- B) Hooks Airflow lifecycle events for audit, metrics, notifications
- C) Stores large data
- D) Parses Dag files

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Listeners hook DagRun, task instance, asset, and import-error events, integrating with audit and notification systems.

</details>

---

### Question 4 — Medium

**When is multi-team mode worth the overhead?**

- A) Always, for any deployment
- B) When distinct teams share one instance but must not see or exhaust each other's resources
- C) Only for single-user laptops
- D) Never; use separate instances instead

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Multi-team scopes bundles, pools, executor config, and asset events per team; for one team it is pure overhead.

</details>

---

### Question 5 — Medium

**Why install Airflow with a constraints file?**

- A) It speeds up installation
- B) It pins transitive dependencies for a given Airflow and Python version
- C) It encrypts the install
- D) It skips tests

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Installing without constraints is the most common cause of an unimportable Airflow due to dependency conflicts.

</details>

---

### Question 6 — Medium

**What belongs in object storage versus the task state store?**

- A) Data in the state store, coordination in object storage
- B) Data in object storage, coordination state in the state store
- C) Both in XCom
- D) Both in the metadata DB

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Object storage carries data (passages, artifacts); the task/asset state store carries coordination state that must survive a worker restart.

</details>

---

### Question 7 — Medium

**What is the cheapest way to catch a broken Dag file before the scheduler does?**

- A) A listener for Dag import errors
- B) A pool with one slot
- C) A retry policy
- D) A SLA

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: A listener on Dag import errors surfaces the failure immediately instead of waiting for the next scheduled run to be missed.

</details>

---

### Question 8 — Hard

**Why must production upgrades be rehearsed on staging?**

- A) Staging is cheaper
- B) Database migrations run on upgrade and must be planned
- C) The UI changes
- D) Constraints files differ

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Live upgrades include database migrations; rehearsing on staging surfaces migration issues before production.

</details>

---

### Question 9 — Hard

**What is the difference between lineage and a listener?**

- A) None; synonyms
- B) Lineage captures data provenance; listeners hook operational events
- C) Lineage is faster
- D) Listeners store data

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Lineage answers "which Dag produced this dataset"; listeners answer "what happened in Airflow". Use both.

</details>

---

### Question 10 — Hard

**Why is tracking "latest" Airflow in production unsafe?**

- A) Latest is slower
- B) Internals change between releases; only the public interface survives
- C) Latest lacks features
- D) Latest is not open source

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Code depending on internals breaks on upgrade; pin the version and constraints, and build against the public interface.

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
| 7 | A | Medium |
| 8 | B | Hard |
| 9 | B | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for the data-engineering capstone |
| 7-8 | Proficient | Review secrets and plugins |
| 5-6 | Developing | Re-study the platform layer |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [21 - Airflow Advanced Authoring](../21-airflow-advanced-authoring/21-airflow-advanced-authoring-quiz.md)
