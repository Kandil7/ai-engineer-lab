# Postgres 06: Connection Pooling — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Connection pool | Warm sessions lent to requests, then returned | pool of 10 |
| Checkout | Borrowing a session; times out loudly when exhausted | 30 s timeout |
| Pool sizing | Concurrency-derived session count, verified under load | 5–20 for small API |
| pgbouncer | External multiplexer: many app conns, few server sessions | transaction mode |
| Session mode | Server session pinned per client connection | safe, modest gains |
| Transaction mode | Server session reassigned per transaction | big gains, session-state breaks |
| Leak | Borrowed-never-returned session draining the pool | idle-in-transaction growth |

---

## Alphabetical Glossary

### Checkout

**Definition:** Taking a session from the pool for one unit of work. Bounded
by a timeout so exhaustion raises instead of hanging forever.

**Example:**
```python
with pool.connection() as conn:  # timed out loudly past 30 s
```

**Related concepts:** Connection pool, Leak

---

### Connection pool

**Definition:** A bounded set of open sessions reused across requests.
Amortizes handshake cost and caps database concurrency at the right boundary.

**Example:**
```python
ConnectionPool(DSN, min_size=2, max_size=10, timeout=30.0)
```

**Related concepts:** Checkout, Pool sizing

---

### Leak

**Definition:** A session checked out and never returned. Presents as pool
exhaustion under flat traffic; diagnosed via pool stats + pg_stat_activity.

**Example:**
```python
# checked-out climbs, traffic flat -> something holds sessions open
```

**Related concepts:** Checkout, pg_stat_activity

---

### pgbouncer

**Definition:** External connection pooler multiplexing thousands of client
connections onto tens of server sessions. The standard Postgres scaling
companion.

**Example:**
```python
# app -> pgbouncer (5000 conns) -> postgres (40 sessions)
```

**Related concepts:** Session mode, Transaction mode

---

### Pool sizing

**Definition:** Choosing session count from workload concurrency (request
concurrency × fraction in-query), verified under load — never from hardware
or worker count alone.

**Example:**
```python
# 50 rps x 20% in-query ~= 10 sessions, not 100 workers
```

**Related concepts:** Connection pool, Checkout

---

### Session mode

**Definition:** pgbouncer mode pinning one server session per client
connection. Compatible with session state; modest multiplexing gains.

**Example:**
```python
# prepared statements and LISTEN survive here
```

**Related concepts:** Transaction mode, pgbouncer

---

### Transaction mode

**Definition:** pgbouncer mode reassigning server sessions per transaction.
Large gains; breaks prepared statements, advisory locks, LISTEN, temp tables.

**Example:**
```python
# standard with short transactions; audit session-state usage first
```

**Related concepts:** Session mode, pgbouncer

---

## Related Concepts

- **pg_stat_activity**: the server-side leak detector
- **Lifespan startup**: pool created once in FastAPI lifespan (week 4)
- **max_connections**: the cap pools exist to respect (topic 01)

## Key Takeaways

1. Pool at the database boundary, size from concurrency.
2. Timeouts turn hangs into alerts.
3. Mode choice is a compatibility audit.
