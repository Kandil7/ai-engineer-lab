# PostgreSQL 04: Indexes — Quiz

> **Topic Overview**: Index families, `EXPLAIN`, and the justification rule.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Which index family is the default?**
- A) GIN
- B) B-tree
- C) BRIN
- D) GiST

<details><summary>Reveal Answer</summary>**B.** Equality, range, order.</details>

### Question 2 — Easy
**Which family serves JSONB containment?**
- A) B-tree
- B) GIN
- C) BRIN
- D) Hash

<details><summary>Reveal Answer</summary>**B.** Contains queries.</details>

### Question 3 — Medium
**When is BRIN right?**
- A) Random updates
- B) Append-only time series where physical order matches the indexed column
- C) Small tables
- D) Text search

<details><summary>Reveal Answer</summary>**B.** Tiny index on ordered piles.</details>

### Question 4 — Medium
**What does a Seq Scan mean?**
- A) Indexed access
- B) No usable index (or a table so small it does not matter)
- C) An error
- D) A lock

<details><summary>Reveal Answer</summary>**B.** Full read.</details>

### Question 5 — Medium
**What does a Nested Loop with 10k iterations suggest?**
- A) Good plan
- B) An N+1-shaped query the planner is executing row by row
- C) A missing table
- D) A deadlock

<details><summary>Reveal Answer</summary>**B.** Fix the query shape.</details>

### Question 6 — Hard
**Why confirm both plan and wall time?**
- A) Redundant
- B) Plans improve on tiny tables without time changing; time improves from cache without the plan changing
- C) Speed
- D) Style

<details><summary>Reveal Answer</summary>**B.** Two independent signals.</details>

### Question 7 — Hard
**How do you find an index earning nothing?**
- A) Guess
- B) `pg_stat_user_indexes` scans over a full workload cycle
- C) Size
- D) Age

<details><summary>Reveal Answer</summary>**B.** Measured usage.</details>

### Question 8 — Hard
**Why does every index need a justification comment?**
- A) Style
- B) The audit needs the query shape; without it, no one can tell a useless index from a seasonal one
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Auditable bets.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You index with evidence. |
| 5-6 | Review families and `EXPLAIN`. |
| < 5 | Re-read the lecture. |
