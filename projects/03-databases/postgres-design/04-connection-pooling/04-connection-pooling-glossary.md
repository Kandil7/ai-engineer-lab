# PostgreSQL 04: Connection Pooling — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Pool | A set of open connections reused on demand | min/max size |
| Borrow | Checking a connection out of the pool | use it |
| Return | Giving the connection back | available again |
| Leak | A connection never returned | pool exhausts |
| Min connections | Always-ready floor | 2 |
| Max connections | The database load cap | 10 |
| Timeout | Fails fast instead of hanging | 10 sec |

---

## Alphabetical Glossary

### Borrow

**Definition:** Checking a connection out of the pool for one request. The
connection is used, then returned.

**Example:**
```python
conn = pool.acquire()
```

**Related concepts:** Return, Leak

---

### Leak

**Definition:** A connection checked out and never returned. The pool
shrinks until it is exhausted and requests hang.

**Example:**
```python
# acquire without release -> leak
```

**Related concepts:** Borrow, Return

---

### Max connections

**Definition:** The pool's upper bound, capping the database load. Tuned
to the workload, not guessed.

**Example:**
```python
pool = Pool(min_size=2, max_size=10)
```

**Related concepts:** Min connections

---

### Min connections

**Definition:** The always-ready floor of the pool. Keeps connections
available for immediate requests.

**Example:**
```python
pool = Pool(min_size=2)
```

**Related concepts:** Max connections

---

### Pool

**Definition:** A set of open connections reused on demand. The buffer
between application demand and database capacity.

**Example:**
```python
pool = Pool(min_size=2, max_size=10)
```

**Related concepts:** Borrow, Return

---

### Return

**Definition:** Giving a connection back to the pool after use. Makes it
available for the next request.

**Example:**
```python
pool.release(conn)
```

**Related concepts:** Borrow, Leak

---

### Timeout

**Definition:** The bound that fails fast instead of hanging. Connection
and statement timeouts prevent runaway waits.

**Example:**
```python
# connection timeout 10 sec
```

**Related concepts:** Pool

---

## Related Concepts

- **Schema design**: the pool serves the schema (topic 01)
- **Indexes**: pooled queries use the indexes (topic 02)
- **Redis**: caching reduces the load the pool serves (redis-cache 01)

## Key Takeaways

1. A pool reuses connections instead of reopening them.
2. Pool settings are tuned to the workload.
3. A connection is borrowed, used, and returned.
4. Leaks exhaust the pool.
5. Use the pool, return the connections.