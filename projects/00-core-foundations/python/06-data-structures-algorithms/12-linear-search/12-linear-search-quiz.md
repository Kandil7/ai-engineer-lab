# DSA 12: Linear Search — Quiz

> **Topic Overview**: Sequential search, its cost, and the sentinel/sorted variants.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the worst-case time of linear search?**
- A) O(1)
- B) O(n)
- C) O(log n)
- D) O(n²)

<details><summary>Reveal Answer</summary>**B.** Target last or absent.</details>

### Question 2 — Easy
**When is linear search the only option?**
- A) Sorted arrays
- B) Unsorted data or linked lists without random access
- C) Hash tables
- D) Heaps

<details><summary>Reveal Answer</summary>**B.** No precondition available.</details>

### Question 3 — Medium
**What does the sentinel variant remove?**
- A) The comparison
- B) The per-iteration bounds check
- C) The target
- D) The array

<details><summary>Reveal Answer</summary>**B.** One comparison becomes one.</details>

### Question 4 — Medium
**Why is the sentinel variant risky?**
- A) It sorts the array
- B) It mutates the array; a failure before restore corrupts state
- C) It is O(n²)
- D) It cannot find the target

<details><summary>Reveal Answer</summary>**B.** Mutation without restore is a bug.</details>

### Question 5 — Medium
**On sorted data, what does the early-exit guard add?**
- A) Nothing
- B) It returns −1 as soon as an element exceeds the target
- C) It sorts
- D) It hashes

<details><summary>Reveal Answer</summary>**B.** Safe only when sorted.</details>

### Question 6 — Hard
**What is the average number of comparisons for a successful search in an array of size n?**
- A) 1
- B) ~n/2
- C) n
- D) log n

<details><summary>Reveal Answer</summary>**B.** Still O(n).</details>

### Question 7 — Hard
**Why can interpolation search beat binary search?**
- A) It is O(1)
- B) On uniformly distributed data it estimates the position, reaching O(log log n)
- C) It needs no sorting
- D) It uses hashing

<details><summary>Reveal Answer</summary>**B.** Distribution helps the estimate.</details>

### Question 8 — Hard
**What is the space complexity of all linear-search variants taught here?**
- A) O(n)
- B) O(1)
- C) O(log n)
- D) O(n²)

<details><summary>Reveal Answer</summary>**B.** Only a few variables.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand linear search. |
| 5-6 | Review the variants and their preconditions. |
| < 5 | Re-read the lecture. |
