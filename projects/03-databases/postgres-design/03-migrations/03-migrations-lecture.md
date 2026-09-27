# PostgreSQL 03: Migrations

## 🎯 Topic Overview

A schema evolves. Migrations are the versioned, ordered changes that move
the schema forward without breaking the data. This lecture covers the
sequential naming, idempotency, rollback, and the discipline of testing
migrations.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Write a sequential, versioned migration
2. Make migrations idempotent where possible
3. Write a rollback for every migration
4. Test migrations against a fresh database
5. Never reorder applied migrations

---

## 1. Sequential Migrations

Migrations are numbered files applied in order. The number is the version;
the order is the history. A migration that has been applied is never
reordered or edited — the schema's history is immutable. The roadmap's
exit test: "the schema evolves through migrations."

```sql
-- 001_create_users.sql
CREATE TABLE users (id UUID PRIMARY KEY, email TEXT UNIQUE NOT NULL);
```

## 2. Idempotency

An idempotent migration can run twice without error. `CREATE TABLE IF NOT
EXISTS` and `ADD COLUMN IF NOT EXISTS` make migrations safe to re-run. Not
every migration can be idempotent, but where possible it removes a class
of failure.

## 3. Rollback

Every migration has a down counterpart that reverses it. The rollback is
the escape hatch: a bad migration is undone, not patched forward. The
roadmap's exit test: "every migration has a rollback."

```sql
-- rollback/001_create_users.sql
DROP TABLE users;
```

## 4. Testing Migrations

Migrations are tested against a fresh database before any shared
environment. The test applies all migrations in order, verifies the
schema, and exercises the rollbacks. A migration that fails on a fresh
database will fail in production.

## 5. The Discipline

Migrations are small and focused: one change per migration. They are
reviewed like code. The roadmap's rule: "migrations are run in order;
never reorder after they have been applied."

## Common Mistakes

- Editing an applied migration.
- No rollback for a migration.
- Non-idempotent migrations where idempotency is possible.
- Testing migrations only in production.
- One migration doing many unrelated changes.

## Key Takeaways

1. Migrations are numbered, ordered, and immutable once applied.
2. Idempotency removes a class of failure.
3. Every migration has a rollback.
4. Test against a fresh database.
5. Small, focused, reviewed migrations.