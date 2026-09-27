"""
Embeddings — 01: Model Selection
================================
Topics: the selection axes and the consistency rule.

Why this matters:
    The embedding model decides retrieval quality. This exercise models
    the selection tradeoff and the consistency requirement.

Run:      python 01-model-selection.py
Verify:   python 01-model-selection.py --verify
"""

from __future__ import annotations

import sys

MODELS = {
    "all-MiniLM-L6-v2": {"dims": 384, "cost": 0.0, "multilingual": False},
    "nomic-embed-text": {"dims": 768, "cost": 0.0, "multilingual": True},
    "text-embedding-3-small": {"dims": 1536, "cost": 0.02, "multilingual": True},
    "text-embedding-3-large": {"dims": 3072, "cost": 0.13, "multilingual": True},
}


def choose(corpus_language: str, context: str) -> str:
    """Choose a model that covers the language and fits the context."""
    candidates = [
        m for m, p in MODELS.items() if p["multilingual"] or corpus_language == "en"
    ]
    if context == "prototype":
        return min(candidates, key=lambda m: MODELS[m]["dims"])
    return min(candidates, key=lambda m: MODELS[m]["cost"])


def main() -> None:
    # For Arabic, only multilingual models qualify.
    assert choose("ar", "prototype") == "nomic-embed-text", "smallest multilingual"
    assert choose("ar", "production") == "text-embedding-3-small", (
        "cheapest multilingual"
    )

    # For English, the monolingual MiniLM qualifies for prototyping.
    assert choose("en", "prototype") == "all-MiniLM-L6-v2"

    # Consistency: the corpus and queries use the same model.
    corpus_model = choose("ar", "production")
    query_model = choose("ar", "production")
    assert corpus_model == query_model, "one model across the pipeline"

    print("Arabic requires a multilingual model")
    print("prototype picks the smallest; production picks the cheapest")
    print("the corpus and queries use the same model")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
