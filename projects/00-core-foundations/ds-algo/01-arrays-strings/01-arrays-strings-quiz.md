# DS-Algo 01: Arrays and Strings — Quiz

> **Topic Overview**: Indexing, slicing, two-pointer, and string building.

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

**Indexing an array is:**

- A) O(n)
- B) O(1)
- C) O(log n)
- D) O(n^2)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The address is computed, not searched.

</details>

---

### Question 2 — Easy

**Slicing a range of length k is:**

- A) O(1)
- B) O(k)
- C) O(n)
- D) O(log k)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The slice copies the range.

</details>

---

### Question 3 — Easy

**Appending to a list is:**

- A) O(n)
- B) Amortized O(1)
- C) O(log n)
- D) O(n^2)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Averaged over operations.

</details>

---

### Question 4 — Medium

**Inserting at the front of a list is:**

- A) O(1)
- B) O(n)
- C) O(log n)
- D) O(n^2)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Every element shifts.

</details>

---

### Question 5 — Medium

**The two-pointer pattern:**

- A) Uses three loops
- B) Scans from both ends or speeds
- C) Sorts the array
- D) Copies the array

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Solves many problems in one pass.

</details>

---

### Question 6 — Medium

**Strings in Python are:**

- A) Mutable
- B) Immutable
- C) Cached
- D) Sorted

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Every modification creates a new string.

</details>

---

### Question 7 — Medium

**Building a string in a loop is:**

- A) O(n)
- B) O(n^2)
- C) O(log n)
- D) O(1)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Each concatenation copies the growing string.

</details>

---

### Question 8 — Hard

**The fix for O(n^2) string building is:**

- A) A loop
- B) join
- C) Slicing
- D) Indexing

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: join builds the string in one pass.

</details>

---

### Question 9 — Hard

**The off-by-one bug is checked by:**

- A) Guessing
- B) Testing boundary conditions
- C) Caching
- D) Sorting

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Empty input, single element, last index.

</details>

---

### Question 10 — Hard**

**A sorted array can be searched in:**

- A) O(n)
- B) O(log n)
- C) O(1)
- D) O(n^2)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Binary search halves the range each step.

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
| 9-10 | Expert | Ready for hash maps |
| 7-8 | Proficient | Review operation costs |
| 5-6 | Developing | Re-study two-pointer |
| 0-4 | Novice | Restart the lecture |

---

**Next**: [02 - Hash Maps](02-hash-maps-quiz.md)