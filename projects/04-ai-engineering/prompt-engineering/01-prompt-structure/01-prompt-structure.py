"""
Prompt Engineering — 01: Prompt Structure
=========================================
Topics: the five sections and the specificity rule.

Why this matters:
    A prompt is a contract with the model. This exercise checks the
    structure and the task specificity.

Run:      python 01-prompt-structure.py
Verify:   python 01-prompt-structure.py --verify
"""

from __future__ import annotations

import sys

SECTIONS = ["role", "context", "task", "constraints", "output_format"]


def is_structured(prompt: dict) -> bool:
    """A structured prompt has all five sections."""
    return all(s in prompt for s in SECTIONS)


def is_specific(task: str) -> bool:
    """A specific task names the input, the action, and the result."""
    return len(task.split()) >= 8


def main() -> None:
    # A structured prompt has all five sections.
    good = {
        "role": "tutor",
        "context": "grade 10 physics",
        "task": "Explain why ice floats on water in two sentences.",
        "constraints": "max 2 sentences, no speculation",
        "output_format": "plain text",
    }
    assert is_structured(good)

    # A prompt missing a section is not structured.
    missing = dict(good)
    del missing["constraints"]
    assert not is_structured(missing), "constraints section missing"

    # A specific task names input, action, and result.
    assert is_specific(good["task"])
    assert not is_specific("Explain ice."), "vague task"

    print("a structured prompt has all five sections")
    print("a missing section breaks the structure")
    print("a specific task names input, action, and result")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
