# GenAI 15: Multi-Agent — Quiz

> **Topic Overview**: Coordinating multiple agents with roles, handoffs, and a supervisor.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a multi-agent system?**
- A) One model
- B) Several agents with distinct roles coordinating on a task
- C) A cache
- D) A chunker

<details><summary>Reveal Answer</summary>**B.** Roles plus coordination.</details>

### Question 2 — Easy
**What is a supervisor pattern?**
- A) A model
- B) One agent routes tasks to worker agents and aggregates results
- C) A cache
- D) A chunker

<details><summary>Reveal Answer</summary>**B.** Central coordination.</details>

### Question 3 — Medium
**When is multi-agent worth its complexity?**
- A) Always
- B) When tasks are genuinely separable and the decomposition reduces error or cost
- C) Never
- D) For any task

<details><summary>Reveal Answer</summary>**B.** Justify the split.</details>

### Question 4 — Medium
**What is the main cost of adding agents?**
- A) Storage
- B) More loops, latency, and error surface, plus coordination overhead
- C) Nothing
- D) Bandwidth

<details><summary>Reveal Answer</summary>**B.** Each agent is a failure point.</details>

### Question 5 — Medium
**What is a handoff?**
- A) A cache
- B) Passing control and context from one agent to another
- C) A model
- D) A chunker

<details><summary>Reveal Answer</summary>**B.** Context must travel with control.</details>

### Question 6 — Hard
**Why is a single agent often the right first design?**
- A) It is always better
- B) It is simpler; split only when measurement shows a multi-agent gain
- C) For style
- D) It is not

<details><summary>Reveal Answer</summary>**B.** Earn the complexity.</details>

### Question 7 — Hard
**What must every agent have to be safe?**
- A) A GPU
- B) A bounded loop, scoped tools, and a way to stop
- C) A cache
- D) A database

<details><summary>Reveal Answer</summary>**B.** Bounds and scope per agent.</details>

### Question 8 — Hard
**How do you evaluate a multi-agent system?**
- A) By reading transcripts
- B) Task completion and error attribution per agent, on a fixed set
- C) Cost only
- D) It cannot be evaluated

<details><summary>Reveal Answer</summary>**B.** Measure end-to-end and per role.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand multi-agent tradeoffs. |
| 5-6 | Review when to split. |
| < 5 | Re-read the lecture. |
