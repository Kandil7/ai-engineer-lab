# Databases — PG01: Setup and psycopg Connection

## Topic Overview

Every ML service that reads features or writes logs goes through a database
connection: stall the pool and you stall inference; leak cursors and you
exhaust the server. This lecture builds the connect-cursor-execute-close
mental model with sqlite3 as a zero-setup stand-in (identical semantics),
then shows the real psycopg3 code path for a live server.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Open, use, and always close a connection; explain why leaks are incidents
2. Read a DSN and state host, port, dbname, user for any connection string
3. Use `with` blocks so cleanup is structural, not remembered
4. Distinguish server-side from client-side cursors and pick correctly
5. Run the exercise with no server (sqlite stand-in) and against a real server

## Prerequisites

| Need | Where |
|---|---|
| Relational model basics | `sql-fundamentals/01-relational-model/` |
| The runnable exercise | [01-setup-and-psycopg.py](01-setup-and-psycopg.py) |
| A live server (optional) | `docker compose up -d postgres` (DevMate infra) |

## 1. The Lifecycle: Connect, Work, Close

A connection is a network session, and Postgres caps them (default
`max_connections = 100`). The universal pattern never varies:

```python
import sqlite3  # stand-in: identical connect/cursor semantics, zero setup

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("SELECT 1")
conn.close()  # ALWAYS — a leaked connection is a future outage
```

Prefer `with` blocks: the close happens on every path, including exceptions.
Cleanup that depends on memory is a bug with a delay timer.

## 2. DSN Anatomy

```python
# postgresql://user:password@host:port/dbname?sslmode=require
#  scheme      auth              host  port  db     options
```

Read any DSN left to right: who is connecting, to which host and port, which
database, with what options. `sslmode=require` in production is not optional;
neither is keeping the password in env, never in code.

## 3. Server-Side vs Client-Side Cursors

Default (client-side) cursors fetch the whole result into the client —
simple, deadly on million-row results. Server-side (named) cursors stream:
the server holds the portal, the client pages through. Rule: aggregates and
small reads use default cursors; bulk exports and ETL use server-side. The
exercise demonstrates both against the stand-in and gates the psycopg3
section behind a live server, printing `[skip]` otherwise.

## 4. psycopg3 on a Live Server

```python
import psycopg  # only when a server exists; never import-crash otherwise

with psycopg.connect("postgresql://devmate:secret@localhost:5432/devmate") as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        print(cur.fetchone())
```

Same shape as the stand-in: connect, cursor, execute, close — the ORM and
the pool (topic 06) wrap this, they don't replace it.

## Common Mistakes

- Opening a connection per request without a pool (topic 06 fixes this).
- Forgetting `close()` on the error path — use `with`.
- Fetching unbounded results into a default cursor (OOM with extra steps).
- Credentials in code or committed `.env` files.

## DevMate Connection

Week 4 persistence (`devmate/src/devmate/db/`, Alembic migrations) sits on
this lifecycle via SQLAlchemy — but every pool misbehavior you will debug
there reduces to a leaked connection or an unbounded fetch from this
lecture. The SQL sprint's "most expensive queries" view reads `pg_stat`
through a connection managed exactly this way.

## Key Takeaways

1. Connect, work, close — structurally, with `with`.
2. Read any DSN left to right; secrets live in env.
3. Big results stream via server-side cursors.
4. sqlite3 teaches the shape; psycopg3 runs it against the server.
