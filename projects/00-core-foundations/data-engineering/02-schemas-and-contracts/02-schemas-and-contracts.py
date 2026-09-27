"""
Data Engineering — 02: Schemas and Contracts
=============================================
Topics: schema design, boundary validation, structural invariants,
        schema evolution.

Why this matters:
    A schema is the contract between a pipeline and its consumers. This
    exercise builds the Document/Passage/SourceLocation contracts and
    proves the invariants are structural — invalid data cannot exist.

Run:      python 02-schemas-and-contracts.py
Verify:   python 02-schemas-and-contracts.py --verify
"""

from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class SourceLocation:
    book_id: str
    page: int
    source_version: str

    def __post_init__(self) -> None:
        if not self.book_id:
            raise ValueError("book_id must not be empty")
        if self.page < 1:
            raise ValueError(f"page must be >= 1, got {self.page}")


@dataclass(frozen=True)
class Passage:
    passage_id: str
    location: SourceLocation
    original: str
    searchable: str

    def __post_init__(self) -> None:
        if not self.passage_id:
            raise ValueError("passage_id must not be empty")
        if not self.original.strip():
            raise ValueError("original must not be empty")
        if not self.searchable.strip():
            raise ValueError("searchable must not be empty")


def main() -> None:
    # Valid construction works.
    loc = SourceLocation("b1", 7, "v1")
    p = Passage("b1:p7:0", loc, "نص عربي", "نص عربي")
    assert p.location.book_id == "b1" and p.location.page == 7

    # Structural invariants: invalid states cannot be constructed.
    for bad in (
        lambda: SourceLocation("", 1, "v1"),
        lambda: SourceLocation("b1", 0, "v1"),
        lambda: Passage("", loc, "نص", "نص"),
        lambda: Passage("x", loc, "   ", "نص"),
    ):
        try:
            bad()
            raise AssertionError("expected ValueError")
        except ValueError:
            pass

    # Schema evolution: additive field is backward-compatible.
    @dataclass(frozen=True)
    class SourceLocationV2(SourceLocation):
        path: str | None = None

    loc2 = SourceLocationV2("b1", 7, "v2", path="book_p7.txt")
    assert loc2.path == "book_p7.txt"
    assert loc2.book_id == "b1"  # old fields still work

    print("structural invariants hold: invalid data cannot be constructed")
    print("additive schema evolution is backward-compatible")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
