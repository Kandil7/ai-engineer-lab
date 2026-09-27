"""Athar learning CLI: read Arabic page files, emit JSONL.

Stage-1 exit test: reads a directory of Arabic text pages, emits one JSONL
row per passage with book_id and page guaranteed, and never loses Arabic.

Usage:
    python cli.py <pages_dir> <book_id> <source_version> -o out.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

from contracts import make_passage  # noqa: E402


def read_pages(pages_dir: Path) -> list[tuple[int, str]]:
    """Read *.txt page files, returning (page_number, text) sorted by page.

    Filename convention: <anything>_<page>.txt or <page>.txt. The page
    number is parsed from the trailing integer before the extension.
    """
    pages: list[tuple[int, str]] = []
    for f in sorted(pages_dir.glob("*.txt")):
        m = re.search(r"(\d+)\s*$", f.stem)
        if m is None:
            raise ValueError(f"cannot parse page number from filename: {f.name}")
        page = int(m.group(1))
        text = f.read_text(encoding="utf-8")
        pages.append((page, text))
    pages.sort(key=lambda p: p[0])
    return pages


def emit_jsonl(
    pages_dir: Path,
    book_id: str,
    source_version: str,
    out_path: Path,
) -> int:
    pages = read_pages(pages_dir)
    rows = []
    for page, text in pages:
        passage = make_passage(
            book_id=book_id,
            page=page,
            text=text,
            source_version=source_version,
            passage_index=0,
            path=str(pages_dir / f"{page}.txt"),
        )
        rows.append(passage.to_jsonl())

    with out_path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Emit Athar passages as JSONL")
    parser.add_argument("pages_dir", type=Path)
    parser.add_argument("book_id", type=str)
    parser.add_argument("source_version", type=str)
    parser.add_argument("-o", "--out", type=Path, default=Path("out.jsonl"))
    args = parser.parse_args()

    n = emit_jsonl(args.pages_dir, args.book_id, args.source_version, args.out)
    print(f"wrote {n} passages to {args.out}")


if __name__ == "__main__":
    main()
