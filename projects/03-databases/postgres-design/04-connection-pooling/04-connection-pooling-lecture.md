# PostgreSQL 04: Connection Pooling

## 🎯 Topic Overview

Opening a database connection is expensive. A pool keeps a set of
connections open and hands them out on demand. This lecture covers the
pool, its settings, and the discipline of returning connections.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why connections are pooled
2. Set the pool size and timeouts
3. Return connections to the pool
4. Avoid connection leaks
5. Choose a pooling library

---

## 1. Why Pool

Opening a connection involves a handshake, authentication, and setup —
expensive per request. A pool opens a set of connections once and reuses
them. The pool is the buffer between the application's demand and the
database's capacity. The roadmap's exit test: "connections are pooled."

## 2. Pool Settings

The pool has a minimum and maximum size, idle time, and timeouts. The
minimum keeps connections ready; the maximum caps the database load. The
timeouts fail fast instead of hanging. The settings are tuned to the
workload, not guessed.

| Setting | Value | Rationale |
|---------|-------|-----------|
| Min connections | 2 | Always ready |
| Max connections | 10 | Caps database load |
| Max idle time | 5 min | Releases unused |
| Connection timeout | 10 sec | Fails fast |

## 3. Returning Connections

A connection is borrowed, used, and returned. Returning it makes it
available for the next request. A connection that is not returned is
leaked — the pool shrinks until it is exhausted. The roadmap's exit test:
"connections are returned to the pool."

## 4. Connection Leaks

A leak happens when a connection is checked out and never returned. The
pool eventually runs dry and requests hang. The fix is discipline: use
context managers or try/finally so the return always happens, even on
error.

## 5. Choosing a Library

Python uses asyncpg or psycopg with a pool; Go uses pgxpool. The library
handles the pool mechanics; the application handles the discipline. The
roadmap's rule: "use the pool, return the connections."

## Common Mistakes

- Opening a connection per request.
- Never returning connections (leaks).
- Pool size guessed, not tuned.
- No timeouts (requests hang).
- Ignoring the pool's health.

## Key Takeaways

1. A pool reuses connections instead of reopening them.
2. Pool settings are tuned to the workload.
3. A connection is borrowed, used, and returned.
4. Leaks exhaust the pool.
5. Use the pool, return the connections.