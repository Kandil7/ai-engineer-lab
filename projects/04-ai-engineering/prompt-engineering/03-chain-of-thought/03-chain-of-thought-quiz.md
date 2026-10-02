# Prompt Engineering 03: Chain-of-Thought — Quiz

> **Topic Overview**: Step-by-step reasoning, when it helps, its cost, and showing vs hiding.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 10 |
| Correct Answers | 0 |
| Score | 0% |

---

## Questions

### Question 1 — Easy

**Chain-of-thought asks the model to:**

- A) Answer immediately
- B) Reason step by step before the answer
- C) Cache the answer
- D) Sort the input

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The intermediate steps are produced before the final answer.

</details>

---

### Question 2 — Easy

**The reasoning steps act as:**

- A) Decoration
- B) The model's scratchpad
- C) A cache
- D) A sort key

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: They hold sub-results the model can check against.

</details>

---

### Question 3 — Easy

**CoT helps most on:**

- A) Simple factual lookups
- B) Multi-step reasoning tasks
- C) Translation
- D) Creative writing

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Tasks with intermediate states, such as math, logic, and code debugging.

</details>

---

### Question 4 — Medium

**Why do steps improve accuracy?**

- A) They are free
- B) They reduce compounding errors by not skipping an intermediate state
- C) They cache the answer
- D) They sort the problem

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Each step can be checked against the previous one.

</details>

---

### Question 5 — Medium

**CoT on a simple factual question is:**

- A) Optimal
- B) Pure cost for no accuracy gain
- C) Required
- D) Faster

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The task has no intermediate state for the steps to help.

</details>

---

### Question 6 — Medium

**The reasoning costs:**

- A) Nothing
- B) Tokens on every call
- C) Disk space
- D) A cache entry

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The steps are generated tokens, paid each time.

</details>

---

### Question 7 — Medium

**In a budget-tight RAG prompt, long reasoning can:**

- A) Help always
- B) Crowd out the retrieved evidence
- C) Cache the evidence
- D) Sort the context

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Reasoning competes with evidence for the context budget.

</details>

---

### Question 8 — Hard

**Whether CoT helps a given task should be:**

- A) Assumed
- B) Measured against the eval set
- C) Cached
- D) Sorted

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The accuracy gain is measured, not assumed.

</details>

---

### Question 9 — Hard

**Hiding the reasoning primarily trades:**

- A) Accuracy for speed only
- B) Transparency for output tokens and latency
- C) Memory for disk
- D) Nothing

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The model reasons internally and emits only the answer.

</details>

---

### Question 10 — Hard

**Few-shot combined with CoT works because:**

- A) Examples replace reasoning
- B) The examples demonstrate the step-by-step format the model imitates
- C) It caches the steps
- D) It sorts the steps

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: An example that jumps to the answer teaches the model to jump.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Hard |
| 9 | B | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Ready for prompt evaluation |
| 7-8 | Proficient | Review the cost and when CoT helps |
| 5-6 | Developing | Re-study the mechanism and misapplication |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [02 - Few-Shot](02-few-shot-quiz.md) | **Next**: [04 - Prompt Evaluation](04-prompt-evaluation-quiz.md)
