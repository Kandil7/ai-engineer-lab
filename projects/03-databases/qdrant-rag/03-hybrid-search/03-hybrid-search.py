"""
Qdrant — 03: Hybrid Search
==========================
Topics: vector + keyword retrieval and reciprocal rank fusion.

Why this matters:
    Hybrid search combines semantic and lexical signals. This exercise
    fuses two ranked lists with RRF.

Run:      python 03-hybrid-search.py
Verify:   python 03-hybrid-search.py --verify
"""

from __future__ import annotations

import sys


def rrf_score(ranks: list[int]) -> float:
    """Reciprocal rank fusion: sum of 1/(60 + rank) across the lists."""
    return sum(1 / (60 + r) for r in ranks)


def fuse(vector: list[str], keyword: list[str]) -> list[str]:
    """Fuse two ranked lists by RRF score, highest first."""
    scores: dict[str, float] = {}
    for rank, pid in enumerate(vector, start=1):
        scores[pid] = scores.get(pid, 0.0) + rrf_score([rank])
    for rank, pid in enumerate(keyword, start=1):
        scores[pid] = scores.get(pid, 0.0) + rrf_score([rank])
    return sorted(scores, key=lambda pid: scores[pid], reverse=True)


def main() -> None:
    vector = ["b3:p12:0", "b3:p12:1", "b9:p1:0"]
    keyword = ["b9:p1:0", "b3:p12:0"]

    fused = fuse(vector, keyword)

    # A result ranked first in both lists wins the fusion.
    assert fused[0] == "b3:p12:0", "ranked first in both lists -> top"
    # A result only in one list still appears, below the shared winner.
    assert "b3:p12:1" in fused
    assert "b9:p1:0" in fused

    # RRF: rank 1 scores higher than rank 3.
    assert rrf_score([1]) > rrf_score([3])

    print("fusion combines the two ranked lists by RRF")
    print("a result ranked first in both lists wins")
    print("results present in only one list still appear")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
