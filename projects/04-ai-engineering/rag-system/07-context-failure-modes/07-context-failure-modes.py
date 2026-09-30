"""
RAG System — 07: Context Failure Modes
=======================================
Topics: missing, noisy, stale, and contradictory material.

Why this matters:
    Context failures are answer failures. This exercise detects each
    failure mode and applies the guard.

Run:      python 07-context-failure-modes.py
Verify:   python 07-context-failure-modes.py --verify
"""

from __future__ import annotations

import sys


def detect_missing(golden_relevant: set[str], context_ids: set[str]) -> bool:
    return not (golden_relevant & context_ids)


def detect_noisy(context: list[dict], min_score: float) -> bool:
    return any(c["score"] < min_score for c in context)


def detect_stale(context_versions: set[str], expected: str) -> bool:
    return expected not in context_versions


def detect_contradictory(context: list[dict]) -> bool:
    claims = [c.get("claim") for c in context if c.get("claim")]
    return len(set(claims)) > 1 and len(claims) > 1


def main() -> None:
    # Missing: the relevant passage is not in the context.
    assert detect_missing({"b3:p12:0"}, {"b9:p1:0", "b9:p2:0"}), "missing material"
    assert not detect_missing({"b3:p12:0"}, {"b3:p12:0", "b9:p1:0"})

    # Noisy: a low-score passage crowds the context.
    context = [{"evidence_id": "a", "score": 0.9}, {"evidence_id": "b", "score": 0.3}]
    assert detect_noisy(context, 0.5), "noisy material"
    assert not detect_noisy(context[:1], 0.5)

    # Stale: the expected source version is absent.
    assert detect_stale({"v1"}, "v2"), "stale material"
    assert not detect_stale({"v1", "v2"}, "v2")

    # Contradictory: two passages make different claims.
    contradictions = [{"claim": "X"}, {"claim": "not-X"}]
    assert detect_contradictory(contradictions), "contradictory material"
    assert not detect_contradictory([{"claim": "X"}, {"claim": "X"}])

    print("missing: relevant passage absent from the context")
    print("noisy: low-score passage crowds the context")
    print("stale: expected source version absent")
    print("contradictory: two passages make different claims")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
