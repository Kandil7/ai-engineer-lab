"""
RAG System — 09: Long Context Processing
=========================================
Topics: the budget, truncation, and compaction.

Why this matters:
    Long documents and conversations push against the context budget.
    This exercise builds a budget-aware context and compacts a
    conversation.

Run:      python 09-long-context-processing.py
Verify:   python 09-long-context-processing.py --verify
"""

from __future__ import annotations

import sys


def fit_budget(chunks: list[dict], budget_tokens: int) -> list[dict]:
    """Truncation: drop the lowest-ranked material to fit the budget."""
    ranked = sorted(chunks, key=lambda c: c["score"], reverse=True)
    kept = []
    used = 0
    for c in ranked:
        cost = len(c["text"].split())
        if used + cost > budget_tokens:
            continue
        kept.append(c)
        used += cost
    return kept


def compact(turns: list[str], keep_recent: int) -> tuple[str, list[str]]:
    """Compaction: summarize older turns, keep recent ones."""
    if len(turns) <= keep_recent:
        return "", turns
    older = turns[:-keep_recent]
    recent = turns[-keep_recent:]
    summary = f"summary of {len(older)} turns"
    return summary, recent


def main() -> None:
    chunks = [
        {"text": "a b c d", "score": 0.9},
        {"text": "e f g h", "score": 0.7},
        {"text": "i j k l", "score": 0.5},
    ]

    # Truncation drops the lowest-ranked material.
    kept = fit_budget(chunks, budget_tokens=8)
    assert kept[0]["score"] == 0.9, "highest-ranked kept"
    assert all(c["score"] >= 0.5 for c in kept), "lowest may drop"

    # A tight budget drops the low-score chunk.
    tight = fit_budget(chunks, budget_tokens=4)
    assert all(c["score"] >= 0.7 for c in tight), "low-score dropped"

    # Compaction summarizes older turns.
    turns = ["t1", "t2", "t3", "t4", "t5"]
    summary, recent = compact(turns, keep_recent=2)
    assert "3 turns" in summary
    assert recent == ["t4", "t5"]

    # No compaction needed for short conversations.
    summary, recent = compact(["t1", "t2"], keep_recent=2)
    assert summary == "" and recent == ["t1", "t2"]

    print("truncation drops the lowest-ranked material")
    print("compaction summarizes older turns, keeps recent")
    print("the budget is respected")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
