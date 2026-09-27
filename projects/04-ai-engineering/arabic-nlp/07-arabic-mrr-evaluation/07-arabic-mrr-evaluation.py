"""
Arabic NLP — 07: MRR Evaluation
================================
Topics: MRR, recall@k, and the Arabic golden set.

Why this matters:
    Retrieval quality is measured, not assumed. This exercise computes
    MRR and recall@k on an Arabic golden set.

Run:      python 07-arabic-mrr-evaluation.py
Verify:   python 07-arabic-mrr-evaluation.py --verify
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def mrr(retrieved: list[str], relevant: set[str]) -> float:
    for i, r in enumerate(retrieved, start=1):
        if r in relevant:
            return 1 / i
    return 0.0


def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    top = set(retrieved[:k])
    return len(top & relevant) / len(relevant)


def main() -> None:
    # An Arabic golden query: the relevant passage is b3:p12:0.
    query = "ما حكم الصلاة في السفر؟"
    relevant = {"b3:p12:0"}
    retrieved = ["b3:p12:0", "b9:p1:0", "b3:p12:1"]

    # The first relevant passage is ranked first: MRR 1.0.
    assert abs(mrr(retrieved, relevant) - 1.0) < 1e-9
    assert abs(recall_at_k(retrieved, relevant, 5) - 1.0) < 1e-9

    # A retriever that buries the answer: recall holds, MRR drops.
    buried = ["b9:p1:0", "b9:p2:0", "b3:p12:0"]
    assert abs(recall_at_k(buried, relevant, 5) - 1.0) < 1e-9
    assert abs(mrr(buried, relevant) - 1 / 3) < 1e-9

    # A retriever that misses the material: recall collapses.
    missing = ["b9:p1:0", "b9:p2:0", "b9:p3:0"]
    assert abs(recall_at_k(missing, relevant, 5) - 0.0) < 1e-9
    assert mrr(missing, relevant) == 0.0

    print(f"golden query: {query}")
    print("first relevant ranked first: MRR 1.0, recall@5 1.0")
    print("buried answer: recall holds, MRR drops to 0.333")
    print("missing material: recall collapses to 0.0")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
