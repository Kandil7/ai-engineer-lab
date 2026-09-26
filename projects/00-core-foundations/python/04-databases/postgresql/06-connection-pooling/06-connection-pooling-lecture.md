# Databases — PG06: Connection Pooling

## Topic Overview

Opening a Postgres connection costs milliseconds of handshake and a server
slot from a capped budget — per-request connections collapse under load.
Pooling keeps warm sessions and lends them out. This lecture covers pool
sizing from first principles, pgbouncer modes, application pools, and leak
detection: the operational end of the lifecycle from topic 01.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why per-request connections fail (handshake latency + slot exhaustion)
2. Size a pool from workers, latency, and concurrency instead of guessing
3. Choose pgbouncer session vs transaction mode (and state what breaks in each)
4. Configure an application pool (psycopg_pool / SQLAlchemy) with timeouts
5. Detect leaks from pool stats and `pg_stat_activity` before users do

## Prerequisites

| Need | Where |
|---|---|
| Connection lifecycle, max_connections | [01](01-setup-and-psycopg-lecture.md) |
| Transactions must stay short | [05](05-transactions-mvcc-lecture.md) |
| The runnable exercise | [06-connection-pooling.py](06-connection-pooling.py) |

## 1. Why Pool

A new connection pays TCP + TLS + auth handshake (single-digit ms locally,
far worse across zones) and occupies one of ~100 server slots. At 50
concurrent requests with per-request connections, the 101st waits or dies —
and connection storms after a deploy restart flatten the database before
traffic does. Pools amortize the handshake over hundreds of reuses and cap
concurrency at the database boundary, where the database — not the app — is
the scarce resource.

## 2. Sizing Without Superstition

Pool size follows the work, not the hardware: concurrent queries the database
should serve at once. Start from request concurrency × fraction actually in a
query (most request time is app/LLM work, not SQL), then verify under load:
pool exhaustion errors mean too small; idle sessions near pool size with slow
queries mean queries, not pool, are the problem. Standard starting shape for
a small API: pool of 5–20 with an overflow allowance and a checkout timeout
(30 s) so failures are loud instead of hangs.

```python
# psycopg_pool: bounded, timed out, closed structurally
from psycopg_pool import ConnectionPool
pool = ConnectionPool("postgresql://...", min_size=2, max_size=10, timeout=30.0)
with pool.connection() as conn:   # borrow; returned (or timed out loudly) after
    ...
pool.close()
```

## 3. pgbouncer Modes

External pooling (pgbouncer) multiplexes thousands of app connections onto
tens of server sessions. Session mode: one server session per client
connection for its life — safe, modest gains. Transaction mode: server
session reassigned per transaction — big gains, and anything bound to a
session breaks: prepared statements, advisory locks, LISTEN/NOTIFY,
temporary tables, `SET` state. The mode choice is a compatibility audit, and
transaction mode plus short transactions (topic 05's rule) is the standard
production combination.

## 4. Leaks: Detection Before Users

A leak is a borrowed-never-returned session: pool exhaustion with idle
traffic. Detect from both sides — pool stats (checked-out count climbing
while traffic is flat) and `pg_stat_activity` (sessions idle-in-transaction
far longer than any legitimate query). Prevention: checkout timeouts (fail
loud), `with` blocks (return structurally), and never holding a pooled
session across an LLM call — the topic-05 rule with dollar signs attached.

## Common Mistakes

- Pool sized == web workers "to be safe" (100 gunicorn workers × pool 20 = 2000 sessions vs 100 slots).
- No checkout timeout (exhaustion becomes a silent hang, not an alert).
- Transaction-mode pgbouncer + prepared statements (breaks mysteriously).
- Holding pooled sessions across model calls (leak-shaped latency).

## DevMate Connection

Week 4's FastAPI lifespan creates the pool once (`main.py`) and every
request borrows — the "loaded once at startup" pattern from the track.
Alembic migrations run outside the pool (DDL doesn't share nicely). The
load-test p50/p95 numbers in week 7 are meaningless without the pool config
recorded next to them: same queries, pool of 5 vs 50, different system.

## Key Takeaways

1. Pools amortize handshakes and cap database concurrency.
2. Size from workload concurrency; timeout checkouts so failures are loud.
3. pgbouncer transaction mode + short transactions is the standard combo.
4. Leaks are detected from pool stats and pg_stat_activity, prevented by structure.
