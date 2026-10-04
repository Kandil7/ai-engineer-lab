"""
MLOps - 20: Continuous Training
===============================
Topics: why models degrade, retraining triggers, champion/challenger
comparison, avoiding thrash.

Why this matters for AI/backend engineering:
    Every production model has an expiration date no one tracks. Continuous
    training rebuilds on signal, promotes only winners, and records every
    reason — so the model stays good without a human remembering to rebuild it.

Run:      python 20-continuous-training.py
Verify:   python 20-continuous-training.py --verify
Reference: https://mlflow.org/docs/latest/model-registry.html
"""

from __future__ import annotations

import sys


# ============================================================
# 1. Retraining Triggers
# ============================================================
def should_retrain(metrics: dict, thresholds: dict) -> list:
    """Return the named reasons a retrain is due (empty means hold)."""
    reasons = []
    if metrics["days_since_train"] >= thresholds["max_age_days"]:
        reasons.append("stale")
    if metrics["psi"] >= thresholds["psi"]:
        reasons.append("drift")
    if metrics["accuracy"] <= thresholds["min_accuracy"]:
        reasons.append("performance")
    if metrics["new_rows"] >= thresholds["min_new_rows"]:
        reasons.append("data")
    return reasons


# ============================================================
# 2. Champion and Challenger
# ============================================================
def champion_challenger(challenger_acc: float, champion_acc: float, tol: float = 0.0) -> str:
    """A challenger must beat the champion (within tolerance) to promote."""
    if challenger_acc >= champion_acc - tol:
        return "promote: challenger wins"
    return "hold: champion retains"


# ============================================================
# 3. Thrash Guards
# ============================================================
def cooldown_ok(days_since_last_retrain: int, min_interval_days: int) -> bool:
    return days_since_last_retrain >= min_interval_days


# ============================================================
# 4. The CT Decision
# ============================================================
def ct_decision(metrics: dict, thresholds: dict, champion_acc: float, challenger_acc: float) -> str:
    reasons = should_retrain(metrics, thresholds)
    if not reasons:
        return "hold: no trigger"
    if not cooldown_ok(metrics["days_since_train"], thresholds["min_interval_days"]):
        return "hold: cooldown"
    return champion_challenger(challenger_acc, champion_acc)


def main() -> None:
    thresholds = {
        "max_age_days": 30,
        "psi": 0.25,
        "min_accuracy": 0.88,
        "min_new_rows": 10000,
        "min_interval_days": 7,
    }

    print("Example 1: triggers name their reasons")
    m1 = {"days_since_train": 45, "psi": 0.10, "accuracy": 0.90, "new_rows": 2000}
    print(f"  {should_retrain(m1, thresholds)}")
    assert should_retrain(m1, thresholds) == ["stale"]

    m2 = {"days_since_train": 5, "psi": 0.31, "accuracy": 0.90, "new_rows": 12000}
    print(f"  {should_retrain(m2, thresholds)}")
    assert should_retrain(m2, thresholds) == ["drift", "data"]

    m3 = {"days_since_train": 5, "psi": 0.10, "accuracy": 0.90, "new_rows": 1000}
    assert should_retrain(m3, thresholds) == []

    print("\nExample 2: champion and challenger")
    print(f"  {champion_challenger(0.92, 0.91)}")
    assert champion_challenger(0.92, 0.91) == "promote: challenger wins"
    assert champion_challenger(0.89, 0.91) == "hold: champion retains"

    print("\nExample 3: cooldown prevents thrash")
    print(f"  3 days since last, min 7 -> {cooldown_ok(3, 7)}")
    assert not cooldown_ok(3, 7)
    assert cooldown_ok(10, 7)

    print("\nExample 4: the CT decision")
    print(f"  drifted but in cooldown -> {ct_decision(m2, thresholds, 0.91, 0.92)}")
    assert ct_decision(m2, thresholds, 0.91, 0.92) == "hold: cooldown"
    m4 = {"days_since_train": 40, "psi": 0.10, "accuracy": 0.90, "new_rows": 1000}
    print(f"  stale and past cooldown -> {ct_decision(m4, thresholds, 0.91, 0.93)}")
    assert ct_decision(m4, thresholds, 0.91, 0.93) == "promote: challenger wins"

    print("\n--- Summary ---")
    print("1. Rebuild on signal (named triggers), not on hope.")
    print("2. Promote only winners (champion/challenger).")
    print("3. Space retrains apart (cooldowns) and record every reason.")


def _verify() -> None:
    thresholds = {
        "max_age_days": 30,
        "psi": 0.25,
        "min_accuracy": 0.88,
        "min_new_rows": 10000,
        "min_interval_days": 7,
    }
    m_hold = {"days_since_train": 5, "psi": 0.10, "accuracy": 0.90, "new_rows": 1000}
    assert should_retrain(m_hold, thresholds) == []
    m_perf = {"days_since_train": 5, "psi": 0.10, "accuracy": 0.85, "new_rows": 1000}
    assert should_retrain(m_perf, thresholds) == ["performance"]

    assert champion_challenger(0.92, 0.91) == "promote: challenger wins"
    assert champion_challenger(0.91, 0.91) == "promote: challenger wins"
    assert champion_challenger(0.89, 0.91) == "hold: champion retains"

    assert not cooldown_ok(3, 7) and cooldown_ok(7, 7)

    assert ct_decision(m_hold, thresholds, 0.91, 0.92) == "hold: no trigger"
    m_stale = {"days_since_train": 40, "psi": 0.10, "accuracy": 0.90, "new_rows": 1000}
    assert ct_decision(m_stale, thresholds, 0.91, 0.93) == "promote: challenger wins"
    assert ct_decision(m_stale, thresholds, 0.93, 0.91) == "hold: champion retains"
    print("[OK] 20-continuous-training: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        main()
        _verify()
