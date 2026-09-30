# PostgreSQL 04: Connection Pooling

## Topic Overview

Opening a database connection is expensive: it involves a network handshake, authentication, and
session setup. A pool keeps a set of connections open and hands them out on demand, turning a per-
request cost into a one-time cost. Without a pool, a service under load spends its time opening
connections instead of doing work, and the database spends its connections on churn instead of queries.

This lecture covers why connections are pooled, the pool settings and how to tune them, the discipline
of returning connections, connection leaks, and choosing a pooling library.

The core discipline is symmetric: acquire, use, release. A connection that is acquired and not released
is a leak, and enough leaks exhaust the pool and hang every request. Context managers and try/finally
are what make the release happen even on error.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why connections are pooled.
2. Set the pool size and timeouts for a workload.
3. Return connections to the pool reliably.
4. Detect and avoid connection leaks.
5. Choose a pooling library.
6. Explain the relationship between pool size and database load.

## Prerequisites

- PostgreSQL 01 to 03.
- Basic concurrency (a pool is a shared, bounded resource).

---

## 1. Why Pool

### The cost

Opening a connection involves a handshake, authentication, and setup, all of which cost time and
database resources. A pool opens a set of connections once and reuses them:

```text
without a pool: request -> open connection -> query -> close   (every request)
with a pool:    request -> borrow -> query -> return           (reused)
```

### The buffer

The pool is the buffer between the application's demand and the database's capacity. It absorbs bursts
and smooths the load, which is what keeps a service responsive under concurrency.

### The exit test

The roadmap's exit test is that connections are pooled. A service opening a connection per request is a
service that will fall over at load.

## 2. Pool Settings

### The settings

- **Minimum size:** connections kept ready.
- **Maximum size:** the cap on concurrent connections.
- **Max idle time:** how long an idle connection is kept before closing.
- **Connection timeout:** how long a request waits for a connection before failing.

| Setting | Value | Rationale |
| --- | --- | --- |
| Min connections | 2 | Always ready |
| Max connections | 10 | Caps database load |
| Max idle time | 5 min | Releases unused |
| Connection timeout | 10 sec | Fails fast |

### Why tune

The settings are tuned to the workload, not guessed. A pool larger than the database can serve causes
connection contention; a pool too small leaves requests waiting. The maximum should be set against the
database's connection limit, which is a shared resource across all services.

### The timeout

The connection timeout is what makes an overloaded pool fail fast instead of hanging. A request that
waits forever for a connection is worse than one that fails with a clear error, because the hang
consumes a worker.

## 3. Returning Connections

### The lifecycle

A connection is borrowed, used, and returned:

```python
assert pool.acquire()
# ... use the connection ...
pool.release()
assert pool.acquire(), "returned connection is available again"
```

Returning it makes it available for the next request. There is no other way the pool grows back.

### The context manager

Use a context manager or try/finally so the release happens even when the work raises. This is the
discipline that prevents most leaks:

```python
with pool.connection() as conn:
    conn.execute(...)  # released on exit, success or failure
```

### The exit test

The roadmap's exit test is that connections are returned to the pool. It is a discipline, not a
feature, and the context manager is how the discipline is enforced.

## 4. Connection Leaks

### What a leak is

A leak happens when a connection is acquired and never returned:

```python
pool2 = Pool(size=1)
assert pool2.acquire()
assert pool2.exhausted(), "borrowed without return -> exhausted"
assert not pool2.acquire()
```

The pool shrinks until it is exhausted, and requests hang. A slow leak is hard to diagnose because the
service works until it suddenly does not.

### The causes

Leaks come from a connection acquired on an error path that skips the release, a connection stored and
forgotten, or an exception between acquire and release without a finally.

### The fix

Context managers and try/finally make the release unconditional. The fix is structural, not
vigilance-based, because vigilance fails under pressure.

## 5. Choosing a Library

### The options

Python uses `asyncpg` or `psycopg` with a pool; Go uses `pgxpool`. The library handles the pool
mechanics; the application handles the discipline.

### What the library does not do

It does not enforce that you return connections; a leaked connection is still leaked. The library
provides the context manager; using it is the application's job.

### The rule

Use the pool, return the connections. The library and the discipline together make the connection
handling safe.

## 6. The Exercise

### What it models

The exercise models a pool with a fixed size, acquire/release, exhaustion, and a leak.

### The assertions

```python
assert pool.acquire() and pool.acquire()
assert not pool.acquire(), "pool exhausted at max size"
pool.release()
assert pool.acquire(), "returned connection is available again"
```

The leak case shows exhaustion when a connection is borrowed and never returned, and the release
restoring capacity.

## Real-World Application

- A FastAPI service using an async connection pool so each request borrows a connection and returns it.
- Setting the pool's maximum against the database's connection limit so the service cannot exhaust it.
- A connection timeout so an overloaded pool fails fast instead of hanging requests.
- Using a connection context manager so an error path cannot leak a connection.

## Common Mistakes

1. **Opening a connection per request.** The handshake cost dominates.
2. **Never returning connections.** Leaks exhaust the pool.
3. **Pool size guessed, not tuned.** Too large causes contention; too small causes waits.
4. **No timeouts.** Requests hang when the pool is empty.
5. **Ignoring the database's connection limit.** The pool can exhaust the shared resource.
6. **Acquiring without a context manager.** An error path leaks.

## Key Takeaways

1. A pool reuses connections instead of reopening them, turning a per-request cost into a one-time one.
2. Pool settings are tuned to the workload and bounded by the database's connection limit.
3. A connection is borrowed, used, and returned; the release must be unconditional.
4. Leaks exhaust the pool and hang requests; context managers prevent them.
5. Use the pool and return the connections; the library cannot enforce the discipline for you.

## Self-Check Questions

1. What does opening a connection cost, and how does a pool change it?
2. Why should the pool's maximum respect the database's connection limit?
3. Why is a connection timeout necessary under load?
4. What causes a connection leak, and how does a context manager prevent it?
5. Why does the library not eliminate the need for the return discipline?

## Further Reading / Connections

- PostgreSQL 01-03 — the schema and migrations the connections serve.
- Embeddings 02 (batch processing) — concurrency and bounded resources.
- RAG System 02 (hard filters) — the same bounded-resource discipline for retrieval.
- `docs/cheat-sheets/postgres.md` — the command reference.
