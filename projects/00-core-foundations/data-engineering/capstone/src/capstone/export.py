"""Export gold rows to DevMate-shaped JSONL and Parquet. YOUR TURN: implement all three."""

from __future__ import annotations

import hashlib  # noqa: F401  (scaffold seam: used once devmate_doc_id is implemented)
import json  # noqa: F401  (scaffold seam: used once export_jsonl is implemented)
from pathlib import (
    Path,  # noqa: F401  (scaffold seam: used once exporters are implemented)
)

import polars as pl  # noqa: F401  (scaffold seam: used once export_parquet is implemented)


def devmate_doc_id(source: str, position: int, content: str) -> str:
    """32-hex id identical to DevMate's ``BaseChunker._generate_id``.

    Contract: ``md5(f"{source}:{position}:{content[:100]}")`` hex digest.
    Byte-identical formula to
    ``projects/04-ai-engineering/devmate/src/devmate/ingest/chunker.py`` so a
    32-hex string parses as a dashless UUID that Qdrant accepts.
    """
    raise NotImplementedError("YOUR TURN: implement devmate_doc_id (md5 formula)")


def export_jsonl(rows: list[dict[str, str]], path: str) -> int:
    """Write one ``Document.to_dict()``-shaped record per line.

    Contract: each line is ``{"id", "content", "metadata"}`` where ``id`` comes
    from ``devmate_doc_id(source, position, content)`` (position = row index),
    ``content`` is the row text, and ``metadata`` carries at least ``source``
    and ``passage_id``. Returns the record count. Non-ASCII preserved
    (``ensure_ascii=False``), LF newlines.
    """
    raise NotImplementedError("YOUR TURN: implement export_jsonl (Document shape)")


def export_parquet(rows: list[dict[str, str]], path: str) -> int:
    """Write gold rows to Parquet with columns passage_id/text/source. Returns count."""
    raise NotImplementedError("YOUR TURN: implement export_parquet (polars write)")
