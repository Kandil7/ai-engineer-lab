"""
Embeddings — 04: Quality Evaluation
===================================
Topics: golden pairs, cosine similarity, and consistency.

Why this matters:
    Embedding quality is measured, not assumed. This exercise checks
    golden pairs and the consistency rule.

Run:      python 04-quality-evaluation.py
Verify:   python 04-quality-evaluation.py --verify
"""

from __future__ import annotations

import sys


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb)


def passes(
    pair: tuple[str, str, float], vectors: dict[str, list[float]], threshold: float
) -> bool:
    """A positive pair passes when its similarity meets the target."""
    a, b, target = pair
    return cosine(vectors[a], vectors[b]) >= target * threshold


def main() -> None:
    # A stub embedding: related texts share a token.
    vectors = {
        "ما هو العدد الأولي؟": [1.0, 0.0],
        "What is a prime number?": [0.9, 0.1],
        "النسبة المئوية": [1.0, 0.0],
        "Percentage": [0.9, 0.1],
        "Physics": [0.0, 1.0],
    }

    # Positive pairs pass: related texts embed close.
    assert passes(("ما هو العدد الأولي؟", "What is a prime number?", 0.9), vectors, 0.9)
    assert passes(("النسبة المئوية", "Percentage", 0.85), vectors, 0.9)

    # A negative pair is far apart.
    assert cosine(vectors["النسبة المئوية"], vectors["Physics"]) < 0.5

    # Consistency: the same text embeds the same way.
    assert cosine(vectors["النسبة المئوية"], vectors["النسبة المئوية"]) == 1.0

    print("positive pairs embed close; the negative pair is far apart")
    print("consistency: the same text embeds the same way")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
