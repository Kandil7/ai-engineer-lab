# DSA 11: Graphs — Quiz

> **Topic Overview**: Representations, BFS/DFS, cycles, shortest paths, and topological order.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the difference between directed and undirected graphs?**
- A) Size
- B) Whether edges have direction
- C) Weight
- D) Color

<details><summary>Reveal Answer</summary>**B.** Direction of edges.</details>

### Question 2 — Easy
**Which representation is O(V + E) space?**
- A) Adjacency matrix, O(V²)
- B) Adjacency list, O(V + E)
- C) Edge set only
- D) Hash map

<details><summary>Reveal Answer</summary>**B.** Lists store only edges.</details>

### Question 3 — Medium
**Which traversal finds the shortest path in an unweighted graph?**
- A) DFS
- B) BFS
- C) Topological sort
- D) Dijkstra only

<details><summary>Reveal Answer</summary>**B.** BFS explores in distance layers.</details>

### Question 4 — Medium
**Why mark visited when enqueuing in BFS?**
- A) For speed
- B) Otherwise nodes are enqueued repeatedly, causing loops or blowup
- C) To sort
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Prevent re-processing.</details>

### Question 5 — Medium
**What does topological sort require?**
- A) Any graph
- B) A directed acyclic graph (DAG)
- C) A tree
- D) Weights

<details><summary>Reveal Answer</summary>**B.** Cycles make order undefined.</details>

### Question 6 — Hard
**Which algorithm handles non-negative weighted shortest paths?**
- A) BFS
- B) Dijkstra
- C) DFS
- D) Topological sort

<details><summary>Reveal Answer</summary>**B.** Weighted distances.</details>

### Question 7 — Hard
**What is a bipartite graph?**
- A) A tree
- B) A graph whose vertices split into two sets with edges only across sets
- C) A complete graph
- D) A DAG

<details><summary>Reveal Answer</summary>**B.** Two-colourable.</details>

### Question 8 — Hard
**How do you detect a cycle in an undirected graph with DFS?**
- A) Count edges
- B) A visited neighbour that is not the parent indicates a cycle
- C) Sort nodes
- D) Hash edges

<details><summary>Reveal Answer</summary>**B.** Back edge to a non-parent.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand graphs. |
| 5-6 | Review BFS/DFS and topological sort. |
| < 5 | Re-read the lecture. |
