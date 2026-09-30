"""
Prompt Engineering — 04: Prompt Evaluation
==========================================
Topics: test cases, scoring, and variation comparison.

Why this matters:
    A prompt is a hypothesis until it is measured. This exercise scores
    variations on the same test cases and selects the best.

Run:      python 04-prompt-evaluation.py
Verify:   python 04-prompt-evaluation.py --verify
"""

from __future__ import annotations

import sys


def score(variation: dict, cases: list[dict]) -> float:
    """Score a variation: the fraction of cases it answers correctly."""
    correct = 0
    for case in cases:
        answer = variation["answer_fn"](case["input"])
        if answer == case["expected"]:
            correct += 1
    return correct / len(cases)


def select(variations: list[dict], cases: list[dict]) -> str:
    """The best-scoring variation wins."""
    return max(variations, key=lambda v: score(v, cases))["name"]


def main() -> None:
    cases = [
        {"input": "2x + 5 = 15", "expected": "x = 5"},
        {"input": "x^2 - 4 = 0", "expected": "x = 2 or -2"},
    ]

    # v1 answers only the easy case; v2 answers both.
    v1 = {"name": "v1", "answer_fn": lambda i: "x = 5" if "2x" in i else "unknown"}
    v2 = {"name": "v2", "answer_fn": lambda i: "x = 5" if "2x" in i else "x = 2 or -2"}

    assert score(v1, cases) == 0.5
    assert score(v2, cases) == 1.0

    # The best-scoring variation wins, not the best-reading one.
    assert select([v1, v2], cases) == "v2"

    print("v1 scores 0.5; v2 scores 1.0 on the same test cases")
    print("the best-scoring variation wins")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
