# FastAPI 44: Metrics with Prometheus — Quiz

> **Topic Overview**: Counters, gauges, histograms, RED/USE, and SLOs.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What are the three Prometheus metric types?**
- A) Logs, traces, events
- B) Counters, gauges, histograms (plus summaries)
- C) CPU, RAM, disk
- D) OK, warn, crit

<details><summary>Reveal Answer</summary>**B.** The three primitives.</details>

### Question 2 — Easy
**When is a counter right?**
- A) Current value
- B) Monotonically increasing totals like requests or errors
- C) Latency
- D) Queue depth

<details><summary>Reveal Answer</summary>**B.** Only ever increases.</details>

### Question 3 — Medium
**Counter vs gauge?**
- A) Same
- B) Counters accumulate; gauges show a current level that rises and falls
- C) Gauges accumulate
- D) Neither scrapes

<details><summary>Reveal Answer</summary>**B.** Total vs level.</details>

### Question 4 — Medium
**What are RED signals?**
- A) Colors
- B) Rate, Errors, Duration per service
- C) Logs
- D) Traces

<details><summary>Reveal Answer</summary>**B.** Request-oriented health.</details>

### Question 5 — Medium
**What is USE for?**
- A) Users
- B) Utilization, Saturation, Errors of resources
- C) Latency
- D) Traces

<details><summary>Reveal Answer</summary>**B.** Resource-oriented health.</details>

### Question 6 — Hard
**Why is label cardinality the silent killer?**
- A) It is not
- B) Each unique label set is a new series; user ids in labels explode storage
- C) Speed
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Bound your labels.</details>

### Question 7 — Hard
**What relates SLI, SLO, and error budget?**
- A) Nothing
- B) SLI measures, SLO targets, budget quantifies how much failure is allowed
- C) They are the same
- D) Budget is cost

<details><summary>Reveal Answer</summary>**B.** Measurement to policy.</details>

### Question 8 — Hard
**Why histograms over averages for latency SLOs?**
- A) Style
- B) Histograms preserve the distribution so p95/p99 is computable; averages destroy it
- C) Speed
- D) Size

<details><summary>Reveal Answer</summary>**B.** Tails need distributions.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You measure services well. |
| 5-6 | Review metric types and cardinality. |
| < 5 | Re-read the lecture. |
