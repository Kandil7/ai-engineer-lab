"""
Challenge 07: Backup and Restore — Tests
=========================================
Default run targets starter.py and MUST FAIL (NotImplementedError) until solved.

Validate the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 04-databases/postgresql/challenges/07-backup-and-restore/test_challenge.py -q

Guards use statement counting — never wall-clock time.
"""

from __future__ import annotations

import importlib.util
import os
import sqlite3
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


def _catalog(n_books: int = 3, n_editions: int = 5) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT)")
    conn.execute("CREATE TABLE editions (id INTEGER PRIMARY KEY, label TEXT)")
    conn.executemany(
        "INSERT INTO books (title) VALUES (?)", [(f"كتاب {i}",) for i in range(n_books)]
    )
    conn.executemany(
        "INSERT INTO editions (label) VALUES (?)",
        [(f"نسخة {i}",) for i in range(n_editions)],
    )
    conn.commit()
    return conn


def _empty() -> sqlite3.Connection:
    return sqlite3.connect(":memory:")


class TestDumpAndRestore:
    """Bronze: the restore drill round-trip."""

    def test_basic(self, tmp_path: Path) -> None:
        src = _catalog(3, 5)
        dst = _empty()
        out = mod.dump_and_restore(src, tmp_path / "dump.sql", dst)
        assert out == {"tables": {"books": 3, "editions": 5}}

    def test_dump_file_written(self, tmp_path: Path) -> None:
        src = _catalog(1, 1)
        dump = tmp_path / "d.sql"
        mod.dump_and_restore(src, dump, _empty())
        assert dump.exists() and "CREATE TABLE" in dump.read_text(encoding="utf-8")

    def test_empty_database(self, tmp_path: Path) -> None:
        out = mod.dump_and_restore(_empty(), tmp_path / "e.sql", _empty())
        assert out == {"tables": {}}

    def test_content_survives(self, tmp_path: Path) -> None:
        src = _catalog(1, 1)
        dst = _empty()
        mod.dump_and_restore(src, tmp_path / "c.sql", dst)
        title = dst.execute("SELECT title FROM books").fetchone()[0]
        assert title == "كتاب 0"


class TestVerifyRestore:
    """Silver: detect drift at identical row counts; statement budget."""

    def test_clean_restore(self, tmp_path: Path) -> None:
        src = _catalog(3, 5)
        dst = _empty()
        mod.dump_and_restore(src, tmp_path / "v.sql", dst)
        assert mod.verify_restore(src, dst) == []

    def test_detects_content_drift_same_counts(self, tmp_path: Path) -> None:
        """The adversarial case: row counts identical, content flipped."""
        src = _catalog(3, 5)
        dst = _empty()
        mod.dump_and_restore(src, tmp_path / "v.sql", dst)
        dst.execute("UPDATE books SET title = 'مزوّر' WHERE id = 1")
        dst.commit()
        problems = mod.verify_restore(src, dst)
        assert any("books" in p and "drift" in p for p in problems), (
            "count-only verification misses content drift at equal counts"
        )

    def test_detects_row_count_mismatch(self, tmp_path: Path) -> None:
        src = _catalog(3, 5)
        dst = _empty()
        mod.dump_and_restore(src, tmp_path / "v.sql", dst)
        dst.execute("DELETE FROM editions WHERE id = 1")
        dst.commit()
        problems = mod.verify_restore(src, dst)
        assert any("editions" in p and "count" in p for p in problems)

    def test_detects_missing_table(self, tmp_path: Path) -> None:
        src = _catalog(3, 5)
        dst = _empty()
        mod.dump_and_restore(src, tmp_path / "v.sql", dst)
        dst.execute("DROP TABLE editions")
        dst.commit()
        problems = mod.verify_restore(src, dst)
        assert any("editions" in p and "missing" in p for p in problems)

    def test_statement_budget(self, tmp_path: Path) -> None:
        """Per-row comparison loops issue O(n) statements and must fail."""
        n = 20_000
        src = _catalog(n, 0)
        dst = _empty()
        mod.dump_and_restore(src, tmp_path / "big.sql", dst)
        spy = CountingConn(dst)
        problems = mod.verify_restore(src, spy)
        assert problems == []
        budget = 4 * 2  # two tables
        assert spy.count <= budget, (
            f"{spy.count} statements exceed budget {budget}; "
            "a per-row compare loop is O(n) statements and must fail this guard"
        )


class TestPointInTime:
    """Gold: replay to the target version, exactly once, in version order."""

    BASE = (
        "CREATE TABLE t (key TEXT, val TEXT);"
        "INSERT INTO t VALUES ('a', '0');"
        "INSERT INTO t VALUES ('b', '0');"
    )

    def _wal(self) -> list[tuple[int, str]]:
        return [
            (3, "INSERT INTO t VALUES ('a', '3')"),
            (7, "DELETE FROM t WHERE key = 'b'"),
            (9, "INSERT INTO t VALUES ('b', '9')"),
            (12, "INSERT INTO t VALUES ('c', '12')"),
            (3, "INSERT INTO t VALUES ('a', '3')"),  # redelivered duplicate
        ]

    def test_recovery_at_target(self) -> None:
        dst = sqlite3.connect(":memory:")
        out = mod.point_in_time_recovery(self.BASE, self._wal(), 8, dst)
        assert out["applied"] == 2 and out["skipped"] == 3
        rows = dst.execute("SELECT key, val FROM t ORDER BY rowid").fetchall()
        # v7 delete is visible, v9 restore is NOT — that is point-in-time
        assert rows == [("a", "0"), ("a", "3")]
        assert ("b", "9") not in rows

    def test_duplicates_applied_once(self) -> None:
        dst = sqlite3.connect(":memory:")
        mod.point_in_time_recovery(self.BASE, self._wal(), 8, dst)
        count = dst.execute("SELECT COUNT(*) FROM t WHERE val = '3'").fetchone()[0]
        assert count == 1, "a redelivered redo record must not create a duplicate row"

    def test_out_of_order_input(self) -> None:
        dst = sqlite3.connect(":memory:")
        shuffled = list(reversed(self._wal()))
        out = mod.point_in_time_recovery(self.BASE, shuffled, 8, dst)
        assert out["applied"] == 2 and out["skipped"] == 3
        rows = dst.execute("SELECT key, val FROM t ORDER BY rowid").fetchall()
        assert rows == [("a", "0"), ("a", "3")]

    def test_target_below_all(self) -> None:
        dst = sqlite3.connect(":memory:")
        out = mod.point_in_time_recovery(self.BASE, self._wal(), 1, dst)
        assert out["applied"] == 0
        rows = dst.execute("SELECT key FROM t ORDER BY rowid").fetchall()
        assert rows == [("a",), ("b",)]

    def test_statement_budget(self) -> None:
        dst = sqlite3.connect(":memory:")
        spy = CountingConn(dst)
        out = mod.point_in_time_recovery(self.BASE, self._wal(), 8, spy)
        assert spy.count == out["applied"] + 1, (
            f"{spy.count} statements for applied={out['applied']}; "
            "duplicates must be skipped, not re-executed"
        )

    def test_empty_wal(self) -> None:
        dst = sqlite3.connect(":memory:")
        out = mod.point_in_time_recovery(self.BASE, [], 10, dst)
        assert out == {"applied": 0, "skipped": 0, "final_version": 0}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
