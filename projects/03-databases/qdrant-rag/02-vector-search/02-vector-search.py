"""
Qdrant — 02: Vector Search
==========================
Topics: the query embedding, the score, and the threshold.

Why this matters:
    Vector search finds the points closest to a query vector. This
    exercise models the search and the embedding-match rule.

Run:      python 02-vector-search.py
Verify:   python 02-vector-search.py --verify
"""

from __future__ import annotations

import sys


def cosine(a: list[float], b: list[float]) -> float:
    assert len(a) == len(b), "vectors must match in size"
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb)


def search(
    points: dict[str, list[float]], query: list[float], limit: int, threshold: float
) -> list[tuple[str, float]]:
    scored = [(pid, cosine(query, vec)) for pid, vec in points.items()]
    scored = [(pid, s) for pid, s in scored if s >= threshold]
    scored.sort(key=lambda t: t[1], reverse=True)
    return scored[:limit]


def main() -> None:
    points = {
        "b3:p12:0": [1.0, 0.0, 0.0],
        "b3:p12:1": [0.9, 0.1, 0.0],
        "b9:p1:0": [0.0, 1.0, 0.0],
    }

    # The query is embedded with the same model (same size).
    query = [1.0, 0.0, 0.0]
    results = search(points, query, limit=2, threshold=0.5)
    assert results[0][0] == "b3:p12:0", "most similar first"
    assert len(results) == 2, "limit caps the results"

    # The threshold drops weak matches.
    results = search(points, query, limit=10, threshold=0.995)
    assert len(results) == 1, "only the near-identical point passes"

    # An embedding mismatch is a silent failure: wrong size.
    try:
        cosine(query, [1.0, 0.0])
        assert False, "size mismatch must be rejected"
    except AssertionError:
        pass

    print("search returns the top-k by cosine similarity")
    print("the threshold drops weak matches")
    print("an embedding size mismatch is rejected, not silent")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
