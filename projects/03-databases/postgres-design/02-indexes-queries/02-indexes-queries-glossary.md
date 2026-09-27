# PostgreSQL 02: Indexes and Queries — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Index | A sorted structure mapping values to rows | speeds reads |
| B-tree | The default balanced sorted index | equality + range |
| Composite index | Multiple columns in order | (session_id, created_at) |
| GIN | Index for JSONB and full-text | to_tsvector |
| EXPLAIN | The query plan | index vs sequential scan |
| Sequential scan | Reading every row | missing index signal |
| Unique index | Enforces uniqueness, speeds lookups | email |

---

## Alphabetical Glossary

### B-tree

**Definition:** The default index: sorted, balanced, good for equality and
range queries. Most indexes are B-trees.

**Example:**
```sql
CREATE INDEX idx_users_email ON users (email);
```

**Related concepts:** Index

---

### Composite index

**Definition:** An index covering multiple columns in order. The order must
match the query pattern.

**Example:**
```sql
CREATE INDEX idx_messages_session_time ON messages (session_id, created_at);
```

**Related concepts:** Index

---

### EXPLAIN

**Definition:** The command that shows the query plan: sequential scan or
index scan, estimated rows, and cost. Verifies the index is used.

**Example:**
```sql
EXPLAIN SELECT * FROM messages WHERE session_id = 's1';
```

**Related concepts:** Sequential scan

---

### GIN

**Definition:** The index type for JSONB containment and full-text search.
The search config must match between index and query.

**Example:**
```sql
CREATE INDEX idx_lessons_search ON lessons USING GIN (to_tsvector('simple', content));
```

**Related concepts:** Index

---

### Index

**Definition:** A sorted structure that maps a column's values to the rows
that hold them. Speeds reads, slows writes.

**Example:**
```sql
CREATE INDEX idx_users_email ON users (email);
```

**Related concepts:** B-tree, Composite index

---

### Sequential scan

**Definition:** Reading every row because no index serves the query. On a
large table, the signal for a missing index.

**Example:**
```sql
-- Seq Scan on messages (cost=...)
```

**Related concepts:** EXPLAIN

---

### Unique index

**Definition:** An index that enforces uniqueness and speeds lookups on the
same column.

**Example:**
```sql
CREATE UNIQUE INDEX idx_users_email ON users (email);
```

**Related concepts:** B-tree

---

## Related Concepts

- **Schema design**: indexes serve the schema's access patterns (topic 01)
- **Migrations**: indexes are created in migrations (topic 03)
- **Qdrant**: vector search uses a different index family (qdrant-rag 02)

## Key Takeaways

1. An index maps values to rows; reads speed up, writes slow down.
2. B-tree is the default for equality and range.
3. Composite indexes must match the query pattern.
4. GIN serves JSONB and full-text search.
5. EXPLAIN shows whether the index is used.