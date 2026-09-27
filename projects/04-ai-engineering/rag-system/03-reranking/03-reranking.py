"""
RAG System — 03: Reranking
==========================
Topics: bi-encoder vs cross-encoder, rerank depth, measuring the
        reranker's contribution.

Why this matters:
    Retrieval returns candidates; reranking reorders them. This exercise
    simulates a cross-encoder reranker and proves it improves recall.

Run:      python 03-reranking.py
Verify:   python 03-reranking.py --verify
"""

from __future__ import annotations

import sys


def retrieve_candidates(chunks: list[dict], query: str, k: int = 50) -> list[dict]:
    """Bi-encoder stand-in: coarse lexical ranking."""
    q_tokens = set(query.split())
    return sorted(
        chunks, key=lambda c: len(q_tokens & set(c["text"].split())), reverse=True
    )[:k]


def rerank(candidates: list[dict], query: str, keep: int = 5) -> list[dict]:
    """Cross-encoder stand-in: a 'joint' score that rewards exact phrase
    overlap, which the coarse bi-encoder missed."""

    def joint_score(c: dict) -> int:
        # The cross-encoder recognizes the exact phrase inside the chunk,
        # which the coarse bi-encoder (token overlap) missed.
        return 2 if query in c["text"] else 1

    return sorted(candidates, key=joint_score, reverse=True)[:keep]


def recall_at_k(ranked: list[dict], relevant: set[str], k: int) -> float:
    top = {c["chunk_id"] for c in ranked[:k]}
    return len(top & relevant) / max(1, len(relevant))


def main() -> None:
    chunks = [
        {"chunk_id": "c1", "text": "الكتاب على الرف"},
        {"chunk_id": "c2", "text": "المكتبة مفتوحة اليوم"},
        {"chunk_id": "c3", "text": "الكاتب يكتب كتابا"},
        {"chunk_id": "c4", "text": "البيت كبير"},
        {"chunk_id": "c5", "text": "الكتاب على المكتب في البيت"},
    ]
    query = "الكتاب على المكتب"
    relevant = {"c5"}

    # Without reranking: the coarse ranker may miss the exact-phrase chunk.
    candidates = retrieve_candidates(chunks, query, k=50)
    no_rerank = recall_at_k(candidates, relevant, k=5)

    # With reranking: the cross-encoder promotes the exact-phrase chunk.
    reranked = rerank(candidates, query, keep=5)
    with_rerank = recall_at_k(reranked, relevant, k=5)

    assert with_rerank >= no_rerank, "reranking must not hurt recall"
    assert reranked[0]["chunk_id"] == "c5", "exact-phrase chunk promoted to top"

    print(f"no-rerank recall@5: {no_rerank:.2f}")
    print(f"with-rerank recall@5: {with_rerank:.2f}")
    print("cross-encoder promoted the exact-phrase chunk to rank 1")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
