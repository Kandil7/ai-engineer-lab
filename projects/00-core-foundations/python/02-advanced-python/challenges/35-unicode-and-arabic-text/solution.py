"""
Challenge 35: Unicode and Arabic Text — Reference Solution
==========================================================
"""

from __future__ import annotations

import json
import unicodedata
from collections.abc import Callable, Iterable

_HARAKAT = set(range(0x064B, 0x0653)) | {0x0670}
_DIGIT_FOLD = str.maketrans(
    {0x0660 + i: str(i) for i in range(10)} | {0x06F0 + i: str(i) for i in range(10)}
)


def normalize_record(record: dict) -> dict:
    """Return a normalized copy: page -> ASCII int, text cleaned, search_key folded.

    Why this approach: NFKC first so presentation forms become standard
    letters before any folding; digits fold at the boundary so page is
    always an int; the search_key applies the extra letter unifications
    (hamza/maqsura/ta-marbuta) only to the key, never to display text.
    """
    text = unicodedata.normalize("NFKC", str(record.get("text", "")))
    text = "".join(ch for ch in text if ord(ch) not in _HARAKAT)
    text = " ".join(text.split())
    key = text.translate(_DIGIT_FOLD)
    key = key.replace("\u0623", "\u0627").replace("\u0625", "\u0627")
    key = key.replace("\u0622", "\u0627")
    key = key.replace("\u0649", "\u064a")
    key = key.replace("\u0629", "\u0647")
    return {
        **record,
        "page": int(str(record.get("page", 0)).translate(_DIGIT_FOLD)),
        "text": text,
        "search_key": key,
    }


def find_duplicates(records: list[dict]) -> list[list[dict]]:
    """Group records whose search_key collides.

    Why this approach: dict.setdefault groups in O(n) hash lookups. A
    pairwise comparison of search keys is O(n^2) string comparisons and
    fails the comparison budget at n=5000 (~12.5M comparisons vs ~5k).
    """
    groups: dict[str, list[dict]] = {}
    order: list[str] = []
    for rec in records:
        key = rec.get("search_key", "")
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(rec)
    return [groups[k] for k in order if len(groups[k]) >= 2]


def import_corpus(
    lines: Iterable[str],
    batch_size: int,
    on_error: Callable[[int, str], None],
) -> dict:
    """Stream JSONL in batches; report broken records via on_error.

    Why this approach: the batch list is the ONLY materialized state, so
    memory stays O(batch_size) no matter how long the corpus is. Errors
    are located by line number (1-based) so a quarantined record can be
    found in the source file without a debugger.
    """
    imported = 0
    batches = 0
    errors = 0
    batch: list[dict] = []
    for line_no, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            errors += 1
            on_error(line_no, f"invalid JSON: {exc.msg}")
            continue
        if not isinstance(obj, dict) or "id" not in obj or "text" not in obj:
            errors += 1
            on_error(line_no, "missing fields: id/text")
            continue
        batch.append(obj)
        if len(batch) >= batch_size:
            imported += len(batch)
            batches += 1
            batch = []
    if batch:
        imported += len(batch)
        batches += 1
    return {"imported": imported, "batches": batches, "errors": errors}
