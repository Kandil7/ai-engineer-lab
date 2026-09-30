# PostgreSQL 03: Migrations

## Topic Overview

A schema evolves. Migrations are the versioned, ordered changes that move the schema forward without
breaking the data or the running application. They are the database's version control, and they carry
the same discipline as code: reviewed, tested, and immutable once applied.

This lecture covers sequential versioned migrations, idempotency, rollback, testing against a fresh
database, and the discipline that makes migrations safe to run on a live system.

The core rule is that an applied migration is history: never edited, never reordered. A schema's
history must be truthful, because it is what a fresh database is built from, and the fresh build is
what production must match.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write a sequential, versioned migration.
2. Make a migration idempotent where possible.
3. Write a rollback for every migration.
4. Test migrations against a fresh database.
5. Plan a safe rollout for a breaking change.
6. Explain why applied migrations are immutable.

## Prerequisites

- PostgreSQL 01 (schema design) and 02 (indexes) for what a migration changes.

---

## 1. Sequential Migrations

### The numbering

Migrations are numbered files applied in order. The number is the version; the order is the history:

```sql
-- 001_create_users.sql
CREATE TABLE users (id UUID PRIMARY KEY, email TEXT UNIQUE NOT NULL);
```

### Immutability

A migration that has been applied is never reordered or edited. The schema's history is immutable,
because a fresh database is built by replaying the migrations in order, and editing one changes what
every environment gets.

### The exit test

The roadmap's exit test is that the schema evolves through migrations. Every schema change is a
migration, never a manual `ALTER` on a running database, because the manual change is not in the
history and the fresh build will not have it.

## 2. Idempotency

### The idea

An idempotent migration can run twice without error. `CREATE TABLE IF NOT EXISTS` and `ADD COLUMN IF
NOT EXISTS` make a migration safe to re-run:

```sql
CREATE TABLE IF NOT EXISTS sessions (...);
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS user_id UUID;
```

### Why it helps

Not every migration can be idempotent, but where possible it removes a class of failure: a half-applied
migration that is re-run does not error on the part that already applied.

### The exercise

```python
m.apply("003", ["sessions"], idempotent=True)   # safe to re-run
```

The exercise models an idempotent migration and a non-idempotent one that fails on an existing table,
making the difference concrete.

## 3. Rollback

### The down migration

Every migration has a down counterpart that reverses it:

```sql
-- rollback/001_create_users.sql
DROP TABLE users;
```

### The escape hatch

The rollback is the escape hatch when a migration is bad: it is undone, not patched forward. A
migration without a rollback is a one-way door, and one-way doors are dangerous on a live system.

### The exit test

The roadmap's exit test is that every migration has a rollback. It is designed with the migration, not
after it, because the reverse is often harder to reason about than the forward.

## 4. Testing Migrations

### Against a fresh database

Migrations are tested against a fresh database before any shared environment. The test applies all
migrations in order, verifies the schema, and exercises the rollbacks.

### Why fresh

A migration that fails on a fresh database will fail in production, and a migration that only works on
a database that has drifted will fail when the next environment is built. The fresh build is the
canonical test.

### The CI gate

The migration test runs in CI, so a migration that does not apply cleanly or does not roll back is
caught before it reaches a shared environment.

## 5. Safe Rollout of a Breaking Change

### The expand-contract pattern

A breaking change (a new required column, a rename) is rolled out in steps so that old and new code
both work throughout:

1. **Expand:** add the new column as nullable (or with a default).
2. **Dual-write:** the application writes both old and new.
3. **Backfill:** fill the new column for existing rows.
4. **Switch reads:** the application reads the new column.
5. **Contract:** drop the old column.

### Why the pattern

At every step, both old and new code work, so the deploy and the migration can happen in any order
without an outage. This is the same expand-backfill-contract shape as the contract migration (Data
Engineering 02), because it is the same problem: a rolling upgrade across a schema change.

### The exit test

The result is a migration that never requires taking the system down, which is the standard for a
production database.

## 6. The Exercise

### What it models

The exercise models a migrator with an applied-migration list, idempotent and non-idempotent apply, and
rollback.

### The assertions

```python
m.apply("001", ["users"])
m.apply("002", ["messages"])
assert m.applied == ["001", "002"]
m.apply("003", ["sessions"], idempotent=True)   # safe to re-run
m.rollback("003", ["sessions"])
assert "003" not in m.applied
```

The rollback restores the prior schema, which is the escape hatch.

## Real-World Application

- Adding a `messages` table as a numbered migration so every environment gets it by replay.
- Making an index migration idempotent so a re-run after a partial failure is safe.
- Rolling out a new required column with expand-contract so no deploy needs downtime.
- Testing all migrations and rollbacks against a fresh database in CI.

## Common Mistakes

1. **Editing an applied migration.** Every environment's fresh build changes.
2. **No rollback.** A one-way door on a live system.
3. **Non-idempotent migrations where idempotency is possible.** Re-runs fail.
4. **Testing migrations only in production.** The failure is discovered by users.
5. **One migration doing many unrelated changes.** Hard to review and roll back.
6. **A breaking change in one step.** An outage during the deploy.

## Key Takeaways

1. Migrations are numbered, ordered, and immutable once applied.
2. Idempotency removes a class of failure where it is possible.
3. Every migration has a rollback, designed alongside the forward migration.
4. Test migrations against a fresh database in CI.
5. Rolling out a breaking change uses expand-contract so old and new code both work.

## Self-Check Questions

1. Why is an applied migration immutable?
2. What does idempotency buy a migration, and when is it not possible?
3. Why must every migration have a rollback?
4. Why test migrations against a fresh database rather than a shared one?
5. Describe the expand-contract steps for adding a required column.

## Further Reading / Connections

- PostgreSQL 01, 02, and 04 — the schema the migrations change.
- Data Engineering 02 (schemas and contracts) — the application-side version of the same pattern.
- `projects/00-core-foundations/python/04-databases/sqlalchemy/11-migrations-alembic/` — the tool.
