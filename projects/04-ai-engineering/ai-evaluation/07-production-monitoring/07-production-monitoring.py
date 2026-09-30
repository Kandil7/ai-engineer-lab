"""
AI Evaluation — 07: Production Monitoring
==========================================
Topics: metrics, alerts, and quality drift.

Why this matters:
    A system that passes evals can fail in production. This exercise
    detects drift and fires alerts.

Run:      python 07-production-monitoring.py
Verify:   python 07-production-monitoring.py --verify
"""

from __future__ import annotations

import sys


def detect_drift(rolling: list[float], baseline: float, tolerance: float) -> bool:
    """Drift when the rolling quality drops below the baseline minus tolerance."""
    recent = rolling[-3:]
    avg = sum(recent) / len(recent)
    return avg < baseline - tolerance


def should_alert(latency_p95: float, error_rate: float, thresholds: dict) -> list[str]:
    """Fire alerts on threshold crossings."""
    alerts = []
    if latency_p95 > thresholds["latency_p95"]:
        alerts.append("latency")
    if error_rate > thresholds["error_rate"]:
        alerts.append("error_rate")
    return alerts


def main() -> None:
    baseline = 0.92

    # Stable quality: no drift.
    stable = [0.92, 0.91, 0.93, 0.92]
    assert not detect_drift(stable, baseline, tolerance=0.05)

    # Drifting quality: the rolling average drops.
    drifting = [0.92, 0.88, 0.85, 0.82]
    assert detect_drift(drifting, baseline, tolerance=0.05), "drift detected"

    # Alerts fire on threshold crossings.
    thresholds = {"latency_p95": 2000, "error_rate": 0.01}
    assert should_alert(500, 0.005, thresholds) == [], "healthy"
    assert should_alert(3000, 0.005, thresholds) == ["latency"]
    assert should_alert(500, 0.02, thresholds) == ["error_rate"]
    assert len(should_alert(3000, 0.02, thresholds)) == 2

    print("drift detected when rolling quality drops below the baseline")
    print("alerts fire on latency and error-rate threshold crossings")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
