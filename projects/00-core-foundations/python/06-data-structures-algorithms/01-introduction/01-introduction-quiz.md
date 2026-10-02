# DSA 01: Introduction to Data Structures & Algorithms — Quiz

> **Topic Overview**: Data structures, algorithm analysis, Big-O, and case analysis.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a data structure?**
- A) A sorting routine
- B) A way of organising data so operations are efficient
- C) A CPU instruction
- D) A file format

<details><summary>Reveal Answer</summary>**B.** Organisation enables efficient operations.</details>

### Question 2 — Easy
**What does O(1) mean?**
- A) One operation
- B) Constant time regardless of input size
- C) Linear time
- D) Quadratic time

<details><summary>Reveal Answer</summary>**B.** Growth, not a literal count.</details>

### Question 3 — Medium
**Which grows slowest as n increases?**
- A) O(n)
- B) O(n²)
- C) O(log n)
- D) O(2ⁿ)

<details><summary>Reveal Answer</summary>**C.** Logarithmic growth is the slowest listed.</details>

### Question 4 — Medium
**Why is `in` on a Python list O(n) but `in` on a set O(1)?**
- A) Sets are smaller
- B) A set hashes; a list scans
- C) Lists are immutable
- D) They are the same

<details><summary>Reveal Answer</summary>**B.** Hashing gives constant average lookup.</details>

### Question 5 — Medium
**What does amortized O(1) mean for `list.append`?**
- A) Always O(1)
- B) Occasional resize cost spread over many appends
- C) Always O(n)
- D) It uses no memory

<details><summary>Reveal Answer</summary>**B.** Resizes are rare and averaged out.</details>

### Question 6 — Hard
**A function is O(n) time but O(n²) space. Is that possible?**
- A) No
- B) Yes; time and space are independent axes
- C) Only for sorting
- D) Only in C

<details><summary>Reveal Answer</summary>**B.** The axes are independent.</details>

### Question 7 — Hard
**Why is O(100n) considered the same as O(n)?**
- A) They are not
- B) Big-O drops constant factors
- C) Because n is large
- D) Because of caching

<details><summary>Reveal Answer</summary>**B.** Constants do not change the growth class.</details>

### Question 8 — Hard
**For n=10, is O(n²) necessarily slower than O(n)?**
- A) Yes always
- B) No; Big-O describes scaling, not absolute speed at small n
- C) Only in Python
- D) Only if n>100

<details><summary>Reveal Answer</summary>**B.** 100 operations can beat a high-constant O(n) at small n.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can reason about complexity. |
| 5-6 | Review Big-O and case analysis. |
| < 5 | Re-read the lecture. |
