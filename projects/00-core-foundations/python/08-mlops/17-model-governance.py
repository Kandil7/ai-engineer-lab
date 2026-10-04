"""
MLOps - 17: Model Governance
============================
Topics: bias sources, group-fairness metrics, proxy detection, local reason
codes, the fairness gate.

Why this matters for AI/backend engineering:
    A model that decides about people must be measurable for fairness and
    explainable per decision, or it cannot ship in a regulated domain. This
    exercise implements the governance primitives: parity, disparate impact,
    proxy detection, reason codes, and the fairness gate.

Run:      python 17-model-governance.py
Verify:   python 17-model-governance.py --verify
Reference: https://fairmlbook.org/
"""

from __future__ import annotations

import sys


# ============================================================
# 1. Demographic Parity
# ============================================================
def demographic_parity_gap(y_pred: list[int], group: list[str]) -> float:
    """Max minus min positive-decision rate across groups."""
    rates = {}
    for y, g in zip(y_pred, group):
        rates.setdefault(g, [0, 0])
        rates[g][1] += 1
        rates[g][0] += y
    rate = {g: pos / total for g, (pos, total) in rates.items()}
    return max(rate.values()) - min(rate.values())


# ============================================================
# 2. Disparate Impact
# ============================================================
def disparate_impact(
    y_pred: list[int], group: list[str], privileged: str, unprivileged: str
) -> float:
    """Ratio of positive rates; below 0.8 signals adverse impact."""
    rp = _rate(y_pred, group, privileged)
    ru = _rate(y_pred, group, unprivileged)
    return ru / rp if rp else float("inf")


def _rate(y_pred: list[int], group: list[str], g: str) -> float:
    vals = [y for y, grp in zip(y_pred, group) if grp == g]
    return sum(vals) / len(vals) if vals else 0.0


# ============================================================
# 3. Proxy Detection (Pearson correlation, stdlib)
# ============================================================
def pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = sum((x - mx) ** 2 for x in xs) ** 0.5
    sy = sum((y - my) ** 2 for y in ys) ** 0.5
    return cov / (sx * sy) if sx and sy else 0.0


def proxy_features(
    columns: dict[str, list[float]], protected: str, candidates: list[str], threshold: float
) -> list[str]:
    """Candidate features correlated with the protected attribute above threshold."""
    flagged = []
    for name in candidates:
        if abs(pearson(columns[protected], columns[name])) >= threshold:
            flagged.append(name)
    return flagged


# ============================================================
# 4. Local Reason Codes
# ============================================================
def reason_codes(contributions: dict[str, float], top_k: int = 3) -> list[str]:
    """Human-readable 'why this decision' from signed feature contributions."""
    ranked = sorted(contributions.items(), key=lambda kv: abs(kv[1]), reverse=True)
    return [f"{name}: {'+' if w > 0 else ''}{w:.2f}" for name, w in ranked[:top_k]]


# ============================================================
# 5. The Fairness Gate
# ============================================================
def governance_gate(candidate: dict, champion: dict, max_dp_gap: float = 0.05) -> tuple[bool, str]:
    """A candidate must stay within the fairness threshold and not regress."""
    if candidate["dp_gap"] > max_dp_gap:
        return False, f"FAIL: dp_gap {candidate['dp_gap']:.3f} > {max_dp_gap}"
    if candidate["dp_gap"] > champion["dp_gap"] + 0.01:
        return False, "FAIL: fairness regressed vs champion"
    return True, "PASS: fairness within bounds"


def main() -> None:
    # A biased scorer: group B gets far fewer positive decisions.
    y_pred = [1, 1, 0, 1, 1, 0, 1, 0, 0, 0]
    group = ["A", "A", "A", "A", "A", "B", "B", "B", "B", "B"]

    print("Example 1: demographic parity")
    dp = demographic_parity_gap(y_pred, group)
    print(f"  dp_gap = {dp:.2f}")
    assert abs(dp - 0.6) < 1e-9

    print("\nExample 2: disparate impact")
    di = disparate_impact(y_pred, group, "A", "B")
    print(f"  disparate_impact = {di:.2f} (< 0.8 flags adverse impact)")
    assert di < 0.8

    print("\nExample 3: proxy detection")
    columns = {
        "protected": [0.0, 0.0, 1.0, 1.0, 0.0, 1.0],
        "zip_code": [0.1, 0.0, 0.9, 1.0, 0.2, 0.8],  # strong proxy
        "tenure": [5.0, 6.0, 5.5, 6.5, 4.5, 5.0],  # not a proxy
    }
    flagged = proxy_features(columns, "protected", ["zip_code", "tenure"], threshold=0.7)
    print(f"  flagged proxies: {flagged}")
    assert flagged == ["zip_code"]

    print("\nExample 4: local reason codes")
    codes = reason_codes({"debt_to_income": 1.2, "recent_delinquency": 0.8, "age": -0.1})
    print(f"  {codes}")
    assert codes[0].startswith("debt_to_income")

    print("\nExample 5: fairness gate")
    ok, msg = governance_gate({"dp_gap": 0.03}, {"dp_gap": 0.02})
    print(f"  {msg}")
    assert ok
    ok2, msg2 = governance_gate({"dp_gap": 0.09}, {"dp_gap": 0.02})
    print(f"  {msg2}")
    assert not ok2

    print("\n--- Summary ---")
    print("1. Measure outcomes by group, never the feature list.")
    print("2. Name the fairness metric and threshold before measuring.")
    print("3. Gate promotion on fairness, and record the choice.")


def _verify() -> None:
    y_pred = [1, 1, 0, 1, 1, 0, 1, 0, 0, 0]
    group = ["A", "A", "A", "A", "A", "B", "B", "B", "B", "B"]
    assert abs(demographic_parity_gap(y_pred, group) - 0.6) < 1e-9
    assert disparate_impact(y_pred, group, "A", "B") < 0.8
    assert disparate_impact([1, 1, 1, 1], ["A", "A", "B", "B"], "A", "B") == 1.0

    columns = {
        "protected": [0.0, 0.0, 1.0, 1.0, 0.0, 1.0],
        "zip_code": [0.1, 0.0, 0.9, 1.0, 0.2, 0.8],
        "tenure": [5.0, 6.0, 5.5, 6.5, 4.5, 5.0],
    }
    assert proxy_features(columns, "protected", ["zip_code", "tenure"], 0.7) == ["zip_code"]

    assert reason_codes({"a": 0.1, "b": -0.9, "c": 0.5})[0].startswith("b")

    assert governance_gate({"dp_gap": 0.03}, {"dp_gap": 0.02})[0]
    assert not governance_gate({"dp_gap": 0.09}, {"dp_gap": 0.02})[0]
    assert not governance_gate({"dp_gap": 0.03}, {"dp_gap": 0.01})[0]  # regressed
    print("[OK] 17-model-governance: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        main()
        _verify()
