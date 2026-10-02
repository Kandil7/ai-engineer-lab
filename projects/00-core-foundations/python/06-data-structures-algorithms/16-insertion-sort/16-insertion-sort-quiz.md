# DSA 16: Insertion Sort — Quiz

> **Topic Overview**: Building a sorted prefix, adaptivity, stability, and hybrid use.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does insertion sort maintain as it scans?**
- A) A sorted suffix
- B) A sorted prefix, inserting each new element into place
- C) A heap
- D) A hash table

<details><summary>Reveal Answer</summary>**B.** Grow the sorted region.</details>

### Question 2 — Easy
**What is the worst-case time?**
- A) O(n)
- B) O(n²)
- C) O(n log n)
- D) O(log n)

<details><summary>Reveal Answer</summary>**B.** Reverse-sorted input.</details>

### Question 3 — Medium
**Why is insertion sort adaptive?**
- A) It detects sortedness and becomes O(n) on nearly sorted input
- B) It sorts descending
- C) It uses hashing
- D) It is not adaptive

<details><summary>Reveal Answer</summary>**A.** Few shifts when nearly sorted.</details>

### Question 4 — Medium
**Is insertion sort stable?**
- A) No
- B) Yes, when shifting only on strict `>`
- C) Only descending
- D) Only for integers

<details><summary>Reveal Answer</summary>**B.** Equal keys keep order.</details>

### Question 5 — Medium
**Why does the outer loop start at index 1?**
- A) Index 0 is already a sorted prefix of length 1
- B) To skip the smallest
- C) To sort descending
- D) For speed

<details><summary>Reveal Answer</summary>**A.** A single element is sorted.</details>

### Question 6 — Hard
**Why must the key be stored before shifting?**
- A) For speed
- B) Shifting overwrites the slot; without saving the key first the value is lost
- C) To sort
- D) It need not be

<details><summary>Reveal Answer</summary>**B.** Save then shift then place.</details>

### Question 7 — Hard
**How is insertion sort used in practice?**
- A) Never
- B) As the small-run base case inside hybrid sorts (e.g. Timsort)
- C) Only for strings
- D) For large arrays

<details><summary>Reveal Answer</summary>**B.** Fast on small or near-sorted runs.</details>

### Question 8 — Hard
**What is binary insertion sort?**
- A) A different algorithm
- B) It binary-searches the insertion point, cutting comparisons but not shifts
- C) A stable radix sort
- D) A heap sort

<details><summary>Reveal Answer</summary>**B.** Fewer comparisons, same O(n²) shifts.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand insertion sort. |
| 5-6 | Review adaptivity and stability. |
| < 5 | Re-read the lecture. |
