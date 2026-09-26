"""
03 - Basic SciPy Functions
===========================
Explore the core utility functions and modules that SciPy provides
for everyday scientific computing tasks.

Topics:
- scipy.optimize basics
- scipy.interpolate quick look
- scipy.spatial distance calculations
- scipy.ndimage basic filtering
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

# ============================================================
# Example 1: Finding Roots of Equations
# ============================================================
print("=" * 60)
print("Example 1: Finding Roots of Equations")
print("=" * 60)

from scipy.optimize import brentq, fsolve


# brentq finds a root of f(x) = 0 in interval [a, b]
# Example: Find where x^3 - 2x - 5 = 0
def f(x):
    return x**3 - 2 * x - 5


# Plot to see where the root is
x_vals = np.linspace(-2, 3, 500)
y_vals = f(x_vals)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x_vals, y_vals, "b-", linewidth=2, label="f(x) = x^3 - 2x - 5")
ax.axhline(y=0, color="k", linewidth=0.5)
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_title("Finding Root of x^3 - 2x - 5")
ax.legend()
ax.grid(True, alpha=0.3)

# Find root using Brent's method
root = brentq(f, 2, 3)
print(f"Root of x^3 - 2x - 5 = 0: x = {root:.6f}")
print(f"Verification: f({root:.6f}) = {f(root):.2e}")

ax.plot(root, f(root), "ro", markersize=10, label=f"Root â‰ˆ {root:.4f}")
ax.legend()
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_03_roots.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_03_roots.png')}")


# System of nonlinear equations with fsolve
def system(vars):
    x, y = vars
    eq1 = x**2 + y**2 - 4  # Circle radius 2
    eq2 = x - y - 1  # Line
    return [eq1, eq2]


solution = fsolve(system, [1, 0])
print(f"\nIntersection of x^2+y^2=4 and x-y=1:")
print(f"  Solution: x={solution[0]:.4f}, y={solution[1]:.4f}")
print(f"  Verify eq1: {solution[0] ** 2 + solution[1] ** 2:.4f} (should be 4)")
print(f"  Verify eq2: {solution[0] - solution[1]:.4f} (should be 1)")

# ============================================================
# Example 2: Numerical Differentiation
# ============================================================
print("\n" + "=" * 60)
print("Example 2: Numerical Differentiation")
print("=" * 60)

from scipy.optimize import approx_fprime


# Custom numerical derivative using finite differences (replaces deprecated scipy.misc.derivative)
def numerical_derivative(func, x0, dx=1e-5, n=1):
    """Compute nth derivative using central finite differences."""
    if n == 1:
        return (func(x0 + dx) - func(x0 - dx)) / (2 * dx)
    elif n == 2:
        return (func(x0 + dx) - 2 * func(x0) + func(x0 - dx)) / (dx**2)
    else:
        raise ValueError(f"Only n=1,2 supported, got n={n}")


# Compute derivatives of f(x) = sin(x)
def g(x):
    return np.sin(x)


x0 = np.pi / 4  # 45 degrees

# First derivative of sin(x) = cos(x)
d1 = numerical_derivative(g, x0, dx=1e-5, n=1)
print(f"First derivative of sin(x) at x=pi/4:")
print(f"  Numerical:  {d1:.6f}")
print(f"  Analytical: {np.cos(x0):.6f}")

# Second derivative of sin(x) = -sin(x)
d2 = numerical_derivative(g, x0, dx=1e-5, n=2)
print(f"\nSecond derivative of sin(x) at x=pi/4:")
print(f"  Numerical:  {d2:.6f}")
print(f"  Analytical: {-np.sin(x0):.6f}")

# Compare derivatives at multiple points
x_pts = np.linspace(0, 2 * np.pi, 200)
numerical_d1 = [numerical_derivative(g, x, dx=1e-6, n=1) for x in x_pts]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x_pts, np.sin(x_pts), "b-", label="sin(x)", linewidth=2)
ax.plot(x_pts, np.cos(x_pts), "r--", label="cos(x) [analytical]", linewidth=1.5)
ax.plot(x_pts, numerical_d1, "g.", label="Numerical derivative", markersize=3)
ax.set_title("Numerical vs Analytical Derivative of sin(x)")
ax.set_xlabel("x")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_03_derivative.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_03_derivative.png')}")

# ============================================================
# Example 3: Spatial Distance Calculations
# ============================================================
print("\n" + "=" * 60)
print("Example 3: Spatial Distance Calculations")
print("=" * 60)

from scipy.spatial.distance import cdist, pdist, squareform

# 2D points (all nonzero so cosine/correlation metrics stay defined)
points_A = np.array([[1, 1], [1, 0], [0, 1], [2, 3]])
points_B = np.array([[0.5, 0.5], [2, 2]])

# Euclidean distances between A and B
dist_matrix = cdist(points_A, points_B, metric="euclidean")
print("Euclidean distances (A x B):")
for i, row in enumerate(dist_matrix):
    print(f"  A[{i}] to B[0]={row[0]:.4f}, B[1]={row[1]:.4f}")

# Different distance metrics
metrics = ["euclidean", "cityblock", "cosine", "correlation"]
print("\nDistance from A[0]=[0,0] to A[3]=[1,1] using different metrics:")
for m in metrics:
    d = cdist(points_A[:1], points_A[3:], metric=m)
    print(f"  {m:<15s}: {d[0, 0]:.4f}")

# Pairwise distances within a set
pairwise = pdist(points_A, metric="euclidean")
pairwise_square = squareform(pairwise)
print(f"\nPairwise Euclidean distances (4 points, 6 pairs):")
print(f"  Compact form: {pairwise}")
print(f"  Square form shape: {pairwise_square.shape}")

# ============================================================
# Example 4: Gaussian Filtering for Data Smoothing
# ============================================================
print("\n" + "=" * 60)
print("Example 4: Gaussian Filtering (Data Smoothing)")
print("=" * 60)

from scipy.ndimage import gaussian_filter1d, gaussian_filter

# Create noisy 1D signal
np.random.seed(42)
x = np.linspace(0, 4 * np.pi, 200)
signal_clean = np.sin(x) * np.exp(-0.2 * x)
signal_noisy = signal_clean + np.random.normal(0, 0.2, len(x))

# Apply Gaussian filter with different sigmas
smoothed_1 = gaussian_filter1d(signal_noisy, sigma=2)
smoothed_3 = gaussian_filter1d(signal_noisy, sigma=5)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, signal_noisy, "gray", alpha=0.5, label="Noisy signal")
ax.plot(x, signal_clean, "b-", linewidth=2, label="Clean signal")
ax.plot(x, smoothed_1, "r-", linewidth=1.5, label="Gaussian Ïƒ=2")
ax.plot(x, smoothed_3, "g-", linewidth=1.5, label="Gaussian Ïƒ=5")
ax.set_title("Gaussian Smoothing of Noisy Signal")
ax.set_xlabel("x")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_03_smoothing.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_03_smoothing.png')}")

# 2D Gaussian filter example
image = np.random.rand(100, 100)
image[30:70, 30:70] += 2  # Bright square region
image_smooth = gaussian_filter(image, sigma=5)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
im0 = axes[0].imshow(image, cmap="viridis")
axes[0].set_title("Noisy 2D Data")
plt.colorbar(im0, ax=axes[0], shrink=0.8)
im1 = axes[1].imshow(image_smooth, cmap="viridis")
axes[1].set_title("After Gaussian Filter (Ïƒ=5)")
plt.colorbar(im1, ax=axes[1], shrink=0.8)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_03_2d_filter.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_03_2d_filter.png')}")

# ============================================================
# Example 5: Quick Optimization (minimize a function)
# ============================================================
print("\n" + "=" * 60)
print("Example 5: Basic Optimization with scipy.optimize.minimize")
print("=" * 60)

from scipy.optimize import minimize


# Minimize the Rosenbrock function (classic optimization test)
# f(x,y) = (1-x)^2 + 100*(y-x^2)^2
def rosenbrock(xy):
    x, y = xy
    return (1 - x) ** 2 + 100 * (y - x**2) ** 2


# Start from different initial guesses
starts = [(-1, 1), (2, -1), (0.5, 0.5)]
print("Rosenbrock function minimum (true min at x=1, y=1):")
for start in starts:
    result = minimize(rosenbrock, start, method="L-BFGS-B")
    print(
        f"  Start {start} -> x={result.x[0]:.6f}, y={result.x[1]:.6f}, "
        f"f={result.fun:.2e}, iters={result.nit}"
    )

print("\n[OK] Basic SciPy functions covered!")
print("   Next: 04-statistics.py for statistical analysis.")
