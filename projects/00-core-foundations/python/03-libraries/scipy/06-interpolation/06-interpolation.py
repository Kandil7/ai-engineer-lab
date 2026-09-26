"""
06 - SciPy Interpolation
=========================
Interpolation estimates values between known data points. SciPy provides
several interpolation methods for 1D, 2D, and higher-dimensional data.

Topics:
- 1D interpolation (linear, cubic, spline)
- 2D interpolation (RegularGridInterpolator)
- Cubic spline interpolation
- Extrapolation and boundary handling
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
from scipy import interpolate

# ============================================================
# Example 1: Basic 1D Interpolation
# ============================================================
print("=" * 60)
print("Example 1: Basic 1D Interpolation Methods")
print("=" * 60)

# Known data points (sparse)
x_data = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y_data = np.sin(x_data * 0.5) + 0.1 * x_data

# Create a fine grid for interpolation
x_fine = np.linspace(0, 10, 300)

# Different interpolation methods
methods = {
    "Linear": interpolate.interp1d(x_data, y_data, kind="linear", fill_value="extrapolate"),
    "Cubic": interpolate.interp1d(x_data, y_data, kind="cubic", fill_value="extrapolate"),
    "Quadratic": interpolate.interp1d(x_data, y_data, kind="quadratic", fill_value="extrapolate"),
}

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x_data, y_data, "ko", markersize=8, label="Data points", zorder=5)
for name, interp_func in methods.items():
    y_interp = interp_func(x_fine)
    ax.plot(x_fine, y_interp, linewidth=2, label=f"{name} interpolation")

# True function for comparison
y_true = np.sin(x_fine * 0.5) + 0.1 * x_fine
ax.plot(x_fine, y_true, "k--", alpha=0.4, linewidth=1, label="True function")
ax.set_title("1D Interpolation Methods Comparison")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_06_1d_interp.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_06_1d_interp.png')}")

# Print interpolation values at specific points
test_points = [1.5, 3.7, 6.2, 8.9]
print(f"\nInterpolation at test points:")
print(f"  {'Point':>6s} {'Linear':>10s} {'Cubic':>10s} {'True':>10s}")
for pt in test_points:
    lin_val = methods["Linear"](pt)
    cub_val = methods["Cubic"](pt)
    true_val = np.sin(pt * 0.5) + 0.1 * pt
    print(f"  {pt:6.1f} {lin_val:10.6f} {cub_val:10.6f} {true_val:10.6f}")

# ============================================================
# Example 2: Cubic Spline Interpolation
# ============================================================
print("\n" + "=" * 60)
print("Example 2: Cubic Spline Interpolation")
print("=" * 60)

# Generate noisy data from a smooth function
np.random.seed(42)
x_noisy = np.sort(np.random.uniform(0, 10, 15))
y_noisy = np.sin(x_noisy) + np.random.normal(0, 0.2, len(x_noisy))

# Cubic spline with different boundary conditions
# bc_type: 'natural' (zero second derivative at endpoints)
spline_natural = interpolate.CubicSpline(x_noisy, y_noisy, bc_type="natural")
# 'not-a-knot' (default, continuity of third derivative at first/last interior knots)
spline_ak = interpolate.CubicSpline(x_noisy, y_noisy, bc_type="not-a-knot")

x_test = np.linspace(0, 10, 300)
y_natural = spline_natural(x_test)
y_ak = spline_ak(x_test)
y_true_full = np.sin(x_test)

# Compute spline derivatives
dy_natural = spline_natural(x_test, 1)  # First derivative
d2y_natural = spline_natural(x_test, 2)  # Second derivative

fig, axes = plt.subplots(2, 1, figsize=(10, 7))
axes[0].plot(x_noisy, y_noisy, "ko", markersize=6, label="Noisy data")
axes[0].plot(x_test, y_natural, "b-", linewidth=2, label="Natural spline")
axes[0].plot(x_test, y_ak, "r--", linewidth=2, label="Not-a-knot spline")
axes[0].plot(x_test, y_true_full, "g--", alpha=0.5, label="True: sin(x)")
axes[0].set_title("Cubic Spline Interpolation")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(x_test, dy_natural, "b-", linewidth=2, label="1st derivative")
axes[1].plot(x_test, d2y_natural, "r--", linewidth=2, label="2nd derivative")
axes[1].set_title("Spline Derivatives")
axes[1].set_xlabel("x")
axes[1].legend()
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_06_spline.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_06_spline.png')}")

# Evaluate spline coefficients
print(f"Spline has {len(spline_natural.c)} coefficient sets")
print(f"Coefficients shape: {spline_natural.c.shape}")

# ============================================================
# Example 3: 2D Interpolation
# ============================================================
print("\n" + "=" * 60)
print("Example 3: 2D Interpolation")
print("=" * 60)

# Create a coarse 2D grid
x_2d = np.linspace(0, 5, 8)
y_2d = np.linspace(0, 5, 8)
X, Y = np.meshgrid(x_2d, y_2d)
Z = np.sin(X) * np.cos(Y) + 0.1 * X

# Create interpolation function
interp_2d = interpolate.RegularGridInterpolator((y_2d, x_2d), Z, method="cubic")

# Evaluate on a finer grid
x_fine_2d = np.linspace(0, 5, 100)
y_fine_2d = np.linspace(0, 5, 100)
X_fine, Y_fine = np.meshgrid(x_fine_2d, y_fine_2d)
points = np.column_stack([Y_fine.ravel(), X_fine.ravel()])
Z_fine = interp_2d(points).reshape(X_fine.shape)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
im0 = axes[0].pcolormesh(X, Y, Z, cmap="viridis", shading="auto")
axes[0].plot(X, Y, "k+", markersize=5)
axes[0].set_title("Coarse Grid (8Ã—8)")
plt.colorbar(im0, ax=axes[0], shrink=0.8)

im1 = axes[1].pcolormesh(X_fine, Y_fine, Z_fine, cmap="viridis", shading="auto")
axes[1].set_title("Interpolated (100Ã—100)")
plt.colorbar(im1, ax=axes[1], shrink=0.8)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_06_2d_interp.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_06_2d_interp.png')}")

# Interpolate specific points
query_points = np.array([[1.5, 2.0], [3.0, 4.0], [0.5, 1.0]])
interp_vals = interp_2d(query_points)
print(f"\n2D interpolation at specific points:")
for pt, val in zip(query_points, interp_vals):
    print(f"  f({pt[0]:.1f}, {pt[1]:.1f}) = {val:.6f}")

# ============================================================
# Example 4: Radial Basis Function (RBF) Interpolation
# ============================================================
print("\n" + "=" * 60)
print("Example 4: Radial Basis Function (RBF) Interpolation")
print("=" * 60)

# Scattered 2D data
np.random.seed(42)
n_scattered = 30
x_scattered = np.random.uniform(0, 5, n_scattered)
y_scattered = np.random.uniform(0, 5, n_scattered)
z_scattered = np.sin(x_scattered) * np.cos(y_scattered) + 0.1 * x_scattered

# RBF interpolation
rbf_interp = interpolate.Rbf(x_scattered, y_scattered, z_scattered, function="multiquadric")

# Evaluate on fine grid
x_rbf = np.linspace(0, 5, 100)
y_rbf = np.linspace(0, 5, 100)
X_rbf, Y_rbf = np.meshgrid(x_rbf, y_rbf)
Z_rbf = rbf_interp(X_rbf, Y_rbf)

# True function
Z_true = np.sin(X_rbf) * np.cos(Y_rbf) + 0.1 * X_rbf

fig, axes = plt.subplots(1, 3, figsize=(16, 4))
# Scattered data
axes[0].scatter(x_scattered, y_scattered, c=z_scattered, s=60, cmap="viridis", edgecolors="k")
axes[0].set_title(f"Scattered Data ({n_scattered} points)")

# RBF result
im1 = axes[1].pcolormesh(X_rbf, Y_rbf, Z_rbf, cmap="viridis", shading="auto")
axes[1].scatter(x_scattered, y_scattered, c="red", s=20, marker="x")
axes[1].set_title("RBF Interpolation")
plt.colorbar(im1, ax=axes[1], shrink=0.8)

# Error
im2 = axes[2].pcolormesh(X_rbf, Y_rbf, np.abs(Z_rbf - Z_true), cmap="hot", shading="auto")
axes[2].set_title("Absolute Error")
plt.colorbar(im2, ax=axes[2], shrink=0.8)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_06_rbf.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_06_rbf.png')}")

print(f"Max interpolation error: {np.abs(Z_rbf - Z_true).max():.6f}")

# ============================================================
# Example 5: Interpolation for Data Resampling
# ============================================================
print("\n" + "=" * 60)
print("Example 5: Data Resampling with Interpolation")
print("=" * 60)

# Simulate irregularly sampled time series
np.random.seed(42)
n_samples = 20
t_irregular = np.sort(np.random.uniform(0, 10, n_samples))
values_irregular = np.sin(t_irregular) + 0.3 * np.random.randn(n_samples)

# Resample to regular time grid
t_regular = np.linspace(0, 10, 200)
interp_func = interpolate.interp1d(
    t_irregular, values_irregular, kind="cubic", fill_value="extrapolate"
)
values_regular = interp_func(t_regular)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(t_irregular, values_irregular, "ro", markersize=8, label=f"Irregular ({n_samples} pts)")
ax.plot(t_regular, values_regular, "b-", linewidth=2, label=f"Resampled ({len(t_regular)} pts)")
ax.set_title("Data Resampling: Irregular â†’ Regular Grid")
ax.set_xlabel("Time")
ax.set_ylabel("Value")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_06_resample.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_06_resample.png')}")

print(f"\nOriginal samples: {n_samples}")
print(f"Resampled points: {len(t_regular)}")

print("\n[OK] SciPy interpolation covered!")
print("   Next: 07-optimization.py for optimization algorithms.")
