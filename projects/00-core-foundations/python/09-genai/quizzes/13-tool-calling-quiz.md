# GenAI 13: Tool Calling — Quiz

> **Topic Overview**: Letting a model invoke functions and use their results.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is tool calling?**
- A) Training a model
- B) The model requesting a function call with typed arguments
- C) Chunking
- D) Caching

<details><summary>Reveal Answer</summary>**B.** The model proposes; the app executes.</details>

### Question 2 — Easy
**Who executes the tool?**
- A) The model
- B) Your application, which runs the function and feeds the result back
- C) The vector DB
- D) The user

<details><summary>Reveal Answer</summary>**B.** The model never runs code itself.</details>

### Question 3 — Medium
**Why validate tool arguments before executing?**
- A) For speed
- B) A malformed or malicious argument can cause harm
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** The tool boundary is a trust boundary.</details>

### Question 4 — Medium
**Why cap the number of tool calls?**
- A) For cost only
- B) To prevent runaway loops and unbounded spend
- C) For accuracy
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** A step cap bounds the loop.</details>

### Question 5 — Medium
**What does a tool result become?**
- A) The final answer
- B) Context for the next model step
- C) A file
- D) A cache entry

<details><summary>Reveal Answer</summary>**B.** The loop continues until the model answers.</details>

### Question 6 — Hard
**Why is tool-calling a security surface?**
- A) It is not
- B) Tools can read/write data; permissions and argument validation matter
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Tools are capabilities that must be scoped.</details>

### Question 7 — Hard
**A tool fails. What should happen?**
- A) Crash
- B) The error is returned to the loop so the model can adapt or stop
- C) Ignore it
- D) Retry forever

<details><summary>Reveal Answer</summary>**B.** Errors are inputs the model can reason about.</details>

### Question 8 — Hard
**Why define tool schemas precisely?**
- A) For style
- B) The model picks arguments from the schema; ambiguity yields wrong calls
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** The schema is the API contract to the model.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand tool calling. |
| 5-6 | Review validation and caps. |
| < 5 | Re-read the lecture. |
