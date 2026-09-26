# Databases — PG05: Transactions and MVCC

## Topic Overview

Eval runs, ingest jobs, and concurrent API writes share one database, so
"it worked in my test" means nothing without transaction semantics. This
lecture covers ACID in Postgres terms, isolation levels, MVCC snapshots
(the reason readers never block writers), and the deadlock/long-transaction
failures that arrive exactly when the system gets busy.

## Learning Objectives

By the end of this lecture, you will be able to:

1. State ACID and map each letter to a Postgres mechanism (WAL, locks, MVCC)
2. Choose READ COMMITTED vs REPEATABLE READ vs SERIALIZABLE deliberately
3. Explain MVCC snapshots: why readers never block writers
4. Write correct BEGIN/COMMIT/ROLLBACK with savepoints for partial retry
5. Diagnose deadlocks and runaway transactions from pg_stat_activity

## Prerequisites

| Need | Where |
|---|---|
| Connections and cursors | [01](01-setup-and-psycopg-lecture.md) |
| Basic DML | `sql-fundamentals/03-insert-update-delete/` |
| The runnable exercise | [05-transactions-mvcc.py](05-transactions-mvcc.py) |

## 1. ACID, Concretely

Atomicity (all-or-nothing via WAL replay), Consistency (constraints hold
across the commit boundary), Isolation (concurrent transactions behave as if
ordered — degree chosen below), Durability (committed means on disk, WAL
first). Each letter is a mechanism, not a vibe; when someone says "Postgres
is safe," these four are the receipt.

```python
with psycopg.connect(DSN) as conn:   # commit on clean exit, rollback on error
    with conn.cursor() as cur:
        cur.execute("INSERT INTO eval_runs ...")
        cur.execute("INSERT INTO eval_scores ...")
# both rows or neither — the harness never records half a run
```

## 2. Isolation Levels

READ COMMITTED (default): each statement sees fresh committed data —
right for most web writes. REPEATABLE READ: one snapshot per transaction —
right for reports that must not shift mid-read. SERIALIZABLE: transactions
behave as strictly ordered, aborting on serialization hazards — right for
money-like invariants, with application retry on abort. Stronger levels cost
concurrency; pick the weakest level your invariant survives.

## 3. MVCC: Readers Never Block Writers

Postgres keeps old row versions until no snapshot needs them. A SELECT reads
its snapshot's version while concurrent UPDATEs write new ones — no read
locks, no waiting. The price: dead versions accumulate (bloat) until VACUUM
reclaims them, which is why long-open transactions are poison — one idle
transaction pins the horizon and blocks cleanup for everyone.

## 4. Deadlocks and Runaway Transactions

Two transactions locking rows in opposite order deadlock; Postgres detects
and aborts one (your code retries the victim — design for it). Diagnose from
`pg_stat_activity`: `state`, `query_start`, and `wait_event_type` name the
stuck. Prevention beats cure: lock in consistent order, keep transactions
short, never hold one open across a network call to an LLM API.

```python
# SAVEPOINT: retry one statement without aborting the whole transaction
cur.execute("SAVEPOINT bulk_part")
try:
    cur.execute("INSERT ...")   # may hit a unique violation on one row
except UniqueViolation:
    cur.execute("ROLLBACK TO SAVEPOINT bulk_part")  # rest of the batch survives
```

## Common Mistakes

- Holding a transaction open across an LLM call (pins vacuum, blocks DDL).
- Catching deadlock aborts without retry (the victim must re-run).
- SERIALIZABLE everywhere "to be safe" (throughput dies, aborts multiply).
- Assuming autocommit: psycopg3 defaults to transactional blocks — commit explicitly.

## DevMate Connection

Eval runs write run + scores atomically (section 1's shape); the ingest job
batches chunk inserts with savepoint-tolerant bulk loads; the API never holds
a transaction across a model call — that rule, from section 4, is what keeps
week-4 latency intact under concurrent `/ask` traffic.

## Key Takeaways

1. ACID is four mechanisms; know each by name.
2. Weakest isolation your invariant survives.
3. Readers don't block writers; long transactions still poison vacuum.
4. Deadlock victims retry by design; transactions never span network calls.
