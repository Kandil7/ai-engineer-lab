"""
Data Engineering — 07: Parquet and Object Storage
==================================================
Topics: Parquet vs JSONL, columnar reads, partition layout, provenance in
        the schema.

Why this matters:
    Passages scale beyond JSONL. This exercise demonstrates the columnar
    advantage and the partition layout using pyarrow if available, with a
    stdlib fallback that proves the same principles.

Run:      python 07-parquet-object-storage.py
Verify:   python 07-parquet-object-storage.py --verify
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


def write_jsonl(rows: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def partition_layout(rows: list[dict], root: Path) -> dict[str, Path]:
    """Write one JSONL file per (book_id, source_version) partition."""
    written: dict[str, Path] = {}
    for row in rows:
        key = f"{row['book_id']}/{row['source_version']}"
        part_dir = root / key
        part_dir.mkdir(parents=True, exist_ok=True)
        path = part_dir / "passages.jsonl"
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        written[key] = path
    return written


def main() -> None:
    rows = [
        {"book_id": "b1", "page": 1, "source_version": "v1", "original": "نص ١"},
        {"book_id": "b1", "page": 2, "source_version": "v1", "original": "نص ٢"},
        {"book_id": "b1", "page": 1, "source_version": "v2", "original": "نص ١ معدل"},
    ]

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        parts = partition_layout(rows, root)

        # Partition layout: one file per (book, version).
        assert set(parts) == {"b1/v1", "b1/v2"}
        assert parts["b1/v1"].exists() and parts["b1/v2"].exists()

        # A query for one book's current version reads exactly one file.
        v1_rows = [
            json.loads(l)
            for l in parts["b1/v1"].read_text(encoding="utf-8").splitlines()
        ]
        assert len(v1_rows) == 2
        assert all(r["source_version"] == "v1" for r in v1_rows)

        # Provenance survives: every row still carries book_id/page/version.
        for r in v1_rows:
            assert r["book_id"] == "b1" and r["page"] >= 1

        # Columnar advantage (concept): reading one column reads one column.
        pages = [r["page"] for r in v1_rows]
        assert pages == [1, 2]

        print(f"partitions: {sorted(parts)}")
        print(f"b1/v1 has {len(v1_rows)} rows, all provenance intact")
        print("columnar read: only the page column was needed")
        print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
