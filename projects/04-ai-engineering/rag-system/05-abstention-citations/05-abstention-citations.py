"""
RAG System — 05: Abstention and Citations
==========================================
Topics: abstention on thin context, citation-required answers, rejecting
        fabricated citations.

Why this matters:
    A RAG answer is only as trustworthy as its evidence. This exercise
    implements abstention and citation validation — the roadmap's exit
    test.

Run:      python 05-abstention-citations.py
Verify:   python 05-abstention-citations.py --verify
"""

from __future__ import annotations

import sys


def validate_citations(cited: list[str], context_ids: set[str]) -> bool:
    """Every cited id must be in the context. Rejects fabricated ids."""
    return all(c in context_ids for c in cited)


def generate(query: str, context: list[dict]) -> dict:
    """A stub generator: answers only from the context, cites evidence,
    abstains when the context cannot support an answer."""
    context_ids = {c["evidence_id"] for c in context}
    hits = [c for c in context if any(t in c["text"] for t in query.split())]
    if not hits:
        return {"abstained": True, "answer": None, "citations": []}
    return {
        "abstained": False,
        "answer": hits[0]["text"],
        "citations": [hits[0]["evidence_id"]],
    }


def main() -> None:
    context = [
        {"evidence_id": "b1:p7:0", "text": "الكتاب على المكتب"},
        {"evidence_id": "b1:p7:1", "text": "المكتبة مفتوحة اليوم"},
    ]
    context_ids = {c["evidence_id"] for c in context}

    # Abstention: no evidence for the query -> refuses, does not guess.
    answer = generate("ما لون السماء", context)
    assert answer["abstained"], "abstains when evidence is absent"
    assert answer["answer"] is None

    # Grounded answer: cites a real evidence id.
    grounded = generate("الكتاب", context)
    assert not grounded["abstained"]
    assert validate_citations(grounded["citations"], context_ids)

    # Fabricated citation: rejected by backend validation.
    fabricated = ["b9:p99:0"]
    assert not validate_citations(fabricated, context_ids), (
        "fabricated citation id rejected"
    )

    print("abstention: no evidence -> refuses to answer")
    print("grounded answer cites a real evidence id")
    print("fabricated citation id rejected by backend validation")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
