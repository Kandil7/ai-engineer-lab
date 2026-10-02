# Advanced Python 19: Logging — Quiz

> **Topic Overview**: Loggers, levels, handlers, and library-vs-app logging.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why use `logging` over `print`?**
- A) It is faster
- B) Levels, timestamps, destinations, and switchable verbosity
- C) It sorts
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Structured control.</details>

### Question 2 — Easy
**How do you get the conventional module logger?**
- A) `logging.root`
- B) `logging.getLogger(__name__)`
- C) `print`
- D) `logger.new()`

<details><summary>Reveal Answer</summary>**B.** Per-module logger hierarchy.</details>

### Question 3 — Medium
**What is the relationship between logger levels and handler levels?**
- A) The same
- B) Both filter; a record must pass the logger level and its handlers' levels
- C) Only handlers filter
- D) Only loggers filter

<details><summary>Reveal Answer</summary>**B.** Two gates.</details>

### Question 4 — Medium
**Why should a library not configure the root logger?**
- A) It cannot
- B) The application owns configuration; a library only adds `NullHandler` and emits
- C) For speed
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Library/app separation.</details>

### Question 5 — Medium
**What is a Handler responsible for?**
- A) Formatting only
- B) Routing records to a destination (console, file, network)
- C) Levels
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Destination.</details>

### Question 6 — Hard
**Why is logging per-request context (e.g. a request id) valuable?**
- A) It is not
- B) It lets you correlate lines across a distributed request for debugging
- C) It hashes
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Correlation IDs.</details>

### Question 7 — Hard
**What is the danger of logging sensitive data?**
- A) None
- B) Logs persist and spread secrets/PII; redact at the source
- C) It is slower
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Logs are a data-leak surface.</details>

### Question 8 — Hard
**Why prefer structured (JSON) logs in production?**
- A) They are smaller
- B) Machines can parse fields for search and alerting
- C) They are faster
- D) They sort

<details><summary>Reveal Answer</summary>**B.** Queryable logs.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You configure logging well. |
| 5-6 | Review levels, handlers, and library rules. |
| < 5 | Re-read the lecture. |
