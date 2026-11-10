# Glossary: K-Means Clustering (Lecture 16)

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| K-Means | Partitions data into K clusters based on centroid proximity | `KMeans(n_clusters=3)` |
| Cluster | Group of similar data points | Customer segment |
| Centroid | Center point of a cluster | Mean of cluster points |
| Inertia | Within-cluster sum of squares | `kmeans.inertia_` |
| Elbow Method | Finding optimal K by plotting inertia vs K | Visual inspection |
| Silhouette Score | Measures cluster separation quality | -1 to 1 |
| K-Means++ | Smart initialization for centroids | Default in scikit-learn |
| n_init | Number of random initializations | 10 (default) |
| Convergence | When centroids stop moving | Algorithm terminates |
| Cluster Variance | Spread within each cluster | Lower = tighter |
| Supervised Learning | Learning with labeled data | Classification |
| Unsupervised Learning | Learning without labels | Clustering |
| Dimensionality Reduction | Reducing number of features | PCA |
| Feature Scaling | Normalizing feature ranges | StandardScaler |
| Outlier | Extreme value affecting clustering | Z-score > 3 |

---

## Detailed Term Definitions

### K-Means

**Definition:** An unsupervised learning algorithm that partitions n observations into K clusters, where each observation belongs to the cluster with the nearest centroid.

**Algorithm Steps:**
1. Initialize K centroids randomly (or K-Means++)
2. Assign each point to nearest centroid
3. Recalculate centroids as mean of assigned points
4. Repeat until convergence

**Example:**
```python
from sklearn.cluster import KMeans
import numpy as np

# Sample data
X = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]])

# Apply K-Means with K=2
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
kmeans.fit(X)

print(f"Labels: {kmeans.labels_}")
print(f"Centroids:\n{kmeans.cluster_centers_}")
print(f"Inertia: {kmeans.inertia_:.4f}")
```

**Related Terms:** Clustering, Centroid, Unsupervised Learning

---

### Cluster

**Definition:** A group of data points that are more similar to each other than to points in other groups.

**Example:**
```python
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd

# Customer data
np.random.seed(42)
X = np.column_stack(
    [
        np.concatenate([np.random.normal(30000, 5000, 50), np.random.normal(80000, 10000, 50)]),
        np.concatenate([np.random.normal(20, 5, 50), np.random.normal(70, 10, 50)]),
    ]
)

# Cluster
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)

# Analyze clusters
df = pd.DataFrame({"income": X[:, 0], "spending": X[:, 1], "cluster": labels})
print("Cluster means:")
print(df.groupby("cluster").mean().round(0))
```

**Related Terms:** K-Means, Centroid, Segment

---

### Centroid

**Definition:** The center point of a cluster, calculated as the mean of all points in that cluster.

**Example:**
```python
import numpy as np
from sklearn.cluster import KMeans

X = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]])

kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
kmeans.fit(X)

print("Cluster Centers (Centroids):")
for i, center in enumerate(kmeans.cluster_centers_):
    print(f"  Cluster {i}: {center}")

# Manual calculation
cluster_0_points = X[kmeans.labels_ == 0]
cluster_0_centroid = cluster_0_points.mean(axis=0)
print(f"\nManual centroid for cluster 0: {cluster_0_centroid}")
```

**Related Terms:** K-Means, Cluster, Mean

---

### Inertia

**Definition:** The within-cluster sum of squares, measuring how compact the clusters are. Lower values indicate tighter clusters.

**Formula:**
```
Inertia = Σ Σ ||xᵢ - μₖ||²
```

**Example:**
```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import numpy as np

X, _ = make_blobs(n_samples=300, centers=4, random_state=42)

# Test different K values
for k in range(1, 8):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    print(f"K={k}: Inertia = {kmeans.inertia_:.2f}")

# Inertia decreases as K increases
# But too high K means overfitting
```

**Properties:**
- Always non-negative
- Decreases as K increases
- 0 when each point is its own cluster
- Used in elbow method

**Related Terms:** Elbow Method, Within-Cluster Sum of Squares

---

### Elbow Method

**Definition:** A technique to find optimal K by plotting inertia vs K and looking for the "elbow" where the rate of decrease sharply changes.

**Example:**
```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np

X, _ = make_blobs(n_samples=300, centers=4, random_state=42)

inertias = []
K_range = range(1, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

plt.figure(figsize=(8, 4))
plt.plot(K_range, inertias, "bo-", linewidth=2, markersize=8)
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.title("Elbow Method")
plt.xticks(K_range)
plt.grid(True, alpha=0.3)
plt.savefig("elbow_method.png", dpi=100)
plt.show()

# The "elbow" is at K=4 (true number of clusters)
```

**Interpretation:**
- Steep decrease: Adding clusters helps
- Plateau: Adding clusters doesn't help much
- Elbow point: Optimal K

**Related Terms:** Inertia, K-Means, Cluster Evaluation

---

### Silhouette Score

**Definition:** A metric measuring how similar a point is to its own cluster compared to other clusters. Range: -1 to 1.

**Formula:**
```
s(i) = (b(i) - a(i)) / max(a(i), b(i))
```

Where:
- `a(i)` = average distance to same cluster
- `b(i)` = average distance to nearest other cluster

**Example:**
```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score
import numpy as np

X, _ = make_blobs(n_samples=300, centers=4, random_state=42)

# Test different K values
for k in range(2, 8):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    print(f"K={k}: Silhouette Score = {score:.4f}")

# Higher score = better defined clusters
```

**Score Interpretation:**

| Score | Meaning |
|-------|---------|
| 0.7 - 1.0 | Strong structure |
| 0.5 - 0.7 | Reasonable structure |
| 0.25 - 0.5 | Weak structure |
| < 0.25 | No substantial structure |
| Negative | Likely wrong clustering |

**Related Terms:** Silhouette Coefficient, Cluster Evaluation

---

### K-Means++

**Definition:** An improved initialization method that selects initial centroids that are far apart, leading to better convergence than random initialization.

**Example:**
```python
from sklearn.cluster import KMeans
import numpy as np

X = np.random.randn(100, 2)

# K-Means++ (default)
kmeans_pp = KMeans(n_clusters=3, init="k-means++", n_init=10, random_state=42)
kmeans_pp.fit(X)
print(f"K-Means++ Inertia: {kmeans_pp.inertia_:.2f}")

# Random initialization (worse)
kmeans_random = KMeans(n_clusters=3, init="random", n_init=10, random_state=42)
kmeans_random.fit(X)
print(f"Random Init Inertia: {kmeans_random.inertia_:.2f}")

# K-Means++ typically gives lower inertia
```

**Benefits:**
- Faster convergence
- Better cluster quality
- More consistent results
- Default in scikit-learn

**Related Terms:** K-Means, Initialization, Centroid

---

### n_init

**Definition:** The number of times K-Means runs with different centroid seeds. The best result (lowest inertia) is returned.

**Example:**
```python
from sklearn.cluster import KMeans
import numpy as np

X = np.random.randn(100, 2)

# Default: 10 initializations
kmeans_10 = KMeans(n_clusters=3, n_init=10, random_state=42)
kmeans_10.fit(X)
print(f"n_init=10: Inertia = {kmeans_10.inertia_:.2f}")

# More initializations (more thorough)
kmeans_50 = KMeans(n_clusters=3, n_init=50, random_state=42)
kmeans_50.fit(X)
print(f"n_init=50: Inertia = {kmeans_50.inertia_:.2f}")

# Single initialization (faster but less reliable)
kmeans_1 = KMeans(n_clusters=3, n_init=1, random_state=42)
kmeans_1.fit(X)
print(f"n_init=1: Inertia = {kmeans_1.inertia_:.2f}")
```

**Tradeoff:**
- Higher n_init = better results, slower
- Lower n_init = faster, less reliable

**Related Terms:** K-Means, Initialization, Convergence

---

### Convergence

**Definition:** When K-Means algorithm stops because centroids no longer move significantly, or maximum iterations reached.

**Example:**
```python
from sklearn.cluster import KMeans
import numpy as np

X = np.random.randn(100, 2)

# Set max iterations
kmeans = KMeans(n_clusters=3, max_iter=100, random_state=42)
kmeans.fit(X)

print(f"Number of iterations: {kmeans.n_iter_}")
print(f"Converged: {kmeans.n_iter_ < 100}")

# Check if converged
if kmeans.n_iter_ < 100:
    print("Algorithm converged before max iterations")
else:
    print("Reached max iterations - may not have converged")
```

**Properties:**
- K-Means always converges (finite iterations)
- Convergence speed depends on data and initialization
- Usually converges in < 20 iterations

**Related Terms:** K-Means, Iteration, Maximum Iterations

---

### Cluster Variance

**Definition:** The spread of data points within each cluster. Lower variance means tighter, more cohesive clusters.

**Example:**
```python
from sklearn.cluster import KMeans
import numpy as np

X = np.random.randn(100, 2)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(X)
labels = kmeans.labels_

# Calculate variance for each cluster
for i in range(3):
    cluster_points = X[labels == i]
    variance = np.var(cluster_points, axis=0)
    print(f"Cluster {i}: Variance = {variance}")

# Overall cluster variance (inertia / n_samples)
overall_variance = kmeans.inertia_ / len(X)
print(f"\nOverall cluster variance: {overall_variance:.4f}")
```

**Related Terms:** Inertia, Within-Cluster Sum of Squares

---

### Feature Scaling

**Definition:** Normalizing features to have similar scales, crucial for distance-based algorithms like K-Means.

**Example:**
```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

# Features with different scales
X = np.array(
    [
        [100000, 50],  # Income: 100k, Age: 50
        [200000, 30],  # Income: 200k, Age: 30
        [150000, 40],  # Income: 150k, Age: 40
    ]
)

# Without scaling (income dominates)
kmeans_unscaled = KMeans(n_clusters=2, random_state=42, n_init=10)
labels_unscaled = kmeans_unscaled.fit_predict(X)

# With scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans_scaled = KMeans(n_clusters=2, random_state=42, n_init=10)
labels_scaled = kmeans_scaled.fit_predict(X_scaled)

print("Without scaling:", labels_unscaled)
print("With scaling:", labels_scaled)
```

**Related Terms:** StandardScaler, MinMaxScaler, Normalization

---

### Outlier

**Definition:** A data point that is significantly different from other observations, potentially distorting cluster formation.

**Example:**
```python
from sklearn.cluster import KMeans
import numpy as np

# Data with outlier
X = np.array([[1, 2], [1.5, 1.8], [2, 2.2], [8, 8], [8.5, 8.2], [9, 8], [50, 50]])  # Outlier!

kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)

print("Cluster labels:", labels)
print("Outlier assigned to cluster:", labels[-1])

# Outlier can pull centroid away
print("\nCentroids:")
print(kmeans.cluster_centers_)
```

**Solutions:**
- Remove outliers before clustering
- Use DBSCAN (handles outliers)
- Use robust scaling

**Related Terms:** K-Means Sensitivity, Data Cleaning, DBSCAN

---

### Supervised Learning

**Definition:** Machine learning where the model learns from labeled training data (input-output pairs).

**Example:**
```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Labeled data (features + target)
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# Supervised learning
model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X_train, y_train)  # Learns from labels

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Supervised Learning Accuracy: {accuracy:.4f}")
```

**Related Terms:** Classification, Regression, Unsupervised Learning

---

### Unsupervised Learning

**Definition:** Machine learning where the model finds patterns in data without labeled outputs. K-Means is an unsupervised algorithm.

**Example:**
```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import numpy as np

# Unlabeled data (no target variable)
X, _ = make_blobs(n_samples=300, centers=3, random_state=42)

# Unsupervised learning
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)  # Discovers clusters

print(f"Found {len(np.unique(labels))} clusters")
print(f"Cluster sizes: {np.bincount(labels)}")
```

**Related Terms:** Clustering, K-Means, PCA, Supervised Learning

---

### Dimensionality Reduction

**Definition:** Reducing the number of features while preserving important information. Useful before clustering high-dimensional data.

**Example:**
```python
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
import numpy as np

iris = load_iris()
X = iris.data  # 4 features

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Reduce to 2 dimensions
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print(f"Original shape: {X.shape}")
print(f"PCA shape: {X_pca.shape}")
print(f"Variance explained: {pca.explained_variance_ratio_.sum():.2%}")

# Cluster in reduced space
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_pca)
print(f"Clusters found: {len(np.unique(labels))}")
```

**Related Terms:** PCA, t-SNE, Feature Selection

---

## Formulas Summary

| Formula | Expression |
|---------|-----------|
| Inertia | Σ Σ \|\|xᵢ - μₖ\|\|² |
| Silhouette Score | (b(i) - a(i)) / max(a(i), b(i)) |
| Centroid | μₖ = (1/nₖ) Σ xᵢ for xᵢ in cluster k |
| Distance (Euclidean) | √(Σ(xᵢ - yᵢ)²) |

---

## Code Snippets Quick Reference

```python
# Basic K-Means
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(X)
labels = kmeans.labels_
centers = kmeans.cluster_centers_
inertia = kmeans.inertia_

# Elbow Method
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)

# Silhouette Score
from sklearn.metrics import silhouette_score

score = silhouette_score(X, labels)

# K-Means++
kmeans = KMeans(n_clusters=3, init="k-means++", random_state=42)

# Feature Scaling (IMPORTANT!)
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Predict new points
new_labels = kmeans.predict(X_new)
```

---

## Common Pitfalls

1. **Not scaling features** — Distance-based, scale matters
2. **Wrong K** — Always use elbow/silhouette to find optimal K
3. **Ignoring outliers** — K-Means is sensitive to outliers
4. **Single initialization** — Use n_init > 1
5. **Non-spherical clusters** — K-Means assumes spherical clusters

---

## Further Reading

- [Scikit-learn - K-Means](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [Wikipedia - K-means Clustering](https://en.wikipedia.org/wiki/K-means_clustering)
- [MLU Explain - K-Means](https://mlu-explain.github.io/k-means/)
