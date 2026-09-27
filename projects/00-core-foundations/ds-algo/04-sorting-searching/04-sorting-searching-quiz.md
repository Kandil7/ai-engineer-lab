# DS-Algo 04: Sorting and Searching — Quiz

> **Topic Overview**: Sort costs, binary search, and the search choice.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 10 |
| Correct Answers | 0 |
| Score | 0% |

---

## Questions

### Question 1 — Easy

**The built-in sort is:**

- A) O(n^2)
- B) O(n log n)
- C) O(n)
- D) O(log n)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Timsort, O(n) on nearly-sorted input.

</details>

---

### Question 2 — Easy

**Binary search requires:**

- A) Any data
- B) Sorted data
- C) A hash map
- D) A cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Halving the range assumes order.

</details>

---

### Question 3 — Easy

**Binary search is:**

- A) O(n)
- B) O(log n)
- C) O(n^2)
- D) O(1)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Each step halves the range.

</details>

---

### Question 4 — Medium

**Linear search is:**

- A) O(log n)
- B) O(n)
- C) O(n^2)
- D) O(1)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Scans every element.

</details>

---

### Question 5 — Medium

**Sorting once costs:**

- A) O(n)
- B) O(n log n)
- C) O(log n)
- D) O(1)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Then searches cost O(log n) each.

</details>

---

### Question 6 — Medium

**Binary search on unsorted data:**

- A) Works
- B) Gives wrong results
- C) Is faster
- D) Is cached

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The halving assumes order.

</details>

---

### Question 7 — Medium

**bisect_left finds:**

- A) The target
- B) The insertion point
- C) The sort
- D) The cache

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Where an element belongs, in O(log n).

</details>

---

### Question 8 — Hard

**The binary search loop condition is:**

- A) lo < hi
- B) lo <= hi
- C) lo == hi
- D) lo >= hi

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The single-element case needs the equality.

</details>

---

### Question 9 — Hard

**The mid adjustment is:**

- A) lo = mid
- B) lo = mid + 1 or hi = mid - 1
- C) hi = mid
- D) lo = hi

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Otherwise the range never shrinks.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for searching is:**

- A) Linear search always
- B) Binary search on sorted data
- C) No search
- D) Cached search

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The right search for the data.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Hard |
| 9 | B | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | DS-Algo section complete |
| 7-8 | Proficient | Review binary search |
| 5-6 | Developing | Re-study sort costs |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [03 - Recursion](03-recursion-quiz.md)