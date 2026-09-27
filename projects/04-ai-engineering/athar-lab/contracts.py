"""Athar learning contracts: Document, Passage, SourceLocation.

The first building block of the Athar roadmap. These contracts enforce the
two-text discipline from the start: every passage keeps its verbatim
original for display and citation, plus a normalized searchable form for
matching. book_id and page are mandatory on every passage — losing either
is a correctness bug, not a cosmetic one.

Deliberately stdlib-only (dataclasses) so the learning copy has zero
dependency friction. The real Athar-Lab ingestion models are deeper and
Shamela-specific; this is the portable learning abstraction.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field
from typing import Optional


def normalize_arabic(text: str) -> str:
    """Normalize Arabic for the searchable text: strip diacritics, unify
    hamza, remove tatweel. Never applied to the original."""
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u0640", "")
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    text = text.replace("ؤ", "و").replace("ئ", "ي")
    return text


@dataclass(frozen=True)
class SourceLocation:
    """Where a passage physically lives in the source corpus."""

    book_id: str
    page: int
    source_version: str
    path: Optional[str] = None  # original file path, for provenance

    def __post_init__(self) -> None:
        if not self.book_id:
            raise ValueError("book_id must not be empty")
        if self.page < 1:
            raise ValueError(f"page must be >= 1, got {self.page}")


@dataclass(frozen=True)
class Document:
    """A source document: one book (or one file) with stable identity."""

    book_id: str
    title: str
    source_version: str
    author: Optional[str] = None


@dataclass(frozen=True)
class Passage:
    """One retrievable unit of text, with provenance and both texts."""

    passage_id: str
    location: SourceLocation
    original: str  # verbatim, for display and citation — never normalized
    searchable: str  # normalized, for indexing and matching
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.passage_id:
            raise ValueError("passage_id must not be empty")
        if not self.original.strip():
            raise ValueError("original text must not be empty")
        if not self.searchable.strip():
            raise ValueError("searchable text must not be empty")

    def to_jsonl(self) -> dict:
        """The JSONL row. book_id and page are guaranteed present."""
        return {
            "passage_id": self.passage_id,
            "book_id": self.location.book_id,
            "page": self.location.page,
            "source_version": self.location.source_version,
            "original": self.original,
            "searchable": self.searchable,
            "metadata": self.metadata,
        }


def make_passage(
    book_id: str,
    page: int,
    text: str,
    source_version: str,
    passage_index: int,
    path: Optional[str] = None,
) -> Passage:
    """Build a Passage from raw page text, applying the two-text discipline."""
    original = text.strip()
    return Passage(
        passage_id=f"{book_id}:p{page}:{passage_index}",
        location=SourceLocation(
            book_id=book_id,
            page=page,
            source_version=source_version,
            path=path,
        ),
        original=original,
        searchable=normalize_arabic(original),
    )
