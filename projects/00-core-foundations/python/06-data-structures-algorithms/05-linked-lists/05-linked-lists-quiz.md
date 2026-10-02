# DSA 05: Linked Lists — Quiz

> **Topic Overview**: Node-based storage, singly/doubly lists, and pointer patterns.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the cost of inserting at the head of a singly linked list?**
- A) O(n)
- B) O(1)
- C) O(log n)
- D) O(n²)

<details><summary>Reveal Answer</summary>**B.** Repoint two links.</details>

### Question 2 — Easy
**What is the cost of accessing the k-th element?**
- A) O(1)
- B) O(k) — you must walk from the head
- C) O(log k)
- D) O(n²)

<details><summary>Reveal Answer</summary>**B.** No random access.</details>

### Question 3 — Medium
**What does Floyd's tortoise-and-hare detect?**
- A) A cycle
- B) The minimum
- C) A duplicate
- D) The length

<details><summary>Reveal Answer</summary>**A.** A fast and slow pointer meet inside a cycle.</details>

### Question 4 — Medium
**Why use a dummy node for head insertion/deletion?**
- A) For speed
- B) It removes the special case where the head changes
- C) It sorts the list
- D) It finds cycles

<details><summary>Reveal Answer</summary>**B.** Uniform handling of edges.</details>

### Question 5 — Medium
**How do you find the middle in one pass?**
- A) Count then walk again
- B) Slow moves one, fast moves two; when fast ends, slow is the middle
- C) Sort
- D) Hash

<details><summary>Reveal Answer</summary>**B.** Two-pointer trick.</details>

### Question 6 — Hard
**What is the classic bug when deleting a node?**
- A) Keeping the reference to the rest of the list
- B) Not losing the link to the remainder before unlinking
- C) Sorting
- D) Using a dummy node

<details><summary>Reveal Answer</summary>**B.** Save `next` before changing links.</details>

### Question 7 — Hard
**Why can merge sort be preferred for linked lists?**
- A) It is faster asymptotically only on lists
- B) It needs no random access, unlike quicksort's partitioning
- C) It uses less memory always
- D) It is stable in arrays only

<details><summary>Reveal Answer</summary>**B.** Merge works with sequential access.</details>

### Question 8 — Hard
**What extra link does a doubly linked list maintain, and what does it enable?**
- A) A hash; O(1) search
- B) A `prev` pointer; O(1) deletion given the node and backward traversal
- C) An index; O(1) access
- D) A counter; O(1) length

<details><summary>Reveal Answer</summary>**B.** Back-links cost memory but simplify removal.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand linked lists. |
| 5-6 | Review pointer patterns and dummy nodes. |
| < 5 | Re-read the lecture. |
