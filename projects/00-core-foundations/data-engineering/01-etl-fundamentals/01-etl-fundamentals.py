"""
Data Engineering — 01: ETL Fundamentals
========================================
Topics: extract/transform/load decomposition, determinism, idempotency,
        per-stage observability.

Why this matters:
    Every data pipeline is ETL. This exercise builds a minimal raw-pages to
    passages pipeline and proves determinism and idempotency with asserts.

Run:      python 01-etl-fundamentals.py
Verify:   python 01-etl-fundamentals.py --verify
"""

from __future__ import annotations

import json
import sys
import unicodedata
from pathlib import Path


def normalize_arabic(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u0640", "")
    text = text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
    return text


def extract(pages_dir: Path) -> list[tuple[int, str]]:
    """Read-only extract: page number + raw text, sorted by page."""
    pages = []
    for f in sorted(pages_dir.glob("*.txt")):
        page = int(f.stem.split("_")[-1])
        pages.append((page, f.read_text(encoding="utf-8")))
    return sorted(pages)


def transform(pages: list[tuple[int, str]], book_id: str) -> list[dict]:
    """Pure transform: build passage rows with the two-text discipline."""
    rows = []
    for page, text in pages:
        original = text.strip()
        rows.append(
            {
                "book_id": book_id,
                "page": page,
                "original": original,
                "searchable": normalize_arabic(original),
            }
        )
    return rows


def load(rows: list[dict], out_path: Path) -> int:
    """Idempotent load: deterministic JSONL output."""
    with out_path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return len(rows)


def main() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        pages_dir = Path(tmp) / "pages"
        pages_dir.mkdir()
        for i in range(1, 4):
            (pages_dir / f"book_p{i}.txt").write_text(
                f"صفحة رقم {i} من الكتاب", encoding="utf-8"
            )

        out = Path(tmp) / "out.jsonl"
        raw = extract(pages_dir)
        rows = transform(raw, "b1")
        n1 = load(rows, out)
        first = out.read_text(encoding="utf-8")
        n2 = load(rows, out)  # re-run
        second = out.read_text(encoding="utf-8")

        assert n1 == n2 == 3
        assert first == second, "deterministic + idempotent: identical output"
        assert all(r["book_id"] == "b1" and r["page"] >= 1 for r in rows)
        assert all("صفحة" in r["original"] for r in rows)
        print(f"extract={len(raw)} transform={len(rows)} load={n1}")
        print("deterministic re-run: identical output")
        print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
