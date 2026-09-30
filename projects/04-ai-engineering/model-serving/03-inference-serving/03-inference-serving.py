"""
Model Serving — 03: Inference Serving
=====================================
Topics: the API contract, metrics, and the fallback chain.

Why this matters:
    Serving is the production boundary. This exercise models the API
    contract and the fallback chain.

Run:      python 03-inference-serving.py
Verify:   python 03-inference-serving.py --verify
"""

from __future__ import annotations

import sys
from typing import Callable, Sequence


def serve(
    request: dict,
    primary: Callable[[dict], dict],
    fallback: Callable[[dict], dict],
) -> dict:
    """Route to the primary; fall back on failure."""
    try:
        return primary(request)
    except Exception:
        return fallback(request)


def p95(values: Sequence[float]) -> float:
    """The 95th percentile latency."""
    sorted_v = sorted(values)
    idx = int(len(sorted_v) * 0.95)
    return sorted_v[min(idx, len(sorted_v) - 1)]


def main() -> None:
    # The fallback chain preserves availability.
    def fail(_):
        raise RuntimeError("primary down")

    def ok(_):
        return {"text": "answer", "usage": {"tokens": 10}}

    result = serve({"q": "hi"}, fail, ok)
    assert result["text"] == "answer", "fallback served the request"

    # When the primary works, the fallback is not used.
    result = serve({"q": "hi"}, ok, fail)
    assert result["text"] == "answer", "primary served the request"

    # Latency metrics: p95 captures the tail.
    latencies = [100, 120, 110, 500, 130]
    assert p95(latencies) >= 130, "p95 captures the slow request"

    print("fallback chain: primary failure routes to the backup")
    print("p95 latency captures the tail")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
