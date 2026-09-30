"""
Model Serving — 01: Choosing a Model
=====================================
Topics: the four axes and golden-set evaluation.

Why this matters:
    Choosing a model is a tradeoff. This exercise evaluates candidates
    on the golden set and picks the best.

Run:      python 01-choosing-a-model.py
Verify:   python 01-choosing-a-model.py --verify
"""

from __future__ import annotations

import sys


def evaluate(candidate: dict, golden: list[dict]) -> float:
    """Score a candidate on the golden set."""
    correct = 0
    for case in golden:
        if candidate["answer_fn"](case["query"]) == case["expected"]:
            correct += 1
    return correct / len(golden)


def choose(candidates: list[dict], golden: list[dict], budget: float) -> str:
    """Pick the best-scoring candidate within the cost budget."""
    within = [c for c in candidates if c["cost"] <= budget]
    return max(within, key=lambda c: evaluate(c, golden))["name"]


def main() -> None:
    golden = [
        {"query": "2+2", "expected": "4"},
        {"query": "3*3", "expected": "9"},
    ]

    cheap = {
        "name": "cheap",
        "cost": 0.01,
        "answer_fn": lambda q: "4" if q == "2+2" else "wrong",
    }
    good = {
        "name": "good",
        "cost": 0.05,
        "answer_fn": lambda q: "4" if q == "2+2" else "9",
    }
    expensive = {
        "name": "expensive",
        "cost": 0.50,
        "answer_fn": lambda q: "4" if q == "2+2" else "9",
    }

    assert evaluate(cheap, golden) == 0.5
    assert evaluate(good, golden) == 1.0

    # The best-scoring candidate within budget wins.
    assert choose([cheap, good, expensive], golden, budget=0.10) == "good"
    assert choose([cheap, good], golden, budget=0.02) == "cheap", "budget excludes good"

    print("candidates evaluated on the golden set")
    print("the best-scoring candidate within budget wins")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
