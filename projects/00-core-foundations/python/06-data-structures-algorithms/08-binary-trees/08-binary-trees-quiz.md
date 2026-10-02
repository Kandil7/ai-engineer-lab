# DSA 08: Binary Trees — Quiz

> **Topic Overview**: Binary nodes, traversal orders, and recursive tree problems.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**How many children can a binary-tree node have?**
- A) Any number
- B) At most two
- C) Exactly two
- D) One

<details><summary>Reveal Answer</summary>**B.** Left and right.</details>

### Question 2 — Easy
**What order is inorder traversal (on a binary tree)?**
- A) Root, left, right
- B) Left, root, right
- C) Left, right, root
- D) Right, root, left

<details><summary>Reveal Answer</summary>**B.** Left, root, right.</details>

### Question 3 — Medium
**In an iterative preorder, why push the right child first?**
- A) It is arbitrary
- B) The stack is LIFO, so pushing right first makes left pop first
- C) To sort
- D) To save memory

<details><summary>Reveal Answer</summary>**B.** Order of pushes reverses on pop.</details>

### Question 4 — Medium
**How many nodes does a full binary tree of height h have at most?**
- A) h
- B) 2h
- C) 2^(h+1) − 1 (with height h as edge count convention aside, exponential)
- D) h²

<details><summary>Reveal Answer</summary>**C.** Each level doubles.</details>

### Question 5 — Medium
**What does inverting a binary tree do?**
- A) Sorts it
- B) Swaps every node's left and right children
- C) Balances it
- D) Deletes leaves

<details><summary>Reveal Answer</summary>**B.** A mirror image.</details>

### Question 6 — Hard
**In a general binary tree, is left < root < right guaranteed?**
- A) Yes
- B) No; that is the BST property only
- C) Only for full trees
- D) Only for complete trees

<details><summary>Reveal Answer</summary>**B.** No ordering without BST.</details>

### Question 7 — Hard
**What is the maximum path sum problem asking for?**
- A) Longest path by edges
- B) The largest sum along any downward path, possibly through the root
- C) Number of leaves
- D) The height

<details><summary>Reveal Answer</summary>**B.** Combine best downward gains.</details>

### Question 8 — Hard
**Why is serialization of a binary tree tricky?**
- A) It is not
- B) You must record null placeholders to preserve shape and enable exact reconstruction
- C) Trees are cyclic
- D) Nodes are hashable

<details><summary>Reveal Answer</summary>**B.** Shape needs explicit markers.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand binary trees. |
| 5-6 | Review traversal orders and LCA. |
| < 5 | Re-read the lecture. |
