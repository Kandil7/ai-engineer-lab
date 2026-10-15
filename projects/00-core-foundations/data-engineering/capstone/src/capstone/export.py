"""Export gold rows to DevMate-shaped JSONL and Parquet (reference implementation)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import polars as pl


def devmate_doc_id(source: str, position: int, content: str) -> str:
    """32-hex id identical to DevMate's ``BaseChunker._generate_id``.

    Contract: ``md5(f"{source}:{position}:{content[:100]}")`` hex digest.
    Byte-identical formula to
    ``projects/04-ai-engineering/devmate/src/devmate/ingest/chunker.py`` so a
    32-hex string parses as a dashless UUID that Qdrant accepts.
    """
    return hashlib.md5(f"{source}:{position}:{content[:100]}".encode()).hexdigest()


def export_jsonl(rows: list[dict[str, str]], path: str) -> int:
    """Write one ``Document.to_dict()``-shaped record per line.

    Contract: each line is ``{"id", "content", "metadata"}`` where ``id`` comes
    from ``devmate_doc_id(source, position, content)`` (position = row index),
    ``content`` is the row text, and ``metadata`` carries at least ``source``
    and ``passage_id``. Returns the record count. Non-ASCII preserved
    (``ensure_ascii=False``), LF newlines.
    """
    lines = [
        json.dumps(
            {
                "id": devmate_doc_id(row["source"], i, row["text"]),
                "content": row["text"],
                "metadata": {
                    "source": row["source"],
                    "passage_id": row["passage_id"],
                },
            },
            ensure_ascii=False,
        )
        for i, row in enumerate(rows)
    ]
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return len(rows)


def export_parquet(rows: list[dict[str, str]], path: str) -> int:
    """Write gold rows to Parquet with columns passage_id/text/source. Returns count."""
    frame = pl.DataFrame(
        rows,
        schema={"passage_id": pl.String, "text": pl.String, "source": pl.String},
    )
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    frame.write_parquet(target)
    return frame.height
