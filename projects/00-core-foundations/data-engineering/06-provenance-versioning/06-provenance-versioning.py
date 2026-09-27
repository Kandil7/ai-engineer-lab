"""
Data Engineering — 06: Provenance and Versioning
=================================================
Topics: provenance fields, source versioning, tracing to origin, stale
        passage detection.

Why this matters:
    Provenance answers "where did this come from?" and versioning answers
    "which version produced this?" Together they make every passage
    traceable — the roadmap's exit test.

Run:      python 06-provenance-versioning.py
Verify:   python 06-provenance-versioning.py --verify
"""

from __future__ import annotations

import sys


class Source:
    """A versioned source snapshot."""

    def __init__(self, book_id: str, version: str, pages: dict[int, str]) -> None:
        self.book_id = book_id
        self.version = version
        self.pages = pages

    def locate(self, page: int) -> str:
        if page not in self.pages:
            raise KeyError(f"page {page} not in {self.book_id} {self.version}")
        return self.pages[page]


def trace(passage: dict, sources: dict[str, dict[str, Source]]) -> str:
    """Passage -> origin lookup. Fails loudly, never guesses."""
    book = sources.get(passage["book_id"])
    if book is None:
        raise KeyError(f"unknown book {passage['book_id']}")
    src = book.get(passage["source_version"])
    if src is None:
        raise KeyError(f"unknown version {passage['source_version']}")
    return src.locate(passage["page"])


def is_stale(passage: dict, current: dict[str, str]) -> bool:
    """True if the passage's source version is not the current one."""
    return current.get(passage["book_id"]) != passage["source_version"]


def main() -> None:
    v1 = Source("b1", "v1", {1: "نص الصفحة الأولى", 2: "نص الصفحة الثانية"})
    v2 = Source("b1", "v2", {1: "نص الصفحة الأولى معدل", 2: "نص الصفحة الثانية"})
    sources = {"b1": {"v1": v1, "v2": v2}}

    passage = {"book_id": "b1", "page": 1, "source_version": "v1"}
    origin = trace(passage, sources)
    assert origin == "نص الصفحة الأولى", "traced to the exact source page"

    # Stale detection: source moved to v2, passage still says v1.
    current = {"b1": "v2"}
    assert is_stale(passage, current), "passage is stale after source update"
    fresh = {"book_id": "b1", "page": 1, "source_version": "v2"}
    assert not is_stale(fresh, current), "fresh passage is not stale"

    # Tracing fails loudly on a missing link.
    broken = {"book_id": "b1", "page": 1, "source_version": "v9"}
    try:
        trace(broken, sources)
        raise AssertionError("expected KeyError")
    except KeyError:
        pass

    print(f"trace: page 1 of b1 v1 -> '{origin}'")
    print("stale detection: v1 passage flagged after source moved to v2")
    print("missing version fails loudly, no guess returned")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
