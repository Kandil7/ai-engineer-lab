# PostgreSQL 01: Schema Design — Quiz

> **Topic Overview**: Tables, keys, constraints, and referential integrity.

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

**What is a schema?**

- A) A cache
- B) The contract between app and data
- C) A query
- D) A connection

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tables, types, constraints, and relationships.

</details>

---

### Question 2 — Easy

**What does a primary key do?**

- A) Links tables
- B) Identifies a row uniquely
- C) Caches rows
- D) Deletes rows

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The primary key is the anchor of every reference.

</details>

---

### Question 3 — Easy

**What does a foreign key do?**

- A) Identifies a row
- B) Links rows across tables
- C) Caches rows
- D) Deletes rows

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: A foreign key references a row in another table.

</details>

---

### Question 4 — Medium

**Referential integrity means:**

- A) Rows can be orphaned
- B) No row references a nonexistent row
- C) Rows are cached
- D) Rows are deleted

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Foreign keys enforce it.

</details>

---

### Question 5 — Medium

**Constraints should live:**

- A) Only in the application
- B) In the database
- C) Only in the cache
- D) Nowhere

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Database-level rules prevent bad data from every entry point.

</details>

---

### Question 6 — Medium

**Normalization removes:**

- A) Tables
- B) Redundancy
- C) Keys
- D) Constraints

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Each fact is stored once.

</details>

---

### Question 7 — Medium

**A soft delete:**

- A) Deletes the row
- B) Sets a deleted_at column
- C) Caches the row
- D) Rejects the row

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: History is preserved and recoverable.

</details>

---

### Question 8 — Hard

**Over-normalizing causes:**

- A) Faster queries
- B) Join-heavy queries
- C) Fewer tables
- D) Fewer keys

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Normalize facts; denormalize only what is measured.

</details>

---

### Question 9 — Hard

**The roadmap's rule about user data is:**

- A) Hard-delete it
- B) Never hard-delete it
- C) Cache it
- D) Ignore it

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Soft deletes preserve history.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for the schema is:**

- A) It is designed after the app
- B) It is designed before the application
- C) It is optional
- D) It is cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The schema is the contract, designed first.

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
| 9-10 | Expert | Ready for indexes |
| 7-8 | Proficient | Review constraints |
| 5-6 | Developing | Re-study keys |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [02 - Indexes and Queries](02-indexes-queries-quiz.md)