"""
Prompt Engineering — 02: Few-Shot
=================================
Topics: example selection and the token cost.

Why this matters:
    Few-shot examples teach the pattern by imitation. This exercise
    checks pattern coverage and the cost tradeoff.

Run:      python 02-few-shot.py
Verify:   python 02-few-shot.py --verify
"""

from __future__ import annotations

import sys


def covers_pattern(examples: list[dict], cases: set[str]) -> bool:
    """Examples cover the pattern when each case appears."""
    covered = {e["case"] for e in examples}
    return cases <= covered


def token_cost(examples: list[dict], tokens_per_example: int) -> int:
    return len(examples) * tokens_per_example


def main() -> None:
    # Two different cases cover the pattern better than five similar ones.
    examples = [
        {"case": "easy", "problem": "2x + 5 = 15", "answer": "x = 5"},
        {"case": "hard", "problem": "x^2 - 4 = 0", "answer": "x = 2 or -2"},
    ]
    assert covers_pattern(examples, {"easy", "hard"})

    # Five identical examples do not cover the pattern.
    similar = [{"case": "easy", "problem": "2x + 5 = 15", "answer": "x = 5"}] * 5
    assert not covers_pattern(similar, {"easy", "hard"}), "no coverage"

    # Examples cost tokens: more examples, more cost.
    assert token_cost(examples, 100) == 200
    assert token_cost(similar, 100) == 500

    print("two different cases cover the pattern")
    print("five identical examples do not")
    print("examples cost tokens: 200 vs 500")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
