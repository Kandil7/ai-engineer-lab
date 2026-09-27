"""
Arabic NLP — 06: Approximate Nearest Neighbor (ANN) Search
==========================================================
Topics: the recall/speed tradeoff and the index parameters.

Why this matters:
    Exact search does not scale. This exercise models the ANN tradeoff
    and measures the recall loss.

Run:      python 06-arabic-ann-search.py
Verify:   python 06-arabic-ann-search.py --verify
"""

from __future__ import annotations

import sys


def exact_search(
    points: dict[str, list[float]], query: list[float], k: int
) -> list[str]:
    """Exact: score every vector, return the top-k."""
    scored = sorted(
        points, key=lambda pid: sum((a - b) ** 2 for a, b in zip(points[pid], query))
    )
    return scored[:k]


def ann_search(
    points: dict[str, list[float]], query: list[float], k: int, prune: float
) -> list[str]:
    """ANN: score only a fraction of the vectors (the pruned set)."""
    n = max(1, int(len(points) * prune))
    sampled = list(points)[:n]  # stub: the index prunes to this subset
    scored = sorted(
        sampled, key=lambda pid: sum((a - b) ** 2 for a, b in zip(points[pid], query))
    )
    return scored[:k]


def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    top = set(retrieved[:k])
    return len(top & relevant) / len(relevant)


def main() -> None:
    points = {f"p{i}": [float(i), 0.0] for i in range(100)}
    query = [3.0, 0.0]
    relevant = {"p3"}

    # Exact search finds the true neighbor.
    exact = exact_search(points, query, 5)
    assert exact[0] == "p3", "exact search returns the true neighbor"

    # ANN with light pruning keeps recall.
    ann_light = ann_search(points, query, 5, prune=0.5)
    assert recall_at_k(ann_light, relevant, 5) == 1.0

    # ANN with heavy pruning loses recall: the true neighbor is pruned.
    ann_heavy = ann_search(points, query, 5, prune=0.02)
    assert recall_at_k(ann_heavy, relevant, 5) < 1.0, "heavy pruning loses recall"

    print("exact search returns the true neighbor")
    print("light pruning keeps recall; heavy pruning loses it")
    print("the recall/speed tradeoff is controlled by the index parameters")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
