# DSA 19: Radix Sort — Quiz

> **Topic Overview**: Digit-by-digit sorting, LSD vs MSD, and the stability requirement.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does radix sort process?**
- A) The whole value
- B) One digit at a time, LSD or MSD
- C) Hashes
- D) Pivots

<details><summary>Reveal Answer</summary>**B.** Digit by digit.</details>

### Question 2 — Easy
**Which sub-sort must radix sort use, and why?**
- A) Any
- B) A stable one, or previous digit order is destroyed
- C) Quicksort
- D) Heapsort

<details><summary>Reveal Answer</summary>**B.** Stability is mandatory.</details>

### Question 3 — Medium
**What is the time complexity for n keys of d digits in base b?**
- A) O(n log n)
- B) O(d(n + b))
- C) O(n²)
- D) O(log n)

<details><summary>Reveal Answer</summary>**B.** d passes of counting sort.</details>

### Question 4 — Medium
**Which order does LSD radix sort use?**
- A) Most significant first
- B) Least significant digit first
- C) Random
- D) Sorted

<details><summary>Reveal Answer</summary>**B.** LSD processes from the right.</details>

### Question 5 — Medium
**When is radix sort a poor choice?**
- A) Many integers
- B) Keys with a large range / many digits, or non-integer keys
- C) Small arrays
- D) Fixed-width integers

<details><summary>Reveal Answer</summary>**B.** d grows with key width.</details>

### Question 6 — Hard
**What does MSD radix sort enable that LSD does not?**
- A) Stability
- B) Partial/streaming sorts and early stopping (it buckets by the top digit first)
- C) Less memory always
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Top-down partitioning.</details>

### Question 7 — Hard
**How are negative numbers handled?**
- A) They cannot be
- B) Separate them, sort magnitudes, then merge reversed
- C) Hash them
- D) Sort descending

<details><summary>Reveal Answer</summary>**B.** Sign split plus magnitude sort.</details>

### Question 8 — Hard
**What is the classic implementation bug?**
- A) Using a stable sort
- B) Forgetting to copy the output array back before the next pass
- C) Using base 10
- D) Extracting digits

<details><summary>Reveal Answer</summary>**B.** Each pass must feed the next.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand radix sort. |
| 5-6 | Review LSD/MSD and stability. |
| < 5 | Re-read the lecture. |
