# DSA Graphs Interview Practice

## Topic Overview

Graphs model relationships between entities. They consist of vertices (nodes) and edges (connections). Graph problems test your understanding of **traversal** (BFS/DFS), **shortest path** algorithms, **connectivity**, and **topological ordering**.

**Graph Representations:**
- **Adjacency list:** `graph = {A: [B, C], B: [A, D]}` — most common, space O(V+E)
- **Adjacency matrix:** `graph[i][j] = 1 if edge` — space O(V²), faster edge lookup
- **Edge list:** `[(A,B), (B,C)]` — compact, good for Kruskal's

**Graph Types:**
- **Directed vs Undirected**
- **Weighted vs Unweighted**
- **Cyclic vs Acyclic (DAG)**
- **Connected vs Disconnected**
- **Complete:** Every vertex connected to every other

**Time/Space for Representations:**

| Operation | Adjacency List | Adjacency Matrix |
|-----------|---------------|-----------------|
| Space | O(V + E) | O(V²) |
| Check edge | O(degree) | O(1) |
| List neighbors | O(degree) | O(V) |
| Add edge | O(1) | O(1) |
| Remove edge | O(degree) | O(1) |

---

## Interview Questions (with Answers)

### Q1: Explain BFS and DFS. When would you use each?

**Answer:**
**BFS (Breadth-First Search):** Explores layer by layer using a queue.
- Finds shortest path in unweighted graphs
- Level-order traversal
- Checking connectivity

```python
from collections import deque


def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order
```

**DFS (Depth-First Search):** Explores as deep as possible before backtracking using a stack (or recursion).
- Cycle detection
- Topological sort
- Finding connected components
- Path existence

```python
def dfs(graph, start):
    visited = set()
    order = []

    def dfs_helper(node):
        visited.add(node)
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs_helper(neighbor)

    dfs_helper(start)
    return order


# Iterative DFS
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)

    return order
```

**When to use which:**
- BFS: Shortest path (unweighted), level-order, closest neighbor
- DFS: Cycle detection, path finding, topological sort, connected components

---

### Q2: How do you detect a cycle in a directed graph?

**Answer:**
DFS with coloring: WHITE (unvisited), GRAY (in progress), BLACK (finished).

```python
def has_cycle_directed(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}

    def dfs(node):
        color[node] = GRAY
        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True  # Back edge found
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        color[node] = BLACK
        return False

    for node in graph:
        if color[node] == WHITE:
            if dfs(node):
                return True
    return False
```

**For undirected graphs:** Track parent. If you visit a visited node that's not the parent, there's a cycle.

```python
def has_cycle_undirected(graph):
    visited = set()

    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        return False

    for node in graph:
        if node not in visited:
            if dfs(node, -1):
                return True
    return False
```

---

### Q3: What is topological sort? When is it used?

**Answer:**
Topological sort orders vertices in a DAG so that for every directed edge (u, v), u comes before v.

**Applications:**
- Task scheduling with dependencies
- Course prerequisites
- Build systems (Makefile)
- Spreadsheet formula evaluation

**DFS-based (O(V + E)):**
```python
def topological_sort_dfs(graph):
    visited = set()
    order = []

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        order.append(node)

    for node in graph:
        if node not in visited:
            dfs(node)

    return order[::-1]


# Test
graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
assert topological_sort_dfs(graph) in [["A", "C", "B", "D"], ["A", "B", "C", "D"]]
```

**Kahn's Algorithm (BFS-based, O(V + E)):**
```python
from collections import deque


def topological_sort_kahn(graph):
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    queue = deque([node for node in graph if in_degree[node] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(graph):
        return []  # Cycle exists
    return order
```

---

### Q4: Explain Dijkstra's algorithm.

**Answer:**
Dijkstra's finds the shortest path from a source to all vertices in a weighted graph with non-negative weights.

```python
import heapq


def dijkstra(graph, start):
    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    heap = [(0, start)]
    previous = {node: None for node in graph}

    while heap:
        curr_dist, node = heapq.heappop(heap)

        if curr_dist > distances[node]:
            continue

        for neighbor, weight in graph[node]:
            distance = curr_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = node
                heapq.heappush(heap, (distance, neighbor))

    return distances, previous


# Test
graph = {
    "A": [("B", 1), ("C", 4)],
    "B": [("A", 1), ("C", 2), ("D", 5)],
    "C": [("A", 4), ("B", 2), ("D", 1)],
    "D": [("B", 5), ("C", 1)],
}
distances, previous = dijkstra(graph, "A")
assert distances == {"A": 0, "B": 1, "C": 3, "D": 4}
```

**Time: O((V + E) log V)** with binary heap, **O(V²)** with array.

---

### Q5: How do you find connected components in a graph?

**Answer:**
```python
def connected_components(graph):
    visited = set()
    components = []

    def dfs(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, component)

    for node in graph:
        if node not in visited:
            component = []
            dfs(node, component)
            components.append(component)

    return components


# Test
graph = {"A": ["B"], "B": ["A"], "C": ["D"], "D": ["C"], "E": []}
assert connected_components(graph) == [["A", "B"], ["C", "D"], ["E"]]
```

---

### Q6: What is Union-Find (Disjoint Set Union)?

**Answer:**
Union-Find tracks elements partitioned into disjoint sets. Supports:
- `find(x)`: Find which set x belongs to
- `union(x, y)`: Merge sets containing x and y

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

**Time: O(α(n))** amortized (α is inverse Ackermann, nearly constant).

**Applications:** Kruskal's MST, detecting cycles, dynamic connectivity.

---

### Q7: How do you find the minimum spanning tree?

**Answer:**
**Kruskal's Algorithm (O(E log E)):**
```python
def kruskal(n, edges):
    # edges: list of (weight, u, v)
    edges.sort()
    uf = UnionFind(n)
    mst = []

    for weight, u, v in edges:
        if uf.union(u, v):
            mst.append((weight, u, v))
            if len(mst) == n - 1:
                break

    return mst
```

**Prim's Algorithm (O(E log V)):**
```python
import heapq


def prim(graph, start=0):
    mst = []
    visited = set()
    heap = [(0, start, -1)]  # (weight, node, parent)

    while heap and len(mst) < len(graph):
        weight, node, parent = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        if parent != -1:
            mst.append((weight, parent, node))

        for neighbor, w in graph[node]:
            if neighbor not in visited:
                heapq.heappush(heap, (w, neighbor, node))

    return mst
```

---

### Q8: How do you find the shortest path in an unweighted graph?

**Answer:**
BFS gives the shortest path:

```python
from collections import deque


def shortest_path(graph, start, end):
    queue = deque([(start, [start])])
    visited = set([start])

    while queue:
        node, path = queue.popleft()
        if node == end:
            return path

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return []  # No path
```

---

### Q9: What is Bellman-Ford algorithm?

**Answer:**
Finds shortest paths from source, handles negative weights (but not negative cycles).

```python
def bellman_ford(n, edges, start):
    distances = [float("inf")] * n
    distances[start] = 0

    for _ in range(n - 1):
        for u, v, w in edges:
            if distances[u] + w < distances[v]:
                distances[v] = distances[u] + w

    # Check for negative cycle
    for u, v, w in edges:
        if distances[u] + w < distances[v]:
            return None  # Negative cycle exists

    return distances
```

**Time: O(V * E)**

---

### Q10: How do you detect a negative cycle?

**Answer:**
Run Bellman-Ford for V iterations. If any distance still decreases in the V-th iteration, there's a negative cycle.

```python
def has_negative_cycle(n, edges, start):
    distances = [float("inf")] * n
    distances[start] = 0

    for _ in range(n - 1):
        for u, v, w in edges:
            if distances[u] + w < distances[v]:
                distances[v] = distances[u] + w

    for u, v, w in edges:
        if distances[u] + w < distances[v]:
            return True

    return False
```

---

### Q11: How do you find all paths from source to destination?

**Answer:**
```python
def find_all_paths(graph, start, end):
    result = []

    def dfs(node, path):
        if node == end:
            result.append(path[:])
            return
        for neighbor in graph[node]:
            if neighbor not in path:
                path.append(neighbor)
                dfs(neighbor, path)
                path.pop()

    dfs(start, [start])
    return result


# Test
graph = {"A": ["B", "C"], "B": ["D", "E"], "C": ["E"], "D": [], "E": []}
assert find_all_paths(graph, "A", "E") == [["A", "B", "E"], ["A", "B", "D", "E"], ["A", "C", "E"]]
```

---

### Q12: How do you implement a course schedule (topological sort application)?

**Answer:**
```python
from collections import deque


def can_finish(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    count = 0

    while queue:
        node = queue.popleft()
        count += 1
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return count == num_courses


# Test
assert can_finish(2, [[1, 0]]) == True
assert can_finish(2, [[1, 0], [0, 1]]) == False
```

---

### Q13: How do you find bridges in a graph?

**Answer:**
An edge is a bridge if removing it disconnects the graph. Uses Tarjan's algorithm.

```python
def find_bridges(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    disc = [-1] * n
    low = [-1] * n
    bridges = []
    timer = [0]

    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1

        for v in graph[u]:
            if disc[v] == -1:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((u, v))
            elif v != parent:
                low[u] = min(low[u], disc[v])

    for i in range(n):
        if disc[i] == -1:
            dfs(i, -1)

    return bridges
```

---

### Q14: What is the difference between BFS and DFS in terms of memory?

**Answer:**

| Aspect | BFS | DFS |
|--------|-----|-----|
| Data structure | Queue | Stack (or recursion) |
| Memory | O(V) worst case (wide tree) | O(V) worst case (deep tree) |
| Shortest path | Yes (unweighted) | No |
| Complete | Yes | Yes (with visited set) |
| Time | O(V + E) | O(V + E) |

**Memory trade-off:** BFS uses more memory for wide graphs. DFS uses more for deep graphs (recursion stack).

---

### Q15: How do you find the number of islands?

**Answer:**
```python
def num_islands(grid):
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"  # Mark visited
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                dfs(r, c)
                count += 1

    return count


# Test
grid = [
    ["1", "1", "1", "1", "0"],
    ["1", "1", "0", "1", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "0", "0", "0"],
]
assert num_islands(grid) == 1
```

---

## Coding Challenges

### Challenge 1: Number of Islands
```python
def num_islands(grid):
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                dfs(r, c)
                count += 1
    return count
```
**Time: O(m*n), Space: O(m*n) worst case recursion**

---

### Challenge 2: Clone Graph
```python
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(node):
    if not node:
        return None

    clones = {}

    def dfs(curr):
        if curr in clones:
            return clones[curr]

        clone = Node(curr.val)
        clones[curr] = clone

        for neighbor in curr.neighbors:
            clone.neighbors.append(dfs(neighbor))

        return clone

    return dfs(node)
```
**Time: O(V + E), Space: O(V)**

---

### Challenge 3: Course Schedule
```python
from collections import deque


def can_finish(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    count = 0

    while queue:
        node = queue.popleft()
        count += 1
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return count == num_courses
```
**Time: O(V + E), Space: O(V)**

---

### Challenge 4: Pacific Atlantic Water Flow
```python
def pacific_atlantic(heights):
    if not heights:
        return []

    rows, cols = len(heights), len(heights[0])
    pacific = set()
    atlantic = set()

    def dfs(r, c, prev, ocean):
        if (r, c) in ocean:
            return
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if heights[r][c] < prev:
            return

        ocean.add((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, heights[r][c], ocean)

    for r in range(rows):
        dfs(r, 0, 0, pacific)
        dfs(r, cols - 1, 0, atlantic)

    for c in range(cols):
        dfs(0, c, 0, pacific)
        dfs(rows - 1, c, 0, atlantic)

    return list(pacific & atlantic)
```
**Time: O(m*n), Space: O(m*n)**

---

### Challenge 5: Word Ladder
```python
from collections import deque


def ladder_length(begin_word, end_word, word_list):
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    queue = deque([(begin_word, 1)])
    visited = set([begin_word])

    while queue:
        word, length = queue.popleft()
        for i in range(len(word)):
            for c in "abcdefghijklmnopqrstuvwxyz":
                new_word = word[:i] + c + word[i + 1 :]
                if new_word == end_word:
                    return length + 1
                if new_word in word_set and new_word not in visited:
                    visited.add(new_word)
                    queue.append((new_word, length + 1))

    return 0
```
**Time: O(M² * N)** where M = word length, N = word list size

---

### Challenge 6: Alien Dictionary (Topological Sort)
```python
from collections import defaultdict, deque


def alien_order(words):
    adj = defaultdict(set)
    in_degree = {c: 0 for word in words for c in word}

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break
        else:
            if len(w1) > len(w2):
                return ""

    queue = deque([c for c in in_degree if in_degree[c] == 0])
    result = []

    while queue:
        char = queue.popleft()
        result.append(char)
        for neighbor in adj[char]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(in_degree):
        return ""

    return "".join(result)
```
**Time: O(C)** where C = total characters in all words

---

### Challenge 7: Number of Provinces (Connected Components)
```python
def find_province_num(is_connected):
    n = len(is_connected)
    visited = set()
    count = 0

    def dfs(city):
        visited.add(city)
        for neighbor in range(n):
            if is_connected[city][neighbor] == 1 and neighbor not in visited:
                dfs(neighbor)

    for city in range(n):
        if city not in visited:
            dfs(city)
            count += 1

    return count


# Test
assert find_province_num([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
```
**Time: O(n²), Space: O(n)**

---

### Challenge 8: Shortest Path in Binary Matrix
```python
from collections import deque


def shortest_path_binary_matrix(grid):
    n = len(grid)
    if grid[0][0] == 1 or grid[n - 1][n - 1] == 1:
        return -1

    queue = deque([(0, 0, 1)])
    visited = set([(0, 0)])

    while queue:
        r, c, dist = queue.popleft()
        if r == n - 1 and c == n - 1:
            return dist

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))

    return -1
```
**Time: O(n²), Space: O(n²)**

---

### Challenge 9: Graph Valid Tree
```python
def valid_tree(n, edges):
    if len(edges) != n - 1:
        return False

    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()

    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if not dfs(neighbor, node):
                    return False
            elif neighbor != parent:
                return False
        return True

    return dfs(0, -1) and len(visited) == n
```
**Time: O(V + E), Space: O(V)**

---

### Challenge 10: Network Delay Time (Dijkstra)
```python
import heapq


def network_delay(times, n, k):
    graph = [[] for _ in range(n + 1)]
    for u, v, w in times:
        graph[u].append((v, w))

    distances = {i: float("inf") for i in range(1, n + 1)}
    distances[k] = 0
    heap = [(0, k)]

    while heap:
        curr_dist, node = heapq.heappop(heap)
        if curr_dist > distances[node]:
            continue
        for neighbor, weight in graph[node]:
            distance = curr_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (distance, neighbor))

    max_dist = max(distances.values())
    return max_dist if max_dist < float("inf") else -1
```
**Time: O(E log V), Space: O(V + E)**

---

## Common Follow-Up Questions

1. **"What if the graph is very large?"** — Use BFS/DFS with visited set. Consider iterative DFS to avoid stack overflow.
2. **"What about weighted edges?"** — Use Dijkstra (non-negative) or Bellman-Ford (negative weights).
3. **"Can you do it in O(1) space?"** — Usually no for graph traversal, but you can modify the input graph.
4. **"What if the graph has cycles?"** — Use visited set to avoid infinite loops. For directed, use coloring.
5. **"How would you store the graph?"** — Adjacency list for sparse graphs, matrix for dense.

---

## Tips for Answering Graph Questions

1. **Choose the right representation:** Adjacency list is usually best.
2. **Use a visited set:** Prevents infinite loops in cyclic graphs.
3. **Think about the traversal pattern:** BFS for shortest path, DFS for exhaustive search.
4. **Handle disconnected graphs:** Loop through all nodes.
5. **Consider edge cases:** Single node, empty graph, complete graph.
6. **Know the algorithms:** Dijkstra, Bellman-Ford, Floyd-Warshall, Kruskal, Prim.

---

## Complexity Cheat Sheet

| Algorithm | Time | Space |
|-----------|------|-------|
| BFS | O(V + E) | O(V) |
| DFS | O(V + E) | O(V) |
| Topological Sort | O(V + E) | O(V) |
| Dijkstra | O((V+E) log V) | O(V) |
| Bellman-Ford | O(V * E) | O(V) |
| Kruskal's MST | O(E log E) | O(V) |
| Prim's MST | O(E log V) | O(V) |
| Floyd-Warshall | O(V³) | O(V²) |
| Union-Find | O(α(n)) per op | O(V) |
| Connected Components | O(V + E) | O(V) |
| Bridges (Tarjan) | O(V + E) | O(V) |
