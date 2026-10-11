"""
GenAI - 09: RAG Baseline
========================
Topics: the minimal correct pipeline - ingest -> chunk -> embed -> store ->
retrieve -> generate with citations; build the baseline before optimizing.

Why this matters for AI/backend engineering:
    A correct-but-simple RAG system beats a fancy-but-broken one. The
    baseline gives you a number to beat: build it end to end first,
    measure it, THEN add rerankers and hybrid search.

Run:      python 09-rag-baseline.py
Verify:   python 09-rag-baseline.py --verify
Reference: https://docs.llamaindex.ai/en/stable/getting_started/concepts/
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from typing import Callable


# ============================================================
# 1. The Pipeline Building Blocks (compact, from earlier topics)
# ============================================================


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0


def toy_embed(text: str, dim: int = 64) -> list[float]:
    vec = [0.0] * dim
    for ch in text.lower():
        if ch.isalnum():
            vec[ord(ch) % dim] += 1.0
    return vec


@dataclass
class Chunk:
    text: str
    source: str
    index: int


def fixed_chunks(text: str, size: int = 120, overlap: int = 20) -> list[str]:
    if not text:
        return []
    step = size - overlap
    return [text[i : i + size] for i in range(0, len(text), step)]


# ============================================================
# 2. The Vector Store
# ============================================================


class VectorStore:
    def __init__(self) -> None:
        self._vectors: list[list[float]] = []
        self._chunks: list[Chunk] = []

    def add(self, chunk: Chunk, vector: list[float]) -> None:
        self._chunks.append(chunk)
        self._vectors.append(vector)

    def search(self, query_vec: list[float], k: int = 3) -> list[tuple[Chunk, float]]:
        scored = [
            (self._chunks[i], cosine_similarity(query_vec, self._vectors[i]))
            for i in range(len(self._chunks))
        ]
        scored.sort(key=lambda t: t[1], reverse=True)
        return scored[:k]


# ============================================================
# 3. Ingestion + Retrieval
# ============================================================


def ingest(documents: dict[str, str]) -> VectorStore:
    """chunk -> embed -> store, the whole ingestion side."""
    store = VectorStore()
    for source, text in documents.items():
        for i, piece in enumerate(fixed_chunks(text)):
            store.add(Chunk(piece, source, i), toy_embed(piece))
    return store


def retrieve(store: VectorStore, query: str, k: int = 2) -> list[tuple[Chunk, float]]:
    return store.search(toy_embed(query), k=k)


# Example 1: a working baseline
docs = {
    "manual.md": (
        "The API key lives in your environment file. Rotate it every 90 days. Never commit it."
    ),
    "pricing.md": ("Plans start at $10 per month. Enterprise includes SSO and audit logs."),
    "faq.md": (
        "To reset your password, click the link in the email. Support responds within 24 hours."
    ),
}
store = ingest(docs)
hits = retrieve(store, "where does the API key live?", k=2)
print("Example 1: baseline retrieval")
for chunk, score in hits:
    print(f"  [{score:.3f}] {chunk.source} #{chunk.index}: {chunk.text[:50]}")
assert any("API key" in c.text for c, _ in hits), "retrieves the right chunk"

# ============================================================
# 4. Generate with Citations
# ============================================================
# The generator gets the retrieved chunks AND must cite their sources.
# Citations are what make RAG outputs trustworthy and debuggable.


def generate_with_citations(
    query: str, hits: list[tuple[Chunk, float]], model: Callable[[str], str]
) -> str:
    context = "\n".join(f"[{i + 1}] {chunk.text}" for i, (chunk, _) in enumerate(hits))
    sources = ", ".join(f"[{i + 1}]({chunk.source})" for i, (chunk, _) in enumerate(hits))
    answer = model(context)
    return f"{answer}\n\nSources: {sources}"


def stub_model(context: str) -> str:
    return "The API key is stored in the environment file."


# Example 2: generated answer with citations
answer = generate_with_citations("where is the key?", hits, stub_model)
print("\nExample 2: generation with citations")
print(f"  {answer}")
assert "Sources:" in answer and "manual.md" in answer, "citations attached"

# ============================================================
# 5. The Baseline Contract
# ============================================================
# Before optimizing anything, lock the baseline score. Every technique
# (hybrid, rerank, chunk tuning) must beat THIS number.


@dataclass
class RAGSystem:
    store: VectorStore
    model: Callable[[str], str]

    def answer(self, query: str, k: int = 2) -> dict:
        hits = retrieve(self.store, query, k=k)
        text = generate_with_citations(query, hits, self.model)
        return {
            "answer": text,
            "retrieved": [(c.source, round(s, 4)) for c, s in hits],
        }


def baseline_accuracy(system: RAGSystem, cases: list[tuple[str, str]]) -> float:
    """Fraction of questions whose answer mentions the expected source."""
    hits = 0
    for query, expected_source in cases:
        result = system.answer(query)
        if expected_source in result["answer"]:
            hits += 1
    return hits / len(cases)


# Example 3: measure the baseline
system = RAGSystem(store, stub_model)
acc = baseline_accuracy(
    system,
    [
        ("where is the api key?", "manual.md"),
        ("how much is enterprise?", "pricing.md"),
    ],
)
print("\nExample 3: baseline score")
print(f"  baseline answer-recall: {acc:.0%}")
assert acc >= 0.5, "baseline answers at least one case"

# ============================================================
# Production Pattern
# ============================================================
# The production shape: ingest once at startup, retrieve per query,
# generate with citations, and measure continuously.


def build_rag(documents: dict[str, str]) -> RAGSystem:
    return RAGSystem(ingest(documents), stub_model)


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: optimizing retrieval before the baseline exists
# MISTAKE: no citations - the answer is unverifiable
# MISTAKE: re-ingesting on every query (do it once at startup)
# MISTAKE: assuming retrieval quality without measuring it


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    store = ingest({"a.md": "Apples are red fruits. " * 30, "b.md": "Bananas are yellow. " * 30})
    hits = retrieve(store, "banana yellow", k=1)
    assert any("Bananas" in c.text for c, _ in hits), "banana query finds bananas"

    ans = generate_with_citations("q", [(Chunk("x", "src.md", 0), 0.9)], stub_model)
    assert "Sources: [1](src.md)" in ans, "citation rendered"

    sys2 = RAGSystem(store, stub_model)
    out = sys2.answer("apple")
    assert out["retrieved"], "retrieval recorded"
    assert "Sources:" in out["answer"]

    assert baseline_accuracy(sys2, [("banana", "b.md")]) == 1.0, "easy case answered"
    # a source that is never retrieved can never be cited
    assert baseline_accuracy(sys2, [("banana", "missing.md")]) == 0.0, (
        "an unretrieved source is never claimed"
    )
    print("[OK] 09-rag-baseline: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Baseline pipeline: ingest -> chunk -> embed -> store -> retrieve -> generate.")
        print("2. Cite sources in every answer.")
        print("3. Measure the baseline before you optimize anything.")
        _verify()
