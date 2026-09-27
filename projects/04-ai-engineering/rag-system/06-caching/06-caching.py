"""
RAG System — 06: Caching
=========================
Topics: cache keys with versions, semantic caching, invalidation, and the
        never-cache-bad-answers rule.

Why this matters:
    Caching is where RAG cost and latency are won. This exercise builds a
    version-keyed cache and proves stale answers are never served.

Run:      python 06-caching.py
Verify:   python 06-caching.py --verify
"""

from __future__ import annotations

import sys


class AnswerCache:
    """A version-keyed answer cache with validate-before-cache."""

    def __init__(self) -> None:
        self._entries: dict[tuple, dict] = {}

    def key(self, query: str, prompt_version: str, corpus_version: str) -> tuple:
        return (query.strip(), prompt_version, corpus_version)

    def get(self, query: str, prompt_version: str, corpus_version: str) -> dict | None:
        return self._entries.get(self.key(query, prompt_version, corpus_version))

    def put(
        self, query: str, prompt_version: str, corpus_version: str, answer: dict
    ) -> None:
        # Never cache abstained or malformed answers.
        if answer.get("abstained") or not answer.get("answer"):
            return
        self._entries[self.key(query, prompt_version, corpus_version)] = answer


def main() -> None:
    cache = AnswerCache()
    good = {"answer": "الكتاب على المكتب", "citations": ["b1:p7:0"]}
    abstained = {"abstained": True, "answer": None, "citations": []}

    # Cache a good answer under v1.
    cache.put("الكتاب", "prompt_v1", "corpus_v1", good)
    assert cache.get("الكتاب", "prompt_v1", "corpus_v1") == good

    # Abstained answers are never cached.
    cache.put("ما لون السماء", "prompt_v1", "corpus_v1", abstained)
    assert cache.get("ما لون السماء", "prompt_v1", "corpus_v1") is None

    # Corpus change invalidates: v2 misses the v1 entry.
    assert cache.get("الكتاب", "prompt_v1", "corpus_v2") is None, (
        "corpus change invalidates the cache"
    )

    # Prompt change invalidates too.
    assert cache.get("الكتاب", "prompt_v2", "corpus_v1") is None

    print("good answer cached under (query, prompt_v1, corpus_v1)")
    print("abstained answer never cached")
    print("corpus or prompt change invalidates: stale answers never served")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
