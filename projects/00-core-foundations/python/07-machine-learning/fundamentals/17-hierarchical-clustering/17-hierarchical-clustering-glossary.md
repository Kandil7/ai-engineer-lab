# Glossary: Hierarchical Clustering (Lecture 17)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Hierarchical Clustering | Builds cluster hierarchy (tree) | Dendrogram |
| Agglomerative | Bottom-up: merge closest clusters | `AgglomerativeClustering()` |
| Divisive | Top-down: split largest cluster | DiANA algorithm |
| Linkage | Method to measure cluster distance | Ward, Complete, Average |
| Ward | Minimizes variance within clusters | `linkage='ward'` |
| Complete Linkage | Maximum distance between points | `linkage='complete'` |
| Average Linkage | Average distance between points | `linkage='average'` |
| Single Linkage | Minimum distance between points | `linkage='single'` |
| Dendrogram | Tree diagram of cluster hierarchy | `scipy.cluster.hierarchy.dendrogram` |
| Linkage Matrix | Condensed distance matrix | `scipy.cluster.hierarchy.linkage` |
| Cut Height | Threshold to flatten dendrogram | Determines number of clusters |
| Cophenetic Distance | Distance at which two clusters merge | From dendrogram |
| Cluster Hierarchy | Nested cluster structure | Multi-level grouping |
| Distance Metric | Measure of point similarity | Euclidean, Manhattan |

---

## Detailed Term Definitions

### Hierarchical Clustering

**Definition:** A method of cluster analysis that builds a hierarchy of clusters by either merging or splitting clusters iteratively.

**Types:**
- **Agglomerative** (bottom-up): Start with individual points, merge
- **Divisive** (top-down): Start with one cluster, split

**Example:**
```python
from sklearn.cluster import AgglomerativeClustering
import numpy as np

X = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]])

# Agglomerative clustering
clustering = AgglomerativeClustering(n_clusters=2)
labels = clustering.fit_predict(X)

print(f"Labels: {labels}")
print(f"Number of clusters: {clustering.n_clusters_}")
```

**Related Terms:** Agglomerative, Divisive, Dendrogram

---

### Agglomerative Clustering

**Definition:** A bottom-up hierarchical clustering approach where each observation starts as its own cluster, and pairs of clusters are merged as one moves up the hierarchy.

**Algorithm:**
1. Start with n clusters (one per point)
2. Compute distance matrix
3. Merge two closest clusters
4. Update distance matrix
5. Repeat until K clusters remain

**Example:**
```python
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score
import numpy as np

X, _ = make_blobs(n_samples=100, centers=3, random_state=42)

# Apply agglomerative clustering
clustering = AgglomerativeClustering(n_clusters=3, linkage="ward")
labels = clustering.fit_predict(X)

sil = silhouette_score(X, labels)
print(f"Silhouette Score: {sil:.4f}")
print(f"Cluster sizes: {np.bincount(labels)}")
```

**Related Terms:** Hierarchical Clustering, Linkage, Dendrogram

---

### Divisive Clustering

**Definition:** A top-down hierarchical clustering approach where all observations start in one cluster, and splits are performed recursively.

**Example:**
```python
# Divisive clustering is less common in scikit-learn
# Can be implemented manually or using specific libraries

# Example concept:
"""
Start: [1, 2, 3, 4, 5, 6, 7, 8]
Split: [1, 2, 3, 4] and [5, 6, 7, 8]
Split: [1, 2] and [3, 4] | [5, 6] and [7, 8]
Split: [1] [2] [3] [4] [5] [6] [7] [8]
"""

print("Divisive: Top-down approach")
print("Start with one cluster, recursively split")
```

**Related Terms:** Hierarchical Clustering, Agglomerative, DIANA Algorithm

---

### Linkage

**Definition:** A method for measuring the distance between clusters. Determines which clusters to merge at each step.

**Types:**

| Linkage | Description | Characteristics |
|---------|-------------|-----------------|
| Ward | Minimizes variance | Often best, balanced |
| Complete | Maximum distance | Compact clusters |
| Average | Average distance | Compromise |
| Single | Minimum distance | Can chain points |

**Example:**
```python
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_moons
from sklearn.metrics import silhouette_score
import numpy as np

X, _ = make_moons(n_samples=200, noise=0.1, random_state=42)

methods = ["ward", "complete", "average", "single"]
for method in methods:
    clustering = AgglomerativeClustering(n_clusters=2, linkage=method)
    labels = clustering.fit_predict(X)
    sil = silhouette_score(X, labels)
    print(f"{method:>10}: Silhouette = {sil:.4f}")
```

**Related Terms:** Ward, Complete, Average, Single

---

### Ward Linkage

**Definition:** A linkage method that minimizes the total within-cluster variance when merging clusters. Often produces the most balanced clusters.

**Formula:**
```
Δ(A,B) = (|A|·|B|)/(|A|+|B|) · ||μ_A - μ_B||²
```

**Example:**
```python
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, dendrogram
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
X = np.random.randn(50, 2)

# Ward linkage
Z = linkage(X, method="ward")

plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
dendrogram(Z, truncate_mode="lastp", p=10)
plt.title("Ward Linkage")

# Single linkage for comparison
Z_single = linkage(X, method="single")
plt.subplot(1, 2, 2)
dendrogram(Z_single, truncate_mode="lastp", p=10)
plt.title("Single Linkage")

plt.tight_layout()
plt.savefig("linkage_comparison.png", dpi=100)
plt.show()
```

**Properties:**
- Tends to produce equal-sized clusters
- Sensitive to outliers (less than complete)
- Usually the best default choice

**Related Terms:** Linkage, Within-Cluster Variance

---

### Complete Linkage

**Definition:** A linkage method that uses the maximum distance between points in two clusters. Tends to produce compact, spherical clusters.

**Formula:**
```
d(A,B) = max{d(a,b) : a ∈ A, b ∈ B}
```

**Example:**
```python
from sklearn.cluster import AgglomerativeClustering
import numpy as np

X = np.array([[1, 2], [1.5, 1.8], [2, 2.2], [8, 8], [8.5, 8.2], [9, 8]])

# Complete linkage produces compact clusters
clustering = AgglomerativeClustering(n_clusters=2, linkage="complete")
labels = clustering.fit_predict(X)

for i in range(2):
    cluster = X[labels == i]
    print(f"Cluster {i}: {cluster}")
```

**Properties:**
- Produces compact, equal-sized clusters
- Less sensitive to outliers than single
- Can break large clusters

**Related Terms:** Linkage, Single, Average, Ward

---

### Average Linkage

**Definition:** A linkage method that uses the average distance between all pairs of points in two clusters. A compromise between single and complete.

**Formula:**
```
d(A,B) = (1/|A|·|B|) Σ d(a,b) for a ∈ A, b ∈ B
```

**Example:**
```python
from sklearn.cluster import AgglomerativeClustering
import numpy as np

X = np.array([[1, 2], [1.5, 1.8], [2, 2.2], [8, 8], [8.5, 8.2], [9, 8]])

clustering = AgglomerativeClustering(n_clusters=2, linkage="average")
labels = clustering.fit_predict(X)

print(f"Labels: {labels}")
for i in range(2):
    print(f"Cluster {i}: {X[labels == i]}")
```

**Properties:**
- Compromise between single and complete
- Less sensitive to outliers than single
- Can handle uneven cluster sizes

**Related Terms:** Linkage, Single, Complete, Ward

---

### Single Linkage

**Definition:** A linkage method that uses the minimum distance between points in two clusters. Can detect non-convex shapes but prone to chaining.

**Formula:**
```
d(A,B) = min{d(a,b) : a ∈ A, b ∈ B}
```

**Example:**
```python
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_moons
import numpy as np

# Single linkage works well with non-convex shapes
X, _ = make_moons(n_samples=200, noise=0.1, random_state=42)

clustering = AgglomerativeClustering(n_clusters=2, linkage="single")
labels = clustering.fit_predict(X)

from sklearn.metrics import silhouette_score

sil = silhouette_score(X, labels)
print(f"Single linkage silhouette: {sil:.4f}")
```

**Properties:**
- Can detect non-convex shapes
- Prone to chaining (long, thin clusters)
- Sensitive to noise

**Related Terms:** Linkage, Complete, Average, Ward

---

### Dendrogram

**Definition:** A tree diagram showing the hierarchical relationship between clusters. The height of each merge indicates the distance between clusters.

**Example:**
```python
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
X, _ = make_blobs(n_samples=50, centers=3, random_state=42)

# Create linkage matrix
Z = linkage(X, method="ward")

# Plot dendrogram
plt.figure(figsize=(10, 6))
dendrogram(
    Z,
    truncate_mode="lastp",  # Show only last 20 merges
    p=20,
    leaf_rotation=90,
    leaf_font_size=10,
    show_contracted=True,
    color_threshold=7,
)
plt.title("Hierarchical Clustering Dendrogram")
plt.xlabel("Sample Index or Cluster Size")
plt.ylabel("Distance")
plt.axhline(y=7, color="r", linestyle="--", label="Cut for 3 clusters")
plt.legend()
plt.tight_layout()
plt.savefig("dendrogram_example.png", dpi=100)
plt.show()
```

**Interpretation:**
- Height = distance at which merge occurred
- Longer vertical lines = more distinct clusters
- Cut horizontally to determine number of clusters

**Related Terms:** Linkage Matrix, Cut Height, Cluster Hierarchy

---

### Linkage Matrix

**Definition:** A condensed matrix returned by `scipy.cluster.hierarchy.linkage` containing merge history and distances.

**Format:**
```
[cluster1_idx, cluster2_idx, distance, sample_count]
```

**Example:**
```python
from scipy.cluster.hierarchy import linkage
import numpy as np

X = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]])

# Create linkage matrix
Z = linkage(X, method="ward")

print("Linkage Matrix (last 5 rows):")
print("  [cluster1, cluster2, distance, count]")
print(Z[-5:])

# Interpretation
print("\nFirst merge: clusters", int(Z[0, 0]), "and", int(Z[0, 1]))
print("Distance:", Z[0, 2])
```

**Related Terms:** Dendrogram, Hierarchical Clustering

---

### Cut Height

**Definition:** The threshold distance at which to cut the dendrogram to obtain a flat clustering. Determines the number of clusters.

**Example:**
```python
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.datasets import make_blobs
import numpy as np

np.random.seed(42)
X, _ = make_blobs(n_samples=50, centers=3, random_state=42)

Z = linkage(X, method="ward")

# Cut at different heights
for height in [5, 7, 10]:
    labels = fcluster(Z, t=height, criterion="distance")
    n_clusters = len(np.unique(labels))
    print(f"Cut height {height}: {n_clusters} clusters")

# The "elbow" in dendrogram height suggests optimal cut
```

**Related Terms:** Dendrogram, Number of Clusters

---

### Cophenetic Distance

**Definition:** The distance at which two points are first merged in the hierarchical clustering. Used to evaluate cluster quality.

**Example:**
```python
from scipy.cluster.hierarchy import linkage, cophenet
from scipy.spatial.distance import pdist
from sklearn.datasets import make_blobs
import numpy as np

np.random.seed(42)
X, _ = make_blobs(n_samples=50, centers=3, random_state=42)

# Calculate cophenetic correlation
Z = linkage(X, method="ward")
c, coph_dists = cophenet(Z, pdist(X))

print(f"Cophenetic correlation: {c:.4f}")
print("Higher is better (closer to 1)")
print("Measures how well dendrogram preserves pairwise distances")
```

**Related Terms:** Linkage Matrix, Cluster Quality

---

### Distance Metric

**Definition:** A function measuring similarity/dissimilarity between data points. Affects which points cluster together.

**Common Metrics:**

| Metric | Formula | Use Case |
|--------|---------|----------|
| Euclidean | √(Σ(xᵢ-yᵢ)²) | Default, continuous data |
| Manhattan | Σ\|xᵢ-yᵢ\| | Sparse data, outliers |
| Cosine | 1 - cos(θ) | Text, high-dimensional |

**Example:**
```python
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import numpy as np

X = np.random.randn(100, 5)

# Euclidean (default)
clustering_euc = AgglomerativeClustering(n_clusters=3, metric="euclidean")
labels_euc = clustering_euc.fit_predict(X)

# Manhattan
clustering_man = AgglomerativeClustering(n_clusters=3, metric="manhattan")
labels_man = clustering_man.fit_predict(X)

sil_euc = silhouette_score(X, labels_euc)
sil_man = silhouette_score(X, labels_man)

print(f"Euclidean: {sil_euc:.4f}")
print(f"Manhattan: {sil_man:.4f}")
```

**Related Terms:** Euclidean Distance, Cosine Similarity

---

## Formulas Summary

| Formula | Expression |
|---------|-----------|
| Complete Linkage | max{d(a,b) : a ∈ A, b ∈ B} |
| Single Linkage | min{d(a,b) : a ∈ A, b ∈ B} |
| Average Linkage | (1/\|A\|·\|B\|) Σ d(a,b) |
| Ward Linkage | (\|A\|·\|B\|)/(\|A\|+\|B\|) · \|\|μ_A - μ_B\|\|² |
| Euclidean Distance | √(Σ(xᵢ - yᵢ)²) |

---

## Code Snippets Quick Reference

```python
# Agglomerative Clustering
from sklearn.cluster import AgglomerativeClustering

clustering = AgglomerativeClustering(n_clusters=3, linkage="ward")
labels = clustering.fit_predict(X)

# Linkage Matrix
from scipy.cluster.hierarchy import linkage

Z = linkage(X, method="ward")

# Dendrogram
from scipy.cluster.hierarchy import dendrogram

dendrogram(Z)

# Cut Dendrogram
from scipy.cluster.hierarchy import fcluster

labels = fcluster(Z, t=7, criterion="distance")

# Cophenetic Correlation
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist

c, _ = cophenet(Z, pdist(X))

# Different Linkage Methods
for method in ["ward", "complete", "average", "single"]:
    clustering = AgglomerativeClustering(n_clusters=3, linkage=method)
```

---

## Common Pitfalls

1. **Using on large datasets** — O(n³) complexity, use K-Means
2. **Ignoring linkage method** — Different methods give different results
3. **Not scaling features** — Distance-based, scale matters
4. **Not visualizing dendrogram** — Hard to interpret without it
5. **Wrong cut height** — Results in wrong number of clusters

---

## Further Reading

- [Scikit-learn - Hierarchical Clustering](https://scikit-learn.org/stable/modules/clustering.html#hierarchical-clustering)
- [SciPy - Hierarchical Clustering](https://docs.scipy.org/doc/scipy/reference/cluster.hierarchy.html)
- [Wikipedia - Hierarchical Clustering](https://en.wikipedia.org/wiki/Hierarchical_clustering)
