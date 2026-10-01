# GenAI 24: Case Study — Agent — Quiz

> **Topic Overview**: Building a tool-using agent with a bounded loop and evaluation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the core loop of a tool-using agent?**
- A) Generate only
- B) Reason → act (tool) → observe → repeat
- C) Chunk
- D) Cache

<details><summary>Reveal Answer</summary>**B.** The ReAct loop.</details>

### Question 2 — Easy
**Why start with one tool?**
- A) For speed
- B) Get one tool working before adding more, so failures are isolated
- C) For cost
- D) It is required

<details><summary>Reveal Answer</summary>**B.** Incremental, testable growth.</details>

### Question 3 — Medium
**What must every agent loop have?**
- A) A GPU
- B) A step cap and loop detection
- C) A cache
- D) A database

<details><summary>Reveal Answer</summary>**B.** Bounds prevent runaway loops.</details>

### Question 4 — Medium
**How do you evaluate an agent?**
- A) By reading transcripts
- B) Task completion rate and tool-selection accuracy on a fixed set
- C) Cost only
- D) It cannot be

<details><summary>Reveal Answer</summary>**B.** Measured task success.</details>

### Question 5 — Medium
**Why validate tool arguments?**
- A) For speed
- B) Wrong or malicious arguments can harm systems or data
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** The tool boundary is a trust boundary.</details>

### Question 6 — Hard
**Why add a framework (e.g. LangGraph) only after a hand-rolled loop?**
- A) Always use a framework
- B) The hand-rolled version teaches the mechanism and gives a comparison baseline
- C) For speed
- D) It is required

<details><summary>Reveal Answer</summary>**B.** Earn the abstraction.</details>

### Question 7 — Hard
**What is the differentiator for a portfolio agent project?**
- A) The model
- B) An MCP server exposing the retrieval to real clients, few candidates have it
- C) The dataset
- D) The UI

<details><summary>Reveal Answer</summary>**B.** MCP is a rare, current signal.</details>

### Question 8 — Hard
**The agent loops forever on a query. What failed?**
- A) The model
- B) The loop bound or detection, which should have stopped it
- C) The GPU
- D) The dataset

<details><summary>Reveal Answer</summary>**B.** Bounds are mandatory.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can build an agent. |
| 5-6 | Review bounds and evaluation. |
| < 5 | Re-read the lecture. |
