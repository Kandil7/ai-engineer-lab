# Challenge 11: Migrations and Schema Evolution — The Edition Migration

An Athar catalog adds an `edition` column to its sources table while ingest
workers keep writing. If the change is one big ALTER, the workers break. If the
index rebuild loses `source_ref`, citations die. Do it right.

## 🥉 Bronze — The Revision Chain (~15 min)

**Task:** Implement `run_chain(conn, chain, target_revision)`, applying
migration steps in order to reach a target revision: `chain` is a list of
`(revision_id, upgrade_fn, downgrade_fn)`; each function takes the sqlite
connection. Track the current revision in a `chain_state` table and apply
`upgrade_fn` forward or `downgrade_fn` backward as needed. Returns the current
revision (`""` for base).

**Signature:**
```python
def run_chain(conn, chain: list[tuple[str, Callable, Callable]], target: str) -> str
```

| Input | Expected |
|---|---|
| 3-step chain, target "v3" | upgrades applied in order, returns "v3" |
| already at "v3", target "v3" | no-op, returns "v3" |
| at "v3", target "v1" | downgrades applied in reverse, returns "v1" |
| target "" | full downgrade to base |

**Constraints:** linear chain. Any correct bookkeeping passes.

---

## 🥈 Silver — Expand → Backfill → Contract (~35 min)

**Task:** Implement `expand_backfill_contract(conn, phase)`, where `phase` is
`"expand"`, `"backfill"`, or `"contract"`:
- **expand** — add a nullable `edition` column to `sources` if missing. A
  legacy writer inserting without `edition` must still succeed afterwards.
- **backfill** — fill NULL `edition` values with `'default'`, leaving explicit
  editions untouched. Idempotent: running twice changes nothing further.
- **contract** — raise `ValueError` if any `edition` is still NULL (you may not
  tighten before backfilling), then create a unique index on
  `(book, edition, page)`.

**Signature:**
```python
def expand_backfill_contract(conn, phase: str) -> None
```

| Scenario | Expected |
|---|---|
| expand then legacy insert (no edition) | insert succeeds |
| backfill twice | same row count; explicit edition preserved |
| contract with NULLs remaining | raises ValueError |
| contract after clean backfill | unique index rejects duplicate (book, edition, page) |

**Constraints:** populated table. **Guard:** a naive one-shot
`ALTER TABLE ... NOT NULL` fails the legacy-insert check; an unconditional
`UPDATE sources SET edition='default'` clobbers the explicit edition and fails
the preservation check. **Adversarial case:** rows with Arabic page text and
NULL edition mixed with rows that already carry an edition.

---

## 🥇 Gold — Rebuild Preserving Lineage (~75 min)

**Task:** Implement `rebuild_index_preserving_lineage(conn, edits)`, applying
`edits: dict[source_ref -> new_text]` as in-place UPDATEs (never
DELETE+INSERT), then rebuilding the derived `idx` table from `sources`. Return
the number of resolvable refs (idx rows whose `source_ref` exists in
`sources`), which must equal the row count.

**Signature:**
```python
def rebuild_index_preserving_lineage(conn, edits: dict[str, str]) -> int
```

| Input | Expected |
|---|---|
| 50k rows, 1 edit | returns 50000; every ref resolves |
| edit a row's text | updated text in idx; row count unchanged |
| empty edits | pure rebuild, count preserved |

**Constraints:** 50k rows, memory ceiling 8 MB peak (`tracemalloc`) —
`fetchall()` of the whole table blows it. **Guard (statement budget):** a spy
on `conn.execute` asserts ≤ `3 * ceil(n / 1000) + 5` statements — the per-row
Python rebuild loop (~50k statements) fails; set-based SQL (`INSERT INTO idx
SELECT ...`) passes. **Follow-up:** what breaks first at 10^8 rows? *(Answer:
rebuild duration and lock windows — you need incremental rebuild or parallel
workers, and the runbook must say which.)*

---

## Running

```bash
python -m pytest 04-databases/sqlalchemy/challenges/11-migrations-alembic/test_challenge.py -q
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 04-databases/sqlalchemy/challenges/11-migrations-alembic/test_challenge.py -q
```
