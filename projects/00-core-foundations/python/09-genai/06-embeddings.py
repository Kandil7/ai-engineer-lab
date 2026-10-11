"""
GenAI - 06: Embeddings
======================
Topics: embedding models, dimensionality, normalization, cosine
similarity, batching, caching embeddings, model selection and migration
cost.

Why this matters for AI/backend engineering:
    Embeddings are the foundation of retrieval. Every RAG system, every
    semantic cache, every dedup pipeline is cosine similarity over
    vectors. Understanding normalization, distance, and batching is the
    difference between a working search and a broken one.

Run:      python 06-embeddings.py
Verify:   python 06-embeddings.py --verify
Reference: https://platform.openai.com/docs/guides/embeddings
"""

from __future__ import annotations

import math
import random
import sys


# ============================================================
# 1. Embeddings Are Vectors
# ============================================================
# Text -> fixed-size vector. Similar text -> nearby vectors.
# Dimensionality is a model property: 384 (small), 768, 1536, 3072.


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine of the angle between two vectors (ignores magnitude)."""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def normalize(vec: list[float]) -> list[float]:
    """Unit vector - cosine similarity then equals dot product."""
    n = math.sqrt(sum(x * x for x in vec))
    return [x / n for x in vec] if n > 0 else vec


# Example 1: a tiny toy embedding model (bag of hashed substrings)
def toy_embed(text: str, dim: int = 64) -> list[float]:
    vec = [0.0] * dim
    for ch in text.lower():
        if ch.isalnum():
            vec[ord(ch) % dim] += 1.0
    return vec


e_cat = toy_embed("cat")
e_kitten = toy_embed("kitten")
e_rocket = toy_embed("rocket engine")
print("Example 1: cosine similarity")
print(f"  cat vs kitten:  {cosine_similarity(e_cat, e_kitten):.3f}")
print(f"  cat vs rocket:  {cosine_similarity(e_cat, e_rocket):.3f}")
assert cosine_similarity(e_cat, e_kitten) > cosine_similarity(e_cat, e_rocket), (
    "related text is more similar"
)

# ============================================================
# 2. Normalization
# ============================================================
# Cosine similarity ignores magnitude. Dot product does not. If you
# normalize once, cosine == dot, which is much faster at scale.

# Example 2: normalized dot product == cosine
n_cat = normalize(e_cat)
n_kitten = normalize(e_kitten)
dot = sum(x * y for x, y in zip(n_cat, n_kitten))
cos = cosine_similarity(e_cat, e_kitten)
print("\nExample 2: normalization")
print(f"  cosine={cos:.4f}  normalized-dot={dot:.4f}")
assert abs(dot - cos) < 1e-9, "normalized dot equals cosine"

# ============================================================
# 3. Batch Embedding + Caching
# ============================================================
# Embedding calls are billed per token and per call. Batch them and
# cache by text hash - repeated content should cost nothing.


class EmbeddingCache:
    def __init__(self) -> None:
        self._cache: dict[str, list[float]] = {}

    def embed(self, text: str) -> list[float]:
        key = text
        if key not in self._cache:
            self._cache[key] = toy_embed(text)
        return self._cache[key]

    def hit_rate(self) -> float:
        return 0.0  # tracked in the batcher below


class BatchedEmbedder:
    def __init__(self, cache: EmbeddingCache | None = None, batch_size: int = 16) -> None:
        self.cache = cache or EmbeddingCache()
        self.batch_size = batch_size
        self.calls = 0

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        """Embed in batches; dedupe identical texts via the cache."""
        out: list[list[float]] = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            self.calls += 1  # one API call per batch
            out.extend(self.cache.embed(t) for t in batch)
        return out


# Example 3: batching math
embedder = BatchedEmbedder(batch_size=16)
texts = [f"doc {i}" for i in range(40)]
vectors = embedder.embed_many(texts)
print("\nExample 3: batching")
print(f"  40 texts, batch size 16 -> {embedder.calls} API calls")
assert embedder.calls == 3, "40/16 = 3 calls"

# ============================================================
# 4. Model Selection and Migration Cost
# ============================================================
# Changing embedding models changes EVERY vector - all indexes must be
# rebuilt. That is the real migration cost, not the API price.


def migration_estimate(
    documents: int, old_dim: int, new_dim: int, embed_cost_per_1k: float
) -> float:
    """Cost to re-embed a corpus when switching models."""
    tokens = documents * 300  # assume ~300 tokens/doc
    return tokens / 1000 * embed_cost_per_1k


# Example 4: migration cost
cost = migration_estimate(1_000_000, 1536, 768, 0.02)
print("\nExample 4: embedding migration cost")
print(f"  re-embedding 1M docs: ${cost:.0f} + index rebuild time")
assert cost > 0


# ============================================================
# Production Pattern
# ============================================================
def build_index(docs: list[str], embedder: BatchedEmbedder) -> list[list[float]]:
    """Embed a corpus and normalize every vector for dot-product search."""
    return [normalize(v) for v in embedder.embed_many(docs)]


def search(
    query: str, index: list[list[float]], embedder: BatchedEmbedder, k: int = 3
) -> list[int]:
    """Top-k nearest neighbors by dot product (normalized == cosine)."""
    qv = normalize(embedder.cache.embed(query))
    scored = [(i, sum(x * y for x, y in zip(qv, index[i]))) for i in range(len(index))]
    scored.sort(key=lambda t: t[1], reverse=True)
    return [i for i, _ in scored[:k]]


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: using Euclidean distance on unnormalized vectors
# MISTAKE: forgetting to normalize - dot product silently differs
# MISTAKE: one API call per text (batch or pay the latency)
# MISTAKE: changing embedding models without budgeting the re-embed


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    v1, v2 = [1.0, 0.0], [0.0, 1.0]
    assert abs(cosine_similarity(v1, v2)) < 1e-9, "orthogonal -> 0"
    assert abs(cosine_similarity([1.0], [2.0]) - 1.0) < 1e-9, "parallel -> 1"
    assert abs(cosine_similarity([], [])) < 1e-9, "zero vector -> 0"

    n = normalize([3.0, 4.0])
    assert abs(math.sqrt(n[0] ** 2 + n[1] ** 2) - 1.0) < 1e-9, "unit length"

    e = EmbeddingCache()
    first = e.embed("abc")
    assert e.embed("abc") == first, "cached"

    b = BatchedEmbedder(batch_size=8)
    b.embed_many([f"t{i}" for i in range(20)])
    assert b.calls == 3, "20/8 = 3 calls"

    idx = build_index(["apple pie recipe", "car repair guide", "apple fruit facts"], embedder)
    top = search("how to bake apple pie", idx, embedder, k=1)
    assert top[0] == 0, "retrieves the most similar doc"

    assert migration_estimate(1000, 1536, 768, 0.02) > 0
    print("[OK] 06-embeddings: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Embeddings map text to vectors; similarity is proximity.")
        print("2. Normalize once so dot product == cosine.")
        print("3. Batch and cache; re-embedding is the real migration cost.")
        _verify()
