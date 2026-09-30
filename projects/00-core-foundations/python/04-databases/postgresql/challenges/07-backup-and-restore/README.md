# Challenge 07: Backup and Restore — The Restore Drill

A backup is not a file — it is a restored database that matches the source. An
Athar catalog dump sits on disk; nobody has ever restored it. Now a migration
goes wrong at 14:32 and the runbook must be real.

## 🥉 Bronze — Dump and Restore (~15 min)

**Task:** Implement `dump_and_restore(src_conn, dump_path, dst_conn)`, writing a
logical dump of `src_conn` to `dump_path` (SQL text via `iterdump`), executing
it on `dst_conn`, and returning `{"tables": {name: row_count}}` for the
restored database.

**Signature:**
```python
def dump_and_restore(src_conn, dump_path, dst_conn) -> dict
```

| Input | Expected |
|---|---|
| 2 tables, 3+5 rows | `{"tables": {"books": 3, "editions": 5}}` |
| empty database | `{"tables": {}}` |

**Constraints:** sqlite3 connections. Any correct approach passes.

---

## 🥈 Silver — Verify by Comparison (~35 min)

**Task:** Implement `verify_restore(src_conn, dst_conn)`, comparing row counts
per table AND sampled text content byte-for-byte. Return violation strings
(empty list = verified). Must detect corruption at **identical row counts**.

**Signature:**
```python
def verify_restore(src_conn, dst_conn) -> list[str]
```

| Scenario | Expected |
|---|---|
| clean restore | `[]` |
| one row's text flipped, same count | a violation naming the table |
| row-count mismatch | a violation with both counts |
| table missing in dst | a violation naming the table |

**Constraints:** 20k rows. **Guard (statement budget):** a spy on
`dst_conn.execute` asserts ≤ `4 * num_tables` statements — a per-row Python
compare loop issues ~20k queries and fails. **Adversarial case:** tampering
that preserves row counts (content drift only) — an "exit status == 0" or
count-only verifier misses it entirely.

---

## 🥇 Gold — Point-in-Time Recovery (~75 min)

**Task:** Implement `point_in_time_recovery(base_dump, wal_records,
target_version, dst_conn)`, restoring the base SQL then replaying only redo
records `(version, sql)` with `version <= target_version`, in version order,
applying each **at most once** (WAL redelivers duplicates). Return
`{"applied": int, "skipped": int, "final_version": int}` where `skipped` counts
records after the target and duplicates.

**Signature:**
```python
def point_in_time_recovery(base_dump: str, wal_records: list[tuple[int, str]],
                           target_version: int, dst_conn) -> dict
```

| Input | Expected |
|---|---|
| delete at v7, restore at v9, target 8 | delete visible; no v9 row |
| duplicate redo records | applied once; rest skipped |
| out-of-order input | version order governs |
| target below all versions | `applied == 0` |

**Constraints:** 20k WAL records. **Guards:** (a) correctness at the target
version — a naive "apply all" shows the v9 row and fails; (b) **statement
budget** — a spy counts `execute` calls: exactly `applied + 1` data statements
(base + one per applied record); re-applying duplicates fails the count;
(c) out-of-order input must not corrupt state. **Follow-up:** what breaks first
at 10^9 WAL records? *(Answer: replay duration and storage — you need
checkpointed base backups so replay is bounded to the delta since the last
checkpoint.)*

---

## Running

```bash
python -m pytest 04-databases/postgresql/challenges/07-backup-and-restore/test_challenge.py -q
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 04-databases/postgresql/challenges/07-backup-and-restore/test_challenge.py -q
```
