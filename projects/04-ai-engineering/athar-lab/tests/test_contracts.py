"""Tests for the Athar learning contracts and CLI.

The exit test for stage 1: no passage ever loses book_id or page, Arabic
survives the round trip, and the two-text discipline holds (original is
verbatim, searchable is normalized).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from contracts import (  # noqa: E402
    Passage,
    SourceLocation,
    make_passage,
    normalize_arabic,
)

SAMPLE = "قالَ اللهُ تعالى في كتابه العزيز"


def test_normalize_strips_diacritics() -> None:
    assert normalize_arabic("كَتَبَ") == "كتب"


def test_normalize_unifies_hamza() -> None:
    assert normalize_arabic("أَلْكِتَابُ") == "الكتاب"


def test_source_location_rejects_empty_book_id() -> None:
    with pytest.raises(ValueError):
        SourceLocation(book_id="", page=1, source_version="v1")


def test_source_location_rejects_page_zero() -> None:
    with pytest.raises(ValueError):
        SourceLocation(book_id="b1", page=0, source_version="v1")


def test_passage_keeps_original_verbatim() -> None:
    p = make_passage("b1", 1, SAMPLE, "v1", 0)
    assert p.original == SAMPLE  # diacritics preserved for citation
    assert p.searchable == normalize_arabic(SAMPLE)  # normalized for search


def test_passage_jsonl_has_book_id_and_page() -> None:
    p = make_passage("b1", 7, "نص عربي", "v1", 0)
    row = p.to_jsonl()
    assert row["book_id"] == "b1"
    assert row["page"] == 7
    assert row["source_version"] == "v1"
    assert row["passage_id"] == "b1:p7:0"


def test_passage_id_is_unique_per_page_index() -> None:
    a = make_passage("b1", 1, "نص", "v1", 0)
    b = make_passage("b1", 1, "نص", "v1", 1)
    assert a.passage_id != b.passage_id


def test_arabic_survives_json_round_trip() -> None:
    p = make_passage("b1", 1, SAMPLE, "v1", 0)
    row = json.dumps(p.to_jsonl(), ensure_ascii=False)
    back = json.loads(row)
    assert back["original"] == SAMPLE


def test_cli_emits_rows_without_losing_ids(tmp_path: Path) -> None:
    pages = tmp_path / "pages"
    pages.mkdir()
    for i in range(1, 11):
        (pages / f"book_p{i}.txt").write_text(
            f"صفحة رقم {i} من الكتاب", encoding="utf-8"
        )

    out = tmp_path / "out.jsonl"
    from cli import emit_jsonl

    n = emit_jsonl(pages, "b1", "v1", out)
    assert n == 10

    rows = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 10
    for row in rows:
        assert row["book_id"] == "b1"
        assert row["page"] >= 1
        assert "صفحة" in row["original"]  # Arabic intact


def test_cli_is_idempotent(tmp_path: Path) -> None:
    pages = tmp_path / "pages"
    pages.mkdir()
    for i in range(1, 4):
        (pages / f"p{i}.txt").write_text(f"نص الصفحة {i}", encoding="utf-8")

    out = tmp_path / "out.jsonl"
    from cli import emit_jsonl

    emit_jsonl(pages, "b1", "v1", out)
    first = out.read_text(encoding="utf-8")
    emit_jsonl(pages, "b1", "v1", out)
    assert out.read_text(encoding="utf-8") == first  # deterministic output


def test_cli_rejects_unparseable_filename(tmp_path: Path) -> None:
    pages = tmp_path / "pages"
    pages.mkdir()
    (pages / "no_number.txt").write_text("نص", encoding="utf-8")

    from cli import read_pages

    with pytest.raises(ValueError):
        read_pages(pages)
