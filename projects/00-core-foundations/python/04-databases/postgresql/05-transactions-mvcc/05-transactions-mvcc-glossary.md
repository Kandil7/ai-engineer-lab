# Postgres 05: Transactions and MVCC — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| ACID | Atomicity, Consistency, Isolation, Durability | commit guarantees |
| WAL | Write-ahead log making commits durable + replayable | crash recovery |
| Isolation level | How strictly concurrent transactions appear ordered | read committed…serializable |
| MVCC | Multi-version concurrency: snapshots isolate readers | no read locks |
| Deadlock | Two transactions waiting on each other's locks | abort + retry victim |
| Savepoint | Named sub-transaction point for partial rollback | bulk-load tolerance |
| VACUUM | Reclaims dead row versions MVCC leaves behind | bloat control |

---

## Alphabetical Glossary

### ACID

**Definition:** The commit contract: atomic all-or-nothing, consistent
constraints, ordered-appearing concurrency, disk-durable results.

**Example:**
```python
# eval run + scores commit together or not at all
```

**Related concepts:** WAL, Isolation level

---

### Deadlock

**Definition:** Cyclic lock wait between transactions. Postgres detects it,
aborts one participant; application code retries the victim.

**Example:**
```python
# lock rows in consistent order everywhere to prevent the cycle
```

**Related concepts:** Isolation level, Savepoint

---

### Isolation level

**Definition:** The strictness of apparent transaction ordering: READ
COMMITTED (per-statement snapshots), REPEATABLE READ (per-transaction),
SERIALIZABLE (strict order, abort on hazard + retry).

**Example:**
```python
# reports: REPEATABLE READ — web writes: READ COMMITTED default
```

**Related concepts:** MVCC, ACID

---

### MVCC

**Definition:** Multi-Version Concurrency Control: readers see snapshots,
writers create new versions. No read locks; dead versions need VACUUM.

**Example:**
```python
# SELECT never waits on concurrent UPDATE of the same rows
```

**Related concepts:** VACUUM, Isolation level

---

### Savepoint

**Definition:** A marker inside a transaction allowing rollback to that point
without aborting everything. Bulk-load error tolerance.

**Example:**
```sql
SAVEPOINT bulk_part; ... ROLLBACK TO SAVEPOINT bulk_part;
```

**Related concepts:** Deadlock, ACID

---

### VACUUM

**Definition:** Reclamation of dead row versions. Blocked globally by the
oldest open transaction — hence: never hold transactions open.

**Example:**
```python
# pg_stat_activity: one idle txn pins the horizon, bloat grows
```

**Related concepts:** MVCC

---

### WAL

**Definition:** Write-Ahead Log: every change hits the log before data pages.
Makes commits durable and crash recovery a replay.

**Example:**
```python
# committed = in WAL = survives a crash mid-checkpoint
```

**Related concepts:** ACID

---

## Related Concepts

- **pg_stat_activity**: live view naming stuck transactions
- **Autocommit**: psycopg3 defaults to blocks — commit explicitly
- **Idempotency**: retry-safe writes for deadlock victims (week 4 API)

## Key Takeaways

1. Four letters, four mechanisms.
2. Snapshots free readers; horizons punish idlers.
3. Short transactions, ordered locks, explicit commits.
