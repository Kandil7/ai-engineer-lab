# Lecture 11: Graphs - Data Structures and Algorithms

## Topic Overview

Graphs are one of the most versatile and powerful data structures in computer science. They model relationships between entities, making them essential for solving problems involving networks, connections, and paths. This lecture covers graph fundamentals, representations, traversals, and key algorithms.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Understand graph terminology (vertices, edges, directed/undirected, weighted/unweighted)
2. Implement graphs using adjacency lists and adjacency matrices
3. Perform BFS and DFS traversals
4. Detect cycles in directed and undirected graphs
5. Find shortest paths using BFS and Dijkstra's algorithm
6. Perform topological sorting on DAGs
7. Find connected components and check bipartiteness

## Key Concepts

### 1. Graph Fundamentals

A **graph** G = (V, E) consists of:
- **Vertices (V)**: Nodes or points in the graph
- **Edges (E)**: Connections between vertices

**Types of Graphs:**
- **Directed (Digraph)**: Edges have direction (A → B)
- **Undirected**: Edges are bidirectional (A ↔ B)
- **Weighted**: Edges have associated costs/weights
- **Unweighted**: All edges have equal weight
- **Cyclic**: Contains at least one cycle
- **Acyclic**: No cycles (DAG - Directed Acyclic Graph)

**Example:**
```
Social Network (Undirected):
    Alice --- Bob
     |        |
    Carol --- David

Road Map (Weighted Directed):
    CityA --5--> CityB
     |          |
    3           2
     v          v
    CityC --4--> CityD
```

### 2. Graph Representations

#### Adjacency List
```python
class Graph:
    def __init__(self, directed=False):
        self.adj_list = {}
        self.directed = directed
    
    def add_edge(self, v1, v2, weight=None):
        self.add_vertex(v1)
        self.add_vertex(v2)
        self.adj_list[v1].append((v2, weight))
        if not self.directed:
            self.adj_list[v2].append((v1, weight))
    
    def add_vertex(self, vertex):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []
```

**Pros:** Space efficient for sparse graphs O(V + E)
**Cons:** Edge lookup can be O(degree)

#### Adjacency Matrix
```python
class AdjMatrixGraph:
    def __init__(self, vertices, directed=False):
        self.vertices = vertices
        self.vertex_map = {v: i for i, v in enumerate(vertices)}
        self.matrix = [[0] * len(vertices) for _ in range(len(vertices))]
    
    def add_edge(self, v1, v2, weight=1):
        i, j = self.vertex_map[v1], self.vertex_map[v2]
        self.matrix[i][j] = weight
        if not self.directed:
            self.matrix[j][i] = weight
```

**Pros:** O(1) edge lookup
**Cons:** O(V²) space, inefficient for sparse graphs

### 3. Graph Traversals

#### BFS (Breadth-First Search)
Explores level by level using a queue.

```python
def bfs(graph, start):
    visited = set()
    queue = [start]
    visited.add(start)
    order = []
    
    while queue:
        vertex = queue.pop(0)
        order.append(vertex)
        
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return order
```

**Time Complexity:** O(V + E)
**Space Complexity:** O(V)

**Applications:**
- Shortest path in unweighted graphs
- Level-order traversal
- Finding connected components

#### DFS (Depth-First Search)
Explores as deep as possible before backtracking.

```python
def dfs_recursive(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    order = [start]
    
    for neighbor, _ in graph.get_neighbors(start):
        if neighbor not in visited:
            order.extend(dfs_recursive(graph, neighbor, visited))
    
    return order
```

**Applications:**
- Cycle detection
- Topological sorting
- Path finding
- Connected components

### 4. Cycle Detection

**Undirected Graph:**
```python
def has_cycle_undirected(graph):
    visited = set()
    
    def dfs(vertex, parent):
        visited.add(vertex)
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                if dfs(neighbor, vertex):
                    return True
            elif neighbor != parent:
                return True
        return False
    
    for v in graph.get_vertices():
        if v not in visited:
            if dfs(v, None):
                return True
    return False
```

**Directed Graph (Three-Color Method):**
```python
def has_cycle_directed(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph.get_vertices()}
    
    def dfs(vertex):
        color[vertex] = GRAY
        for neighbor, _ in graph.get_neighbors(vertex):
            if color[neighbor] == GRAY:
                return True
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        color[vertex] = BLACK
        return False
    
    for v in graph.get_vertices():
        if color[v] == WHITE:
            if dfs(v):
                return True
    return False
```

### 5. Shortest Path Algorithms

#### BFS (Unweighted Graphs)
```python
def shortest_path_bfs(graph, start, end):
    if start == end:
        return [start]
    
    visited = {start}
    queue = [(start, [start])]
    
    while queue:
        vertex, path = queue.pop(0)
        
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                new_path = path + [neighbor]
                if neighbor == end:
                    return new_path
                visited.add(neighbor)
                queue.append((neighbor, new_path))
    
    return None
```

#### Dijkstra's Algorithm (Weighted Graphs)
```python
import heapq


def dijkstra(graph, start):
    distances = {v: float("inf") for v in graph.get_vertices()}
    distances[start] = 0
    previous = {v: None for v in graph.get_vertices()}
    pq = [(0, start)]
    visited = set()

    while pq:
        dist, vertex = heapq.heappop(pq)

        if vertex in visited:
            continue
        visited.add(vertex)

        for neighbor, weight in graph.get_neighbors(vertex):
            if neighbor not in visited:
                new_dist = dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = vertex
                    heapq.heappush(pq, (new_dist, neighbor))

    return distances, previous
```

**Time Complexity:** O((V + E) log V)

### 6. Topological Sort

Orders vertices in a DAG such that for every directed edge (u, v), u comes before v.

```python
def topological_sort(graph):
    visited = set()
    stack = []
    
    def dfs(vertex):
        visited.add(vertex)
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(vertex)
    
    for v in graph.get_vertices():
        if v not in visited:
            dfs(v)
    
    return stack[::-1]
```

**Applications:**
- Task scheduling with dependencies
- Course prerequisites
- Build systems

### 7. Connected Components

```python
def connected_components(graph):
    visited = set()
    components = []
    
    def dfs(vertex, component):
        visited.add(vertex)
        component.append(vertex)
        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                dfs(neighbor, component)
    
    for v in graph.get_vertices():
        if v not in visited:
            component = []
            dfs(v, component)
            components.append(component)
    
    return components
```

### 8. Bipartite Check

A graph is bipartite if vertices can be divided into two disjoint sets such that every edge connects vertices from different sets.

```python
def is_bipartite(graph):
    color = {}
    
    def bfs_check(start):
        queue = [start]
        color[start] = 0
        
        while queue:
            vertex = queue.pop(0)
            for neighbor, _ in graph.get_neighbors(vertex):
                if neighbor not in color:
                    color[neighbor] = 1 - color[vertex]
                    queue.append(neighbor)
                elif color[neighbor] == color[vertex]:
                    return False
        return True
    
    for v in graph.get_vertices():
        if v not in color:
            if not bfs_check(v):
                return False
    return True
```

## Code Examples

### Example 1: Social Network Analysis
```python
# Create social network
social = Graph()
social.add_edge("Alice", "Bob")
social.add_edge("Alice", "Carol")
social.add_edge("Bob", "David")
social.add_edge("Carol", "David")
social.add_edge("David", "Eve")

# Find shortest path between users
path = shortest_path_bfs(social, "Alice", "Eve")
print(f"Path: {' -> '.join(path)}")

# Find all connected users
components = connected_components(social)
print(f"Connected groups: {components}")
```

### Example 2: Task Scheduling
```python
# Course prerequisites
courses = Graph(directed=True)
courses.add_edge("CS101", "CS201")
courses.add_edge("CS101", "CS202")
courses.add_edge("CS201", "CS301")
courses.add_edge("CS202", "CS301")

# Topological order for course schedule
order = topological_sort(courses)
print(f"Course order: {order}")
```

### Example 3: Navigation System
```python
# City road network
roads = Graph(directed=True)
roads.add_edge("A", "B", 4)
roads.add_edge("A", "C", 2)
roads.add_edge("B", "D", 3)
roads.add_edge("C", "B", 1)
roads.add_edge("D", "E", 5)

# Find shortest routes
distances, previous = dijkstra(roads, "A")
for city in roads.get_vertices():
    path = get_path(previous, city)
    print(f"A to {city}: {' -> '.join(path)} ({distances[city]} km)")
```

## Common Mistakes to Avoid

1. **Forgetting to mark visited nodes** in BFS/DFS → infinite loops
2. **Not handling disconnected graphs** → missed vertices
3. **Using adjacency matrix for sparse graphs** → wasted memory
4. **Ignoring edge cases** → empty graphs, single nodes
5. **Not resetting visited set** between traversals

## Best Practices

1. **Choose the right representation:**
   - Adjacency list for sparse graphs
   - Adjacency matrix for dense graphs
2. **Use BFS for shortest path in unweighted graphs**
3. **Use DFS for cycle detection and topological sort**
4. **Always check for visited nodes** to avoid infinite loops
5. **Consider using sets for O(1) lookup** of visited nodes

## Practice Exercises

### Easy
1. Implement a graph class with add_vertex, add_edge, get_neighbors methods
2. Write BFS to find if a path exists between two nodes
3. Count the number of connected components in an undirected graph

### Medium
4. Detect if a directed graph has a cycle
5. Find the shortest path between two nodes in an unweighted graph
6. Implement topological sort using Kahn's algorithm (BFS-based)

### Hard
7. Implement Dijkstra's algorithm with priority queue
8. Find all bridges (critical connections) in an undirected graph
9. Detect negative cycles in a weighted directed graph

## Summary

- **Graphs model relationships** between entities
- **Adjacency list** is preferred for most real-world graphs (sparse)
- **BFS** explores level-by-level, good for shortest path in unweighted graphs
- **DFS** explores depth-first, good for cycle detection and topological sort
- **Dijkstra's algorithm** finds shortest paths in weighted graphs
- **Topological sort** orders tasks with dependencies
- **Connected components** identify isolated groups

**Time Complexity Reference:**

| Operation | Adjacency List | Adjacency Matrix |
|-----------|----------------|------------------|
| Add vertex | O(1) | O(V²) |
| Add edge | O(1) | O(1) |
| Remove edge | O(degree) | O(1) |
| BFS/DFS | O(V + E) | O(V²) |
| Shortest path (unweighted) | O(V + E) | O(V²) |
| Dijkstra | O((V + E) log V) | O(V²) |

**Key Takeaway:** Graphs are fundamental for modeling networks, relationships, and paths. Master BFS, DFS, and Dijkstra's to solve a wide range of problems efficiently.