"""
04 - SciPy Statistics
======================
SciPy's stats module provides a comprehensive set of probability
distributions and statistical tests.

Topics:
- Probability distributions (continuous and discrete)
- Descriptive statistics
- Hypothesis testing (t-test, chi-square, ANOVA)
- Probability density/mass functions
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
from scipy import stats

# ============================================================
# Example 1: Probability Distributions
# ============================================================
print("=" * 60)
print("Example 1: Working with Probability Distributions")
print("=" * 60)

# Normal distribution
np.random.seed(42)
normal_dist = stats.norm(loc=100, scale=15)  # mean=100, std=15

print("Normal Distribution (mu=100, sigma=15):")
print(f"  PDF at x=100:     {normal_dist.pdf(100):.6f}")
print(f"  PDF at x=115:     {normal_dist.pdf(115):.6f}")
print(f"  CDF at x=100:     {normal_dist.cdf(100):.4f} (50th percentile)")
print(f"  CDF at x=115:     {normal_dist.cdf(115):.4f} (84th percentile)")
print(f"  Mean:             {normal_dist.mean():.1f}")
print(f"  Variance:         {normal_dist.var():.1f}")
print(f"  Std deviation:    {normal_dist.std():.1f}")

# Generate random samples
samples = normal_dist.rvs(size=10000)
print(f"\n  Generated {len(samples)} samples:")
print(f"  Sample mean:      {samples.mean():.2f}")
print(f"  Sample std:       {samples.std():.2f}")

# Plot PDF and histogram
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
x = np.linspace(40, 160, 300)
axes[0].plot(x, normal_dist.pdf(x), "b-", linewidth=2, label="PDF")
axes[0].fill_between(x, normal_dist.pdf(x), alpha=0.2)
axes[0].set_title("Normal Distribution PDF")
axes[0].set_xlabel("Value")
axes[0].set_ylabel("Density")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].hist(samples, bins=50, density=True, alpha=0.7, color="steelblue", edgecolor="white")
axes[1].plot(x, normal_dist.pdf(x), "r-", linewidth=2, label="Theoretical PDF")
axes[1].set_title("Sample Histogram vs PDF")
axes[1].legend()
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_04_distributions.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_04_distributions.png')}")

# ============================================================
# Example 2: Comparing Multiple Distributions
# ============================================================
print("\n" + "=" * 60)
print("Example 2: Comparing Multiple Distributions")
print("=" * 60)

distributions = {
    "Normal(0,1)": stats.norm(0, 1),
    "Uniform(0,1)": stats.uniform(0, 1),
    "Exponential(1)": stats.expon(0, 1),
    "Beta(2,5)": stats.beta(2, 5),
    "Gamma(2,1)": stats.gamma(2, 0, 1),
}

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
x = np.linspace(-3, 8, 500)

for name, dist in distributions.items():
    axes[0].plot(x, dist.pdf(x), label=name, linewidth=2)
    axes[1].plot(x, dist.cdf(x), label=name, linewidth=2)

axes[0].set_title("Probability Density Functions")
axes[0].set_xlabel("x")
axes[0].set_ylabel("f(x)")
axes[0].legend()
axes[0].grid(True, alpha=0.3)
axes[0].set_ylim(0, 2.5)

axes[1].set_title("Cumulative Distribution Functions")
axes[1].set_xlabel("x")
axes[1].set_ylabel("F(x)")
axes[1].legend()
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_04_multi_dist.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_04_multi_dist.png')}")

# Quick stats summary for each
print(f"\n{'Distribution':<20s} {'Mean':>8s} {'Std':>8s} {'Skew':>8s} {'Kurt':>8s}")
print("-" * 52)
for name, dist in distributions.items():
    rvs = dist.rvs(size=10000, random_state=42)
    print(
        f"{name:<20s} {rvs.mean():8.4f} {rvs.std():8.4f} "
        f"{stats.skew(rvs):8.4f} {stats.kurtosis(rvs):8.4f}"
    )

# ============================================================
# Example 3: Descriptive Statistics
# ============================================================
print("\n" + "=" * 60)
print("Example 3: Descriptive Statistics with scipy.stats")
print("=" * 60)

# Generate sample data (exam scores)
np.random.seed(42)
exam_scores = np.concatenate(
    [
        np.random.normal(72, 12, 80),  # Main group
        np.random.normal(90, 5, 20),  # High performers
    ]
)
exam_scores = np.clip(exam_scores, 0, 100)

# Full descriptive statistics
desc = stats.describe(exam_scores)
print(f"Exam Scores Analysis (n={desc.nobs}):")
print(f"  Mean:            {desc.mean:.2f}")
print(f"  Std deviation:   {np.sqrt(desc.variance):.2f}")
print(f"  Min:             {desc.minmax[0]:.2f}")
print(f"  Max:             {desc.minmax[1]:.2f}")
print(f"  Skewness:        {desc.skewness:.4f}")
print(f"  Excess kurtosis: {desc.kurtosis:.4f}")

# Percentiles
percentiles = [25, 50, 75, 90, 95, 99]
print(f"\nPercentiles:")
for p in percentiles:
    val = np.percentile(exam_scores, p)
    print(f"  {p}th: {val:.2f}")

# Moment statistics
m = stats.moment(exam_scores, order=3)
print(f"\nThird central moment: {m:.2f}")
print(f"Fourth central moment: {stats.moment(exam_scores, order=4):.2f}")

# ============================================================
# Example 4: Hypothesis Testing
# ============================================================
print("\n" + "=" * 60)
print("Example 4: Hypothesis Testing")
print("=" * 60)

# --- One-sample t-test ---
# Test if mean of data equals a specific value
np.random.seed(42)
data = np.random.normal(loc=52, scale=10, size=50)
t_stat, p_value = stats.ttest_1samp(data, popmean=50)
print("One-sample t-test (H0: mu = 50):")
print(f"  Sample mean: {data.mean():.4f}")
print(f"  t-statistic: {t_stat:.4f}")
print(f"  p-value:     {p_value:.4f}")
print(f"  Significant at alpha=0.05? {'Yes' if p_value < 0.05 else 'No'}")

# --- Two-sample t-test ---
group_a = np.random.normal(loc=75, scale=10, size=40)
group_b = np.random.normal(loc=80, scale=12, size=40)
t_stat2, p_val2 = stats.ttest_ind(group_a, group_b)
print(f"\nIndependent two-sample t-test (A vs B):")
print(f"  Group A mean: {group_a.mean():.4f}")
print(f"  Group B mean: {group_b.mean():.4f}")
print(f"  t-statistic:  {t_stat2:.4f}")
print(f"  p-value:      {p_val2:.4f}")
print(f"  Significant?  {'Yes' if p_val2 < 0.05 else 'No'}")

# --- Paired t-test ---
before = np.random.normal(100, 15, 30)
after = before + np.random.normal(5, 8, 30)  # Treatment effect
t_stat3, p_val3 = stats.ttest_rel(before, after)
print(f"\nPaired t-test (before vs after treatment):")
print(f"  Before mean: {before.mean():.4f}")
print(f"  After mean:  {after.mean():.4f}")
print(f"  Mean diff:   {(after - before).mean():.4f}")
print(f"  p-value:     {p_val3:.4f}")

# --- Chi-square test ---
observed = np.array([50, 30, 20])
expected = np.array([1 / 3, 1 / 3, 1 / 3]) * observed.sum()
chi2_result = stats.chisquare(observed, f_exp=expected)
chi2, p_chi2 = chi2_result
dof = len(observed) - 1
print(f"\nChi-square goodness-of-fit test:")
print(f"  Observed: {observed}")
print(f"  Expected: {expected.astype(int)}")
print(f"  Chi2={chi2:.4f}, p={p_chi2:.4f}, df={dof}")

# ============================================================
# Example 5: Correlation and Regression
# ============================================================
print("\n" + "=" * 60)
print("Example 5: Correlation and Linear Regression")
print("=" * 60)

np.random.seed(42)
x = np.linspace(0, 10, 100)
y = 2.5 * x + 3.0 + np.random.normal(0, 2, 100)

# Pearson correlation
r_pearson, p_pearson = stats.pearsonr(x, y)
print(f"Pearson correlation:  r={r_pearson:.4f}, p={p_pearson:.2e}")

# Spearman rank correlation
r_spearman, p_spearman = stats.spearmanr(x, y)
print(f"Spearman correlation: rho={r_spearman:.4f}, p={p_spearman:.2e}")

# Linear regression
slope, intercept, r_val, p_val, std_err = stats.linregress(x, y)
print(f"\nLinear regression (y = mx + b):")
print(f"  Slope (m):     {slope:.4f} (true: 2.5)")
print(f"  Intercept (b): {intercept:.4f} (true: 3.0)")
print(f"  RÂ²:            {r_val**2:.4f}")
print(f"  Std error:     {std_err:.4f}")

# Plot regression
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(x, y, alpha=0.5, s=20, label="Data points")
ax.plot(x, slope * x + intercept, "r-", linewidth=2, label=f"Fit: y={slope:.2f}x + {intercept:.2f}")
ax.set_title("Linear Regression with scipy.stats.linregress")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_04_regression.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_04_regression.png')}")

print("\n[OK] SciPy statistics module covered!")
print("   Next: 05-integration.py for numerical integration.")
