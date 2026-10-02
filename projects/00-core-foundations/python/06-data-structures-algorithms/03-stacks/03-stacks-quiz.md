# DSA 03: Stacks — Quiz

> **Topic Overview**: LIFO access, list vs linked-list implementations, and parsing.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What order does a stack enforce?**
- A) FIFO
- B) LIFO
- C) Random
- D) Priority

<details><summary>Reveal Answer</summary>**B.** Last in, first out.</details>

### Question 2 — Easy
**Which list operations make an O(1) stack?**
- A) `insert(0, x)` and `pop(0)`
- B) `append` and `pop`
- C) `sort` and `reverse`
- D) `index` and `count`

<details><summary>Reveal Answer</summary>**B.** Both act at the end.</details>

### Question 3 — Medium
**Why is `insert(0, x)` wrong for a stack push?**
- A) It is O(n) because it shifts all elements
- B) It is LIFO
- C) It is O(1)
- D) It is not wrong

<details><summary>Reveal Answer</summary>**A.** Push must be O(1).</details>

### Question 4 — Medium
**What does a stack do in balanced-parentheses checking?**
- A) Sorts brackets
- B) Pushes openers and pops on matching closers
- C) Counts total brackets
- D) Hashes brackets

<details><summary>Reveal Answer</summary>**B.** A pop must match the last opener.</details>

### Question 5 — Medium
**In postfix evaluation, why does operand order matter?**
- A) It does not
- B) Subtraction and division are not commutative; the second pop is the left operand
- C) For speed
- D) For memory

<details><summary>Reveal Answer</summary>**B.** `a - b` needs `a` before `b`.</details>

### Question 6 — Hard
**How does a Min Stack return the minimum in O(1)?**
- A) It sorts on each push
- B) An auxiliary stack tracks the running minimum
- C) It scans on each call
- D) It uses a heap

<details><summary>Reveal Answer</summary>**B.** Parallel minimum history.</details>

### Question 7 — Hard
**Why must a `pop` guard against an empty stack?**
- A) For speed
- B) Popping an empty stack raises or corrupts state; the caller must handle underflow
- C) It cannot be empty
- D) For memory

<details><summary>Reveal Answer</summary>**B.** Underflow is a real case.</details>

### Question 8 — Hard
**What is the time complexity of converting infix to postfix with a stack?**
- A) O(n²)
- B) O(n) — each token is pushed and popped at most once
- C) O(log n)
- D) O(2ⁿ)

<details><summary>Reveal Answer</summary>**B.** Amortized single pass.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand stacks. |
| 5-6 | Review postfix and Min Stack. |
| < 5 | Re-read the lecture. |
