"""
Prompt Engineering — 03: Chain-of-Thought
=========================================
Topics: when CoT helps and the token cost.

Why this matters:
    CoT improves accuracy on multi-step problems but costs tokens. This
    exercise classifies tasks and checks the cost.

Run:      python 03-chain-of-thought.py
Verify:   python 03-chain-of-thought.py --verify
"""

from __future__ import annotations

import sys

MULTI_STEP = {"math", "science_reasoning", "code_debugging", "logic"}
NON_REASONING = {"simple_fact", "creative_writing", "translation"}


def cot_helps(task: str) -> bool:
    return task in MULTI_STEP


def token_cost(steps: int, tokens_per_step: int) -> int:
    return steps * tokens_per_step


def main() -> None:
    # CoT helps on multi-step problems.
    assert cot_helps("math")
    assert cot_helps("logic")
    assert not cot_helps("simple_fact"), "no steps needed"
    assert not cot_helps("translation"), "not a reasoning task"

    # The cost grows with the steps.
    assert token_cost(5, 20) == 100
    assert token_cost(0, 20) == 0, "no steps, no cost"

    print("CoT helps on multi-step problems: math, logic")
    print("CoT does not help on simple facts or translation")
    print("the token cost grows with the steps")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
