"""
Challenge 05: Architecture Decision Records — Starter Code
===========================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations


def render_adr(adr: dict) -> str:
    """Render an ADR dict to the standard markdown layout."""
    raise NotImplementedError


def validate_adr(md: str) -> list[str]:
    """Return ALL completeness problems with an ADR document."""
    raise NotImplementedError


def manage_lifecycle(ledger: list[dict], action: dict) -> list[dict]:
    """Apply a lifecycle action in place; return the ledger. Never rewrite text."""
    raise NotImplementedError


def effective_decision(ledger: list[dict], topic: str) -> dict | None:
    """Return the highest-numbered accepted ADR for the topic, or None."""
    raise NotImplementedError
