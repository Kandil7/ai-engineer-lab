# DS-Algo 03: Recursion — Quiz

> **Topic Overview**: The base case, the call stack, and memoization.

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

**The base case:**

- A) Calls itself
- B) Returns directly, stopping recursion
- C) Sorts the input
- D) Caches the input

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The exit of the recursion.

</details>

---

### Question 2 — Easy

**The recursive case:**

- A) Returns directly
- B) Calls itself on a smaller input
- C) Sorts the input
- D) Caches the input

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The progress toward the base case.

</details>

---

### Question 3 — Easy

**A missing base case causes:**

- A) Fast recursion
- B) Infinite recursion
- C) A cache miss
- D) A sort

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The recursion never exits.

</details>

---

### Question 4 — Medium

**Each recursive call:**

- A) Pushes a stack frame
- B) Pops a stack frame
- C) Sorts the stack
- D) Caches the stack

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: The stack unwinds on return.

</details>

---

### Question 5 — Medium

**Deep recursion hits:**

- A) The cache
- B) The depth limit
- C) The sort
- D) The hash

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: RecursionError.

</details>

---

### Question 6 — Medium

**Iteration:**

- A) Uses the stack
- B) Avoids the stack limit
- C) Is always slower
- D) Is always recursive

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Loops do not push frames.

</details>

---

### Question 7 — Medium

**Memoization stores:**

- A) The stack
- B) Computed results
- C) The input
- D) The sort

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Each value is computed once.

</details>

---

### Question 8 — Hard

**Unmemoized Fibonacci is:**

- A) Linear
- B) Exponential
- C) Logarithmic
- D) Constant

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The same values are recomputed.

</details>

---

### Question 9 — Hard

**Memoized Fibonacci is:**

- A) Exponential
- B) Linear
- C) Logarithmic
- D) Constant

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Each value computed once.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for recursion is:**

- A) It has no base case
- B) It has a base case
- C) It is always used
- D) It is never used

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The base case is the exit.

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
| 9-10 | Expert | Ready for sorting |
| 7-8 | Proficient | Review the call stack |
| 5-6 | Developing | Re-study memoization |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [02 - Hash Maps](02-hash-maps-quiz.md) | **Next**: [04 - Sorting and Searching](04-sorting-searching-quiz.md)