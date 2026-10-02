# DSA 15: Selection Sort — Quiz

> **Topic Overview**: Repeated minimum selection, swap count, and instability.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does selection sort do each pass?**
- A) Swap adjacent
- B) Find the minimum of the unsorted part and swap it into place
- C) Partition
- D) Merge

<details><summary>Reveal Answer</summary>**B.** One swap per pass.</details>

### Question 2 — Easy
**What is the time complexity?**
- A) O(n)
- B) O(n²)
- C) O(n log n)
- D) O(log n)

<details><summary>Reveal Answer</summary>**B.** Comparisons dominate.</details>

### Question 3 — Medium
**How many swaps does selection sort do at most?**
- A) n²
- B) n − 1
- C) n log n
- D) 0

<details><summary>Reveal Answer</summary>**B.** One per outer pass.</details>

### Question 4 — Medium
**Is selection sort stable?**
- A) Yes
- B) No, the long-distance swap can reorder equal keys
- C) Only ascending
- D) Only for integers

<details><summary>Reveal Answer</summary>**B.** Swaps cross equal elements.</details>

### Question 5 — Medium
**When is selection sort attractive?**
- A) Large random arrays
- B) When writes are expensive (flash memory) — fewest swaps
- C) Linked lists only
- D) Never

<details><summary>Reveal Answer</summary>**B.** Minimise writes.</details>

### Question 6 — Hard
**Why does selection sort do the same number of comparisons on sorted input?**
- A) It detects order
- B) It always scans the unsorted region fully; no early exit
- C) It is adaptive
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Not adaptive.</details>

### Question 7 — Hard
**What is the classic mistake in the inner loop?**
- A) Swapping during the search instead of after finding the true minimum
- B) Using a temp variable
- C) Tracking the index
- D) Starting at 0

<details><summary>Reveal Answer</summary>**A.** Find first, swap once.</details>

### Question 8 — Hard
**Which sort would you choose if stability matters?**
- A) Selection
- B) Insertion or merge
- C) Quick (Lomuto)
- D) Heap

<details><summary>Reveal Answer</summary>**B.** Stable sorts preserve order.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand selection sort. |
| 5-6 | Review swap count and stability. |
| < 5 | Re-read the lecture. |
