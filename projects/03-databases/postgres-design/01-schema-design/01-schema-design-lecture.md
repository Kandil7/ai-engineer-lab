# PostgreSQL 01: Schema Design

## Topic Overview

A schema is the contract between the application and the data. Tables, types, constraints, and
normalization decide what the database can store and how reliably it can store it. A schema designed
well makes invalid data unrepresentable; a schema designed carelessly lets corruption in through every
entry point and pushes the burden onto application code that will forget.

This lecture covers the core schema decisions: tables and column types, primary and foreign keys,
constraints, normalization, and the timestamp and soft-delete conventions. The through-line is that
the database is the last line of defense for data integrity, so the rules belong there, not only in
the application.

The most valuable habit is designing the schema before the application. A schema chosen after the code
is written is a schema shaped by convenience rather than by the data's actual structure.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Design tables with the right column types.
2. Apply primary and foreign keys.
3. Enforce constraints at the database level.
4. Normalize the facts and denormalize only what is measured.
5. Use timestamps and soft deletes consistently.
6. Explain why the database is the last line of integrity defense.

## Prerequisites

- Basic SQL (tables, keys, queries).
- The idea of referential integrity.

---

## 1. Tables and Types

### The table

A table is a set of rows with a fixed shape. The columns and their types are the contract: an integer
column is an integer, a timestamp column is a timestamp:

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### The types are the contract

Choosing the right type prevents bad data from entering. A date stored as text accepts anything; a
money value stored as a float accumulates rounding error. The type is the first constraint, and it is
enforced on every insert.

### UUIDs and identity

A UUID primary key is stable, globally unique, and safe to expose in URLs, unlike a sequential integer
that leaks row counts. For a system that cites records, a stable identity is the right choice.

## 2. Keys

### Primary key

The primary key identifies a row. It must be unique and non-null, and the database enforces both. It
is the row's identity, and it is what other tables reference.

### Foreign key

The foreign key links rows across tables and enforces referential integrity: a row cannot reference a
row that does not exist:

```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES sessions(id),
    body TEXT NOT NULL
);
```

### Why it matters

Without the foreign key, a message can reference a missing session, and the orphan is discovered much
later as a broken join. The constraint makes the orphan impossible.

### The cascade question

A foreign key can cascade on delete (delete the children when the parent goes), restrict (refuse), or
set null. The choice is a data-lifecycle decision, and it belongs in the schema, not in application
cleanup code.

## 3. Constraints

### The constraint set

Constraints are the database's own rules: `NOT NULL`, `UNIQUE`, `CHECK`, and the keys. They are the
last line of defense against bad data:

```sql
ALTER TABLE users ADD CONSTRAINT email_format CHECK (email LIKE '%@%');
```

### Why in the database

Enforcing rules only in the application means every new entry point (a migration, a background job, a
manual fix) can violate them. The database constraint applies to all of them, which is why integrity
belongs there.

### The cost

Constraints cost a little on write and can complicate bulk loads. The cost is small against the value
of never storing corruption, and the bulk-load complication is handled by deferring or disabling
constraints deliberately.

## 4. Normalization

### The principle

Normalization removes redundancy: each fact is stored once. A user's name lives in the users table,
not repeated in every message:

- **1NF:** atomic values, no repeating groups.
- **2NF/3NF:** no partial or transitive dependencies on the key.

### Over-normalization

Over-normalizing adds joins for no benefit, turning a simple read into a five-table join. The
discipline is to normalize the facts and denormalize only what is measured: if a join is measurably
slow and the redundancy is controlled, denormalization is a deliberate trade.

### The tension with read performance

Normalized schemas optimize for write integrity; read-heavy systems sometimes denormalize for speed.
The decision is a measured trade, recorded when it is made (a materialized view, a derived column) and
kept consistent by the pipeline.

## 5. Timestamps and Soft Deletes

### Timestamps

Every table carries `created_at` and `updated_at`. They answer "when was this made?" and "when did it
change?", which are the first questions in any incident review.

### Soft deletes

A soft delete sets a `deleted_at` column instead of removing the row. History is preserved and
recoverable:

```sql
UPDATE users SET deleted_at = now() WHERE id = $1;
```

### Why not hard-delete

Hard-deleting user data is irreversible and often a compliance problem. A soft delete preserves the
history, keeps foreign keys valid, and allows recovery. The rule is to never hard-delete user data;
purge only under an explicit retention policy.

## 6. The Exercise

### What it models

The exercise models tables, primary and foreign keys, constraints, and referential integrity
assertions. The key assertions check that a foreign key reference to a missing row is refused and that
a unique constraint rejects a duplicate.

### The lesson

The exercise demonstrates that integrity rules enforced by the schema are the ones that cannot be
bypassed, which is the argument for putting them in the database.

## Real-World Application

- A `messages` table with a foreign key to `sessions` so an orphan message cannot exist.
- A `CHECK` constraint on an email column so malformed data cannot be stored by any entry point.
- `created_at`/`updated_at` on every table so incident review has timestamps.
- Soft-deleting a user so their history is preserved while they are removed from views.

## Common Mistakes

1. **Wrong column types.** Text for dates, floats for money.
2. **No foreign keys.** Orphan rows and broken joins.
3. **Constraints only in the application.** New entry points bypass them.
4. **Over-normalizing.** Join-heavy queries for no benefit.
5. **Hard-deleting user data.** Irreversible and a compliance risk.
6. **Designing the schema after the application.** The schema follows convenience, not the data.

## Key Takeaways

1. The schema is the contract between the application and the data; the types are the first constraint.
2. Foreign keys enforce referential integrity, making orphans impossible.
3. Constraints live in the database so every entry point is covered.
4. Normalize the facts; denormalize only what is measured.
5. Timestamps and soft deletes preserve history and make data recoverable.

## Self-Check Questions

1. Why do the column types act as the first constraint?
2. What does a foreign key prevent, and where does the orphan surface without it?
3. Why must constraints live in the database rather than the application?
4. When is denormalization the right choice, and what must control it?
5. Why soft-delete rather than hard-delete user data?

## Further Reading / Connections

- PostgreSQL 02 (indexes and queries), 03 (migrations), and 04 (connection pooling) — the rest of the
  database design.
- Data Engineering 02 (schemas and contracts) — the application-side schema contract.
- `docs/cheat-sheets/postgres.md` — the command reference.
