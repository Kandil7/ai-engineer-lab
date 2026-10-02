# DSA 09: Binary Search Trees — Quiz

> **Topic Overview**: The BST invariant, search/insert/delete, and validation.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the BST property?**
- A) Any shape
- B) Left subtree < node < right subtree, recursively
- C) Balanced
- D) Complete

<details><summary>Reveal Answer</summary>**B.** Ordering at every node.</details>

### Question 2 — Easy
**What is the average search time in a balanced BST?**
- A) O(1)
- B) O(log n)
- C) O(n)
- D) O(n²)

<details><summary>Reveal Answer</summary>**B.** Height-bounded.</details>

### Question 3 — Medium
**What is the worst-case height of an unbalanced BST?**
- A) O(1)
- B) O(log n)
- C) O(n) — a degenerate chain
- D) O(n²)

<details><summary>Reveal Answer</summary>**C.** Sorted insertions create a list.</details>

### Question 4 — Medium
**What traversal of a BST yields sorted order?**
- A) Preorder
- B) Inorder
- C) Postorder
- D) Level-order

<details><summary>Reveal Answer</summary>**B.** Inorder is sorted.</details>

### Question 5 — Medium
**Why is checking only immediate children wrong for validating a BST?**
- A) It is correct
- B) A node in the left subtree's right side can still exceed the root
- C) It is slow
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Range constraints must propagate.</details>

### Question 6 — Hard
**How do you delete a node with two children?**
- A) Remove it
- B) Replace with its inorder successor (or predecessor), then delete that node
- C) Swap subtrees
- D) Rehash

<details><summary>Reveal Answer</summary>**B.** Preserve the ordering.</details>

### Question 7 — Hard
**Building a BST from a sorted array by taking the middle as root gives what?**
- A) A degenerate chain
- B) A balanced BST of height O(log n)
- C) A heap
- D) A hash table

<details><summary>Reveal Answer</summary>**B.** Median splits balance.</details>

### Question 8 — Hard
**What is the inorder successor of a node with a right subtree?**
- A) Its parent
- B) The leftmost node of its right subtree
- C) Its right child
- D) The root

<details><summary>Reveal Answer</summary>**B.** Smallest greater value.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand BSTs. |
| 5-6 | Review validation and deletion. |
| < 5 | Re-read the lecture. |
