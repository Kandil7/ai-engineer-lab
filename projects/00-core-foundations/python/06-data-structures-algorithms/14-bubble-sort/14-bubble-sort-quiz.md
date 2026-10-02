# DSA 14: Bubble Sort — Quiz

> **Topic Overview**: Adjacent swaps, early termination, stability, and cocktail sort.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does bubble sort repeatedly do?**
- A) Picks the minimum
- B) Swaps adjacent elements that are out of order
- C) Partitions
- D) Merges

<details><summary>Reveal Answer</summary>**B.** Larger values bubble right.</details>

### Question 2 — Easy
**What is the worst-case time?**
- A) O(n)
- B) O(n²)
- C) O(n log n)
- D) O(log n)

<details><summary>Reveal Answer</summary>**B.** Two nested loops.</details>

### Question 3 — Medium
**What does tracking swaps enable?**
- A) Stability
- B) Early termination when a pass makes no swaps (already sorted)
- C) Less memory
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Best case becomes O(n).</details>

### Question 4 — Medium
**Why should the inner loop stop at `n - i - 1`?**
- A) Style
- B) The last i elements are already sorted
- C) To sort descending
- D) To avoid stability

<details><summary>Reveal Answer</summary>**B.** Shrink the unsorted region.</details>

### Question 5 — Medium
**Is bubble sort stable?**
- A) No
- B) Yes, when it swaps only on strict `>`
- C) Only descending
- D) Only for integers

<details><summary>Reveal Answer</summary>**B.** Equal elements keep order.</details>

### Question 6 — Hard
**What problem does cocktail shaker sort fix?**
- A) Stability
- B) A small element near the end moves only one slot per pass in plain bubble sort
- C) Memory
- D) Hashing

<details><summary>Reveal Answer</summary>**B.** Bidirectional passes move turtles faster.</details>

### Question 7 — Hard
**Why is `>=` in the swap condition a bug?**
- A) It is not
- B) It swaps equal elements, breaking stability
- C) It is slower
- D) It sorts descending

<details><summary>Reveal Answer</summary>**B.** Strict `>` preserves order.</details>

### Question 8 — Hard
**When is bubble sort a reasonable choice?**
- A) Large random arrays
- B) Small, nearly sorted arrays
- C) Linked lists only
- D) Never

<details><summary>Reveal Answer</summary>**B.** Early exit exploits near-sortedness.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand bubble sort. |
| 5-6 | Review early exit and stability. |
| < 5 | Re-read the lecture. |
