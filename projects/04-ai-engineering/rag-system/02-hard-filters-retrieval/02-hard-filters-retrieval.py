"""
RAG System — 02: Hard Filters and Retrieval
============================================
Topics: filter types, pre- vs post-filtering, tenant isolation, and the
        no-leak test.

Why this matters:
    Hard filters are correctness tools first. This exercise builds a
    filtered retriever and proves tenant isolation holds.

Run:      python 02-hard-filters-retrieval.py
Verify:   python 02-hard-filters-retrieval.py --verify
"""

from __future__ import annotations

import sys


def search(chunks: list[dict], query: str, tenant: str, k: int = 3) -> list[dict]:
    """Pre-filtered search: tenant filter applied before ranking."""
    eligible = [c for c in chunks if c["tenant"] == tenant]
    # Simple lexical ranking: count query-token overlap.
    q_tokens = set(query.split())
    ranked = sorted(
        eligible, key=lambda c: len(q_tokens & set(c["text"].split())), reverse=True
    )
    return ranked[:k]


def main() -> None:
    chunks = [
        {"chunk_id": "t1:1", "tenant": "t1", "text": "الكتاب على المكتب"},
        {"chunk_id": "t1:2", "tenant": "t1", "text": "المكتبة مفتوحة"},
        {"chunk_id": "t2:1", "tenant": "t2", "text": "الكتاب في بيت آخر"},
        {"chunk_id": "t2:2", "tenant": "t2", "text": "بيانات سرية للطرف الثاني"},
    ]

    # Tenant isolation: t1 query never returns t2 data.
    results = search(chunks, "الكتاب", tenant="t1")
    assert all(r["tenant"] == "t1" for r in results), "no cross-tenant leak"
    assert len(results) == 2

    # The t2 secret is unreachable from t1.
    assert all("سرية" not in r["text"] for r in results)

    # Same query from t2 returns only t2 data.
    results_t2 = search(chunks, "الكتاب", tenant="t2")
    assert all(r["tenant"] == "t2" for r in results_t2)

    print(f"t1 search returned {len(results)} chunks, all tenant t1")
    print("t2 secret unreachable from t1: isolation holds")
    print("same query from t2 returns only t2 data")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
