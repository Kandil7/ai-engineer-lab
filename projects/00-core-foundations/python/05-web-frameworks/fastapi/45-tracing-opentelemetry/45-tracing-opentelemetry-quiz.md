# FastAPI 45: Tracing with OpenTelemetry — Quiz

> **Topic Overview**: Spans, context propagation, and sampling.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a span?**
- A) A log line
- B) A timed unit of work with a name, attributes, and parent links
- C) A metric
- D) A cache entry

<details><summary>Reveal Answer</summary>**B.** Trace building block.</details>

### Question 2 — Easy
**What is a trace?**
- A) A log file
- B) The tree of spans for one request across services
- C) A metric
- D) An error

<details><summary>Reveal Answer</summary>**B.** End-to-end path.</details>

### Question 3 — Medium
**How does context cross a service boundary?**
- A) Automatically
- B) Through propagated headers (traceparent) the client/server inject and extract
- C) The database
- D) A shared file

<details><summary>Reveal Answer</summary>**B.** Header propagation.</details>

### Question 4 — Medium
**What breaks propagation?**
- A) Nothing
- B) A hop that drops headers (a proxy, queue, or library that does not forward context)
- C) Sampling
- D) Spans

<details><summary>Reveal Answer</summary>**B.** Context loss splits the trace.</details>

### Question 5 — Medium
**Why sample traces?**
- A) Style
- B) Full capture is unaffordable at volume; sample head or tail by policy
- C) Speed
- D) Accuracy

<details><summary>Reveal Answer</summary>**B.** Cost-controlled visibility.</details>

### Question 6 — Hard
**Head vs tail sampling?**
- A) Same
- B) Head decides at start (cheap, blind); tail decides after (sees errors, costs buffers)
- C) Tail is cheaper
- D) Head sees errors

<details><summary>Reveal Answer</summary>**B.** When the decision happens.</details>

### Question 7 — Hard
**What should an RAG pipeline trace record?**
- A) The final answer
- B) Retrieval candidates, rerank scores, prompt version, token counts, guardrail verdicts
- C) The model file
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Stage-level evidence.</details>

### Question 8 — Hard
**Auto vs manual instrumentation?**
- A) Auto suffices always
- B) Auto covers frameworks; manual spans cover business stages the library cannot see
- C) Manual only
- D) Neither

<details><summary>Reveal Answer</summary>**B.** Both layers.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You trace for debugging. |
| 5-6 | Review propagation and sampling. |
| < 5 | Re-read the lecture. |
