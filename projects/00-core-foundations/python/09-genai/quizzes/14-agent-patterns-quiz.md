# GenAI 14: Agent Patterns — Quiz

> **Topic Overview**: ReAct, planning, and reflection loops for tool-using agents.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the ReAct pattern?**
- A) A model architecture
- B) Reason → act → observe, repeated until the task is done
- C) A chunking method
- D) A cache

<details><summary>Reveal Answer</summary>**B.** Reasoning interleaves with tool use.</details>

### Question 2 — Easy
**What distinguishes an agent from a single prompt-response?**
- A) It is faster
- B) It loops, using tools and observations across steps
- C) It is cheaper
- D) It is smaller

<details><summary>Reveal Answer</summary>**B.** Multi-step action loops.</details>

### Question 3 — Medium
**Why cap the loop?**
- A) For cost only
- B) Agents can loop indefinitely; a step/loop cap bounds them
- C) For accuracy
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Bounded loops prevent runaway agents.</details>

### Question 4 — Medium
**What is reflection?**
- A) Training
- B) The agent critiques its own output and revises
- C) Chunking
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Self-critique improves output.</details>

### Question 5 — Medium
**What is planning?**
- A) Tool calling
- B) The agent decomposes the task into steps before acting
- C) Caching
- D) Chunking

<details><summary>Reveal Answer</summary>**B.** Decompose then execute.</details>

### Question 6 — Hard
**Why categorize loop-detection as necessary, not nice-to-have?**
- A) It is not
- B) Without it an agent can repeat an action forever, burning cost and time
- C) For accuracy
- D) For style

<details><summary>Reveal Answer</summary>**B.** Loop detection is a safety control.</details>

### Question 7 — Hard
**Why measure task completion rate for an agent?**
- A) For speed
- B) It is the primary quality signal, alongside tool-selection accuracy
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Agent quality is completion quality.</details>

### Question 8 — Hard
**When is a single tool call better than an agent?**
- A) Never
- B) When the task is a fixed mapping; an agent adds cost and unpredictability for nothing
- C) Always
- D) For reasoning tasks

<details><summary>Reveal Answer</summary>**B.** Complexity must be justified.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand agent patterns. |
| 5-6 | Review loops and caps. |
| < 5 | Re-read the lecture. |
