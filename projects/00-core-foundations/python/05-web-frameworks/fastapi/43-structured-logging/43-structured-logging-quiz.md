# FastAPI 43: Structured Logging — Quiz

> **Topic Overview**: JSON logs, correlation IDs, PII redaction, and sampling.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why log JSON in production?**
- A) Smaller
- B) Machines can parse fields for search and alerting
- C) Faster
- D) Prettier

<details><summary>Reveal Answer</summary>**B.** Queryable logs.</details>

### Question 2 — Easy
**What is a correlation ID?**
- A) A user id
- B) A per-request id carried through async context so all lines join
- C) A password
- D) A trace id only

<details><summary>Reveal Answer</summary>**B.** Request-scoped join key.</details>

### Question 3 — Medium
**Why pass the ID through async contextvars?**
- A) Style
- B) `asyncio` tasks share threads, so thread-locals leak across requests
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Task-scoped context.</details>

### Question 4 — Medium
**What must be redacted and where?**
- A) Nothing
- B) PII and secrets at the logging boundary, before the record leaves the process
- C) Errors only
- D) Successes only

<details><summary>Reveal Answer</summary>**B.** Redact at the edge.</details>

### Question 5 — Medium
**What separates levels from sampling?**
- A) Nothing
- B) Levels filter by severity; sampling thins high-volume successes while keeping all errors
- C) Speed
- D) Size

<details><summary>Reveal Answer</summary>**B.** Two different dials.</details>

### Question 6 — Hard
**Why is logging cost part of the request cost?**
- A) It is not
- B) Every line is bytes, CPU, and storage; verbose success logs are a bill
- C) Speed
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Logs are metered output.</details>

### Question 7 — Hard
**What makes a log line actionable?**
- A) Length
- B) The fields an alert or a human needs: who, what, outcome, identity, duration
- C) JSON
- D) Color

<details><summary>Reveal Answer</summary>**B.** Decision-ready fields.</details>

### Question 8 — Hard
**Why is PII in logs a compliance exposure?**
- A) It is not
- B) Logs replicate everywhere and are kept long, spreading the data beyond its consent scope
- C) Speed
- D) Size

<details><summary>Reveal Answer</summary>**B.** Retention multiplies risk.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You log for production. |
| 5-6 | Review IDs, redaction, levels. |
| < 5 | Re-read the lecture. |
