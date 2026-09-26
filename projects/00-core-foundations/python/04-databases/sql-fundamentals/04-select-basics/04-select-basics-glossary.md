# SQL 04: SELECT Basics — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Projection | Choosing output columns (the SELECT list) | SELECT id, title |
| WHERE | Row filter before grouping/ordering | eligible subset |
| ORDER BY | The only source of result ordering | ranked output |
| LIMIT / OFFSET | Top-N and paging (OFFSET cost grows) | page 1, keyset later |
| DISTINCT | Deduplicates output rows | unique languages |
| Alias | Temporary AS name for columns/tables | readable output |
| SELECT list | Columns/expressions returned per row | the read contract |

---

## Alphabetical Glossary

### Alias

**Definition:** A temporary AS name for a column or table, clarifying output
and shortening qualified references. Cosmetic, but readability compounds.

**Example:**
```sql
SELECT c.title AS conversation FROM conversations c;
```

**Related concepts:** Projection

---

### DISTINCT

**Definition:** Deduplicates result rows. Answers "which values exist" —
and its cost is a sort/hash, so prefer it deliberately, not defensively.

**Example:**
```sql
SELECT DISTINCT language FROM chunks;  -- the filter facet list
```

**Related concepts:** Projection, GROUP BY

---

### LIMIT / OFFSET

**Definition:** LIMIT caps rows returned; OFFSET skips N first. OFFSET cost
grows with N (rows still scanned) — keyset pagination replaces it at scale.

**Example:**
```sql
LIMIT 10 OFFSET 20  -- page 3; fine small, keyset past thousands
```

**Related concepts:** ORDER BY, Keyset pagination

---

### ORDER BY

**Definition:** The sole determinant of result order. Without it, order is
whatever the plan produced — never assume, especially across pagination.

**Example:**
```sql
ORDER BY created_at DESC, id DESC  -- total order, stable pages
```

**Related concepts:** LIMIT / OFFSET, Set thinking

---

### Projection

**Definition:** The SELECT list: which columns/expressions each row returns.
Project only what the consumer needs — SELECT * in hot paths is a latency
and breakage tax on every schema change.

**Example:**
```sql
SELECT id, title  -- the read contract, explicit and narrow
```

**Related concepts:** Alias, WHERE

---

### SELECT list

**Definition:** The expressions between SELECT and FROM. Defines the output
shape; the API's read contract with the database.

**Example:**
```python
# changing the list changes every consumer: treat as API surface
```

**Related concepts:** Projection, Alias

---

### WHERE

**Definition:** The row filter applied before grouping and ordering. Indexed
columns here decide whether the plan scans or seeks.

**Example:**
```sql
WHERE conversation_id = 7  -- B-tree seek, not a scan
```

**Related concepts:** Indexes, ORDER BY

---

## Related Concepts

- **Keyset pagination**: WHERE id > last_seen ORDER BY id LIMIT n (stable at scale)
- **EXPLAIN**: proves the WHERE uses the index (PG04)
- **N+1**: per-row SELECTs in a loop (SQLAlchemy 06)

## Key Takeaways

1. Project narrowly, filter on indexes, order explicitly.
2. OFFSET is a loan with growing interest; keyset pays cash.
3. The SELECT list is API surface — change it deliberately.
