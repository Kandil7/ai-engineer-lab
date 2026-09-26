"""
05 - SciPy Integration
=======================
SciPy provides powerful numerical integration tools for computing
definite integrals, solving ODEs, and more.

Topics:
- scipy.integrate.quad for single integrals
- dblquad for double integrals
- solve_ivp for initial value problems (ODEs)
- Cumulative trapezoid integration
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
from scipy import integrate

# ============================================================
# Example 1: Definite Integration with quad
# ============================================================
print("=" * 60)
print("Example 1: Definite Integration with quad()")
print("=" * 60)

# Integrate sin(x) from 0 to pi â€” exact answer is 2
result, error = integrate.quad(np.sin, 0, np.pi)
print(f"Integral from 0 to pi of sin(x) dx")
print(f"  Numerical: {result:.10f}")
print(f"  Exact:     2.0")
print(f"  Error est: {error:.2e}")

# Integrate x^2 from 0 to 1 â€” exact answer is 1/3
result2, err2 = integrate.quad(lambda x: x**2, 0, 1)
print(f"\nIntegral from 0 to 1 of x^2 dx")
print(f"  Numerical: {result2:.10f}")
print(f"  Exact:     {1 / 3:.10f}")
print(f"  Error est: {err2:.2e}")

# Gaussian integral: exp(-x^2) from -inf to inf = sqrt(pi)
result3, err3 = integrate.quad(lambda x: np.exp(-(x**2)), -np.inf, np.inf)
print(f"\nIntegral from -inf to inf of exp(-x^2) dx")
print(f"  Numerical: {result3:.10f}")
print(f"  Exact:     {np.sqrt(np.pi):.10f}")
print(f"  Error est: {err3:.2e}")


# More complex integrand
def complicated(x):
    return np.exp(-x) * np.sin(10 * x) * np.log(1 + x**2)


result4, err4 = integrate.quad(complicated, 0, 10)
print(f"\nIntegral from 0 to 10 of e^(-x)*sin(10x)*ln(1+x^2) dx")
print(f"  Result:  {result4:.10f}")
print(f"  Error:   {err4:.2e}")

# Plot the integrand
x = np.linspace(0, 10, 500)
y = complicated(x)
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, "b-", linewidth=2)
ax.fill_between(x, y, alpha=0.2)
ax.set_title(f"Integrand: e^(-x)Â·sin(10x)Â·ln(1+xÂ²), âˆ«â‰ˆ{result4:.4f}")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_05_quad.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_05_quad.png')}")

# ============================================================
# Example 2: Double Integration with dblquad
# ============================================================
print("\n" + "=" * 60)
print("Example 2: Double Integration with dblquad()")
print("=" * 60)


# Integrate f(x,y) = x^2 + y^2 over the unit square [0,1]x[0,1]
def integrand_2d(y, x):
    return x**2 + y**2


# Note: dblquad signature is dblquad(func, a, b, gfun, hfun)
# where func(y, x), a,b are x limits, gfun,hfun are y limits
result_2d, error_2d = integrate.dblquad(
    integrand_2d,
    0,
    1,  # x limits
    0,
    1,  # y limits (functions of x, here constants)
)

# Exact: âˆ«âˆ« (xÂ² + yÂ²) dx dy = 2/3
exact_2d = 2 / 3
print(f"Double integral of (x^2 + y^2) dx dy over [0,1]x[0,1]")
print(f"  Numerical: {result_2d:.10f}")
print(f"  Exact:     {exact_2d:.10f}")
print(f"  Error est: {error_2d:.2e}")


# Circular region: xÂ² + yÂ² <= 1
def circular_integrand(y, x):
    return np.sqrt(x**2 + y**2)


def y_lower(x):
    return -np.sqrt(max(0, 1 - x**2))


def y_upper(x):
    return np.sqrt(max(0, 1 - x**2))


result_circ, err_circ = integrate.dblquad(circular_integrand, -1, 1, y_lower, y_upper)
print(f"\nDouble integral of sqrt(x^2+y^2) dx dy over unit disk")
print(f"  Result: {result_circ:.6f}")
print(f"  (Volume under cone over unit circle)")

# ============================================================
# Example 3: Solving ODEs with solve_ivp
# ============================================================
print("\n" + "=" * 60)
print("Example 3: Solving Ordinary Differential Equations")
print("=" * 60)


# --- Example 3a: Simple exponential decay ---
# dy/dt = -k*y, y(0) = y0  =>  y(t) = y0 * exp(-k*t)
def decay(t, y, k=0.5):
    return -k * y[0]


sol = integrate.solve_ivp(
    decay, [0, 10], [1.0], args=(0.5,), t_eval=np.linspace(0, 10, 200), dense_output=True
)

print("Exponential decay: dy/dt = -0.5y, y(0) = 1")
print(f"  t=0:  numerical={sol.y[0][0]:.4f}, analytical={np.exp(0):.4f}")
idx_5 = np.argmin(np.abs(sol.t - 5))
print(f"  t=5:  numerical={sol.y[0][idx_5]:.4f}, analytical={np.exp(-2.5):.4f}")
print(f"  t=10: numerical={sol.y[0][-1]:.4f}, analytical={np.exp(-5):.4f}")


# --- Example 3b: Lotka-Volterra (predator-prey) ---
def lotka_volterra(t, z, a=1.5, b=1.0, c=3.0, d=1.0):
    x, y = z  # x=prey, y=predator
    dxdt = a * x - b * x * y
    dydt = -c * y + d * x * y
    return [dxdt, dydt]


sol_lv = integrate.solve_ivp(
    lotka_volterra,
    [0, 20],
    [1.0, 0.5],
    args=(1.5, 1.0, 3.0, 1.0),
    t_eval=np.linspace(0, 20, 1000),
    dense_output=True,
)

print(f"\nLotka-Volterra predator-prey model:")
print(f"  Prey  range: [{sol_lv.y[0].min():.2f}, {sol_lv.y[0].max():.2f}]")
print(f"  Predator range: [{sol_lv.y[1].min():.2f}, {sol_lv.y[1].max():.2f}]")

# Plot ODE solutions
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].plot(sol.t, sol.y[0], "b-", linewidth=2, label="Numerical")
t_fine = np.linspace(0, 10, 200)
axes[0].plot(t_fine, np.exp(-0.5 * t_fine), "r--", linewidth=1, label="Analytical")
axes[0].set_title("Exponential Decay: dy/dt = -0.5y")
axes[0].set_xlabel("t")
axes[0].set_ylabel("y(t)")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(sol_lv.y[0], sol_lv.y[1], "b-", linewidth=2)
axes[1].plot(sol_lv.y[0][0], sol_lv.y[1][0], "ro", markersize=10, label="Start")
axes[1].set_title("Lotka-Volterra Phase Plot")
axes[1].set_xlabel("Prey population")
axes[1].set_ylabel("Predator population")
axes[1].legend()
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_05_ode.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_05_ode.png')}")

# ============================================================
# Example 4: Spring-Mass-Damper System
# ============================================================
print("\n" + "=" * 60)
print("Example 4: Spring-Mass-Damper ODE System")
print("=" * 60)


# m*x'' + c*x' + k*x = 0
# Rewrite as: x' = v, v' = (-c*v - k*x) / m
def spring_mass(t, state, m=1.0, c=0.3, k=4.0):
    x, v = state
    dxdt = v
    dvdt = (-c * v - k * x) / m
    return [dxdt, dvdt]


sol_sm = integrate.solve_ivp(
    spring_mass,
    [0, 15],
    [1.0, 0.0],  # x(0)=1, v(0)=0
    t_eval=np.linspace(0, 15, 500),
    dense_output=True,
)

# Calculate energy
x = sol_sm.y[0]
v = sol_sm.y[1]
KE = 0.5 * v**2  # kinetic
PE = 0.5 * 4.0 * x**2  # potential (k=4)
TE = KE + PE

print("Spring-mass-damper: m=1, c=0.3, k=4")
print(f"  Initial energy: {TE[0]:.4f}")
print(f"  Final energy:   {TE[-1]:.4f}")
print(f"  Energy lost:    {TE[0] - TE[-1]:.4f} (damping)")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].plot(sol_sm.t, x, "b-", linewidth=2, label="Position")
axes[0].plot(sol_sm.t, v, "r--", linewidth=1.5, label="Velocity")
axes[0].set_title("Spring-Mass-Damper Response")
axes[0].set_xlabel("Time (s)")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(sol_sm.t, KE, "r-", linewidth=1.5, label="Kinetic Energy")
axes[1].plot(sol_sm.t, PE, "b-", linewidth=1.5, label="Potential Energy")
axes[1].plot(sol_sm.t, TE, "k--", linewidth=2, label="Total Energy")
axes[1].set_title("Energy Over Time")
axes[1].set_xlabel("Time (s)")
axes[1].set_ylabel("Energy")
axes[1].legend()
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_05_spring.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_05_spring.png')}")

# ============================================================
# Example 5: Cumulative Integration (Area Under Curve)
# ============================================================
print("\n" + "=" * 60)
print("Example 5: Cumulative Trapezoid Integration")
print("=" * 60)

# Integrate a discrete signal using cumulative_trapezoid
t = np.linspace(0, 2 * np.pi, 500)
signal = np.sin(t) + 0.5 * np.sin(3 * t)

cumulative = integrate.cumulative_trapezoid(signal, t, initial=0)
total_area = cumulative[-1]

print(f"Integrating sin(x) + 0.5*sin(3x) from 0 to 2*pi:")
print(f"  Total area: {total_area:.6f}")
print(f"  Expected:   0.0 (full period, symmetric)")

fig, axes = plt.subplots(2, 1, figsize=(10, 6))
axes[0].plot(t, signal, "b-", linewidth=2)
axes[0].fill_between(t, signal, alpha=0.2)
axes[0].set_title("Signal: sin(x) + 0.5Â·sin(3x)")
axes[0].set_ylabel("f(t)")
axes[0].grid(True, alpha=0.3)

axes[1].plot(t, cumulative, "r-", linewidth=2)
axes[1].axhline(y=total_area, color="k", linestyle="--", alpha=0.5)
axes[1].set_title(f"Cumulative Integral (total = {total_area:.4f})")
axes[1].set_xlabel("t")
axes[1].set_ylabel("âˆ« f(t) dt")
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_05_cumulative.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_05_cumulative.png')}")

print("\n[OK] SciPy integration module covered!")
print("   Next: 06-interpolation.py for interpolation techniques.")
