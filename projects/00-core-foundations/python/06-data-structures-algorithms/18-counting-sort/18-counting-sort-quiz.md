# DSA 18: Counting Sort — Quiz

> **Topic Overview**: Integer key counting, non-comparison O(n + k), and stability.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What kind of keys must counting sort use?**
- A) Any comparable
- B) Integers in a known, bounded range
- C) Strings only
- D) Floats only

<details><summary>Reveal Answer</summary>**B.** It indexes a count array by value.</details>

### Question 2 — Easy
**What is its time complexity?**
- A) O(n log n)
- B) O(n + k), where k is the key range
- C) O(n²)
- D) O(log n)

<details><summary>Reveal Answer</summary>**B.** Non-comparison sort.</details>

### Question 3 — Medium
**What is the count array indexed by?**
- A) Position
- B) Value
- C) Hash
- D) Random

<details><summary>Reveal Answer</summary>**B.** count[value] = frequency.</details>

### Question 4 — Medium
**Why are cumulative counts needed?**
- A) For stability and placement
- B) To reduce memory
- C) To hash
- D) They are not

<details><summary>Reveal Answer</summary>**A.** They give each element's output slot.</details>

### Question 5 — Medium
**How is stability achieved in the output pass?**
- A) Forward traversal
- B) Backward traversal so equal keys keep relative order
- C) Sorting again
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Right-to-left preserves order.</details>

### Question 6 — Hard
**Why can counting sort be slower than quicksort?**
- A) It is not
- B) A huge key range makes the k-sized count array dominate
- C) It is unstable
- D) It needs comparisons

<details><summary>Reveal Answer</summary>**B.** O(n + k) with large k is bad.</details>

### Question 7 — Hard
**How do you handle negative numbers?**
- A) You cannot
- B) Offset keys by min(keys) so indices are non-negative
- C) Sort descending
- D) Hash them

<details><summary>Reveal Answer</summary>**B.** Shift into range.</details>

### Question 8 — Hard
**Why must the count array be sized `max + 1`?**
- A) For speed
- B) To include index `max` itself
- C) To sort
- D) For stability

<details><summary>Reveal Answer</summary>**B.** Off-by-one crashes on the max value.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand counting sort. |
| 5-6 | Review cumulative counts and stability. |
| < 5 | Re-read the lecture. |
