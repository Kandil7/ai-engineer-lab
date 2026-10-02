# SQL SQLite 10: Drop Table — Quiz

> **Topic Overview**: Finality, `TRUNCATE`, and the safe-drop checklist.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `DROP TABLE` remove?**
- A) Rows only
- B) The definition and all data, permanently
- C) An index
- D) A view

<details><summary>Reveal Answer</summary>**B.** Total removal.</details>

### Question 2 — Easy
**What does `TRUNCATE` preserve?**
- A) The rows
- B) The table structure, removing only rows
- C) The indexes only
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Empty but intact.</details>

### Question 3 — Medium
**Which of the three is transactional and selective?**
- A) `DROP`
- B) `TRUNCATE`
- C) `DELETE ... WHERE`
- D) None

<details><summary>Reveal Answer</summary>**C.** Row-selective removal.</details>

### Question 4 — Medium
**Why does the engine refuse to drop a referenced table?**
- A) A bug
- B) The foreign key would dangle; resolve dependents first
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Referential protection.</details>

### Question 5 — Medium
**What does `IF EXISTS` add?**
- A) Speed
- B) Idempotent scripts that do not fail on missing tables
- C) Backups
- D) Locks

<details><summary>Reveal Answer</summary>**B.** Safe re-runs.</details>

### Question 6 — Hard
**What must precede a production drop?**
- A) Nothing
- B) A verified backup plus confirmation nothing references the table
- C) A restart
- D) An index

<details><summary>Reveal Answer</summary>**B.** Backup-then-drop.</details>

### Question 7 — Hard
**Why does SQLite lack `TRUNCATE`?**
- A) It is slow
- B) `DELETE FROM t` covers the case; the engine optimizes the full-table delete
- C) It errors
- D) It locks

<details><summary>Reveal Answer</summary>**B.** Covered by `DELETE`.</details>

### Question 8 — Hard
**Why run drops inside migrations, not ad-hoc?**
- A) Style
- B) Ordered, reviewed, reversible-process change instead of a one-off surprise
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Change control.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You drop deliberately. |
| 5-6 | Review the three removals and FK rules. |
| < 5 | Re-read the lecture. |
