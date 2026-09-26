# SQL 02: DDL Schema Definition — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| DDL | Data Definition Language: shapes, not rows | CREATE/ALTER/DROP |
| CREATE TABLE | Declares a relation with columns, types, constraints | new entity |
| ALTER TABLE | Evolves live schema (add/drop/alter columns) | migration body |
| DROP TABLE | Deletes a relation and its data irreversibly | dangerous, guarded |
| NOT NULL | Rejects absent values at the boundary | required fields |
| DEFAULT | Value used when INSERT omits the column | created_at now() |
| CHECK | Row-level predicate enforced on write | amount >= 0 |

---

## Alphabetical Glossary

### ALTER TABLE

**Definition:** DDL evolving an existing table: add, drop, rename, or
retype columns. The body of every migration; always paired with a downgrade.

**Example:**
```sql
ALTER TABLE messages ADD COLUMN read BOOLEAN NOT NULL DEFAULT FALSE;
```

**Related concepts:** DDL, Migrations

---

### CHECK

**Definition:** A row predicate the database enforces on every write.
Honest validation living next to the data, not just in app code.

**Example:**
```sql
amount NUMERIC CHECK (amount >= 0)  -- negative money impossible
```

**Related concepts:** NOT NULL, DEFAULT

---

### CREATE TABLE

**Definition:** DDL declaring a relation: name, columns with types, keys,
and constraints. The schema's unit of creation.

**Example:**
```sql
CREATE TABLE conversations (id INTEGER PRIMARY KEY, title TEXT NOT NULL);
```

**Related concepts:** DDL, Schema

---

### DDL

**Definition:** Data Definition Language — CREATE, ALTER, DROP. Changes
structure; versioned in migrations, reviewed like code.

**Example:**
```python
# every Alembic revision is DDL with a downgrade path
```

**Related concepts:** DML, Migrations

---

### DEFAULT

**Definition:** The value written when INSERT omits a column. Encodes the
normal case once instead of repeating it at every call site.

**Example:**
```sql
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
```

**Related concepts:** NOT NULL, CHECK

---

### DROP TABLE

**Definition:** DDL deleting a relation and all its rows. Irreversible
without backups; production drops go through deprecation, not courage.

**Example:**
```sql
DROP TABLE legacy_events;  -- only after the replacement ships + backfill
```

**Related concepts:** DDL, ALTER TABLE

---

### NOT NULL

**Definition:** Column constraint rejecting NULL. Required fields declared
where the data lives, so every reader can rely on presence.

**Example:**
```sql
question TEXT NOT NULL  -- golden sets never have missing questions
```

**Related concepts:** NULL, DEFAULT

---

## Related Concepts

- **Migrations**: DDL as reviewable, reversible history
- **Keys**: PRIMARY/FOREIGN wiring declared at CREATE time (topic 01)
- **Types**: the Postgres mapping table (PG02)

## Key Takeaways

1. DDL is code: reviewed, versioned, reversible.
2. Constraints at the boundary beat validation scattered in apps.
3. DROP is a process, not a statement.
