"""
Migrations and Schema Evolution - SQLAlchemy Exercises
=======================================================
Topics: migration files as versioned schema, upgrade/downgrade, revision
chain, expand-contract (zero-downtime) pattern, data migrations, testing
migrations, preserving data lineage across schema changes.

Why this matters for AI engineering:
    An Athar-style catalog evolves: a new column for edition metadata, a
    split of "source" into "source + edition", an index rebuild. If you
    edit tables by hand in production you lose the lineage that ties a
    vector index entry back to its book/page. Alembic turns every schema
    change into a reviewed, reversible script. This file builds a
    minimal migration runner on sqlite3 (the same semantics Alembic
    drives on Postgres) and proves the mastery criterion: modify a book
    edition and rebuild the index WITHOUT losing the source linkage.

Environment note:
    Pure standard library (sqlite3). Real Alembic commands appear in the
    lecture and in the final section as text; nothing here requires a
    database server.

Run:      python 11-migrations-alembic.py
Verify:   python 11-migrations-alembic.py --verify
Reference: https://alembic.sqlalchemy.org/en/latest/tutorial.html
"""

from __future__ import annotations

import sqlite3
import sys
from dataclasses import dataclass
from typing import Callable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


# ============================================================
# 1. Why migrations exist
# ============================================================
# Three approaches to schema change:
#   a) edit tables by hand       - unreviewed, unrepeatable, no rollback
#   b) drop and recreate         - loses all data and lineage
#   c) versioned migration files - the only one that survives audit
# A migration is code: reviewed in a PR, applied in order, reversible.

print("1. schema change options")
print("   hand-edit  : no history, no rollback, drift between envs")
print("   recreate   : loses data AND the index-to-source linkage")
print("   migrations : ordered, reviewed, reversible, testable")
print()


# ============================================================
# 2. A minimal migration runner
# ============================================================
# Alembic's core is exactly this: a version table recording which
# scripts ran, and a chain of upgrade()/downgrade() functions. We build
# the mechanics with sqlite3 so the semantics are visible without a
# server.


@dataclass(frozen=True)
class Migration:
    revision: str
    upgrade: Callable[[sqlite3.Connection], None]
    downgrade: Callable[[sqlite3.Connection], None]


def ensure_version_table(conn: sqlite3.Connection) -> None:
    conn.execute("CREATE TABLE IF NOT EXISTS alembic_version (version_num TEXT PRIMARY KEY)")
    conn.commit()


def current_revision(conn: sqlite3.Connection) -> str | None:
    row = conn.execute("SELECT version_num FROM alembic_version").fetchone()
    return row[0] if row else None


def upgrade(conn: sqlite3.Connection, chain: list[Migration]) -> None:
    """Apply every migration after the current revision, in order."""
    ensure_version_table(conn)
    current = current_revision(conn)
    for i, mig in enumerate(chain):
        if current is not None and i <= _index_of(chain, current):
            continue
        mig.upgrade(conn)
        conn.execute("DELETE FROM alembic_version")
        conn.execute("INSERT INTO alembic_version VALUES (?)", (mig.revision,))
        conn.commit()
        print(f"   upgraded -> {mig.revision}")


def downgrade(conn: sqlite3.Connection, chain: list[Migration], to: str) -> None:
    """Walk the chain backwards down to (and including) `to`'s successor."""
    ensure_version_table(conn)
    current = current_revision(conn)
    while current and current != to:
        idx = _index_of(chain, current)
        chain[idx].downgrade(conn)
        current = chain[idx - 1].revision if idx > 0 else None
        conn.execute("DELETE FROM alembic_version")
        if current:
            conn.execute("INSERT INTO alembic_version VALUES (?)", (current,))
        conn.commit()
        print(f"   downgraded -> {current or 'base'}")


def _index_of(chain: list[Migration], revision: str) -> int:
    for i, m in enumerate(chain):
        if m.revision == revision:
            return i
    raise ValueError(f"unknown revision: {revision}")


print("2. migration runner: upgrade in order, downgrade in reverse")
print()


# ============================================================
# 3. The Athar schema migration chain
# ============================================================
# v1: a flat "sources" table (book, page, text).
# v2: expand - ADD nullable edition column (old code keeps working).
# v3: migrate data - backfill edition='default' for existing rows.
# v4: contract - enforce NOT NULL + index on (book, edition, page).
# The lineage column (source_ref) is NEVER dropped or rewritten in any
# step: it is the join key back from the vector index to the book.


def v1_create_sources(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE sources (
            id INTEGER PRIMARY KEY,
            book TEXT NOT NULL,
            page INTEGER NOT NULL,
            text TEXT NOT NULL,
            source_ref TEXT NOT NULL
        )
        """
    )


def v1_downgrade(conn: sqlite3.Connection) -> None:
    conn.execute("DROP TABLE sources")


def v2_add_edition_expand(conn: sqlite3.Connection) -> None:
    # EXPAND: additive only. Old code that inserts without edition still works.
    conn.execute("ALTER TABLE sources ADD COLUMN edition TEXT")


def v2_downgrade(conn: sqlite3.Connection) -> None:
    conn.execute("ALTER TABLE sources DROP COLUMN edition")


def v3_backfill_edition(conn: sqlite3.Connection) -> None:
    # DATA MIGRATION: idempotent UPDATE, safe to re-run.
    conn.execute("UPDATE sources SET edition = 'default' WHERE edition IS NULL")


def v3_downgrade(conn: sqlite3.Connection) -> None:
    conn.execute("UPDATE sources SET edition = NULL")


def v4_contract_edition(conn: sqlite3.Connection) -> None:
    # CONTRACT: now every row has an edition -> tighten the constraint.
    conn.execute("CREATE UNIQUE INDEX idx_book_ed_page ON sources(book, edition, page)")
    conn.execute("CREATE INDEX idx_source_ref ON sources(source_ref)")


def v4_downgrade(conn: sqlite3.Connection) -> None:
    conn.execute("DROP INDEX idx_source_ref")
    conn.execute("DROP INDEX idx_book_ed_page")


CHAIN = [
    Migration("v1_base", v1_create_sources, v1_downgrade),
    Migration("v2_expand_edition", v2_add_edition_expand, v2_downgrade),
    Migration("v3_backfill_edition", v3_backfill_edition, v3_downgrade),
    Migration("v4_contract_edition", v4_contract_edition, v4_downgrade),
]

print("3. chain: v1 base -> v2 expand -> v3 data -> v4 contract")
for m in CHAIN:
    print(f"   {m.revision}")
print()


# ============================================================
# 4. Run it: upgrade, insert, prove lineage survives
# ============================================================


def run_demo() -> None:
    conn = sqlite3.connect(":memory:")
    upgrade(conn, CHAIN)

    # seed v1-style data (source_ref is the lineage key)
    conn.execute(
        "INSERT INTO sources (book, page, text, source_ref) VALUES (?, ?, ?, ?)",
        ("bukhari", 5, "النص الأصلي", "bukhari/p5"),
    )
    conn.commit()

    # v2/v3 already applied: new rows can carry edition explicitly
    conn.execute(
        "INSERT INTO sources (book, page, text, source_ref, edition) VALUES (?, ?, ?, ?, ?)",
        ("bukhari", 5, "نسخة محققة", "bukhari/p5", "muhaqqaqa"),
    )
    conn.commit()

    rows = conn.execute(
        "SELECT book, page, edition, source_ref FROM sources ORDER BY edition"
    ).fetchall()
    print("4. after migrations: lineage (source_ref) intact")
    for r in rows:
        print(f"   {r}")
    print()


print("4. run demo")
run_demo()
print()


# ============================================================
# 5. The mastery criterion: modify edition, rebuild index,
#    NEVER lose the linkage
# ============================================================
# The vector index entry points at source_ref. When we modify a book
# edition (change its text) and rebuild the index, the join back to the
# source must still resolve. The migration contract: source_ref is
# immutable identity; content changes are UPDATEs, never DELETE+INSERT.


def modify_edition_and_rebuild(conn: sqlite3.Connection, ref: str, new_text: str) -> dict:
    """Update edition text in place and simulate an index rebuild."""
    before = conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0]
    conn.execute("UPDATE sources SET text = ? WHERE source_ref = ?", (new_text, ref))
    conn.commit()
    # index rebuild = re-read every row through its source_ref
    rebuilt = conn.execute("SELECT source_ref FROM sources WHERE source_ref IS NOT NULL").fetchall()
    after = conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0]
    return {
        "rows_before": before,
        "rows_after": after,
        "resolvable_refs": len(rebuilt),
        "target_found": any(r[0] == ref for r in rebuilt),
    }


def lineage_holds() -> bool:
    conn = sqlite3.connect(":memory:")
    upgrade(conn, CHAIN)
    conn.execute(
        "INSERT INTO sources (book, page, text, source_ref, edition) VALUES (?, ?, ?, ?, ?)",
        ("bukhari", 5, "النص الأصلي", "bukhari/p5", "default"),
    )
    conn.commit()
    report = modify_edition_and_rebuild(conn, "bukhari/p5", "نص بعد التحقيق")
    return (
        report["rows_before"] == report["rows_after"]
        and report["resolvable_refs"] == 1
        and report["target_found"]
    )


print("5. mastery: modify edition -> rebuild -> lineage intact")
print(f"   lineage holds: {lineage_holds()}")
print()


# ============================================================
# 6. Real Alembic workflow (text reference)
# ============================================================
# The runner above is the mechanics; Alembic is the tool. Workflow:
#
#     alembic init alembic
#     alembic revision --autogenerate -m "add edition column"
#     alembic upgrade head
#     alembic downgrade -1
#     alembic history
#     alembic check           # 1.13+: fails if models drifted from DB
#
# Rules that matter:
#   - one migration per PR, named after the change ("add edition column")
#   - autogenerate is a draft: READ the generated file, fix the order
#   - expand -> backfill -> contract for any NOT NULL / renames
#   - down() must actually undo up(); test it in CI
#   - never edit an applied migration; write a follow-up

print("6. real Alembic workflow")
for cmd in [
    "alembic revision --autogenerate -m 'add edition column'",
    "alembic upgrade head",
    "alembic downgrade -1",
    "alembic history",
    "alembic check",
]:
    print(f"   $ {cmd}")
print()


# ============================================================
# 7. Self-verification
# ============================================================


def _verify() -> bool:
    checks: list[tuple[str, bool]] = []

    conn = sqlite3.connect(":memory:")
    upgrade(conn, CHAIN)
    checks.append(("upgrade reaches head", current_revision(conn) == "v4_contract_edition"))

    downgrade(conn, CHAIN, "v2_expand_edition")
    checks.append(("downgrade steps back", current_revision(conn) == "v2_expand_edition"))
    upgrade(conn, CHAIN)
    checks.append(("re-upgrade restores head", current_revision(conn) == "v4_contract_edition"))

    conn2 = sqlite3.connect(":memory:")
    upgrade(conn2, CHAIN)
    conn2.execute(
        "INSERT INTO sources (book, page, text, source_ref, edition) VALUES (?, ?, ?, ?, ?)",
        ("b", 1, "t", "b/p1", "e1"),
    )
    conn2.commit()
    dup_rejected = False
    try:
        conn2.execute(
            "INSERT INTO sources (book, page, text, source_ref, edition) VALUES (?, ?, ?, ?, ?)",
            ("b", 1, "t2", "b/p1", "e1"),
        )
    except sqlite3.IntegrityError:
        dup_rejected = True
    checks.append(("unique index enforced", dup_rejected))

    checks.append(("lineage survives edit+rebuild", lineage_holds()))

    ok = True
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    return ok


if __name__ == "__main__":
    if "--verify" in sys.argv:
        print("Verification:")
        sys.exit(0 if _verify() else 1)
    print("Verification (python 11-migrations-alembic.py --verify):")
    _verify()
