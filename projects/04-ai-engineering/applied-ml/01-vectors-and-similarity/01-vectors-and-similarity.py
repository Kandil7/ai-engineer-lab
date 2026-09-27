"""
Applied ML — 01: Vectors and Similarity
========================================
Topics: dot product, cosine similarity, Euclidean distance, the unit-vector
        identity, and how normalization changes rankings.

Why this matters:
    Every AI system rests on vectors. This exercise builds the three
    metrics, proves the unit-vector identity, and shows normalization
    changes rankings.

Run:      python 01-vectors-and-similarity.py
Verify:   python 01-vectors-and-similarity.py --verify
"""

from __future__ import annotations

import math
import sys


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(v: list[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def cosine(a: list[float], b: list[float]) -> float:
    return dot(a, b) / (norm(a) * norm(b))


def euclidean(a: list[float], b: list[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def normalize(v: list[float]) -> list[float]:
    n = norm(v)
    return [x / n for x in v]


def main() -> None:
    a = [3.0, 4.0, 0.0]
    b = [1.0, 2.0, 1.0]

    # Unit-vector identity: cosine equals dot on normalized vectors.
    an, bn = normalize(a), normalize(b)
    assert abs(cosine(a, b) - dot(an, bn)) < 1e-9

    # Cosine is magnitude-free: scaling a does not change cosine.
    assert abs(cosine(a, b) - cosine([x * 10 for x in a], b)) < 1e-9

    # Euclidean is magnitude-sensitive: scaling changes distance.
    assert euclidean(a, b) != euclidean([x * 10 for x in a], b)

    # Normalization changes rankings: a long vector wins by dot, not cosine.
    short = [1.0, 0.0, 0.0]
    long = [5.0, 0.0, 0.0]
    q = [1.0, 0.0, 0.0]
    assert dot(long, q) > dot(short, q)  # magnitude wins by dot
    assert cosine(long, q) == cosine(short, q)  # direction equal by cosine

    print(f"cosine(a,b)={cosine(a, b):.3f} euclidean(a,b)={euclidean(a, b):.3f}")
    print("unit-vector identity holds: cosine == dot on normalized vectors")
    print(
        "normalization changes rankings: dot favors magnitude, cosine favors direction"
    )
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
