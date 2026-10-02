# DSA 13: Binary Search — Quiz

> **Topic Overview**: Halving a sorted range, boundary variants, and pitfalls.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What precondition does binary search require?**
- A) Unique elements
- B) A sorted array
- C) A hash function
- D) A heap

<details><summary>Reveal Answer</summary>**B.** Order enables halving.</details>

### Question 2 — Easy
**What is the time complexity?**
- A) O(n)
- B) O(log n)
- C) O(1)
- D) O(n log n)

<details><summary>Reveal Answer</summary>**B.** The range halves each step.</details>

### Question 3 — Medium
**Why use `low + (high - low) // 2` instead of `(low + high) // 2`?**
- A) It is faster
- B) It avoids integer overflow in fixed-width languages
- C) It sorts
- D) They differ in Python results

<details><summary>Reveal Answer</summary>**B.** Safe midpoint.</details>

### Question 4 — Medium
**Why update `low = mid + 1` and not `low = mid`?**
- A) For speed
- B) `low = mid` can loop forever when not found
- C) It sorts
- D) They are equal

<details><summary>Reveal Answer</summary>**B.** Must make progress.</details>

### Question 5 — Medium
**How do you find the first occurrence with duplicates?**
- A) Any match
- B) On a match, record it and keep searching the left half
- C) Sort again
- D) Use linear search

<details><summary>Reveal Answer</summary>**B.** Shrink left to find the boundary.</details>

### Question 6 — Hard
**What is the boundary-variant loop invariant?**
- A) The answer is always mid
- B) The target, if present, is always within [low, high]
- C) The array is unsorted
- D) Mid is the peak

<details><summary>Reveal Answer</summary>**B.** Invariant preserves correctness.</details>

### Question 7 — Hard
**How does binary search find a peak element?**
- A) It cannot
- B) Compare mid with its neighbour and move toward the higher side
- C) Sort
- D) Hash

<details><summary>Reveal Answer</summary>**B.** Local ascent guarantees a peak.</details>

### Question 8 — Hard
**What does Python's `bisect` module provide?**
- A) Sorting
- B) Binary-search insertion points (`bisect_left/right`)
- C) Hashing
- D) Heaps

<details><summary>Reveal Answer</summary>**B.** Library boundary search.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand binary search. |
| 5-6 | Review boundary variants and pitfalls. |
| < 5 | Re-read the lecture. |
