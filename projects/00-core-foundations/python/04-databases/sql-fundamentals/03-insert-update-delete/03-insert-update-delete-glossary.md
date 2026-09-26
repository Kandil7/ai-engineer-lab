# SQL 03: INSERT UPDATE DELETE — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| DML | Data Manipulation Language: rows, not shapes | INSERT/UPDATE/DELETE |
| INSERT | Adds rows; RETURNING hands back generated values | new conversation |
| RETURNING | Clause returning written rows without a second query | new id in one round trip |
| Upsert | Insert-or-update on conflict (ON CONFLICT) | idempotent ingest |
| Bulk insert | Multi-row writes in one statement/transaction | chunk loading |
| UPDATE | Modifies rows matching WHERE; omitted WHERE hits all | scoped writes only |
| DELETE | Removes rows matching WHERE; omitted WHERE empties | guarded deletes |

---

## Alphabetical Glossary

### Bulk insert

**Definition:** Writing many rows in one statement or transaction instead of
per-row round trips. Orders-of-magnitude faster ingest; the chunk-loading
pattern.

**Example:**
```python
cur.executemany("INSERT INTO chunks ...", rows)  # one trip, not N
```

**Related concepts:** Upsert, Transactions

---

### DELETE

**Definition:** DML removing rows matching WHERE. No WHERE means every row —
the most expensive typo in SQL, prevented by process (read replicas for
ad-hoc, transactions, backups).

**Example:**
```sql
DELETE FROM sessions WHERE expires_at < now();  -- scoped, always scoped
```

**Related concepts:** UPDATE, DML

---

### DML

**Definition:** Data Manipulation Language — INSERT, UPDATE, DELETE, SELECT.
Changes rows under transactional guarantees; the application hot path.

**Example:**
```python
# every DevMate write path is DML inside a transaction block
```

**Related concepts:** DDL, Transactions

---

### INSERT

**Definition:** DML adding rows. Bulk form for ingest, RETURNING form for
single-row creates needing generated ids back immediately.

**Example:**
```sql
INSERT INTO conversations (title) VALUES ('qdrant eval') RETURNING id;
```

**Related concepts:** RETURNING, Upsert

---

### RETURNING

**Definition:** Postgres clause returning written rows from INSERT/UPDATE/
DELETE — no second SELECT round trip for generated ids or final values.

**Example:**
```sql
INSERT ... RETURNING id, created_at  -- use the row, don't re-fetch it
```

**Related concepts:** INSERT, Upsert

---

### UPDATE

**Definition:** DML modifying rows matching WHERE. Always qualify: an
unqualified UPDATE rewrites the table, and no constraint saves you.

**Example:**
```sql
UPDATE messages SET read = TRUE WHERE conversation_id = 7;
```

**Related concepts:** DELETE, DML

---

### Upsert

**Definition:** INSERT ... ON CONFLICT DO UPDATE/ NOTHING: idempotent writes
safe to retry. The ingest primitive for at-least-once pipelines.

**Example:**
```sql
INSERT INTO chunks ... ON CONFLICT (doc_id, chunk_n) DO UPDATE SET text = EXCLUDED.text;
```

**Related concepts:** INSERT, Bulk insert

---

## Related Concepts

- **Idempotency**: retry-safe writes for deadlock victims and re-ingest
- **Savepoints**: partial-failure tolerance inside bulk loads (PG05)
- **Ingest jobs**: DevMate chunk loading as the canonical bulk writer

## Key Takeaways

1. RETURNING kills the fetch-after-write round trip.
2. Upserts make retries safe; bulk makes ingest fast.
3. UPDATE/DELETE always carry WHERE.
