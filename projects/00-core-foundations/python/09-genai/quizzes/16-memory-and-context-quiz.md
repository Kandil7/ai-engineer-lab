# GenAI 16: Memory and Context — Quiz

> **Topic Overview**: Managing conversation history and durable memory within the context budget.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the context budget?**
- A) The GPU memory
- B) The tokens available for prompt, history, evidence, and output
- C) The dataset size
- D) The cache size

<details><summary>Reveal Answer</summary>**B.** Everything competes for it.</details>

### Question 2 — Easy
**What are the three memory types?**
- A) RAM, disk, cache
- B) Conversation, semantic, episodic
- C) L1, L2, L3
- D) Hot, warm, cold

<details><summary>Reveal Answer</summary>**B.** Different lifetimes and retrieval.</details>

### Question 3 — Medium
**What is compaction?**
- A) Compressing the model
- B) Summarizing older turns while keeping recent ones
- C) Deleting memory
- D) Caching

<details><summary>Reveal Answer</summary>**B.** It keeps a long conversation within budget.</details>

### Question 4 — Medium
**Why bound memory growth?**
- A) For speed
- B) Unbounded memory is a cost and relevance problem
- C) For accuracy
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Bound with TTL and caps.</details>

### Question 5 — Medium
**Why can memory be a security concern?**
- A) It is not
- B) Memory must be per-user scoped, or it leaks across users
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Same as any tenant data.</details>

### Question 6 — Hard
**Why test memory coherence across sessions?**
- A) For speed
- B) The system can contradict its own past, eroding trust
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Coherence is a correctness property.</details>

### Question 7 — Hard
**Why filter memory by relevance before injecting it?**
- A) For speed
- B) Otherwise memory floods the budget and starves retrieval
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Memory competes with evidence.</details>

### Question 8 — Hard
**What should you pin so it survives compaction?**
- A) Nothing
- B) Important facts (semantic memory) that must outlive the summarized turns
- C) All turns
- D) The model

<details><summary>Reveal Answer</summary>**B.** Durable facts persist.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can manage memory. |
| 5-6 | Review budget and coherence. |
| < 5 | Re-read the lecture. |
