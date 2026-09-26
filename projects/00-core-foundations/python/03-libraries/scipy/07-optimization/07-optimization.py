"""
07 - SciPy Optimization
========================
SciPy's optimize module provides algorithms for function minimization,
curve fitting, root finding, and more.

Topics:
- Function minimization (minimize, minimize_scalar)
- Curve fitting (curve_fit)
- Root finding (root, brentq)
- Linear programming (linprog)
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
from scipy import optimize

# ============================================================
# Example 1: Scalar Minimization
# ============================================================
print("=" * 60)
print("Example 1: Minimizing a Scalar Function")
print("=" * 60)


# Minimize f(x) = (x-3)^2 + 2*sin(2*pi*x)
def objective(x):
    return (x - 3) ** 2 + 2 * np.sin(2 * np.pi * x)


# Use minimize_scalar to find the minimum
result = optimize.minimize_scalar(objective, bounds=(-5, 10), method="bounded")
print(f"minimize_scalar result:")
print(f"  Minimum at x = {result.x:.6f}")
print(f"  Minimum value = {result.fun:.6f}")
print(f"  Success: {result.success}")

# Try different methods
methods = ["brent", "bounded", "golden"]
print(f"\nComparison of methods:")
for m in methods:
    if m == "bounded":
        r = optimize.minimize_scalar(objective, bounds=(-5, 10), method=m)
    else:
        r = optimize.minimize_scalar(objective, method=m)
    print(f"  {m:<10s}: x={r.x:.6f}, f(x)={r.fun:.6f}")

# Plot the function and found minimum
x_plot = np.linspace(-5, 10, 500)
y_plot = objective(x_plot)
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x_plot, y_plot, "b-", linewidth=2, label="f(x) = (x-3)Â² + 2sin(2Ï€x)")
ax.plot(
    result.x, result.fun, "r*", markersize=15, label=f"Minimum ({result.x:.2f}, {result.fun:.2f})"
)
ax.set_title("Scalar Minimization")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_07_scalar_min.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_07_scalar_min.png')}")

# ============================================================
# Example 2: Multivariate Minimization
# ============================================================
print("\n" + "=" * 60)
print("Example 2: Multivariate Function Minimization")
print("=" * 60)


# Rosenbrock function (classic test): f(x,y) = (1-x)^2 + 100*(y-x^2)^2
def rosenbrock(xy):
    x, y = xy
    return (1 - x) ** 2 + 100 * (y - x**2) ** 2


# Method comparison
starts = [np.array([-1.0, 1.0]), np.array([2.0, -1.0]), np.array([0.5, 0.5])]
methods = ["Nelder-Mead", "BFGS", "L-BFGS-B"]

print(f"Rosenbrock function minimum (true: x=1, y=1, f=0):")
print(f"{'Start':<20s} {'Method':<15s} {'x':>10s} {'y':>10s} {'f(x,y)':>12s} {'Iters':>6s}")
print("-" * 73)

results = {}
for start in starts:
    for method in methods:
        res = optimize.minimize(rosenbrock, start, method=method)
        results[(tuple(start), method)] = res
        print(
            f"  {str(list(start)):<18s} {method:<15s} {res.x[0]:10.6f} {res.x[1]:10.6f} "
            f"{res.fun:12.2e} {res.nit:6d}"
        )

# Contour plot with optimization path
fig, ax = plt.subplots(figsize=(8, 6))
x_grid = np.linspace(-1.5, 2.5, 200)
y_grid = np.linspace(-1, 3, 200)
X, Y = np.meshgrid(x_grid, y_grid)
Z = (1 - X) ** 2 + 100 * (Y - X**2) ** 2
ax.contour(X, Y, Z, levels=np.logspace(-1, 3, 20), cmap="viridis")
ax.plot(1, 1, "r*", markersize=20, label="True minimum")

colors = ["red", "blue", "green"]
for i, start in enumerate(starts):
    res = results[(tuple(start), "L-BFGS-B")]
    ax.plot(start[0], start[1], "o", color=colors[i], markersize=8)
ax.set_title("Rosenbrock Function Contours")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_07_rosenbrock.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_07_rosenbrock.png')}")

# ============================================================
# Example 3: Curve Fitting with curve_fit
# ============================================================
print("\n" + "=" * 60)
print("Example 3: Curve Fitting with curve_fit")
print("=" * 60)

# Generate data from a model: y = A * exp(-B * x) + C
np.random.seed(42)
x_data = np.linspace(0, 5, 50)
A_true, B_true, C_true = 2.5, 0.8, 0.5
y_true = A_true * np.exp(-B_true * x_data) + C_true
y_noisy = y_true + np.random.normal(0, 0.15, len(x_data))


# Define the model function
def exp_decay(x, A, B, C):
    return A * np.exp(-B * x) + C


# Fit the curve
popt, pcov = optimize.curve_fit(exp_decay, x_data, y_noisy, p0=[2, 1, 0])
perr = np.sqrt(np.diag(pcov))  # Standard errors

print(f"Curve fitting: y = AÂ·exp(-BÂ·x) + C")
print(f"  Fitted parameters:")
print(f"    A = {popt[0]:.4f} Â± {perr[0]:.4f} (true: {A_true})")
print(f"    B = {popt[1]:.4f} Â± {perr[1]:.4f} (true: {B_true})")
print(f"    C = {popt[2]:.4f} Â± {perr[2]:.4f} (true: {C_true})")

# Goodness of fit
y_fit = exp_decay(x_data, *popt)
ss_res = np.sum((y_noisy - y_fit) ** 2)
ss_tot = np.sum((y_noisy - np.mean(y_noisy)) ** 2)
r_squared = 1 - ss_res / ss_tot
print(f"  R-squared = {r_squared:.6f}")
print(f"  RMSE = {np.sqrt(np.mean((y_noisy - y_fit) ** 2)):.6f}")

# Plot
x_plot = np.linspace(0, 5, 300)
fig, ax = plt.subplots(figsize=(10, 5))
ax.errorbar(x_data, y_noisy, yerr=0.15, fmt="o", markersize=4, alpha=0.5, label="Data")
ax.plot(x_plot, exp_decay(x_plot, *popt), "r-", linewidth=2, label="Fitted curve")
ax.plot(x_plot, exp_decay(x_plot, A_true, B_true, C_true), "b--", linewidth=1.5, label="True curve")
ax.set_title(f"Exponential Decay Curve Fit (R2 = {r_squared:.4f})")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_07_curve_fit.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_07_curve_fit.png')}")

# ============================================================
# Example 4: Root Finding
# ============================================================
print("\n" + "=" * 60)
print("Example 4: Root Finding")
print("=" * 60)

from scipy.optimize import brentq, fsolve


# Find root of f(x) = x^3 - 2x + 1
def cubic(x):
    return x**3 - 2 * x + 1


# Plot to identify intervals
x_plot = np.linspace(-2, 2, 500)
y_plot = cubic(x_plot)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x_plot, y_plot, "b-", linewidth=2)
ax.axhline(y=0, color="k", linewidth=0.5)

# Find all roots
roots_found = []
intervals = [(-2, -1), (-0.5, 0.5), (0.5, 1.5)]
for a, b in intervals:
    try:
        root = brentq(cubic, a, b)
        roots_found.append(root)
        ax.plot(root, 0, "ro", markersize=10)
        print(f"  Root in [{a}, {b}]: x = {root:.6f}")
    except ValueError:
        pass

ax.set_title("Root Finding: x^3 - 2x + 1 = 0")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_07_roots.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_07_roots.png')}")

# Verify roots
print(f"\nVerification:")
for i, r in enumerate(roots_found):
    print(f"  f({r:.6f}) = {cubic(r):.2e}")

# System of nonlinear equations
print(f"\nNonlinear system: x^2 + y^2 = 4, x*y = 1")


def system_eqs(vars):
    x, y = vars
    return [x**2 + y**2 - 4, x * y - 1]


sol = fsolve(system_eqs, [1, 1])
print(f"  Solution: x={sol[0]:.6f}, y={sol[1]:.6f}")
print(f"  Verify: x^2+y^2={sol[0] ** 2 + sol[1] ** 2:.4f}, xy={sol[0] * sol[1]:.4f}")

# ============================================================
# Example 5: Linear Programming
# ============================================================
print("\n" + "=" * 60)
print("Example 5: Linear Programming with linprog")
print("=" * 60)

# Maximize: z = 3x + 5y
# Subject to:
#   x + y <= 4      (resource 1)
#   2x + y <= 6     (resource 2)
#   x, y >= 0

# linprog minimizes, so negate the objective for maximization
c = [-3, -5]  # Negate for maximization

# Inequality constraints: Ax <= b
A_ub = [
    [1, 1],  # x + y <= 4
    [2, 1],  # 2x + y <= 6
]
b_ub = [4, 6]

# Variable bounds
x_bounds = (0, None)
y_bounds = (0, None)

result_lp = optimize.linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[x_bounds, y_bounds])
print(f"Linear Programming result:")
print(f"  Status: {'Optimal' if result_lp.success else 'Failed'}")
print(f"  x = {result_lp.x[0]:.2f}")
print(f"  y = {result_lp.x[1]:.2f}")
print(f"  Maximum z = {-result_lp.fun:.2f}")  # Negate back

# Plot feasible region
fig, ax = plt.subplots(figsize=(8, 6))
x_range = np.linspace(0, 4, 300)
y1 = 4 - x_range  # x + y <= 4
y2 = 6 - 2 * x_range  # 2x + y <= 6
ax.fill_between(x_range, 0, np.minimum(y1, y2), alpha=0.3, color="green", label="Feasible region")
ax.plot(x_range, y1, "b-", linewidth=2, label="x + y = 4")
ax.plot(x_range, y2, "r-", linewidth=2, label="2x + y = 6")
ax.plot(
    result_lp.x[0],
    result_lp.x[1],
    "k*",
    markersize=15,
    label=f"Optimal ({result_lp.x[0]:.0f}, {result_lp.x[1]:.0f})",
)
ax.set_xlim(-0.5, 4)
ax.set_ylim(-0.5, 7)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Linear Programming: Max 3x + 5y")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_07_linprog.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_07_linprog.png')}")

print("\n[OK] SciPy optimization covered!")
print("   Next: 08-linear-algebra.py for matrix operations.")
