"""
Fine-Tuning — 06: RAG vs Fine-Tuning
=====================================
Topics: the knowledge/behavior split and the hybrid decision.

Why this matters:
    RAG and fine-tuning solve different problems. This exercise classifies
    a problem to the right tool and records the decision.

Run:      python 06-rag-vs-fine-tuning.py
Verify:   python 06-rag-vs-fine-tuning.py --verify
"""

from __future__ import annotations

import sys


def choose_tool(problem: dict) -> str:
    """Knowledge problems go to RAG; behavior problems go to fine-tuning."""
    if problem["kind"] == "knowledge":
        return "rag"
    if problem["kind"] == "behavior":
        return "fine-tuning"
    return "hybrid"


def main() -> None:
    # Knowledge: the corpus changes and answers must cite sources.
    facts = {"kind": "knowledge", "changes": True, "cites": True}
    assert choose_tool(facts) == "rag"

    # Behavior: a stable format the model must follow.
    format_task = {"kind": "behavior", "stable": True}
    assert choose_tool(format_task) == "fine-tuning"

    # Hybrid: facts from retrieval, citation behavior from fine-tuning.
    hybrid = {"kind": "hybrid", "facts": "rag", "behavior": "fine-tuning"}
    assert choose_tool(hybrid) == "hybrid"

    # The decision is recorded as an ADR, not left implicit.
    adr = {
        "problem": "answer Islamic-text questions with citations",
        "decision": "RAG for knowledge, fine-tuning for citation behavior",
        "rationale": "corpus changes; answers must cite; format is stable",
    }
    assert adr["decision"] and adr["rationale"]

    print("knowledge problem -> RAG (changing corpus, citations required)")
    print("behavior problem -> fine-tuning (stable format)")
    print("hybrid: RAG for facts, fine-tuning for citation behavior")
    print("decision recorded as an ADR with rationale")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
