"""
Challenge 11: Migrations and Schema Evolution — Starter Code
============================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Callable


def run_chain(
    conn: sqlite3.Connection,
    chain: list[
        tuple[str, Callable[[sqlite3.Connection], None], Callable[[sqlite3.Connection], None]]
    ],
    target: str,
) -> str:
    """Apply migrations forward/backward to reach target; return current revision."""
    raise NotImplementedError


def expand_backfill_contract(conn: sqlite3.Connection, phase: str) -> None:
    """Run one phase: 'expand', 'backfill', or 'contract' (raises on NULLs)."""
    raise NotImplementedError


def rebuild_index_preserving_lineage(conn: sqlite3.Connection, edits: dict[str, str]) -> int:
    """Apply in-place text edits, rebuild derived idx from sources, return resolvable refs."""
    raise NotImplementedError
