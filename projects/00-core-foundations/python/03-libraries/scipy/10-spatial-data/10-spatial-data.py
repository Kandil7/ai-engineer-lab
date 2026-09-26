"""
10 - SciPy Spatial Data
========================
SciPy's spatial module provides tools for spatial data structures
and algorithms, including KD-Trees, Delaunay triangulation, and
convex hulls.

Topics:
- KD-Tree for nearest neighbor queries
- Delaunay triangulation
- Convex hull computation
- Voronoi diagrams
- Distance computations in spatial data
"""

import numpy as np

# Ensure output directory exists (Tier 0 fix: Windows + CI)
import os

OUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "outputs", "scipy"
)
os.makedirs(OUT_DIR, exist_ok=True)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.spatial import KDTree, Delaunay, ConvexHull, Voronoi, voronoi_plot_2d

# ============================================================
# Example 1: KD-Tree Nearest Neighbor Search
# ============================================================
print("=" * 60)
print("Example 1: KD-Tree for Nearest Neighbor Search")
print("=" * 60)

# Generate random 2D points
np.random.seed(42)
n_points = 1000
points = np.random.rand(n_points, 2)

# Build KD-Tree
tree = KDTree(points)

# Query: find 5 nearest neighbors to a specific point
query_point = np.array([0.5, 0.5])
distances, indices = tree.query(query_point, k=5)

print(f"Query point: {query_point}")
print(f"5 nearest neighbors:")
for i, (idx, dist) in enumerate(zip(indices, distances)):
    print(f"  #{i + 1}: point {points[idx]}, distance = {dist:.4f}")

# Range query: find all points within radius r
radius = 0.1
within_radius = tree.query_ball_point(query_point, radius)
print(f"\nPoints within radius {radius}: {len(within_radius)} / {n_points}")

# Bulk query: nearest neighbor for multiple points
query_points = np.array([[0.2, 0.8], [0.7, 0.3], [0.9, 0.9]])
dists, idxs = tree.query(query_points, k=3)
print(f"\n3-NN for multiple query points:")
for q, d, idx in zip(query_points, dists, idxs):
    print(f"  Query {q}: distances = {d}")

# Visualize
fig, ax = plt.subplots(figsize=(8, 8))
ax.scatter(points[:, 0], points[:, 1], s=5, alpha=0.5, color="gray", label="All points")
ax.scatter(query_point[0], query_point[1], c="red", s=100, marker="*", label="Query point")
ax.scatter(points[indices, 0], points[indices, 1], c="blue", s=80, marker="D", label="5 nearest")
circle = plt.Circle(query_point, radius, fill=False, color="green", linestyle="--", linewidth=2)
ax.add_patch(circle)
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.set_title(f"KD-Tree: {len(within_radius)} points within radius {radius}")
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_aspect("equal")
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_10_kdtree.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_10_kdtree.png')}")

# ============================================================
# Example 2: Delaunay Triangulation
# ============================================================
print("\n" + "=" * 60)
print("Example 2: Delaunay Triangulation")
print("=" * 60)

# Points forming a shape
np.random.seed(42)
n = 50
theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
r = 0.5 + 0.2 * np.sin(3 * theta)  # Star-like shape
points_tri = np.column_stack([r * np.cos(theta), r * np.sin(theta)])
# Add some interior points
interior = np.random.randn(20, 2) * 0.2
points_tri = np.vstack([points_tri, interior])

# Compute Delaunay triangulation
tri = Delaunay(points_tri)
print(f"Number of points: {len(points_tri)}")
print(f"Number of triangles: {len(tri.simplices)}")


# Compute triangle areas
def triangle_area(p1, p2, p3):
    return 0.5 * abs((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1]))


areas = [triangle_area(points_tri[s[0]], points_tri[s[1]], points_tri[s[2]]) for s in tri.simplices]
print(f"Triangle areas: min={min(areas):.4f}, max={max(areas):.4f}, mean={np.mean(areas):.4f}")

# Visualize
fig, ax = plt.subplots(figsize=(8, 8))
ax.triplot(points_tri[:, 0], points_tri[:, 1], tri.simplices, "b-", linewidth=0.8)
ax.scatter(points_tri[:, 0], points_tri[:, 1], c="red", s=30, zorder=5)
ax.set_title(f"Delaunay Triangulation ({len(tri.simplices)} triangles)")
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_10_delaunay.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_10_delaunay.png')}")

# Point-in-triangle test
test_point = np.array([0.0, 0.0])
# Find which simplex contains the test point
simplex_idx = tri.find_simplex(test_point)
print(f"\nPoint {test_point} is in simplex #{simplex_idx}")

# ============================================================
# Example 3: Convex Hull
# ============================================================
print("\n" + "=" * 60)
print("Example 3: Convex Hull Computation")
print("=" * 60)

# Random points
np.random.seed(42)
points_hull = np.random.randn(100, 2)

# Compute convex hull
hull = ConvexHull(points_hull)
print(f"Input points: {len(points_hull)}")
print(f"Hull vertices: {len(hull.vertices)}")
print(f"Hull area: {hull.volume:.4f}")  # In 2D, volume is area

# The hull vertices (in order)
hull_points = points_hull[hull.vertices]
print(f"Hull vertex indices: {hull.vertices}")
print(f"Hull perimeter: {hull.area:.4f}")  # In 2D, area is perimeter

# Visualize
fig, ax = plt.subplots(figsize=(8, 8))
ax.scatter(points_hull[:, 0], points_hull[:, 1], s=30, alpha=0.5, color="blue")
# Draw hull
hull_loop = np.append(hull.vertices, hull.vertices[0])
ax.plot(
    points_hull[hull_loop, 0], points_hull[hull_loop, 1], "r-", linewidth=2, label="Convex hull"
)
ax.scatter(
    points_hull[hull.vertices, 0],
    points_hull[hull.vertices, 1],
    c="red",
    s=80,
    marker="D",
    zorder=5,
    label="Hull vertices",
)
ax.set_title(f"Convex Hull ({len(hull.vertices)} vertices, area={hull.volume:.4f})")
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_aspect("equal")
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_10_convexhull.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_10_convexhull.png')}")

# ============================================================
# Example 4: Voronoi Diagram
# ============================================================
print("\n" + "=" * 60)
print("Example 4: Voronoi Diagram")
print("=" * 60)

# Well-spaced points
np.random.seed(42)
n_vor = 15
points_vor = np.random.rand(n_vor, 2)

# Compute Voronoi
vor = Voronoi(points_vor)
print(f"Number of input points: {n_vor}")
print(f"Number of Voronoi regions: {len(vor.regions)}")
print(f"Number of Voronoi vertices: {len(vor.vertices)}")

# Count infinite regions (regions that extend to infinity)
infinite_regions = [i for i, region in enumerate(vor.regions) if -1 in region]
print(f"Infinite regions: {len(infinite_regions)}")

# Plot
fig, ax = plt.subplots(figsize=(8, 8))
voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors="blue", line_width=1.5)
ax.scatter(points_vor[:, 0], points_vor[:, 1], c="red", s=80, zorder=5, label="Sites")
ax.set_title(f"Voronoi Diagram ({n_vor} sites)")
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 1.1)
ax.set_aspect("equal")
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_10_voronoi.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_10_voronoi.png')}")

# ============================================================
# Example 5: Spatial Distance and Proximity
# ============================================================
print("\n" + "=" * 60)
print("Example 5: Spatial Distance Metrics")
print("=" * 60)

from scipy.spatial.distance import cdist, pdist, squareform

# Two sets of 3D points
np.random.seed(42)
set_a = np.random.rand(5, 3) * 10  # 5 points in 3D
set_b = np.random.rand(3, 3) * 10  # 3 points in 3D

# Compute pairwise distances with different metrics
metrics = ["euclidean", "cityblock", "cosine", "chebyshev"]
print("Distance matrix A to B (5x3) with different metrics:")
for m in metrics:
    dist = cdist(set_a, set_b, metric=m)
    print(f"\n  {m}:")
    print(f"  {dist}")

# Intrinsic dimensionality estimation using nearest neighbor distances
from scipy.spatial.distance import pdist as pdist_func

# Random points on a 2D manifold embedded in 5D
n_manifold = 200
t = np.random.uniform(0, 2 * np.pi, n_manifold)
manifold_points = np.column_stack(
    [
        np.cos(t),
        np.sin(t),
        0.1 * np.cos(2 * t),
        0.1 * np.sin(2 * t),
        0.05 * np.random.randn(n_manifold),
    ]
)

# Build tree and compute k-NN distances
tree_manifold = KDTree(manifold_points)
k_values = [1, 2, 5, 10, 20, 50]
print("\nIntrinsic dimensionality estimation:")
for k in k_values:
    dists_k, _ = tree_manifold.query(manifold_points, k=k + 1)
    avg_log_dist = np.mean(np.log(dists_k[:, -1] + 1e-10))
    if k > 1:
        # crude dimensionality estimate
        print(f"  k={k:3d}: avg log distance = {avg_log_dist:.4f}")

print("\n[OK] SciPy spatial module covered!")
print("   Next: 11-image-processing.py for image operations.")
