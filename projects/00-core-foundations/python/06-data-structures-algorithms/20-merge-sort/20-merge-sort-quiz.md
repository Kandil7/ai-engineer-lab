# DSA 20: Merge Sort — Quiz

> **Topic Overview**: Divide-and-conquer, the merge step, stability, and O(n log n).

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is merge sort's strategy?**
- A) Partition
- B) Divide in half, sort each half, merge
- C) Count
- D) Hash

<details><summary>Reveal Answer</summary>**B.** Divide and conquer.</details>

### Question 2 — Easy
**What is the guaranteed time complexity?**
- A) O(n)
- B) O(n log n) in all cases
- C) O(n²)
- D) O(log n)

<details><summary>Reveal Answer</summary>**B.** No bad case.</details>

### Question 3 — Medium
**Why is merge sort stable?**
- A) It is not
- B) On ties, the left run's element is taken first (`<=`)
- C) It sorts descending
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Left-before-right preserves order.</details>

### Question 4 — Medium
**What is the space cost of standard merge sort?**
- A) O(1)
- B) O(n) for the merged array
- C) O(log n)
- D) O(n²)

<details><summary>Reveal Answer</summary>**B.** Auxiliary buffer.</details>

### Question 5 — Medium
**What is bottom-up merge sort?**
- A) Recursive
- B) Iterative: merge runs of width 1, 2, 4, … avoiding recursion
- C) A heap
- D) A hash

<details><summary>Reveal Answer</summary>**B.** Doubling run widths.</details>

### Question 6 — Hard
**What is the merge step's classic bug?**
- A) Using a temp array
- B) Forgetting to append the remaining elements of one run
- C) Comparing keys
- D) Copying back

<details><summary>Reveal Answer</summary>**B.** Leftover elements must be drained.</details>

### Question 7 — Hard
**What does counting inversions with merge sort exploit?**
- A) The base case
- B) Every cross-run inversion is counted during the merge
- C) Hashing
- D) Pivoting

<details><summary>Reveal Answer</summary>**B.** O(n log n) inversion count.</details>

### Question 8 — Hard
**Why is merge sort preferred for linked lists and external sorting?**
- A) It needs random access
- B) It is sequential-access friendly and streams well to disk
- C) It is in-place
- D) It is unstable

<details><summary>Reveal Answer</summary>**B.** No random access required.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand merge sort. |
| 5-6 | Review the merge step and stability. |
| < 5 | Re-read the lecture. |
