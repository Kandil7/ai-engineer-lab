# GenAI 17: LLM Observability — Quiz

> **Topic Overview**: Tracing LLM calls for debugging, cost, and quality.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is LLM observability?**
- A) Training logs
- B) Traces, metrics, and logs of LLM calls in production
- C) A model file
- D) A dataset

<details><summary>Reveal Answer</summary>**B.** See what the system actually did.</details>

### Question 2 — Easy
**What is a trace?**
- A) A model
- B) A record of a request across its steps (retrieval, generation) with timing and cost
- C) A cache
- D) A chunk

<details><summary>Reveal Answer</summary>**B.** The end-to-end path of one request.</details>

### Question 3 — Medium
**Why trace from day one?**
- A) For speed
- B) Without traces a failure is a mystery and cost is unknown
- C) For accuracy
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Observability is a precondition, not an add-on.</details>

### Question 4 — Medium
**Why track cost per request?**
- A) For storage
- B) To state the price of one answer and catch spend drift
- C) For accuracy
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Cost is a first-class metric.</details>

### Question 5 — Medium
**What should a trace connect?**
- A) Only the final answer
- B) A request id through retrieval and generation, with latency and tokens each step
- C) The dataset
- D) The model file

<details><summary>Reveal Answer</summary>**B.** Correlation across stages.</details>

### Question 6 — Hard
**Why is observability a precondition for eval-driven development?**
- A) It is not
- B) You cannot diagnose a quality change without seeing what the system did
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Evidence requires visibility.</details>

### Question 7 — Hard
**Why must tracing not block the request?**
- A) For style
- B) A tracing failure should not fail the user's request
- C) For accuracy
- D) It must block

<details><summary>Reveal Answer</summary>**B.** Degrade, do not break.</details>

### Question 8 — Hard
**What does a rising cost-per-request trend suggest?**
- A) Nothing
- B) Prompt bloat, retries, or cache rot raising spend silently
- C) Better accuracy
- D) Lower usage

<details><summary>Reveal Answer</summary>**B.** The trend is a signal.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand LLM observability. |
| 5-6 | Review traces and cost. |
| < 5 | Re-read the lecture. |
