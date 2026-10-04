"""
MLOps - 21: Deployment Strategies
=================================
Topics: shadow, canary, blue-green, A/B, rollback, and the decision
framework that chooses among them.

Why this matters for AI/backend engineering:
    A validated model still has to reach users safely. The deployment
    strategy bounds the blast radius of a bad release, and rollback is the
    property you live with at 2 a.m. when the metrics turn red.

Run:      python 21-deployment-strategies.py
Verify:   python 21-deployment-strategies.py --verify
Reference: https://martinfowler.com/bliki/CanaryRelease.html
"""

from __future__ import annotations

import sys


# ============================================================
# 1. Shadow: score without serving
# ============================================================
def shadow_compare(candidate_scores: list, champion_scores: list, tolerance: float) -> tuple:
    diffs = [abs(c - h) for c, h in zip(candidate_scores, champion_scores, strict=False)]
    mean_diff = sum(diffs) / len(diffs)
    return mean_diff <= tolerance, mean_diff


# ============================================================
# 2. Canary: a gated live slice
# ============================================================
def canary_decision(
    candidate_metric: float, champion_metric: float, threshold: float, higher_better: bool = True
) -> tuple:
    if higher_better:
        passed = candidate_metric >= champion_metric - threshold
    else:
        passed = candidate_metric <= champion_metric + threshold
    return ("expand" if passed else "rollback"), passed


# ============================================================
# 3. Blue-green: one switch, instant rollback
# ============================================================
def blue_green_switch(current: str, candidate: str, health_ok: bool) -> tuple:
    if health_ok:
        return candidate, f"switched {current} -> {candidate}"
    return current, f"holding on {current}: candidate unhealthy"


# ============================================================
# 4. A/B: statistics decide promotion
# ============================================================
def ab_decision(
    lift: float, p_value: float, alpha: float = 0.05, guardrails_ok: bool = True
) -> str:
    if not guardrails_ok:
        return "rollback: guardrail violated"
    if p_value < alpha and lift > 0:
        return "promote: significant positive lift"
    return "hold: no significant lift"


# ============================================================
# 5. Rollback and the decision framework
# ============================================================
def rollback(deployments: list, target_version: str) -> tuple:
    if target_version not in deployments:
        return None, f"FAIL: {target_version} unknown, cannot roll back"
    return target_version, f"rolled back to {target_version}"


def choose_strategy(
    risk: str, need_instant_rollback: bool, need_business_proof: bool, budget_for_two_envs: bool
) -> str:
    if risk == "low":
        return "direct"
    if need_business_proof:
        return "A/B"
    if need_instant_rollback and budget_for_two_envs:
        return "blue-green"
    return "shadow, then canary"


def main() -> None:
    print("Example 1: shadow on live traffic")
    ok, diff = shadow_compare([0.90, 0.80, 0.85], [0.91, 0.79, 0.86], tolerance=0.05)
    print(f"  match={ok} mean_diff={diff:.3f} (zero user impact)")
    assert ok

    print("\nExample 2: canary slice with a gate")
    action, passed = canary_decision(0.92, 0.91, threshold=0.01)
    print(f"  {action}")
    assert action == "expand"
    action2, _ = canary_decision(0.88, 0.91, threshold=0.01)
    print(f"  regressed canary -> {action2}")
    assert action2 == "rollback"
    # Lower-better (latency): 180 ms vs 190 ms is a pass.
    assert canary_decision(180, 190, 15, higher_better=False)[0] == "expand"

    print("\nExample 3: blue-green switch")
    env, msg = blue_green_switch("blue", "green", health_ok=True)
    print(f"  {msg}")
    assert env == "green"
    env2, msg2 = blue_green_switch("blue", "green", health_ok=False)
    print(f"  {msg2}")
    assert env2 == "blue"

    print("\nExample 4: A/B decides on statistics")
    print(f"  {ab_decision(0.05, 0.01)}")
    assert ab_decision(0.05, 0.01) == "promote: significant positive lift"
    assert ab_decision(0.05, 0.01, guardrails_ok=False) == "rollback: guardrail violated"

    print("\nExample 5: rollback and strategy choice")
    assert rollback(["v1", "v2"], "v1") == ("v1", "rolled back to v1")
    assert rollback(["v1"], "v9")[0] is None
    for args, want in [
        (("low", False, False, False), "direct"),
        (("high", False, True, False), "A/B"),
        (("high", True, False, True), "blue-green"),
        (("high", False, False, False), "shadow, then canary"),
    ]:
        got = choose_strategy(*args)
        print(f"  {args} -> {got}")
        assert got == want

    print("\n--- Summary ---")
    print("1. Shadow validates, canary bounds, blue-green reverts, A/B proves.")
    print("2. Choose by risk, reversibility, cost — in that order.")
    print("3. Test the rollback; record the strategy and its evidence.")


def _verify() -> None:
    ok, diff = shadow_compare([0.90, 0.80], [0.91, 0.79], 0.05)
    assert ok and diff < 0.05
    assert not shadow_compare([0.5, 0.5], [0.9, 0.9], 0.05)[0]

    assert canary_decision(0.92, 0.91, 0.01) == ("expand", True)
    assert canary_decision(0.88, 0.91, 0.01) == ("rollback", False)
    assert canary_decision(180, 190, 15, higher_better=False) == ("expand", True)

    assert blue_green_switch("blue", "green", True) == ("green", "switched blue -> green")
    assert blue_green_switch("blue", "green", False)[0] == "blue"

    assert ab_decision(0.05, 0.01) == "promote: significant positive lift"
    assert ab_decision(-0.01, 0.01) == "hold: no significant lift"
    assert ab_decision(0.05, 0.01, guardrails_ok=False) == "rollback: guardrail violated"

    assert rollback(["v1", "v2"], "v1")[0] == "v1"
    assert rollback(["v1"], "v9")[0] is None
    assert choose_strategy("low", False, False, False) == "direct"
    assert choose_strategy("high", False, True, False) == "A/B"
    assert choose_strategy("high", True, False, True) == "blue-green"
    assert choose_strategy("high", False, False, False) == "shadow, then canary"
    print("[OK] 21-deployment-strategies: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        main()
        _verify()
