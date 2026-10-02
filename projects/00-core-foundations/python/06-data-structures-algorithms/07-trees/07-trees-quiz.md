# DSA 07: Trees — General Concepts — Quiz

> **Topic Overview**: Tree terminology, N-ary nodes, traversals, LCA, and diameter.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a tree?**
- A) A linear structure
- B) An acyclic connected graph with a root and parent-child links
- C) A hash bucket
- D) A sorted array

<details><summary>Reveal Answer</summary>**B.** Hierarchy without cycles.</details>

### Question 2 — Easy
**What is a leaf?**
- A) The root
- B) A node with no children
- C) A node with one child
- D) Any node

<details><summary>Reveal Answer</summary>**B.** End of a branch.</details>

### Question 3 — Medium
**Difference between height and depth?**
- A) They are the same
- B) Height is measured downward to a leaf; depth is the distance from the root to the node
- C) Height is for leaves only
- D) Depth is for roots only

<details><summary>Reveal Answer</summary>**B.** Opposite directions.</details>

### Question 4 — Medium
**Which traversal visits the root before its subtrees?**
- A) Inorder
- B) Preorder
- C) Postorder
- D) Level-order

<details><summary>Reveal Answer</summary>**B.** Root first.</details>

### Question 5 — Medium
**What does postorder naturally compute?**
- A) Nothing useful
- B) Aggregate results that depend on children (height, diameter, subtree sums)
- C) Only sorting
- D) Only searching

<details><summary>Reveal Answer</summary>**B.** Children before parent.</details>

### Question 6 — Hard
**How does the LCA of two nodes in a general tree work?**
- A) Sort the path
- B) Recurse; if both nodes are found in different subtrees (or one is the node), the current node is the LCA
- C) Hash the nodes
- D) BFS only

<details><summary>Reveal Answer</summary>**B.** The split point is the LCA.</details>

### Question 7 — Hard
**How is the diameter of a tree computed in one pass?**
- A) Twice the height
- B) For each node, combine the two deepest child heights and track the maximum
- C) Count nodes
- D) BFS twice from the root only

<details><summary>Reveal Answer</summary>**B.** A postorder accumulation.</details>

### Question 8 — Hard
**What is the main recursion hazard in tree code?**
- A) Stack overflow from a missing base case
- B) Hashing
- C) Sorting
- D) Type errors only

<details><summary>Reveal Answer</summary>**A.** Always handle empty/leaf cases.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand general trees. |
| 5-6 | Review traversals and height/depth. |
| < 5 | Re-read the lecture. |
