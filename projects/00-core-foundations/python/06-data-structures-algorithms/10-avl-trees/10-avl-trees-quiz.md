# DSA 10: AVL Trees — Quiz

> **Topic Overview**: Balance factor, four rotation cases, and guaranteed O(log n).

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does an AVL tree guarantee?**
- A) O(1) search
- B) Height stays O(log n) by rebalancing
- C) Sorted leaves only
- D) No rotations

<details><summary>Reveal Answer</summary>**B.** Strict balance.</details>

### Question 2 — Easy
**How is the balance factor defined?**
- A) Right height − left height
- B) Left height − right height
- C) Node count
- D) Depth

<details><summary>Reveal Answer</summary>**B.** Left minus right.</details>

### Question 3 — Medium
**What balance factors are allowed in AVL?**
- A) Any
- B) −1, 0, +1 only
- C) 0 only
- D) ±2

<details><summary>Reveal Answer</summary>**B.** Beyond that, rotate.</details>

### Question 4 — Medium
**Left-Left imbalance is fixed by which rotation?**
- A) Left rotation
- B) Right rotation
- C) Left then right
- D) Right then left

<details><summary>Reveal Answer</summary>**B.** Single right rotation.</details>

### Question 5 — Medium
**Left-Right imbalance is fixed by which rotations?**
- A) Right only
- B) Left on the child, then right on the node
- C) Left only
- D) None

<details><summary>Reveal Answer</summary>**B.** Double rotation.</details>

### Question 6 — Hard
**Why must heights be updated after a rotation?**
- A) For speed
- B) Balance factors depend on them; stale heights corrupt later decisions
- C) To sort
- D) They need not

<details><summary>Reveal Answer</summary>**B.** Height is the invariant's input.</details>

### Question 7 — Hard
**What is the height of an AVL tree with n nodes?**
- A) O(n)
- B) O(log n)
- C) O(√n)
- D) O(1)

<details><summary>Reveal Answer</summary>**B.** Balanced by construction.</details>

### Question 8 — Hard
**How does AVL differ from a plain BST?**
- A) AVL allows duplicates only
- B) AVL rebalances to bound height; a plain BST can degenerate
- C) AVL uses hashing
- D) They are identical

<details><summary>Reveal Answer</summary>**B.** Rebalancing buys the guarantee.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand AVL balancing. |
| 5-6 | Review the four rotation cases. |
| < 5 | Re-read the lecture. |
