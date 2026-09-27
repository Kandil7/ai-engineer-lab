"""
AI Evaluation — 03: Retrieval Evaluation
=========================================
Topics: recall@k, precision@k, and MRR against the golden set.

Why this matters:
    Retrieval quality is measured with ranked metrics. This exercise
    computes the three metrics and reads the failure pattern they reveal.

Run:      python 03-retrieval-evaluation.py
Verify:   python 03-retrieval-evaluation.py --verify
"""

from __future__ import annotations

import sys


def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    top = set(retrieved[:k])
    return len(top & relevant) / len(relevant)


def precision_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    top = retrieved[:k]
    return sum(1 for r in top if r in relevant) / k


def mrr(retrieved: list[str], relevant: set[str]) -> float:
    for i, r in enumerate(retrieved, start=1):
        if r in relevant:
            return 1 / i
    return 0.0


def main() -> None:
    relevant = {"b3:p12:0", "b3:p12:1", "b3:p12:2"}
    retrieved = ["b3:p12:0", "b9:p1:0", "b3:p12:1", "b9:p2:0", "b3:p12:2"]

    # All three relevant passages are in the top 5.
    assert abs(recall_at_k(retrieved, relevant, 5) - 1.0) < 1e-9
    # But two of the top five are noise.
    assert abs(precision_at_k(retrieved, relevant, 5) - 0.6) < 1e-9
    # The first relevant passage is ranked first.
    assert abs(mrr(retrieved, relevant) - 1.0) < 1e-9

    # A retriever that buries the answer: recall holds, MRR drops.
    buried = ["b9:p1:0", "b9:p2:0", "b3:p12:0", "b3:p12:1", "b3:p12:2"]
    assert abs(recall_at_k(buried, relevant, 5) - 1.0) < 1e-9
    assert abs(mrr(buried, relevant) - 1 / 3) < 1e-9, "first relevant at rank 3"

    # A retriever that misses material: recall collapses.
    missing = ["b9:p1:0", "b9:p2:0", "b9:p3:0", "b9:p4:0", "b3:p12:0"]
    assert abs(recall_at_k(missing, relevant, 5) - 1 / 3) < 1e-9

    print("recall@5=1.0, precision@5=0.6, MRR=1.0 on the good retriever")
    print("buried answer: recall holds, MRR drops to 0.333")
    print("missing material: recall collapses to 0.333")
    print("the three metrics diagnose different failures")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
