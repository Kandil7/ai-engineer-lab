# PostgreSQL 02: Types — Quiz

> **Topic Overview**: Exactness, timezones, and the Postgres↔Python mapping.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Which type for money?**
- A) `float`
- B) `numeric`
- C) `integer`
- D) `text`

<details><summary>Reveal Answer</summary>**B.** Exact decimals.</details>

### Question 2 — Easy
**Which type for event times?**
- A) `timestamp`
- B) `timestamptz`
- C) `date`
- D) `text`

<details><summary>Reveal Answer</summary>**B.** Instants with zones.</details>

### Question 3 — Medium
**Why does `float` fail for money?**
- A) Slow
- B) Binary floating point cannot represent most decimals exactly
- C) Too big
- D) Unindexed

<details><summary>Reveal Answer</summary>**B.** Inexact representation.</details>

### Question 4 — Medium
**What must you pass for a `numeric` column?**
- A) A float
- B) A `Decimal`
- C) A string
- D) An int

<details><summary>Reveal Answer</summary>**B.** Exact from the start.</details>

### Question 5 — Medium
**Why does psycopg3 reject naive datetimes for `timestamptz`?**
- A) A bug
- B) A naive value has no zone, so the instant is undefined
- C) Speed
- D) Size

<details><summary>Reveal Answer</summary>**B.** Ambiguous instant.</details>

### Question 6 — Hard
**Why is `text + CHECK` better than `varchar(255)`?**
- A) Faster
- B) Same storage, but the constraint states the real rule instead of a magic number
- C) Smaller
- D) Indexed

<details><summary>Reveal Answer</summary>**B.** Honest validation.</details>

### Question 7 — Hard
**When is a native array appropriate?**
- A) Always
- B) Small fixed-shape lists; relational or growing lists stay in tables
- C) Never
- D) For joins

<details><summary>Reveal Answer</summary>**B.** Arrays do not join.</details>

### Question 8 — Hard
**Why is `char(n)` a footgun?**
- A) Slow
- B) Space padding changes comparisons and output unexpectedly
- C) Big
- D) Unindexed

<details><summary>Reveal Answer</summary>**B.** Silent padding.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You choose types deliberately. |
| 5-6 | Review exactness and timezones. |
| < 5 | Re-read the lecture. |
