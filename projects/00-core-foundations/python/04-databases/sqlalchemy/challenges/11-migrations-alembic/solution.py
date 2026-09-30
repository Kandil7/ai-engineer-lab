"""
Challenge 11: Migrations and Schema Evolution — Reference Solution
=================================================================
"""

from __future__ import annotations

import sqlite3
from collections.abc import Callable

Migration = tuple[str, Callable[[sqlite3.Connection], None], Callable[[sqlite3.Connection], None]]


def run_chain(conn: sqlite3.Connection, chain: list[Migration], target: str) -> str:
    """Apply migrations forward/backward to reach target; return current revision.

    Why this approach: the chain is a linear timeline; the current revision
    is an index into it. Moving forward applies upgrade() in order, moving
    back applies downgrade() in reverse — the same bookkeeping Alembic
    stores in alembic_version.
    """
    conn.execute("CREATE TABLE IF NOT EXISTS chain_state (current_revision TEXT)")
    row = conn.execute("SELECT current_revision FROM chain_state").fetchone()
    if row is None:
        conn.execute("INSERT INTO chain_state (current_revision) VALUES ('')")
        conn.commit()
        current = ""
    else:
        current = row[0] or ""

    ids = [m[0] for m in chain]
    cur_idx = ids.index(current) + 1 if current in ids else 0
    tgt_idx = ids.index(target) + 1 if target in ids else 0

    while cur_idx < tgt_idx:
        chain[cur_idx][1](conn)
        cur_idx += 1
        conn.execute("UPDATE chain_state SET current_revision = ?", (chain[cur_idx - 1][0],))
        conn.commit()
    while cur_idx > tgt_idx:
        chain[cur_idx - 1][2](conn)
        cur_idx -= 1
        prev = chain[cur_idx - 1][0] if cur_idx > 0 else ""
        conn.execute("UPDATE chain_state SET current_revision = ?", (prev,))
        conn.commit()

    row = conn.execute("SELECT current_revision FROM chain_state").fetchone()
    return row[0] or ""


def expand_backfill_contract(conn: sqlite3.Connection, phase: str) -> None:
    """Run one phase: 'expand', 'backfill', or 'contract'.

    Why this approach: the three phases are separate calls precisely so the
    mixed-version window is real — expand stays additive (legacy writers
    survive), backfill is idempotent and never clobbers explicit values,
    and contract refuses to tighten until the data is clean.
    """
    if phase == "expand":
        cols = [r[1] for r in conn.execute("PRAGMA table_info(sources)")]
        if "edition" not in cols:
            conn.execute("ALTER TABLE sources ADD COLUMN edition TEXT")
        conn.commit()
    elif phase == "backfill":
        conn.execute("UPDATE sources SET edition = 'default' WHERE edition IS NULL")
        conn.commit()
    elif phase == "contract":
        nulls = conn.execute("SELECT COUNT(*) FROM sources WHERE edition IS NULL").fetchone()[0]
        if nulls:
            raise ValueError(f"{nulls} rows still lack edition; backfill first")
        conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_book_ed_page ON sources(book, edition, page)"
        )
        conn.commit()
    else:
        raise ValueError(f"unknown phase: {phase}")


def rebuild_index_preserving_lineage(conn: sqlite3.Connection, edits: dict[str, str]) -> int:
    """Apply in-place text edits, rebuild derived idx from sources.

    Why this approach: edits are UPDATEs keyed by source_ref so identity
    never changes, and the rebuild is one set-based INSERT...SELECT —
    O(1) statements and no Python-side materialization of the corpus.
    A per-row fetchall/loop is O(n) statements and O(n) memory and fails
    both guards at 50k rows.
    """
    for ref, new_text in edits.items():
        conn.execute("UPDATE sources SET text = ? WHERE source_ref = ?", (new_text, ref))
    conn.execute("DELETE FROM idx")
    conn.execute("INSERT INTO idx (source_ref, text) SELECT source_ref, text FROM sources")
    conn.commit()
    return conn.execute(
        "SELECT COUNT(*) FROM idx WHERE source_ref IN (SELECT source_ref FROM sources)"
    ).fetchone()[0]
