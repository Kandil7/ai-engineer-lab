"""
Challenge 07: Backup and Restore — Reference Solution
=====================================================
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


def dump_and_restore(
    src_conn: sqlite3.Connection,
    dump_path: Path,
    dst_conn: sqlite3.Connection,
) -> dict:
    """Logical dump to file, restore into dst, return per-table row counts.

    Why this approach: iterdump produces a re-runnable SQL script — the
    same contract as pg_dump. Restoring from the FILE (not from memory)
    proves the dump artifact itself is usable, which is the whole point
    of a backup drill.
    """
    with open(dump_path, "w", encoding="utf-8") as fh:
        for line in src_conn.iterdump():
            fh.write(f"{line}\n")
    script = dump_path.read_text(encoding="utf-8")
    if script.strip():
        dst_conn.executescript(script)
        dst_conn.commit()
    names = [
        r[0]
        for r in dst_conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
    ]
    tables = {
        name: dst_conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        for name in sorted(names)
    }
    return {"tables": tables}


def verify_restore(src_conn: sqlite3.Connection, dst_conn: sqlite3.Connection) -> list[str]:
    """Compare row counts and sampled content byte-for-byte.

    Why this approach: count equality is necessary but not sufficient —
    content drift at identical counts is exactly the corruption a real
    incident hides behind. Set-based SQL comparison keeps the statement
    count per table constant regardless of row count.
    """
    problems: list[str] = []
    src_tables = {
        r[0]
        for r in src_conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
    }
    dst_tables = {
        r[0]
        for r in dst_conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
    }
    for name in sorted(src_tables):
        if name not in dst_tables:
            problems.append(f"{name}: missing in restored database")
            continue
        n_src = src_conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        n_dst = dst_conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        if n_src != n_dst:
            problems.append(f"{name}: row count {n_src} != {n_dst}")
    for name in sorted(src_tables & dst_tables):
        cols = [r[1] for r in src_conn.execute(f"PRAGMA table_info({name})").fetchall()]
        text_cols = [c for c in cols if c in ("text", "title", "content", "label")]
        for col in text_cols:
            src_rows = src_conn.execute(f"SELECT {col} FROM {name} ORDER BY rowid").fetchall()
            dst_rows = dst_conn.execute(f"SELECT {col} FROM {name} ORDER BY rowid").fetchall()
            if src_rows != dst_rows:
                problems.append(f"{name}.{col}: content drift detected")
    for name in sorted(dst_tables - src_tables):
        problems.append(f"{name}: present in restore but not in source")
    return problems


def point_in_time_recovery(
    base_dump: str,
    wal_records: list[tuple[int, str]],
    target_version: int,
    dst_conn: sqlite3.Connection,
) -> dict:
    """Restore base, replay redo records <= target once each, in version order.

    Why this approach: the WAL is a timeline, not a queue — replay is
    ordered by version and idempotent by (version, sql) identity, because
    real WAL shipping redelivers. Anything past the target is skipped,
    which is what makes the recovery point-in-time.
    """
    if base_dump.strip():
        dst_conn.executescript(base_dump)
    applied = 0
    skipped = 0
    seen: set[tuple[int, str]] = set()
    for version, sql in sorted(wal_records, key=lambda r: r[0]):
        if version > target_version:
            skipped += 1
            continue
        if (version, sql) in seen:
            skipped += 1
            continue
        seen.add((version, sql))
        dst_conn.execute(sql)
        applied += 1
    dst_conn.commit()
    return {
        "applied": applied,
        "skipped": skipped,
        "final_version": max((v for v, _ in wal_records if v <= target_version), default=0),
    }
