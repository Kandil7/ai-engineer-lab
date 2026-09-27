# PostgreSQL 03: Migrations — Quiz

> **Topic Overview**: Sequential versions, idempotency, and rollback.

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

**What is a migration?**

- A) A cache
- B) A versioned, ordered schema change
- C) A query
- D) A connection

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The number is the version; the order is the history.

</details>

---

### Question 2 — Easy

**Migrations are applied:**

- A) In any order
- B) In order
- C) Randomly
- D) Never

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The order is the history.

</details>

---

### Question 3 — Easy

**An idempotent migration:**

- A) Fails on re-run
- B) Is safe to run twice
- C) Deletes data
- D) Caches data

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: IF NOT EXISTS makes it safe.

</details>

---

### Question 4 — Medium

**Every migration has:**

- A) A cache
- B) A rollback
- C) A query
- D) A connection

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The down migration reverses the change.

</details>

---

### Question 5 — Medium

**An applied migration is:**

- A) Editable
- B) Never edited or reordered
- C) Deleted
- D) Cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The schema's history is immutable.

</details>

---

### Question 6 — Medium

**Migrations are tested against:**

- A) Production
- B) A fresh database
- C) The cache
- D) Nothing

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A failure on a fresh database will hit production.

</details>

---

### Question 7 — Medium

**A bad migration is:**

- A) Patched forward
- B) Rolled back
- C) Cached
- D) Ignored

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The rollback is the escape hatch.

</details>

---

### Question 8 — Hard

**A migration should be:**

- A) Large and broad
- B) Small and focused
- C) Cached
- D) Optional

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: One change per migration.

</details>

---

### Question 9 — Hard

**Non-idempotent migrations fail when:**

- A) The table is empty
- B) The table already exists
- C) The cache is cold
- D) The connection drops

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Re-running creates a duplicate.

</details>

---

### Question 10 — Hard**

**The roadmap's rule for migrations is:**

- A) Reorder freely
- B) Never reorder after application
- C) Edit applied ones
- D) Skip rollbacks

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The history is immutable.

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
| 9-10 | Expert | Ready for connection pooling |
| 7-8 | Proficient | Review rollback |
| 5-6 | Developing | Re-study idempotency |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [02 - Indexes](02-indexes-queries-quiz.md) | **Next**: [04 - Connection Pooling](04-connection-pooling-quiz.md)