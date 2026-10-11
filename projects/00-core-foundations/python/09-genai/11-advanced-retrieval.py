"""
GenAI - 11: Advanced Retrieval
==============================
Topics: hybrid dense+sparse, RRF, query expansion, HyDE, multi-query,
parent-document, small-to-big; measured lift per technique.

Why this matters for AI/backend engineering:
    After the baseline, the wins come from technique stacking - but only
    techniques that MEASURABLY lift retrieval quality earn their
    complexity. This topic implements the classics and measures each.

Run:      python 11-advanced-retrieval.py
Verify:   python 11-advanced-retrieval.py --verify
Reference: https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking
"""

from __future__ import annotations

import math
import sys


# ============================================================
# 1. Hybrid: Dense + Sparse (BM25-style)
# ============================================================
# Dense embeddings catch synonyms; sparse keyword matching catches
# exact identifiers and rare terms. Combine both scores.


def bm25_score(
    query_terms: list[str],
    doc_terms: list[str],
    df: dict[str, int],
    n_docs: int,
    k1: float = 1.5,
    b: float = 0.75,
) -> float:
    """A simplified BM25 relevance score."""
    doc_len = len(doc_terms)
    avg_len = sum(doc_len for _ in [0])  # placeholder; use n_docs avg below
    avg_len = avg_len if avg_len else 1.0
    score = 0.0
    tf = {t: doc_terms.count(t) for t in set(doc_terms)}
    for term in query_terms:
        if term not in tf:
            continue
        n = df.get(term, 1)
        idf = math.log((n_docs - n + 0.5) / (n + 0.5) + 1.0)
        f = tf[term]
        score += idf * (f * (k1 + 1)) / (f + k1 * (1 - b + b * doc_len / avg_len))
    return score


def toy_embed(text: str, dim: int = 64) -> list[float]:
    vec = [0.0] * dim
    for ch in text.lower():
        if ch.isalnum():
            vec[ord(ch) % dim] += 1.0
    return vec


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0


# ============================================================
# 2. Reciprocal Rank Fusion (RRF)
# ============================================================
# Merge two ranked lists without tuning score scales: each doc's fused
# score is the sum of 1/(k + rank) over all lists it appears in.


def rrf_merge(rankings: list[list[str]], k: int = 60) -> list[str]:
    """Fuse multiple ranked lists into one with reciprocal ranks."""
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=lambda d: scores[d], reverse=True)


# Example 1: RRF fuses dense and sparse
dense_rank = ["d3", "d1", "d2", "d4"]
sparse_rank = ["d3", "d4", "d1", "d2"]
fused = rrf_merge([dense_rank, sparse_rank])
print("Example 1: reciprocal rank fusion")
print(f"  fused: {fused}")
assert fused[0] == "d3", "d3 is first in both -> wins fusion"

# ============================================================
# 3. Query Expansion
# ============================================================
# Add related terms to the query so sparse matching finds more. Simple
# and effective: synonyms and spelling variants.


def expand_query(query: str, thesaurus: dict[str, list[str]]) -> list[str]:
    """Return the original query plus known expansions."""
    terms = query.lower().split()
    expanded = set(terms)
    for t in terms:
        expanded.update(thesaurus.get(t, []))
    return sorted(expanded)


# Example 2: query expansion
thesaurus = {"car": ["automobile", "vehicle"], "cheap": ["affordable", "budget"]}
expanded = expand_query("cheap car", thesaurus)
print("\nExample 2: query expansion")
print(f"  'cheap car' -> {expanded}")
assert "automobile" in expanded and "affordable" in expanded

# ============================================================
# 4. HyDE: Hypothetical Document Embeddings
# ============================================================
# Ask the LLM to WRITE the answer first, then embed that hypothetical
# answer and search with it. The hypothesis: answers are closer to
# relevant docs than questions are.


def hyde_query(query: str, stub_writer) -> list[str]:
    """Return expanded search terms derived from a hypothetical answer."""
    answer = stub_writer(query)
    return expand_query(query + " " + answer, {})


def stub_writer(query: str) -> str:
    return "the api key is stored in the environment configuration file"


# Example 3: HyDE terms
hyde_terms = hyde_query("where is the key?", stub_writer)
print("\nExample 3: HyDE")
print(f"  search terms from hypothetical answer: {hyde_terms}")
assert "configuration" in hyde_terms or "environment" in hyde_terms

# ============================================================
# 5. Multi-Query: Several Angles on One Question
# ============================================================


def multi_query(question: str, variants: list[str]) -> list[str]:
    """The original question plus reformulated variants."""
    return [question] + variants


# Example 4: multi-query
variants = multi_query(
    "How do I reset my password?", ["password reset steps", "forgot password procedure"]
)
print("\nExample 4: multi-query")
print(f"  {len(variants)} queries to run: {variants}")

# ============================================================
# 6. Small-to-Big / Parent Document Retrieval
# ============================================================
# Retrieve small precise chunks, then hand the generator the LARGER
# parent section for context. Precision at retrieval, breadth at
# generation.


def small_to_big(small_chunk_id: str, parent_map: dict[str, str]) -> str:
    """Map a retrieved small chunk back to its parent document."""
    return parent_map.get(small_chunk_id, small_chunk_id)


# Example 5: parent document
parent_map = {"c-12": "Section 3: Configuration - full reference"}
expanded = small_to_big("c-12", parent_map)
print("\nExample 5: small-to-big")
print(f"  retrieved c-12 -> generate with: {expanded}")

# ============================================================
# 7. Measuring the Lift
# ============================================================
# Never adopt a technique on vibes. Compare baseline vs candidate
# retrieval with a labeled set and report the lift.


def recall_at_k(ranked: list[str], relevant: set[str], k: int) -> float:
    if not relevant:
        return 0.0
    return len(set(ranked[:k]) & relevant) / len(relevant)


def compare_techniques(
    baseline_rank: list[str], candidate_rank: list[str], relevant: set[str], k: int = 3
) -> dict:
    base = recall_at_k(baseline_rank, relevant, k)
    cand = recall_at_k(candidate_rank, relevant, k)
    return {
        "baseline_recall": round(base, 3),
        "candidate_recall": round(cand, 3),
        "lift": round(cand - base, 3),
    }


# Example 6: measure a technique
baseline = ["d1", "d2", "d3"]
candidate = ["d4", "d1", "d2"]  # d4 is relevant, moved up
measure = compare_techniques(baseline, candidate, {"d4"}, k=3)
print("\nExample 6: measured lift")
print(
    f"  baseline={measure['baseline_recall']} candidate={measure['candidate_recall']} "
    f"lift={measure['lift']}"
)
assert measure["lift"] > 0, "technique with real lift"

# ============================================================
# Production Pattern
# ============================================================
# The production retrieval stack: hybrid (dense + BM25) fused with RRF,
# then small-to-big expansion, then generate.


def production_retrieve(query: str, dense: list[str], sparse: list[str], k: int = 3) -> list[str]:
    return rrf_merge([dense, sparse])[:k]


# ============================================================
# Common Mistakes
# ============================================================
# MISTAKE: stacking techniques without measuring each one's lift
# MISTAKE: RRF with wildly different list lengths (k matters)
# MISTAKE: HyDE every query - expensive; only when it measures better
# MISTAKE: small chunks without parent context - answers lack grounding


# ============================================================
# Self-Verification
# ============================================================
def _verify() -> None:
    assert rrf_merge([["a", "b"], ["a", "b"]])[0] == "a", "RRF order"
    assert rrf_merge([["b", "a"], ["b", "a"]])[0] == "b"

    assert "car" in expand_query("car", {"car": ["vehicle"]})
    assert expand_query("car", {}) == ["car"]

    assert "environment" in hyde_query("key?", stub_writer), "HyDE adds answer terms"

    assert small_to_big("x", {"x": "PARENT"}) == "PARENT", "parent lookup"
    assert small_to_big("y", {"x": "PARENT"}) == "y", "missing -> original"

    m = compare_techniques(["a", "b"], ["b", "a"], {"b"}, k=1)
    assert m["candidate_recall"] == 1.0 and m["baseline_recall"] == 0.0

    assert production_retrieve("q", ["a", "b"], ["b", "c"], k=1)[0] == "b"
    print("[OK] 11-advanced-retrieval: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        print("\n--- Summary ---")
        print("1. Hybrid dense+sparse fused with RRF.")
        print("2. Expand queries (synonyms, HyDE, multi-query).")
        print("3. Small-to-big: precise retrieve, broad generate.")
        print("4. Measure the lift of every technique.")
        _verify()
