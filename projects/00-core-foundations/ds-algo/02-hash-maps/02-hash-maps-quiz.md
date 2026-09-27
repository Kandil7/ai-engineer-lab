# DS-Algo 02: Hash Maps — Quiz

> **Topic Overview**: O(1) lookups, counting, deduplication, two-sum.

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

**Hash map lookup is:**

- A) O(n)
- B) O(1) average
- C) O(log n)
- D) O(n^2)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The hash goes straight to the bucket.

</details>

---

### Question 2 — Easy

**A collision is:**

- A) Two keys in the same bucket
- B) A missing key
- C) A duplicate value
- D) A sorted map

<details>
<summary>Reveal Answer</summary>

**Correct Answer: A**

**Explanation**: The bucket stores both; the lookup scans it.

</details>

---

### Question 3 — Easy

**A set is used for:**

- A) Key-value pairs
- B) Membership tests
- C) Sorted access
- D) Indexing

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Keys with no values.

</details>

---

### Question 4 — Medium

**A pathological hash degrades the map to:**

- A) O(1)
- B) O(n)
- C) O(log n)
- D) O(n^2)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Every lookup scans a huge bucket.

</details>

---

### Question 5 — Medium

**Counting in a hash map is:**

- A) Two passes
- B) One pass
- C) O(n^2)
- D) Sorted

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: counts[x] = counts.get(x, 0) + 1.

</details>

---

### Question 6 — Medium

**Two-sum runs in:**

- A) O(n^2)
- B) O(n)
- C) O(log n)
- D) O(1)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: One pass with the complement check.

</details>

---

### Question 7 — Medium

**A list for membership tests is:**

- A) O(1)
- B) O(n)
- C) O(log n)
- D) O(n^2)

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The list is scanned.

</details>

---

### Question 8 — Hard

**Mutable keys are:**

- A) Hashable
- B) Unhashable
- C) Cached
- D) Sorted

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Lists and dicts cannot be keys.

</details>

---

### Question 9 — Hard

**A map when a set suffices is:**

- A) Correct
- B) A mistake
- C) Faster
- D) Required

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Use the minimal structure.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for lookups is:**

- A) Lists are used
- B) Hash maps are used for O(1) lookups
- C) Sorting is used
- D) Caching is used

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: O(1) average lookup.

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
| 9-10 | Expert | Ready for recursion |
| 7-8 | Proficient | Review collisions |
| 5-6 | Developing | Re-study two-sum |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [01 - Arrays](01-arrays-strings-quiz.md) | **Next**: [03 - Recursion](03-recursion-quiz.md)