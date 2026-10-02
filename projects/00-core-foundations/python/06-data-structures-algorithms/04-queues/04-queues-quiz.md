# DSA 04: Queues — Quiz

> **Topic Overview**: FIFO access, deque, circular and priority queues, and BFS.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What order does a queue enforce?**
- A) LIFO
- B) FIFO
- C) Random
- D) Sorted

<details><summary>Reveal Answer</summary>**B.** First in, first out.</details>

### Question 2 — Easy
**Which structure gives O(1) enqueue and dequeue in Python?**
- A) `list.pop(0)`
- B) `collections.deque` with `append` / `popleft`
- C) `set`
- D) `dict`

<details><summary>Reveal Answer</summary>**B.** `deque` is O(1) at both ends.</details>

### Question 3 — Medium
**Why is `list.pop(0)` a poor dequeue?**
- A) It is O(n) — it shifts every remaining element
- B) It is O(1)
- C) It is FIFO
- D) It is not poor

<details><summary>Reveal Answer</summary>**A.** Shifting makes it linear.</details>

### Question 4 — Medium
**What does a priority queue return first?**
- A) The oldest element
- B) The highest-priority element, regardless of insertion order
- C) A random element
- D) The newest element

<details><summary>Reveal Answer</summary>**B.** Priority, not arrival, decides.</details>

### Question 5 — Medium
**What is a crash risk in BFS with a queue?**
- A) Not marking nodes visited when enqueuing, causing infinite loops
- B) Using a deque
- C) Sorting
- D) Using a set

<details><summary>Reveal Answer</summary>**A.** Mark on enqueue to avoid repeats.</details>

### Question 6 — Hard
**What is the purpose of a circular queue?**
- A) To sort
- B) To reuse freed slots in a fixed-size buffer with O(1) operations
- C) To prioritise
- D) To hash

<details><summary>Reveal Answer</summary>**B.** Modulo arithmetic reuses space.</details>

### Question 7 — Hard
**What does the sliding-window maximum use a monotonic deque for?**
- A) Sorting the window
- B) Keeping candidate maxima in decreasing order so the front is the current max
- C) Hashing
- D) Recursion

<details><summary>Reveal Answer</summary>**B.** Amortized O(n) across the array.</details>

### Question 8 — Hard
**How many stacks does it take to implement a queue, and at what cost?**
- A) One, O(1)
- B) Two; enqueue O(1) and dequeue amortized O(1)
- C) Three, O(n²)
- D) None

<details><summary>Reveal Answer</summary>**B.** Two stacks with a transfer step.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand queues. |
| 5-6 | Review BFS marking and monotonic deque. |
| < 5 | Re-read the lecture. |
