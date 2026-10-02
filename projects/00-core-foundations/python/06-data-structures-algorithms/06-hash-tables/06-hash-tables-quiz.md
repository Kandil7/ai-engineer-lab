# DSA 06: Hash Tables — Quiz

> **Topic Overview**: Hashing, collisions, load factor, and Python dict/set internals.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does a hash function map a key to?**
- A) A sorted position
- B) A bucket index
- C) A linked list
- D) A tree

<details><summary>Reveal Answer</summary>**B.** Key to index.</details>

### Question 2 — Easy
**What is the average lookup time in a hash table?**
- A) O(n)
- B) O(1)
- C) O(log n)
- D) O(n²)

<details><summary>Reveal Answer</summary>**B.** With a good hash and load factor.</details>

### Question 3 — Medium
**What is a collision?**
- A) Two keys hash to the same bucket
- B) A key is missing
- C) The table is full
- D) A key is unhashable

<details><summary>Reveal Answer</summary>**A.** Distinct keys, same slot.</details>

### Question 4 — Medium
**Why can't a Python list be a dict key?**
- A) Too large
- B) Lists are mutable, so they are unhashable
- C) Lists are unordered
- D) They can be

<details><summary>Reveal Answer</summary>**B.** Mutable keys break invariants.</details>

### Question 5 — Medium
**What does the load factor measure, and what does rehashing do?**
- A) Time; sorts
- B) Entries per bucket; it grows the table and redistributes
- C) Memory; compresses
- D) Length; truncates

<details><summary>Reveal Answer</summary>**B.** High load triggers a resize.</details>

### Question 6 — Hard
**Why is hash-table worst case O(n), not O(1)?**
- A) It is always O(1)
- B) All keys can collide into one bucket, degrading to a linear scan
- C) Rehashing is slow
- D) Keys are unsorted

<details><summary>Reveal Answer</summary>**B.** Adversarial or poor hashing destroys the average.</details>

### Question 7 — Hard
**Why does a hash map beat nested loops for two-sum?**
- A) Less memory
- B) It stores complements, giving O(n) time instead of O(n²)
- C) It sorts
- D) It is not better

<details><summary>Reveal Answer</summary>**B.** One pass plus lookup.</details>

### Question 8 — Hard
**Group-anagrams uses a dict keyed by what, and why?**
- A) The word; to look up
- B) The sorted word (or a count tuple); anagrams share it
- C) The length; to sort
- D) A hash of the raw word

<details><summary>Reveal Answer</summary>**B.** Canonical form groups them.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand hash tables. |
| 5-6 | Review collisions and load factor. |
| < 5 | Re-read the lecture. |
