"""Quality gates over deduped rows (reference implementation)."""

from __future__ import annotations

from typing import Any

EMPTY = "EMPTY"
TOO_SHORT = "TOO_SHORT"
TOO_LONG = "TOO_LONG"

_ARABIC_RANGES = (
    (0x0600, 0x06FF),
    (0x0750, 0x077F),
    (0x08A0, 0x08FF),
    (0xFB50, 0xFDFF),
    (0xFE70, 0xFEFF),
)


def _is_arabic(char: str) -> bool:
    code = ord(char)
    return any(lo <= code <= hi for lo, hi in _ARABIC_RANGES)


def arabic_ratio(text: str) -> float:
    """Fraction of characters in Arabic Unicode blocks (0600-06FF, 0750-077F,
    08A0-08FF, FB50-FDFF, FE70-FEFF). Empty text -> 0.0. Reported, not gated."""
    if not text:
        return 0.0
    return sum(1 for c in text if _is_arabic(c)) / len(text)


def quality_gates(
    rows: list[dict[str, str]],
    *,
    min_chars: int = 20,
    max_chars: int = 20000,
) -> dict[str, list[dict[str, Any]]]:
    """Split rows into passed and rejected with reasons.

    Contract: return ``{"passed": [...], "rejected": [{"passage_id": ...,
    "reasons": [...]}]}``. A row is rejected when its stripped text is empty
    (``EMPTY``), shorter than ``min_chars`` (``TOO_SHORT``), or longer than
    ``max_chars`` (``TOO_LONG``); reasons accumulate in that check order.
    Input order is preserved in both lists.
    """
    passed: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for row in rows:
        text = row["text"].strip()
        reasons: list[str] = []
        if not text:
            reasons.append(EMPTY)
        elif len(text) < min_chars:
            reasons.append(TOO_SHORT)
        elif len(text) > max_chars:
            reasons.append(TOO_LONG)
        if reasons:
            rejected.append({"passage_id": row["passage_id"], "reasons": reasons})
        else:
            passed.append(row)
    return {"passed": passed, "rejected": rejected}
