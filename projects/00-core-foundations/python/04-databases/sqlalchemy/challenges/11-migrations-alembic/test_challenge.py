"""
Challenge 11: Migrations and Schema Evolution — Tests
=====================================================
Default run targets starter.py and MUST FAIL (NotImplementedError) until solved.

Validate the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 04-databases/sqlalchemy/challenges/11-migrations-alembic/test_challenge.py -q

Guards use statement counting and tracemalloc — never wall-clock time.
"""

from __future__ import annotations

import importlib.util
import os
import sqlite3
import tracemalloc
from pathlib import Path

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
assert _spec is not None and _spec.loader is not None
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)

import pytest  # noqa: E402


class CountingConn:
    """Delegates to a real connection but counts execute/executescript calls."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn
        self.count = 0

    def execute(self, sql: str, *args) -> sqlite3.Cursor:
        self.count += 1
        return self._conn.execute(sql, *args)

    def executescript(self, sql: str) -> None:
        self.count += 1
        self._conn.executescript(sql)

    def commit(self) -> None:
        self._conn.commit()

    def __getattr__(self, name: str):
        return getattr(self._conn, name)


def _fresh() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE sources (id INTEGER PRIMARY KEY, book TEXT, page INTEGER,"
        " text TEXT, source_ref TEXT)"
    )
    return conn


def _chain() -> list[tuple[str, object, object]]:
    def up1(c):
        c.execute("CREATE TABLE t1 (x INTEGER)")

    def down1(c):
        c.execute("DROP TABLE t1")

    def up2(c):
        c.execute("CREATE TABLE t2 (x INTEGER)")

    def down2(c):
        c.execute("DROP TABLE t2")

    def up3(c):
        c.execute("CREATE TABLE t3 (x INTEGER)")

    def down3(c):
        c.execute("DROP TABLE t3")

    return [("v1", up1, down1), ("v2", up2, down2), ("v3", up3, down3)]


def _tables(conn: sqlite3.Connection) -> set[str]:
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'chain_%'"
    ).fetchall()
    return {r[0] for r in rows}


class TestRunChain:
    """Bronze: revision bookkeeping forward and backward."""

    def test_upgrade_to_head(self) -> None:
        conn = _fresh()
        assert mod.run_chain(conn, _chain(), "v3") == "v3"
        assert _tables(conn) == {"sources", "t1", "t2", "t3"}

    def test_partial_upgrade(self) -> None:
        conn = _fresh()
        mod.run_chain(conn, _chain(), "v3")
        conn2 = _fresh()
        assert mod.run_chain(conn2, _chain(), "v2") == "v2"
        assert _tables(conn2) == {"sources", "t1", "t2"}

    def test_noop_when_current(self) -> None:
        conn = _fresh()
        mod.run_chain(conn, _chain(), "v3")
        assert mod.run_chain(conn, _chain(), "v3") == "v3"

    def test_downgrade(self) -> None:
        conn = _fresh()
        mod.run_chain(conn, _chain(), "v3")
        assert mod.run_chain(conn, _chain(), "v1") == "v1"
        assert _tables(conn) == {"sources", "t1"}

    def test_downgrade_to_base(self) -> None:
        conn = _fresh()
        mod.run_chain(conn, _chain(), "v3")
        assert mod.run_chain(conn, _chain(), "") == ""
        assert _tables(conn) == {"sources"}


class TestExpandBackfillContract:
    """Silver: mixed-version safety + idempotent backfill + disciplined contract."""

    def test_legacy_insert_after_expand(self) -> None:
        conn = _fresh()
        mod.expand_backfill_contract(conn, "expand")
        conn.execute(
            "INSERT INTO sources (book, page, text, source_ref) VALUES (?, ?, ?, ?)",
            ("bukhari", 1, "نص", "bukhari/p1"),
        )
        conn.commit()
        assert conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0] == 1

    def test_backfill_idempotent_and_preserves_explicit(self) -> None:
        conn = _fresh()
        mod.expand_backfill_contract(conn, "expand")
        conn.execute(
            "INSERT INTO sources (book, page, text, source_ref) VALUES (?, ?, ?, ?)",
            ("bukhari", 1, "نص", "bukhari/p1"),
        )
        conn.execute(
            "INSERT INTO sources (book, page, text, source_ref, edition) VALUES (?, ?, ?, ?, ?)",
            ("bukhari", 2, "نص محقق", "bukhari/p2", "muhaqqaqa"),
        )
        conn.commit()
        mod.expand_backfill_contract(conn, "backfill")
        mod.expand_backfill_contract(conn, "backfill")
        rows = dict((r[0], r[1]) for r in conn.execute("SELECT source_ref, edition FROM sources"))
        assert rows == {"bukhari/p1": "default", "bukhari/p2": "muhaqqaqa"}

    def test_contract_refuses_nulls(self) -> None:
        conn = _fresh()
        mod.expand_backfill_contract(conn, "expand")
        conn.execute(
            "INSERT INTO sources (book, page, text, source_ref) VALUES (?, ?, ?, ?)",
            ("b", 1, "t", "b/p1"),
        )
        conn.commit()
        with pytest.raises(ValueError):
            mod.expand_backfill_contract(conn, "contract")

    def test_contract_creates_unique_index(self) -> None:
        conn = _fresh()
        mod.expand_backfill_contract(conn, "expand")
        for i in range(2):
            conn.execute(
                "INSERT INTO sources (book, page, text, source_ref, edition)"
                " VALUES (?, ?, ?, ?, ?)",
                ("b", i + 1, "t", f"b/p{i + 1}", "default"),
            )
        conn.commit()
        mod.expand_backfill_contract(conn, "backfill")
        mod.expand_backfill_contract(conn, "contract")
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO sources (book, page, text, source_ref, edition)"
                " VALUES (?, ?, ?, ?, ?)",
                ("b", 1, "t", "b/p1-dup", "default"),
            )

    def test_adversarial_mixed_rows(self) -> None:
        conn = _fresh()
        mod.expand_backfill_contract(conn, "expand")
        conn.executemany(
            "INSERT INTO sources (book, page, text, source_ref) VALUES (?, ?, ?, ?)",
            [("كتاب", i, f"نص {i}", f"كتاب/p{i}") for i in range(1, 21)],
        )
        conn.execute(
            "INSERT INTO sources (book, page, text, source_ref, edition) VALUES (?, ?, ?, ?, ?)",
            ("كتاب", 99, "نص محقق", "كتاب/p99", "محقق"),
        )
        conn.commit()
        mod.expand_backfill_contract(conn, "backfill")
        conn.execute("SELECT COUNT(*) FROM sources WHERE edition IS NULL").fetchone()
        assert conn.execute("SELECT COUNT(*) FROM sources WHERE edition IS NULL").fetchone()[0] == 0
        assert (
            conn.execute("SELECT edition FROM sources WHERE source_ref = 'كتاب/p99'").fetchone()[0]
            == "محقق"
        )


class TestRebuildLineage:
    """Gold: lineage preserved, statement budget, memory ceiling."""

    def _seed(self, n: int) -> sqlite3.Connection:
        conn = _fresh()
        conn.execute("CREATE TABLE idx (source_ref TEXT, text TEXT)")
        conn.executemany(
            "INSERT INTO sources (book, page, text, source_ref) VALUES (?, ?, ?, ?)",
            [("كتاب", i, f"نص {i}", f"كتاب/p{i}") for i in range(1, n + 1)],
        )
        conn.commit()
        return conn

    def test_basic_rebuild(self) -> None:
        conn = self._seed(10)
        assert mod.rebuild_index_preserving_lineage(conn, {}) == 10
        assert conn.execute("SELECT COUNT(*) FROM idx").fetchone()[0] == 10

    def test_edit_updates_in_place(self) -> None:
        conn = self._seed(10)
        mod.rebuild_index_preserving_lineage(conn, {"كتاب/p3": "نص بعد التحقيق"})
        assert (
            conn.execute("SELECT text FROM idx WHERE source_ref = 'كتاب/p3'").fetchone()[0]
            == "نص بعد التحقيق"
        )
        assert conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0] == 10

    def test_lineage_resolvable(self) -> None:
        conn = self._seed(50)
        out = mod.rebuild_index_preserving_lineage(conn, {"كتاب/p1": "x"})
        assert out == 50
        unresolved = conn.execute(
            "SELECT COUNT(*) FROM idx WHERE source_ref NOT IN (SELECT source_ref FROM sources)"
        ).fetchone()[0]
        assert unresolved == 0

    def test_statement_budget(self) -> None:
        """Set-based rebuild: a per-row Python loop fails this budget."""
        n = 5000
        conn = self._seed(n)
        spy = CountingConn(conn)
        mod.rebuild_index_preserving_lineage(spy, {"كتاب/p1": "x"})
        budget = 3 * ((n + 999) // 1000) + 5
        assert spy.count <= budget, (
            f"{spy.count} statements exceed budget {budget}; "
            "a per-row rebuild loop is O(n) statements and must fail this guard"
        )

    def test_memory_ceiling(self) -> None:
        """50k rows: fetchall materialization blows 8 MB."""
        n = 50_000
        conn = self._seed(n)
        tracemalloc.start()
        try:
            out = mod.rebuild_index_preserving_lineage(conn, {"كتاب/p1": "x"})
        finally:
            _cur, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
        assert out == n
        assert peak < 8 * 1024 * 1024, (
            f"peak {peak / 1e6:.1f} MB exceeds the 8 MB ceiling; "
            "the rebuild must not materialize the corpus in Python"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
