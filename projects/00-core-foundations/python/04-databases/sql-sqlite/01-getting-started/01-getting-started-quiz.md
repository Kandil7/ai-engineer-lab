# SQL SQLite 01: Getting Started — Quiz

> **Topic Overview**: Connecting with sqlite3, cursors, and the commit pattern.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does `sqlite3.connect(path)` do?**
- A) Starts a server
- B) Opens the database file, creating it if missing
- C) Creates a table
- D) Runs a query

<details><summary>Reveal Answer</summary>**B.** Open-or-create.</details>

### Question 2 — Easy
**What is a cursor for?**
- A) Committing
- B) Executing statements and fetching results
- C) Closing
- D) Backing up

<details><summary>Reveal Answer</summary>**B.** The execution handle.</details>

### Question 3 — Medium
**When is data actually saved?**
- A) On `execute`
- B) On `commit`
- C) On `close`
- D) Immediately

<details><summary>Reveal Answer</summary>**B.** Commit persists.</details>

### Question 4 — Medium
**What does the `with` statement do for a connection?**
- A) Nothing special
- B) Commits on clean exit, rolls back on exception
- C) Deletes the file
- D) Creates tables

<details><summary>Reveal Answer</summary>**B.** Transactional context.</details>

### Question 5 — Medium
**What is `:memory:` for?**
- A) Production
- B) A transient database for tests, gone when the connection closes
- C) Caching
- D) Backups

<details><summary>Reveal Answer</summary>**B.** Disposable test DB.</details>

### Question 6 — Hard
**Why does an uncommitted write vanish on close?**
- A) A bug
- B) The transaction was never committed, so rollback discards it
- C) The file is locked
- D) The cursor is closed

<details><summary>Reveal Answer</summary>**B.** No commit, no durability.</details>

### Question 7 — Hard
**What does `rollback()` do?**
- A) Commits
- B) Undoes the current transaction's writes
- C) Deletes the file
- D) Closes

<details><summary>Reveal Answer</summary>**B.** Undo pending writes.</details>

### Question 8 — Hard
**Why catch `sqlite3.Error` around database work?**
- A) Style
- B) So integrity errors and missing tables become handled failures with rollback
- C) Speed
- D) Logging only

<details><summary>Reveal Answer</summary>**B.** Controlled failure.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You connect and commit correctly. |
| 5-6 | Review commit/rollback and context managers. |
| < 5 | Re-read the lecture. |
