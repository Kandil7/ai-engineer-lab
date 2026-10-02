# MongoDB 02: Databases — Quiz

> **Topic Overview**: Lazy creation, listing, dropping, and env separation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What creates a MongoDB database?**
- A) `CREATE DATABASE`
- B) The first write to it
- C) `USE db`
- D) A migration

<details><summary>Reveal Answer</summary>**B.** Lazy creation.</details>

### Question 2 — Easy
**How do you list databases?**
- A) `SHOW DBS`
- B) `client.list_database_names()`
- C) `ls`
- D) `find()`

<details><summary>Reveal Answer</summary>**B.** List call.</details>

### Question 3 — Medium
**Why can a typo'd database go unnoticed?**
- A) It errors
- B) Referencing creates nothing, so the typo silently targets emptiness
- C) It is slow
- D) It locks

<details><summary>Reveal Answer</summary>**B.** Silent emptiness.</details>

### Question 4 — Medium
**What does `drop_database` do?**
- A) Backs up
- B) Permanently deletes the database and all collections
- C) Archives
- D) Renames

<details><summary>Reveal Answer</summary>**B.** Final deletion.</details>

### Question 5 — Medium
**How should environments be separated?**
- A) One database
- B) One name per env from config (`app_dev`, `app_test`, `app`)
- C) Prefixes in code
- D) They need not be

<details><summary>Reveal Answer</summary>**B.** Named isolation.</details>

### Question 6 — Hard
**What guard belongs on a drop helper?**
- A) None
- B) Name-prefix restriction plus an explicit confirm flag
- C) Speed
- D) Logging only

<details><summary>Reveal Answer</summary>**B.** Restricted, confirmed drops.</details>

### Question 7 — Hard
**Why verify collections after setup?**
- A) Style
- B) Lazy creation means a failed setup looks identical to an empty one
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Prove setup ran.</details>

### Question 8 — Hard
**`get_database` vs bracket access?**
- A) Same always
- B) `get_database` accepts per-handle options; brackets use client defaults
- C) Brackets are faster
- D) `get_database` creates

<details><summary>Reveal Answer</summary>**B.** Options differ.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You manage MongoDB databases. |
| 5-6 | Review lazy creation and drops. |
| < 5 | Re-read the lecture. |
