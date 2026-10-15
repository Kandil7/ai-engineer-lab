"""Quality gates over deduped rows. YOUR TURN: implement both functions."""

from __future__ import annotations

EMPTY = "EMPTY"
TOO_SHORT = "TOO_SHORT"
TOO_LONG = "TOO_LONG"


def arabic_ratio(text: str) -> float:
    """Fraction of characters in Arabic Unicode blocks (0600-06FF, 0750-077F,
    08A0-08FF, FB50-FDFF, FE70-FEFF). Empty text -> 0.0. Reported, not gated."""
    raise NotImplementedError("YOUR TURN: implement arabic_ratio")


def quality_gates(
    rows: list[dict[str, str]],
    *,
    min_chars: int = 20,
    max_chars: int = 20000,
) -> dict[str, list[dict[str, object]]]:
    """Split rows into passed and rejected with reasons.

    Contract: return ``{"passed": [...], "rejected": [{"passage_id": ...,
    "reasons": [...]}]}``. A row is rejected when its stripped text is empty
    (``EMPTY``), shorter than ``min_chars`` (``TOO_SHORT``), or longer than
    ``max_chars`` (``TOO_LONG``); reasons accumulate in that check order.
    Input order is preserved in both lists.
    """
    raise NotImplementedError("YOUR TURN: implement quality_gates (EMPTY/SHORT/LONG)")
