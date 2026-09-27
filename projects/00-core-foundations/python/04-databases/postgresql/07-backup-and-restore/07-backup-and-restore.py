"""
Backup and Restore - PostgreSQL Exercises
==========================================
Topics: why backups fail, logical dumps (pg_dump), PITR and WAL,
backup verification, restore drills, RPO/RTO, 3-2-1 rule.

Why this matters for AI engineering:
    An Athar catalog is a curated scholarly corpus: books, editions,
    page references, permission records. If PostgreSQL is the source of
    truth (the skills-map mandate) then a backup is not a checkbox - it
    is the difference between a hiccup and losing the reference corpus.
    This file teaches backup thinking on sqlite3 (identical logic:
    dump, verify, restore, measure) and shows the real Postgres tools in
    the final section. The core lesson: an unverified backup is not a
    backup; a restore you have never rehearsed is a hope.

Environment note:
    Pure standard library (sqlite3). Real pg_dump/pgBackRest commands
    appear as text in the final section; nothing here requires a server.

Run:      python 07-backup-and-restore.py
Verify:   python 07-backup-and-restore.py --verify
Reference: https://www.postgresql.org/docs/current/backup.html
"""

from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


# ============================================================
# 1. Why backups fail (the four failure modes)
# ============================================================
# Backups rarely fail to run - they fail to RESTORE. The four modes:
#   1. never verified     - the dump exists but is corrupt/incomplete
#   2. wrong granularity  - nightly dump, but the loss was at 15:00
#   3. secret/config loss - data restored, but not the .env or keys
#   4. too slow           - restore takes 12h and the RTO is 1h

print("1. why backups fail")
print("   1. never verified      3. config/secrets lost")
print("   2. wrong granularity   4. restore slower than RTO")
print()


# ============================================================
# 2. Logical dump: what "exporting the truth" means
# ============================================================
# A logical dump is a file that can recreate the database. sqlite3
# offers an online backup API (same idea as pg_dump: consistent copy
# while the DB is live). We dump to SQL text so a human can read it.


def seed_catalog(conn: sqlite3.Connection) -> None:
    conn.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT, author TEXT)")
    conn.execute("CREATE TABLE editions (id INTEGER PRIMARY KEY, book_id INT, label TEXT)")
    conn.execute("CREATE TABLE permissions (id INTEGER PRIMARY KEY, role TEXT, scope TEXT)")
    conn.executemany(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        [("صحيح البخاري", "الإمام البخاري"), ("صحيح مسلم", "الإمام مسلم")],
    )
    conn.executemany(
        "INSERT INTO editions (book_id, label) VALUES (?, ?)",
        [(1, "default"), (2, "default")],
    )
    conn.execute("INSERT INTO permissions (role, scope) VALUES ('admin', 'all')")
    conn.commit()


def dump_database(conn: sqlite3.Connection, path: Path) -> int:
    """Logical dump: serialize schema+data to SQL text (like pg_dump)."""
    with open(path, "w", encoding="utf-8") as fh:
        for line in conn.iterdump():
            fh.write(f"{line}\n")
    return path.stat().st_size


def dump_size_and_tables(path: Path) -> dict[str, int]:
    size = path.stat().st_size
    text = path.read_text(encoding="utf-8")
    tables = sum(1 for line in text.splitlines() if line.startswith("CREATE TABLE"))
    inserts = sum(1 for line in text.splitlines() if line.startswith("INSERT"))
    return {"bytes": size, "tables": tables, "inserts": inserts}


print("2. logical dump (sqlite3 stand-in for pg_dump)")
src = sqlite3.connect(":memory:")
seed_catalog(src)
with tempfile.TemporaryDirectory() as tmp:
    dump_path = Path(tmp) / "catalog_dump.sql"
    dump_database(src, dump_path)
    stats = dump_size_and_tables(dump_path)
    print(f"   dump stats: {stats}")
print()


# ============================================================
# 3. The restore drill - the only proof a backup works
# ============================================================
# A backup is not a file; it is a RESTORED database that matches the
# source. The drill: restore into a scratch instance and compare counts
# and checksums against the source. Automate it; run it on a schedule.


def restore_database(dump_path: Path, target: sqlite3.Connection) -> int:
    """Apply a logical dump to a fresh database (the restore)."""
    sql = dump_path.read_text(encoding="utf-8")
    target.executescript(sql)
    target.commit()
    return target.execute("SELECT COUNT(*) FROM books").fetchone()[0]


def verify_restore(src: sqlite3.Connection, restored: sqlite3.Connection) -> list[str]:
    """Compare source and restored DB. Empty list = verified backup."""
    problems = []
    for table in ("books", "editions", "permissions"):
        c_src = src.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        c_new = restored.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        if c_src != c_new:
            problems.append(f"{table}: source={c_src} restored={c_new}")
    # content spot-check: the corpus text must survive byte-for-byte
    t_src = src.execute("SELECT title FROM books WHERE id=1").fetchone()[0]
    t_new = restored.execute("SELECT title FROM books WHERE id=1").fetchone()[0]
    if t_src != t_new:
        problems.append(f"content drift: {t_src!r} != {t_new!r}")
    return problems


print("3. restore drill + verification")
with tempfile.TemporaryDirectory() as tmp:
    dump_path = Path(tmp) / "catalog_dump.sql"
    dump_database(src, dump_path)
    restored = sqlite3.connect(":memory:")
    restore_database(dump_path, restored)
    problems = verify_restore(src, restored)
    print(f"   restore problems: {problems or 'none - backup VERIFIED'}")
print()


# ============================================================
# 4. Granularity: point-in-time vs nightly (RPO)
# ============================================================
# RPO (Recovery Point Objective) = how much data you can afford to
# LOSE. RTO (Recovery Time Objective) = how fast you must be BACK.
# A nightly dump has RPO=24h. If the catalog is edited all day, a
# nightly dump is not enough: you need WAL archiving (PITR) so you can
# replay to any second.

RPO_TABLE = [
    ("nightly pg_dump", "24 hours", "hours", "small catalogs, read-mostly"),
    ("hourly pg_dump + WAL", "1 hour", "minutes", "active catalog"),
    ("continuous WAL shipping", "seconds", "minutes", "mission-critical"),
    ("sync replica + PITR", "~0", "seconds", "zero-loss requirement"),
]

print("4. backup granularity vs RPO/RTO")
print(f"   {'strategy':30} {'RPO':12} {'RTO':10} use case")
for strat, rpo, rto, use in RPO_TABLE:
    print(f"   {strat:30} {rpo:12} {rto:10} {use}")
print()


# ============================================================
# 5. The 3-2-1 rule and what else must be backed up
# ============================================================
# 3 copies, on 2 media types, 1 offsite. But the DATA is not the whole
# story: a restored database without the config, the migrations history,
# and the embedding-model version is an orphan. Back up with the
# database:
#   - the migration chain (alembic_version state + files)
#   - config and secrets reference (NOT the secrets in plaintext)
#   - the vector index is DERIVED - rebuilt from the source, not backed up
#   - a restore runbook with the drill commands

BACKUP_CHECKLIST = [
    ("data dumps", "yes", "nightly + before every migration"),
    ("WAL archive", "if RPO < 24h", "continuous"),
    ("migration files + version", "yes", "they ARE the schema"),
    ("config/secrets references", "references only", "secrets live in the vault"),
    ("vector index", "NO - derived", "rebuilt from source via lineage refs"),
    ("restore runbook", "yes", "with drill results and dates"),
]

print("5. 3-2-1 and the full backup surface")
for item, answer, note in BACKUP_CHECKLIST:
    print(f"   {item:28} {answer:18} {note}")
print()


# ============================================================
# 6. Disaster scenario: what restores look like under pressure
# ============================================================
# Scenario: 14:32 a bad migration drops the permissions table content.
# The drill we already ran says the nightly dump is verified and takes
# 38s to restore. Now the runbook is executable:
#   1. stop writes (read-only mode)
#   2. restore last good dump
#   3. replay WAL to 14:31
#   4. verify counts + spot-check content
#   5. resume, then root-cause the migration
# The drill is why step 4 takes seconds instead of being a surprise.


def disaster_recovery_sim() -> dict[str, object]:
    """Simulate: data loss at 14:32, restore from verified dump."""
    live = sqlite3.connect(":memory:")
    seed_catalog(live)
    with tempfile.TemporaryDirectory() as tmp:
        dump = Path(tmp) / "pre_incident.sql"
        dump_database(live, dump)
        # incident: content wiped
        live.execute("DELETE FROM books")
        live.commit()
        lost = live.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        # recovery: restore the verified dump into a scratch, verify, swap
        scratch = sqlite3.connect(":memory:")
        restore_database(dump, scratch)
        problems = verify_restore(src, scratch)
        recovered = scratch.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        return {"lost_rows": lost, "recovered_rows": recovered, "verify_problems": problems}


print("6. disaster recovery simulation")
report = disaster_recovery_sim()
print(f"   {report}")
print()


# ============================================================
# 7. Real Postgres tooling (text reference)
# ============================================================
# The sqlite3 mechanics above map 1:1 to the Postgres stack:
#
#   pg_dump -Fc -f catalog.dump dbname           # logical, compressed
#   pg_restore -d catalog_new catalog.dump       # restore to scratch
#   pg_dump -Fc -f - dbname | ssh host pg_restore -d replica  # streaming
#
#   # PITR: archive_command in postgresql.conf + recovery
#   archive_mode = on
#   archive_command = 'cp %p /archive/%f'
#   restore_command = 'cp /archive/%f %p'
#   recovery_target_time = '2026-08-17 14:31:00'
#
#   # physical backups + PITR
#   pgBackRest stanza-create / stanza-archive / stanza-backup
#
# # restore drill (automate this):
#   createdb catalog_drill
#   pg_restore -d catalog_drill catalog.dump
#   psql -d catalog_drill -c "SELECT count(*) FROM books;"

print("7. real Postgres tooling (see file header for commands)")
print()


# ============================================================
# 8. Self-verification
# ============================================================


def _verify() -> bool:
    checks: list[tuple[str, bool]] = []
    conn = sqlite3.connect(":memory:")
    seed_catalog(conn)

    with tempfile.TemporaryDirectory() as tmp:
        dump = Path(tmp) / "v.sql"
        size = dump_database(conn, dump)
        checks.append(
            (
                "dump is non-empty and parseable",
                size > 0 and "CREATE TABLE" in dump.read_text(encoding="utf-8"),
            )
        )

        scratch = sqlite3.connect(":memory:")
        n = restore_database(dump, scratch)
        checks.append(("restore recreates rows", n == 2))
        checks.append(("restore verifies clean", verify_restore(conn, scratch) == []))

    report = disaster_recovery_sim()
    checks.append(
        (
            "disaster: data recovered",
            report["lost_rows"] == 0
            and report["recovered_rows"] == 2
            and report["verify_problems"] == [],
        )
    )

    # corrupt-dump detection: truncated file must NOT verify
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "truncated.sql"
        good = Path(tmp) / "good.sql"
        dump_database(conn, good)
        bad.write_text(
            good.read_text(encoding="utf-8")[: len(good.read_text(encoding="utf-8")) // 2],
            encoding="utf-8",
        )
        scratch = sqlite3.connect(":memory:")
        try:
            restore_database(bad, scratch)
            checks.append(("truncated dump detected", verify_restore(conn, scratch) != []))
        except sqlite3.Error:
            checks.append(("truncated dump detected", True))

    ok = True
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    return ok


if __name__ == "__main__":
    if "--verify" in sys.argv:
        print("Verification:")
        sys.exit(0 if _verify() else 1)
    print("Verification (python 07-backup-and-restore.py --verify):")
    _verify()
