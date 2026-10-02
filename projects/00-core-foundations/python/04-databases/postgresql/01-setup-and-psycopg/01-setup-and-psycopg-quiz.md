# PostgreSQL 01: Setup and psycopg — Quiz

> **Topic Overview**: The connection lifecycle, DSNs, and cursor kinds.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What are the lifecycle steps of a connection?**
- A) Open, query, forget
- B) Connect, work with a cursor, close
- C) Pool only
- D) Migrate

<details><summary>Reveal Answer</summary>**B.** Connect, work, close.</details>

### Question 2 — Easy
**Why use a `with` block?**
- A) Speed
- B) Cleanup happens on every path, including exceptions
- C) Caching
- D) Pooling

<details><summary>Reveal Answer</summary>**B.** Structural cleanup.</details>

### Question 3 — Medium
**What are the parts of a DSN?**
- A) Host only
- B) Scheme, credentials, host, port, dbname, options
- C) Username only
- D) Port only

<details><summary>Reveal Answer</summary>**B.** Left-to-right identity.</details>

### Question 4 — Medium
**Where must the password live?**
- A) In the code
- B) In env or a secret manager, never committed
- C) In the DSN string in git
- D) In the docs

<details><summary>Reveal Answer</summary>**B.** Out of version control.</details>

### Question 5 — Medium
**When do you need a server-side cursor?**
- A) Always
- B) For bulk reads that would OOM a client-side fetch
- C) For small lookups
- D) Never

<details><summary>Reveal Answer</summary>**B.** Stream big results.</details>

### Question 6 — Hard
**Why does a leaked connection become an outage?**
- A) It does not
- B) The server caps connections; leaks accumulate until new work cannot connect
- C) It is slow
- D) It locks

<details><summary>Reveal Answer</summary>**B.** Finite pool, permanent loss.</details>

### Question 7 — Hard
**What goes wrong mixing `?` and `%s` placeholders?**
- A) Nothing
- B) Each driver has one style; the other is a syntax error or, worse, a literal
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** One style per driver.</details>

### Question 8 — Hard
**Why set `connect_timeout`?**
- A) Speed
- B) A dead host should fail fast, not hang the caller
- C) Caching
- D) Pooling

<details><summary>Reveal Answer</summary>**B.** Bound the wait.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You manage connections well. |
| 5-6 | Review lifecycle and DSNs. |
| < 5 | Re-read the lecture. |
