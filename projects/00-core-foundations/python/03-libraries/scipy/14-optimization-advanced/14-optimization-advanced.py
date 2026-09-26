"""SciPy 14: Optimization Advanced — methods, constraints, robustness.

Why this matters for AI/backend engineering:
Hyperparameter search, calibration, portfolio-style allocation,
and loss-robust fitting all reduce to scipy.optimize problems.
This module covers the advanced surface: choosing a solver
(Nelder-Mead vs BFGS vs L-BFGS-B vs SLSQP), adding bounds and
constraints, robust least squares against outliers, curve_fit
with priors, and global optimization when the landscape is
multimodal.

Docs: https://docs.scipy.org/doc/scipy/reference/optimize.html
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy import optimize  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "outputs", "scipy")
os.makedirs(OUT, exist_ok=True)

rng = np.random.default_rng(42)


# ---------------------------------------------------------------------------
# Example 1: choosing a solver — Nelder-Mead vs BFGS on Rosenbrock
# ---------------------------------------------------------------------------
# Rosenbrock: f(x, y) = (1-x)^2 + 100*(y - x^2)^2, minimum (1, 1), f=0.
# Nelder-Mead: derivative-free simplex, robust, slow on 2+ dims.
# BFGS: uses finite-difference gradients, much faster convergence.


def rosenbrock(z):
    x, y = z
    return (1.0 - x) ** 2 + 100.0 * (y - x**2) ** 2


x0 = np.array([-1.2, 1.0])
res_nm = optimize.minimize(
    rosenbrock, x0, method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-6}
)
res_bfgs = optimize.minimize(rosenbrock, x0, method="BFGS")
print(f"Example 1: Nelder-Mead fun={res_nm.fun:.2e} nfev={res_nm.nfev}")
print(f"Example 1: BFGS         fun={res_bfgs.fun:.2e} nfev={res_bfgs.nfev}")

# ---------------------------------------------------------------------------
# Example 2: bounds — L-BFGS-B keeps the answer inside a box
# ---------------------------------------------------------------------------
# Unconstrained, (x-5)^2 has its minimum at 5. With bounds [0, 2], the
# optimum is clamped to x=2 — bounds are *hard* constraints here.

f_box = lambda x: (x[0] - 5.0) ** 2
res_box = optimize.minimize(f_box, np.array([0.0]), method="L-BFGS-B", bounds=[(0.0, 2.0)])
print(f"Example 2: bounded solution x={res_box.x[0]:.4f} fun={res_box.fun:.4f}")

# ---------------------------------------------------------------------------
# Example 3: constraints — SLSQP with an equality constraint
# ---------------------------------------------------------------------------
# Minimize sum((x_i - 1)^2) over 3 variables subject to sum(x) = 3.
# The constraint forces the solution onto the plane x1+x2+x3=3.


def f_eq(z):
    return np.sum((z - 1.0) ** 2)


cons = {"type": "eq", "fun": lambda z: np.sum(z) - 3.0}
res_slsqp = optimize.minimize(f_eq, np.zeros(3), method="SLSQP", constraints=cons)
print(f"Example 3: solution x={np.round(res_slsqp.x, 5)} sum={res_slsqp.x.sum():.6f}")

# ---------------------------------------------------------------------------
# Example 4: least_squares with robust loss — outliers shouldn't win
# ---------------------------------------------------------------------------
# Plain least squares (loss="linear") is dominated by outliers; the
# cauchy loss down-weights them aggressively. Fit y = a*x + b with 7
# extreme outliers at high x. (Cauchy is the most aggressive robust
# loss; soft_l1/huber are gentler but can stall in a bad basin here.)

x_line = np.linspace(0.0, 10.0, 25)
y_line = 2.0 * x_line + 1.0 + rng.normal(scale=0.3, size=x_line.size)
y_line[-7:] += 40.0  # extreme high-x outliers

res_lin = optimize.least_squares(
    lambda p: p[0] * x_line + p[1] - y_line, x0=[0.0, 0.0], loss="linear"
)
res_rob = optimize.least_squares(
    lambda p: p[0] * x_line + p[1] - y_line, x0=[0.0, 0.0], loss="cauchy"
)
print(f"Example 4: linear  slope={res_lin.x[0]:.3f} (truth 2.0)")
print(f"Example 4: cauchy  slope={res_rob.x[0]:.3f} (truth 2.0)")

# ---------------------------------------------------------------------------
# Example 5: curve_fit with bounds — calibrating a decay model
# ---------------------------------------------------------------------------
# y = A * exp(-B * x) + C, fit with prior bounds; the fitter stays inside
# physically meaningful regions (A, C >= 0, B in (0, 3]).

t = np.linspace(0.0, 5.0, 60)
truth = (3.0, 0.8, 0.5)  # A, B, C
y_curve = truth[0] * np.exp(-truth[1] * t) + truth[2] + rng.normal(scale=0.05, size=t.size)


def decay(x, A, B, C):
    return A * np.exp(-B * x) + C


popt, pcov = optimize.curve_fit(
    decay, t, y_curve, p0=[1.0, 1.0, 0.0], bounds=([0.0, 1e-3, 0.0], [10.0, 3.0, 2.0])
)
print(f"Example 5: fitted A,B,C = {np.round(popt, 3)} (truth {truth})")

# ---------------------------------------------------------------------------
# Example 6: global optimization — the multimodal landscape
# ---------------------------------------------------------------------------
# f(x) = x^2 + 10*sin(x) has several local minima; gradient methods
# converge to whichever basin they start in. differential_evolution
# searches the whole box and (seeded) finds the global minimum.


def multimodal(x):
    return x[0] ** 2 + 10.0 * np.sin(x[0])


res_global = optimize.differential_evolution(multimodal, bounds=[(-10.0, 10.0)], seed=42)
print(f"Example 6: global min x={res_global.x[0]:.4f} fun={res_global.fun:.4f} (true ~ -7.95)")

# ---------------------------------------------------------------------------
# Example 7: convergence diagnostics — read the result object
# ---------------------------------------------------------------------------
# success, message, nfev, nit tell you *why* the solver stopped.
# Never trust x without checking success.

print(f"Example 7: BFGS   success={res_bfgs.success} nfev={res_bfgs.nfev} msg='{res_bfgs.message}'")
print(f"Example 7: SLSQP  success={res_slsqp.success} nit={res_slsqp.nit}")
print(f"Example 7: global success={res_global.success} nfev={res_global.nfev}")

# ---------------------------------------------------------------------------
# Example 8: portfolio-style allocation with bounds + constraints (plot)
# ---------------------------------------------------------------------------
# Maximize expected return - risk over 3 assets: weights in [0, 1],
# sum(w) = 1. Equivalent to minimizing -return + risk.

mu = np.array([0.08, 0.05, 0.12])
cov = np.array([[0.04, 0.01, 0.02], [0.01, 0.02, 0.005], [0.02, 0.005, 0.09]])


def neg_sharpe(w):
    ret = mu @ w
    risk = np.sqrt(w @ cov @ w)
    return -(ret - 0.02) / risk  # excess return / risk


cons_pf = {"type": "eq", "fun": lambda w: np.sum(w) - 1.0}
res_pf = optimize.minimize(
    neg_sharpe,
    np.array([1.0 / 3] * 3),
    method="SLSQP",
    bounds=[(0.0, 1.0)] * 3,
    constraints=cons_pf,
)
w_opt = res_pf.x
print(f"Example 8: optimal weights = {np.round(w_opt, 3)} sum={w_opt.sum():.4f}")

fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.bar(["asset 1", "asset 2", "asset 3"], w_opt, color="#4C72B0")
ax.set_title("Max-Sharpe allocation (SLSQP, sum-to-1 constraint)")
ax.set_ylabel("weight")
ax.set_ylim(0, 1)
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig(os.path.join(OUT, "scipy_14_portfolio.png"), dpi=100)
print("Plot saved: outputs/scipy/scipy_14_portfolio.png")


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
def _verify() -> None:
    # 1. BFGS nails the Rosenbrock minimum
    r1 = optimize.minimize(rosenbrock, np.array([-1.2, 1.0]), method="BFGS")
    assert r1.success and r1.fun < 1e-10
    assert np.allclose(r1.x, [1.0, 1.0], atol=1e-5)

    # 2. L-BFGS-B respects hard bounds
    r2 = optimize.minimize(
        lambda x: (x[0] - 5.0) ** 2, np.array([0.0]), method="L-BFGS-B", bounds=[(0.0, 2.0)]
    )
    assert np.isclose(r2.x[0], 2.0, atol=1e-4) and r2.x[0] <= 2.0

    # 3. SLSQP satisfies the equality constraint
    r3 = optimize.minimize(f_eq, np.zeros(3), method="SLSQP", constraints=cons)
    assert r3.success
    assert abs(r3.x.sum() - 3.0) < 1e-6

    # 4. robust loss beats linear loss on outlier data
    xx = np.linspace(0.0, 10.0, 25)
    yy = 2.0 * xx + 1.0 + rng.normal(scale=0.3, size=xx.size)
    yy[-7:] += 40.0  # extreme high-x outliers
    rl = optimize.least_squares(lambda p: p[0] * xx + p[1] - yy, x0=[0.0, 0.0], loss="linear")
    rr = optimize.least_squares(lambda p: p[0] * xx + p[1] - yy, x0=[0.0, 0.0], loss="cauchy")
    assert abs(rr.x[0] - 2.0) < abs(rl.x[0] - 2.0)

    # 5. curve_fit recovers the decay parameters within bounds
    tt = np.linspace(0.0, 5.0, 60)
    yy5 = 3.0 * np.exp(-0.8 * tt) + 0.5 + rng.normal(scale=0.05, size=tt.size)
    p5, _ = optimize.curve_fit(
        decay, tt, yy5, p0=[1.0, 1.0, 0.0], bounds=([0.0, 1e-3, 0.0], [10.0, 3.0, 2.0])
    )
    assert np.allclose(p5, [3.0, 0.8, 0.5], atol=0.1)

    # 6. global optimizer escapes local minima deterministically
    r6 = optimize.differential_evolution(multimodal, bounds=[(-10.0, 10.0)], seed=42)
    assert r6.success and r6.fun < -7.9

    # 7. portfolio weights satisfy the constraints
    r7 = optimize.minimize(
        neg_sharpe,
        np.array([1.0 / 3] * 3),
        method="SLSQP",
        bounds=[(0.0, 1.0)] * 3,
        constraints=cons_pf,
    )
    assert r7.success
    assert abs(r7.x.sum() - 1.0) < 1e-6
    assert np.all(r7.x >= -1e-6) and np.all(r7.x <= 1.0 + 1e-6)

    # 8. diagnostics: Nelder-Mead burns more evaluations than BFGS here
    nm8 = optimize.minimize(
        rosenbrock,
        np.array([-1.2, 1.0]),
        method="Nelder-Mead",
        options={"xatol": 1e-6, "fatol": 1e-6},
    )
    assert nm8.success and nm8.nfev > res_bfgs.nfev

    print("[OK] SciPy 14: Optimization Advanced")


if __name__ == "__main__":
    _verify()
