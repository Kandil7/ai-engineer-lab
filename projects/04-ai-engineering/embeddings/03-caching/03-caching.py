"""
Embeddings — 03: Caching
========================
Topics: the cache key, cache-aside, and invalidation.

Why this matters:
    Embeddings are expensive to generate. This exercise models the
    model-keyed cache and the invalidation rule.

Run:      python 03-caching.py
Verify:   python 03-caching.py --verify
"""

from __future__ import annotations

import sys


def cache_key(model: str, text: str) -> str:
    """The key carries the model and a content hash."""
    return f"embedding:{model}:{hash(text)}"


class EmbeddingCache:
    def __init__(self) -> None:
        self.store: dict[str, list[float]] = {}

    def get(self, key: str) -> list[float] | None:
        return self.store.get(key)

    def put(self, key: str, vector: list[float]) -> None:
        self.store[key] = vector


def main() -> None:
    cache = EmbeddingCache()
    text = "القصر جائز للمسافر"

    # The key carries the model: a different model misses.
    k1 = cache_key("model-a", text)
    k2 = cache_key("model-b", text)
    assert k1 != k2, "the model is part of the key"

    # Cache-aside: a miss embeds and stores; a hit returns.
    assert cache.get(k1) is None, "first request is a miss"
    cache.put(k1, [0.1, 0.2, 0.3])
    assert cache.get(k1) == [0.1, 0.2, 0.3], "hit returns the cached vector"

    # A model change invalidates: the old entry naturally misses.
    assert cache.get(k2) is None, "model change invalidates the cache"

    print("the cache key carries the model and the content hash")
    print("cache-aside: miss embeds and stores, hit returns")
    print("a model change invalidates: the old entry naturally misses")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
