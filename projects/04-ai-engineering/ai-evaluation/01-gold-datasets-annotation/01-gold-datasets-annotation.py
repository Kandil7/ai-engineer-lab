"""
AI Evaluation — 01: Gold Datasets and Annotation
=================================================
Topics: golden queries, coverage, annotation guidelines, and Cohen's kappa
        for inter-annotator agreement.

Why this matters:
    Evaluation is only as good as the ground truth it measures against.
    This exercise builds a small golden set and measures annotator
    agreement.

Run:      python 01-gold-datasets-annotation.py
Verify:   python 01-gold-datasets-annotation.py --verify
"""

from __future__ import annotations

import sys


def cohen_kappa(a: list[str], b: list[str], categories: set[str]) -> float:
    """Agreement corrected for chance. a and b are parallel label lists."""
    n = len(a)
    assert len(b) == n
    observed = sum(1 for x, y in zip(a, b) if x == y) / n
    chance = 0.0
    for c in categories:
        pa = a.count(c) / n
        pb = b.count(c) / n
        chance += pa * pb
    return (observed - chance) / (1 - chance)


def main() -> None:
    # Two annotators label 50 queries as relevant (R) or not (N).
    # The majority label is N (40 of 50), so chance agreement is high.
    a = ["R"] * 10 + ["N"] * 40
    b = ["R"] * 8 + ["N"] * 42  # agrees on 48, disagrees on 2

    kappa = cohen_kappa(a, b, {"R", "N"})

    # Observed agreement is 96%, but kappa corrects for chance.
    observed = 48 / 50
    assert observed == 0.96
    assert 0.7 <= kappa < 0.96, "kappa is below raw agreement"

    # A golden query carries relevant passages and a verified answer.
    golden = {
        "query": "ما حكم الصلاة في السفر؟",
        "relevant": ["b3:p12:0", "b3:p12:1"],
        "answer": "القصر جائز للمسافر",
    }
    assert golden["relevant"] and golden["answer"]

    # Coverage: the golden set spans question types, not just volume.
    types = {"verse", "hadith", "fiqh", "unanswerable"}
    assert "unanswerable" in types, "abstention cases belong in the set"

    print(f"observed agreement=0.96, Cohen's kappa={kappa:.3f}")
    print("kappa corrects for chance: high raw agreement can hide ambiguity")
    print("golden query carries relevant passages and a verified answer")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
