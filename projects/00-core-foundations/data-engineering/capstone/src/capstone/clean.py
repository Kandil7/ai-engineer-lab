"""Clean raw records into a typed Polars frame (reference implementation)."""

from __future__ import annotations

import re

import polars as pl

_WS_RUN = re.compile(r"\s+")


def clean_text(raw: str) -> str:
    """Collapse every whitespace run to a single space and strip.

    Contract: ``clean_text("  a   b\\n\\n c ") == "a b c"``. Newlines are not
    preserved at this stage (paragraph-aware cleaning is a documented follow-up
    in the lecture for topic 16's companion practice).
    """
    return _WS_RUN.sub(" ", raw).strip()


def frame_from_records(records: list[dict[str, str]]) -> pl.DataFrame:
    """Build a typed frame with a ``char_count`` column.

    Input rows carry ``passage_id`` / ``text`` / ``source`` (all strings).
    Output schema: ``passage_id: String, text: String, source: String,
    char_count: UInt32`` where ``char_count`` is the cleaned text length in
    characters (``str.len_chars()``), computed with expressions, not loops.
    """
    cleaned = [
        {
            "passage_id": r["passage_id"],
            "text": clean_text(r["text"]),
            "source": r["source"],
        }
        for r in records
    ]
    frame = pl.DataFrame(
        cleaned,
        schema={
            "passage_id": pl.String,
            "text": pl.String,
            "source": pl.String,
        },
    )
    return frame.with_columns(
        pl.col("text").str.len_chars().cast(pl.UInt32).alias("char_count")
    )
