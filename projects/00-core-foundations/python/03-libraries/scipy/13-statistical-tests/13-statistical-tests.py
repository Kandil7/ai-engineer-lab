"""SciPy 13: Statistical Tests — hypothesis testing beyond the t-test.

Why this matters for AI/backend engineering:
Every A/B test, every model-evaluation claim ("new model is
better"), and every feature-selection decision is a hypothesis
test. This module covers the scipy.stats surface you need to make
those claims honestly: choosing parametric vs non-parametric
tests, checking assumptions (normality), correcting for multiple
comparisons, and reporting effect size and power instead of just
p-values.

Docs: https://docs.scipy.org/doc/scipy/reference/stats.html
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np
from scipy import stats  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "outputs", "scipy")
os.makedirs(OUT, exist_ok=True)

rng = np.random.default_rng(42)


# ---------------------------------------------------------------------------
# Example 1: the workflow — hypothesis, test, p-value, decision
# ---------------------------------------------------------------------------
# H0: "no effect" (means equal). The p-value is P(data | H0): the chance
# of observing a difference this extreme if there is truly no effect.
# p < alpha (0.05) -> reject H0 -> evidence of an effect.

a = rng.normal(loc=0.0, scale=1.0, size=60)
b = rng.normal(loc=0.5, scale=1.0, size=60)
t, p = stats.ttest_ind(a, b)  # Welch's t-test (equal_var=False default)
print(f"Example 1: t={t:.3f}  p={p:.4f}  significant={p < 0.05}")

# Identical samples -> zero evidence for an effect:
t0, p0 = stats.ttest_ind(a, a)
print(f"Example 1: identical samples -> t={t0:.2f}  p={p0:.2f}")

# ---------------------------------------------------------------------------
# Example 2: paired tests — same units measured twice
# ---------------------------------------------------------------------------
# Paired designs remove between-subject variance; ttest_rel is the
# parametric version, wilcoxon the non-parametric (rank-based) one.

before = rng.normal(loc=100.0, scale=10.0, size=40)
after = before + rng.normal(loc=4.0, scale=5.0, size=40)
t_rel, p_rel = stats.ttest_rel(before, after)
w_stat, p_w = stats.wilcoxon(before, after, method="approx")
print(f"Example 2: paired t: p={p_rel:.4f} | wilcoxon: p={p_w:.4f}")

# ---------------------------------------------------------------------------
# Example 3: ANOVA — three or more groups at once
# ---------------------------------------------------------------------------
# f_oneway tests whether k group means differ. Pairwise t-tests instead
# would inflate the error rate (see Example 8).

g1 = rng.normal(loc=0.0, scale=1.0, size=50)
g2 = rng.normal(loc=0.0, scale=1.0, size=50)
g3 = rng.normal(loc=0.0, scale=1.0, size=50)
g4 = rng.normal(loc=1.5, scale=1.0, size=50)
F_same, p_same = stats.f_oneway(g1, g2, g3)
F_diff, p_diff = stats.f_oneway(g1, g2, g3, g4)
print(f"Example 3: same means: F={F_same:.3f} p={p_same:.4f}")
print(f"Example 3: one shifted: F={F_diff:.3f} p={p_diff:.2e}")

# Non-parametric alternative for 3+ groups:
H, p_kruskal = stats.kruskal(g1, g2, g3, g4)
print(f"Example 3: kruskal: H={H:.3f} p={p_kruskal:.2e}")

# ---------------------------------------------------------------------------
# Example 4: non-parametric two-sample — Mann-Whitney U
# ---------------------------------------------------------------------------
# t-test assumes normality; Mann-Whitney only assumes ordinal values.
# Use it on skewed, heavy-tailed, or bounded data (revenue, latency).

u1 = rng.exponential(scale=1.0, size=80)  # skewed!
u2 = rng.exponential(scale=1.0, size=80)  # same distribution
u3 = rng.exponential(scale=1.3, size=80)  # shifted scale
U_same, p_us = stats.mannwhitneyu(u1, u2, alternative="two-sided")
U_diff, p_ud = stats.mannwhitneyu(u1, u3, alternative="two-sided")
print(f"Example 4: same dist: U={U_same:.0f} p={p_us:.4f}")
print(f"Example 4: shifted:   U={U_diff:.0f} p={p_ud:.2e}")

# ---------------------------------------------------------------------------
# Example 5: chi-square — counts, not means
# ---------------------------------------------------------------------------
# chisquare = goodness of fit (observed vs expected); chi2_contingency
# = independence of two categorical variables.

fair = rng.integers(1, 7, size=600)  # fair die
_, obs = np.unique(fair, return_counts=True)  # np.unique -> (values, counts)
chi2, p_gof = stats.chisquare(obs)
print(f"Example 5: fair die chi2={chi2:.3f} p={p_gof:.4f}")

loaded = rng.choice(np.arange(1, 7), size=600, p=[0.05, 0.1, 0.1, 0.1, 0.1, 0.55])
_, obs2 = np.unique(loaded, return_counts=True)
chi2b, p_gofb = stats.chisquare(obs2)
print(f"Example 5: loaded die chi2={chi2b:.3f} p={p_gofb:.2e}")

table = np.array([[120, 80], [70, 130]])  # rows: variant, cols: outcome
chi2c, p_c, dof_c, expected = stats.chi2_contingency(table)
print(f"Example 5: contingency chi2={chi2c:.3f} p={p_c:.2e} df={dof_c}")

# ---------------------------------------------------------------------------
# Example 6: normality tests — checking the t-test assumption
# ---------------------------------------------------------------------------
# shapiro is the strongest small-sample test (n < 5000); normaltest
# (D'Agostino) combines skew and kurtosis. Failing normality pushes
# you to the non-parametric column of the test menu.

normal = rng.normal(size=300)
uniform = rng.uniform(size=300)
w_n, p_n = stats.shapiro(normal)
w_u, p_u = stats.shapiro(uniform)
print(f"Example 6: normal data  shapiro p={p_n:.3f}")
print(f"Example 6: uniform data shapiro p={p_u:.2e}")

# ---------------------------------------------------------------------------
# Example 7: correlation significance — r is meaningless without p
# ---------------------------------------------------------------------------
# pearsonr: linear association; spearmanr: monotonic (rank) association.

x = rng.normal(size=200)
y = 3.0 * x + rng.normal(scale=0.5, size=200)
r_pear, p_pear = stats.pearsonr(x, y)
r_spear, p_spear = stats.spearmanr(x, y)
print(f"Example 7: pearson r={r_pear:.3f} p={p_pear:.2e}")
print(f"Example 7: spearman rho={r_spear:.3f} p={p_spear:.2e}")

# ---------------------------------------------------------------------------
# Example 8: multiple comparisons — why 20 tests at alpha=0.05 fail
# ---------------------------------------------------------------------------
# 20 independent tests at alpha=0.05: ~1 false positive expected by chance.
# scipy.stats no longer ships multipletests (statsmodels does), but both
# corrections are a few lines — implementing them shows what they do:
#   Bonferroni: multiply every p-value by the number of tests (conservative).
#   Benjamini-Hochberg (FDR): sort, scale by rank, enforce monotonicity.


def bonferroni(pvals: np.ndarray) -> np.ndarray:
    """p-values corrected by the Bonferroni method (cap at 1)."""
    return np.minimum(1.0, np.asarray(pvals, dtype=float) * pvals.size)


def benjamini_hochberg(pvals: np.ndarray) -> np.ndarray:
    """p-values corrected by the Benjamini-Hochberg (FDR) method."""
    p = np.asarray(pvals, dtype=float)
    n = p.size
    order = np.argsort(p)
    adjusted = p[order] * n / np.arange(1, n + 1)
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]  # monotone
    corrected = np.empty_like(adjusted)
    corrected[order] = np.minimum(adjusted, 1.0)
    return corrected


pvals = np.array([0.001, 0.009, 0.02, 0.03, 0.05, 0.07, 0.5, 0.6, 0.8, 0.9])
p_bonf = bonferroni(pvals)
p_bh = benjamini_hochberg(pvals)
print(f"Example 8: raw p<0.05 count: {(pvals < 0.05).sum()}")
print(f"Example 8: bonferroni rejects: {(p_bonf < 0.05).sum()} | BH rejects: {(p_bh < 0.05).sum()}")

# ---------------------------------------------------------------------------
# Example 9: effect size and power — beyond "is it significant?"
# ---------------------------------------------------------------------------
# p answers "is there an effect?"; Cohen's d answers "how big?"; power
# answers "could this study have detected it?".


def cohen_d(group1, group2):
    """Standardized mean difference: (m1 - m2) / pooled std."""
    n1, n2 = group1.size, group2.size
    var_pooled = ((n1 - 1) * group1.var(ddof=1) + (n2 - 1) * group2.var(ddof=1)) / (n1 + n2 - 2)
    return (group1.mean() - group2.mean()) / np.sqrt(var_pooled)


def sample_size_t2(effect_size, alpha=0.05, power=0.8):
    """Per-group n for a two-sample t-test (normal approximation).

    n ~= 2 * (z_{1-alpha/2} + z_power)^2 / d^2
    (scipy.stats no longer ships tt_ind_solve_power; statsmodels does.)
    """
    z_alpha2 = stats.norm.ppf(1.0 - alpha / 2)
    z_power = stats.norm.ppf(power)
    return 2.0 * (z_alpha2 + z_power) ** 2 / effect_size**2


d_effect = cohen_d(rng.normal(0.0, 1.0, 100), rng.normal(0.5, 1.0, 100))
print(f"Example 9: cohen d (0.5 shift) ~ {d_effect:.3f}")

# Required sample size for a two-sample t-test: effect 0.5, alpha 0.05, power 0.8
n_needed = sample_size_t2(effect_size=0.5)
print(f"Example 9: n per group for d=0.5, power=0.8: {n_needed:.1f}")


# ---------------------------------------------------------------------------
# Example 10: a power curve (plot)
# ---------------------------------------------------------------------------
def power_t2(n, effect_size, alpha=0.05):
    """Achieved power of a two-sample t-test at per-group size n.

    power = Phi(sqrt(n * d^2 / 2) - z_{1-alpha/2})
    """
    z_alpha2 = stats.norm.ppf(1.0 - alpha / 2)
    return stats.norm.cdf(np.sqrt(n * effect_size**2 / 2.0) - z_alpha2)


ns = np.arange(10, 201, 5)
powers = [power_t2(n=n, effect_size=0.3) for n in ns]
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(ns, powers, "-", label="effect size d=0.3")
ax.axhline(0.8, color="r", linestyle="--", label="power = 0.8")
ax.set_title("Two-sample t-test: power vs sample size")
ax.set_xlabel("n per group")
ax.set_ylabel("power")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig(os.path.join(OUT, "scipy_13_power.png"), dpi=100)
print("Plot saved: outputs/scipy/scipy_13_power.png")


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
def _verify() -> None:
    # 1. identical samples -> p == 1.0 exactly
    x1 = rng.normal(size=50)
    _, p1 = stats.ttest_ind(x1, x1)
    assert p1 == 1.0

    # 2. a real shift is detected
    x2 = rng.normal(loc=0.0, size=60)
    x3 = rng.normal(loc=2.0, size=60)
    _, p2 = stats.ttest_ind(x2, x3)
    assert p2 < 1e-5

    # 3. ANOVA separates mixed groups
    _, p3 = stats.f_oneway(rng.normal(size=40), rng.normal(size=40), rng.normal(loc=1.5, size=40))
    assert p3 < 1e-3

    # 4. Mann-Whitney detects a scale shift in skewed data
    _, p4 = stats.mannwhitneyu(rng.exponential(size=100), rng.exponential(scale=1.8, size=100))
    assert p4 < 0.01

    # 5. chi-square GOF: fair die passes, loaded die fails
    fair = rng.integers(1, 7, size=600)
    _, obs_f = np.unique(fair, return_counts=True)
    _, p5 = stats.chisquare(obs_f)
    assert p5 > 0.05
    loaded = rng.choice(np.arange(1, 7), size=600, p=[0.05, 0.1, 0.1, 0.1, 0.1, 0.55])
    _, obs_l = np.unique(loaded, return_counts=True)
    _, p6 = stats.chisquare(obs_l)
    assert p6 < 1e-6

    # 6. normality: normal passes, uniform fails
    _, p7 = stats.shapiro(rng.normal(size=300))
    assert p7 > 0.05
    _, p8 = stats.shapiro(rng.uniform(size=300))
    assert p8 < 1e-4

    # 7. correlation: r and p agree with the linear construction
    xx = rng.normal(size=300)
    yy = 2.0 * xx + rng.normal(scale=0.4, size=300)
    r9, p9 = stats.pearsonr(xx, yy)
    assert r9 > 0.95 and p9 < 1e-20

    # 8. Bonferroni multiplies p-values (capped at 1); BH is monotone
    pvals8 = np.array([0.01, 0.5, 0.001])
    assert np.allclose(bonferroni(pvals8), np.minimum(1.0, pvals8 * 3))
    bh8 = benjamini_hochberg(np.array([0.01, 0.04, 0.05]))
    assert np.allclose(bh8, [0.03, 0.05, 0.05])

    # 9. power: n needed for d=0.5, power=0.8 is ~63 per group
    n9 = sample_size_t2(effect_size=0.5, alpha=0.05, power=0.8)
    assert 55 < n9 < 75
    # ... and the power formula inverts it: power(n_needed) ~ 0.8
    assert abs(power_t2(n=n9, effect_size=0.5) - 0.8) < 1e-3

    # 10. Cohen's d of two identical distributions is ~0
    d10 = cohen_d(rng.normal(0.0, 1.0, 100), rng.normal(0.0, 1.0, 100))
    assert abs(d10) < 0.4

    print("[OK] SciPy 13: Statistical Tests")


if __name__ == "__main__":
    _verify()
