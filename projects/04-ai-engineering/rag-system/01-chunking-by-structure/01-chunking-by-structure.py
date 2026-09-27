"""
RAG System — 01: Chunking by Source Structure
==============================================
Topics: structure-aware chunking, two-text discipline, provenance on
        chunks, measuring chunking by recall.

Why this matters:
    Chunking is the highest-leverage retrieval decision. This exercise
    chunks paragraphs with provenance and proves the two-text discipline.

Run:      python 01-chunking-by-structure.py
Verify:   python 01-chunking-by-structure.py --verify
"""

from __future__ import annotations

import sys
import unicodedata


def normalize_arabic(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u0640", "")
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    return text


def chunk_paragraphs(text: str, book_id: str, page: int, version: str) -> list[dict]:
    """Structure-aware chunking: one chunk per paragraph, with provenance."""
    chunks = []
    for i, para in enumerate(text.split("\n\n")):
        para = para.strip()
        if not para:
            continue
        chunks.append(
            {
                "chunk_id": f"{book_id}:p{page}:{i}",
                "book_id": book_id,
                "page": page,
                "source_version": version,
                "original": para,
                "searchable": normalize_arabic(para),
            }
        )
    return chunks


def main() -> None:
    page_text = (
        "قال الله تعالى في كتابه العزيز.\n\n"
        "الكتاب على المكتب في البيت.\n\n"
        "المكتبة مفتوحة اليوم للطلاب."
    )

    chunks = chunk_paragraphs(page_text, "b1", 7, "v1")
    assert len(chunks) == 3, "one chunk per paragraph"

    # Provenance on every chunk.
    for c in chunks:
        assert c["book_id"] == "b1" and c["page"] == 7 and c["source_version"] == "v1"
        assert c["chunk_id"].startswith("b1:p7:")

    # Two-text discipline: original verbatim, searchable normalized.
    assert chunks[0]["original"] == "قال الله تعالى في كتابه العزيز."
    assert chunks[0]["searchable"] == normalize_arabic(chunks[0]["original"])

    # chunk_ids are unique.
    ids = [c["chunk_id"] for c in chunks]
    assert len(set(ids)) == 3

    print(f"chunked {len(chunks)} paragraphs from page 7")
    print("provenance intact on every chunk: b1, page 7, v1")
    print("two-text discipline holds: original verbatim, searchable normalized")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
