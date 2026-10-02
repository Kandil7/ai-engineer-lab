# DSA 17: Quick Sort — Quiz

> **Topic Overview**: Partitioning, pivot choice, average vs worst case, and duplicates.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the core step of quicksort?**
- A) Merge
- B) Partition around a pivot
- C) Count
- D) Hash

<details><summary>Reveal Answer</summary>**B.** Elements split by pivot.</details>

### Question 2 — Easy
**What is the average time complexity?**
- A) O(n)
- B) O(n log n)
- C) O(n²)
- D) O(log n)

<details><summary>Reveal Answer</summary>**B.** Balanced partitions.</details>

### Question 3 — Medium
**When does quicksort hit O(n²)?**
- A) Never
- B) When partitions are maximally unbalanced (e.g. sorted input with a bad pivot)
- C) On small arrays
- D) With duplicates only

<details><summary>Reveal Answer</summary>**B.** Pivot choice decides.</details>

### Question 4 — Medium
**Why randomize the pivot?**
- A) For stability
- B) To make the expected case O(n log n) regardless of input order
- C) To save memory
- D) To sort descending

<details><summary>Reveal Answer</summary>**B.** Avoid adversarial worst cases.</details>

### Question 5 — Medium
**Is quicksort stable?**
- A) Yes
- B) Not by default; partitioning swaps distant elements
- C) Only with Lomuto
- D) Only with Hoare

<details><summary>Reveal Answer</summary>**B.** In-place partitions are unstable.</details>

### Question 6 — Hard
**What does three-way partitioning fix?**
- A) Stability
- B) Many duplicate keys causing unbalanced partitions
- C) Memory
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Groups `<`, `=`, `>`.</details>

### Question 7 — Hard
**What is quickselect?**
- A) A full sort
- B) Partial quicksort that finds the k-th smallest in O(n) average
- C) A merge
- D) A hash

<details><summary>Reveal Answer</summary>**B.** Recurse into one side only.</details>

### Question 8 — Hard
**Why can sorted input cause a stack overflow?**
- A) It cannot
- B) With a first/last pivot, recursion depth becomes O(n)
- C) It sorts
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Random or median-of-three fixes it.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand quicksort. |
| 5-6 | Review pivot choice and partitioning. |
| < 5 | Re-read the lecture. |
