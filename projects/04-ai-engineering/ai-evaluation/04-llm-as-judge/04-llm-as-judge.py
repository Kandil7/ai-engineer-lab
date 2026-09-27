"""
AI Evaluation — 04: LLM-as-Judge
=================================
Topics: judge design, judge bias, and validating the judge against humans.

Why this matters:
    Some evaluation questions cannot be answered mechanically. A judge
    model grades at scale, but only if it agrees with humans. This
    exercise builds a judge and measures its agreement.

Run:      python 04-llm-as-judge.py
Verify:   python 04-llm-as-judge.py --verify
"""

from __future__ import annotations

import sys


def judge_grade(answer: str, rubric: dict) -> dict:
    """A stub judge: grades faithfulness by whether the answer cites a
    context passage, helpfulness by whether it answers at all."""
    faithful = "b3:p12" in answer
    helpful = len(answer.strip()) > 0
    return {
        "faithfulness": 1.0 if faithful else 0.0,
        "helpfulness": 1.0 if helpful else 0.0,
    }


def judge_accuracy(judge_grades: list[float], human_grades: list[float]) -> float:
    """Fraction of judge grades within 0.25 of the human grade."""
    assert len(judge_grades) == len(human_grades)
    close = sum(1 for j, h in zip(judge_grades, human_grades) if abs(j - h) <= 0.25)
    return close / len(judge_grades)


def main() -> None:
    rubric = {"faithfulness": (0, 1), "helpfulness": (0, 1)}

    # A grounded answer grades faithful; an unsupported one does not.
    grounded = judge_grade("القصر جائز (b3:p12:0)", rubric)
    assert grounded["faithfulness"] == 1.0
    invented = judge_grade("صيام رمضان واجب", rubric)
    assert invented["faithfulness"] == 0.0, "no citation -> not faithful"

    # Judge validation: agreement with human grades on a sample.
    judge_grades = [1.0, 0.0, 1.0, 0.0, 1.0]
    human_grades = [1.0, 0.0, 0.8, 0.0, 1.0]
    acc = judge_accuracy(judge_grades, human_grades)
    assert acc >= 0.8, "judge agrees with humans on the sample"

    # A judge that disagrees with humans is not measuring what it claims.
    bad_judge = [1.0, 1.0, 1.0, 1.0, 1.0]
    assert judge_accuracy(bad_judge, human_grades) < 0.8

    print("grounded answer graded faithful; unsupported answer graded 0")
    print(f"judge-human agreement on the sample: {acc:.2f}")
    print("a judge that disagrees with humans is not measuring faithfulness")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
