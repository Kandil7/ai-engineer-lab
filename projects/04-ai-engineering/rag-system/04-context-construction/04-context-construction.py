"""
RAG System — 04: Context Construction
======================================
Topics: assembling the context, ordering by relevance, token budget,
        grounding, thin-context detection.

Why this matters:
    The context is what the model actually reads. This exercise assembles
    a ranked, budget-capped context and detects thin contexts.

Run:      python 04-context-construction.py
Verify:   python 04-context-construction.py --verify
"""

from __future__ import annotations

import sys


def build_context(chunks: list[dict], budget_tokens: int) -> list[dict]:
    """Assemble a ranked, budget-capped context from reranked chunks."""
    ranked = sorted(chunks, key=lambda c: c["score"], reverse=True)
    context = []
    used = 0
    for c in ranked:
        cost = len(c["text"].split())
        if used + cost > budget_tokens:
            continue
        context.append(c)
        used += cost
    return context


def is_thin(context: list[dict], query_terms: set[str]) -> bool:
    """Thin if no chunk touches the query's key terms."""
    return not any(any(t in c["text"] for t in query_terms) for c in context)


def main() -> None:
    chunks = [
        {"evidence_id": "b1:p7:0", "text": "الكتاب على المكتب", "score": 0.9},
        {"evidence_id": "b1:p7:1", "text": "المكتبة مفتوحة اليوم", "score": 0.7},
        {"evidence_id": "b1:p8:0", "text": "الكاتب يكتب كتابا", "score": 0.5},
        {"evidence_id": "b1:p8:1", "text": "البيت كبير وواسع", "score": 0.3},
    ]

    # Budget caps the context; highest-scored chunks survive.
    context = build_context(chunks, budget_tokens=6)
    assert context[0]["evidence_id"] == "b1:p7:0", "highest score first"
    assert all(c["score"] >= 0.5 for c in context), "lowest dropped by budget"

    # Grounding material: the context carries original text + evidence ids.
    for c in context:
        assert c["evidence_id"].startswith("b1:p")
        assert c["text"]

    # Thin context detection: a query about an absent topic is thin.
    thin = build_context(chunks, budget_tokens=6)
    assert is_thin(thin, {"السماء"}), "no chunk mentions السماء -> thin"

    # A query the context covers is not thin.
    assert not is_thin(thin, {"الكتاب"}), "الكتاب is in the context"

    print(f"context: {[c['evidence_id'] for c in context]} (budget-capped, ranked)")
    print("thin-context detection: absent topic flagged, present topic not")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
