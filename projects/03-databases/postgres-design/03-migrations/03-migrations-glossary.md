# PostgreSQL 03: Migrations — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Migration | A versioned, ordered schema change | 001_create_users.sql |
| Idempotent | Safe to run twice | CREATE TABLE IF NOT EXISTS |
| Rollback | The down migration that reverses a change | DROP TABLE |
| Fresh database | A clean test target | test before shared envs |
| Immutable history | Applied migrations are never edited | reorder forbidden |
| Version | The migration's number and identity | 001, 002 |

---

## Alphabetical Glossary

### Fresh database

**Definition:** A clean database used to test migrations before any shared
environment. A migration that fails here will fail in production.

**Example:**
```bash
# apply all migrations to a fresh test database
```

**Related concepts:** Migration

---

### Idempotent

**Definition:** A migration safe to run twice without error. `CREATE TABLE
IF NOT EXISTS` and `ADD COLUMN IF NOT EXISTS` make it so.

**Example:**
```sql
CREATE TABLE IF NOT EXISTS users (...);
```

**Related concepts:** Migration

---

### Immutable history

**Definition:** Applied migrations are never edited or reordered. The
schema's history is fixed.

**Example:**
```bash
# never reorder after a migration has been applied
```

**Related concepts:** Migration

---

### Migration

**Definition:** A versioned, ordered schema change. The number is the
version; the order is the history.

**Example:**
```sql
-- 001_create_users.sql
CREATE TABLE users (...);
```

**Related concepts:** Version, Rollback

---

### Rollback

**Definition:** The down migration that reverses a change. The escape hatch
for a bad migration.

**Example:**
```sql
-- rollback/001_create_users.sql
DROP TABLE users;
```

**Related concepts:** Migration

---

### Version

**Definition:** The migration's number and identity. The order of the
numbers is the order of application.

**Example:**
```bash
# 001, 002, 003 applied in order
```

**Related concepts:** Migration

---

## Related Concepts

- **Schema design**: migrations evolve the schema (topic 01)
- **Indexes**: indexes are created in migrations (topic 02)
- **Connection pooling**: the schema is served through a pool (topic 04)

## Key Takeaways

1. Migrations are numbered, ordered, and immutable once applied.
2. Idempotency removes a class of failure.
3. Every migration has a rollback.
4. Test against a fresh database.
5. Small, focused, reviewed migrations.