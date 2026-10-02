# SQL SQLite 02: Create Database — Quiz

> **Topic Overview**: SQLite files vs MySQL servers, and connection hygiene.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How is a sqlite database created?**
- A) `CREATE DATABASE`
- B) By connecting to a path
- C) By a server
- D) By a migration

<details><summary>Reveal Answer</summary>**B.** Connect to create.</details>

### Question 2 — Easy
**How do you "USE" another database in sqlite3?**
- A) `USE db`
- B) Open a new connection to the other file
- C) `SWITCH db`
- D) You cannot

<details><summary>Reveal Answer</summary>**B.** One connection, one file.</details>

### Question 3 — Medium
**How do you "drop" a sqlite database?**
- A) `DROP DATABASE`
- B) Close the connection and delete the file
- C) `TRUNCATE`
- D) You cannot

<details><summary>Reveal Answer</summary>**B.** File deletion.</details>

### Question 4 — Medium
**Why verify the path before deleting a `.db` file?**
- A) Speed
- B) A relative path resolves against the working directory, not the script
- C) Style
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Confirm absolute paths.</details>

### Question 5 — Medium
**What does `PRAGMA database_list` show?**
- A) Tables
- B) Attached database files for the connection
- C) Users
- D) Indexes

<details><summary>Reveal Answer</summary>**B.** Attached files.</details>

### Question 6 — Hard
**Why do installers not fix open shells?**
- A) They do
- B) PATH changes apply to new processes; old terminals keep the old environment
- C) Speed
- D) Permissions

<details><summary>Reveal Answer</summary>**B.** New shell required.</details>

### Question 7 — Hard
**What goes wrong when pip and python point at different interpreters?**
- A) Nothing
- B) Installed packages land where the running interpreter cannot see them
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** `sys.executable` is the truth.</details>

### Question 8 — Hard
**Why are in-memory databases right for tests?**
- A) Speed only
- B) Each test gets a fresh, isolated database with no file cleanup
- C) They persist
- D) They share state

<details><summary>Reveal Answer</summary>**B.** Isolation by construction.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You manage sqlite databases. |
| 5-6 | Review files vs servers. |
| < 5 | Re-read the lecture. |
