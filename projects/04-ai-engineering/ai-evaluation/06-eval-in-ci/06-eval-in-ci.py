"""
AI Evaluation — 06: Eval in CI
===============================
Topics: the eval harness, thresholds from a baseline, and the verdict.

Why this matters:
    An evaluation that never runs is a document, not a gate. This exercise
    builds a harness that compares a change against the baseline and
    returns a verdict.

Run:      python 06-eval-in-ci.py
Verify:   python 06-eval-in-ci.py --verify
"""

from __future__ import annotations

import sys


def run_harness(
    metrics: dict[str, float], baseline: dict[str, float]
) -> dict[str, str]:
    """Compare current metrics against the baseline floors. A metric below
    its floor fails."""
    verdicts = {}
    for name, floor in baseline.items():
        current = metrics[name]
        verdicts[name] = "PASS" if current >= floor else "FAIL"
    return verdicts


def main() -> None:
    baseline = {"recall@5": 0.80, "faithfulness": 0.90, "resistance": 0.90}

    # A good change: all metrics at or above the baseline.
    good = {"recall@5": 0.85, "faithfulness": 0.92, "resistance": 0.95}
    verdicts = run_harness(good, baseline)
    assert all(v == "PASS" for v in verdicts.values()), "good change passes"

    # A regression: recall improves, faithfulness drops below the floor.
    regression = {"recall@5": 0.88, "faithfulness": 0.80, "resistance": 0.95}
    verdicts = run_harness(regression, baseline)
    assert verdicts["recall@5"] == "PASS"
    assert verdicts["faithfulness"] == "FAIL", "faithfulness below floor"

    # The delta makes the tradeoff explicit.
    delta = regression["faithfulness"] - baseline["faithfulness"]
    assert abs(delta - (-0.10)) < 1e-9

    print("good change: all metrics PASS against the baseline")
    print("regression: recall PASS but faithfulness FAIL (delta -0.10)")
    print("the report makes the tradeoff explicit, not hidden")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
