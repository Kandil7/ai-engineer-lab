# FastAPI 35: Background Jobs — Quiz

> **Topic Overview**: Fire-and-forget limits, brokers, retries, and progress.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is `BackgroundTasks`?**
- A) A worker queue
- B) Fire-and-forget work after the response, in the same process
- C) A cron
- D) A cache

<details><summary>Reveal Answer</summary>**B.** Post-response, in-process.</details>

### Question 2 — Easy
**What is the hard limit of in-process jobs?**
- A) Speed
- B) No durability, no retry, lost on worker restart or crash
- C) Memory only
- D) CPU only

<details><summary>Reveal Answer</summary>**B.** Ephemeral.</details>

### Question 3 — Medium
**What does a broker contract provide?**
- A) Speed
- B) Durable queuing: the job survives worker loss until acknowledged
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Durability.</details>

### Question 4 — Medium
**What is a dead-letter queue for?**
- A) Deleted jobs
- B) Jobs that exhausted retries, parked for inspection instead of being lost
- C) Fast jobs
- D) Cached results

<details><summary>Reveal Answer</summary>**B.** Failure quarantine.</details>

### Question 5 — Medium
**How does a client learn job progress?**
- A) The response
- B) A status endpoint keyed by a job id the enqueue call returns
- C) The logs
- D) It cannot

<details><summary>Reveal Answer</summary>**B.** Poll a status resource.</details>

### Question 6 — Hard
**When is `BackgroundTasks` correct versus a broker?**
- A) Always
- B) Small non-critical work vs durable, retried, long-running jobs
- C) Never
- D) For LLM calls

<details><summary>Reveal Answer</summary>**B.** Durability decides.</details>

### Question 7 — Hard
**Why must jobs be idempotent?**
- A) Style
- B) Retries and redelivery can run a job twice
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** At-least-once reality.</details>

### Question 8 — Hard
**What is the concurrency risk of in-process jobs?**
- A) None
- B) They consume worker capacity and can delay request handling
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Shared workers.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You choose job machinery well. |
| 5-6 | Review durability, retries, idempotency. |
| < 5 | Re-read the lecture. |
