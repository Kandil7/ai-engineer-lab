# DSA 02: Arrays — Quiz

> **Topic Overview**: Contiguous storage, dynamic arrays, and the two-pointer family.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What gives an array O(1) random access?**
- A) Hashing
- B) Elements are at fixed offsets from the start
- C) Sorting
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Index arithmetic is constant time.</details>

### Question 2 — Easy
**What is the cost of inserting at the front of a Python list?**
- A) O(1)
- B) O(n) — all elements shift
- C) O(log n)
- D) O(n²)

<details><summary>Reveal Answer</summary>**B.** Front insertion shifts everything.</details>

### Question 3 — Medium
**What does a dynamic array do on resize?**
- A) Nothing
- B) Allocates a larger block and copies, giving amortized O(1) append
- C) Shifts one element
- D) Rehashes

<details><summary>Reveal Answer</summary>**B.** Growth doubles and amortizes.</details>

### Question 4 — Medium
**In the two-sum problem, what does a hash map buy over nested loops?**
- A) Less memory
- B) O(n) time instead of O(n²)
- C) Sorting
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Store complements for one-pass lookup.</details>

### Question 5 — Medium
**What does the two-pointer technique require?**
- A) A hash map
- B) A sorted array (for the sum variant)
- C) Recursion
- D) A queue

<details><summary>Reveal Answer</summary>**B.** Order lets pointers move decisively.</details>

### Question 6 — Hard
**Why does moving the smaller pointer in two-sum (sorted) preserve correctness?**
- A) It is arbitrary
- B) A smaller left bound cannot form the target with any larger right, so it is safely discarded
- C) It sorts the array
- D) It reduces memory

<details><summary>Reveal Answer</summary>**B.** The discarded pairs cannot be solutions.</details>

### Question 7 — Hard
**Why is `arr[i:i+k]` inside a loop a common performance bug?**
- A) It is O(1)
- B) Each slice allocates a new list, turning the loop into O(n·k) memory churn
- C) It sorts the array
- D) It is faster

<details><summary>Reveal Answer</summary>**B.** Slices copy.</details>

### Question 8 — Hard
**What does the sliding-window technique trade for its speed?**
- A) Memory for time only
- B) It reuses overlapping work by adding and removing one element per step
- C) Sorting
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** O(1) update per window slide.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand arrays and patterns. |
| 5-6 | Review two-pointer and sliding window. |
| < 5 | Re-read the lecture. |
