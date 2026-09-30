"""
Challenge 07: Backup and Restore — Starter Code
================================================
Fill in the function bodies. Do not modify signatures.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


def dump_and_restore(
    src_conn: sqlite3.Connection,
    dump_path: Path,
    dst_conn: sqlite3.Connection,
) -> dict:
    """Logical dump to file, restore into dst, return per-table row counts."""
    raise NotImplementedError


def verify_restore(src_conn: sqlite3.Connection, dst_conn: sqlite3.Connection) -> list[str]:
    """Compare row counts and sampled content byte-for-byte; return violations."""
    raise NotImplementedError


def point_in_time_recovery(
    base_dump: str,
    wal_records: list[tuple[int, str]],
    target_version: int,
    dst_conn: sqlite3.Connection,
) -> dict:
    """Restore base, replay redo records <= target once each, in version order."""
    raise NotImplementedError
