# PostgreSQL 01: Schema Design

## 🎯 Topic Overview

A schema is the contract between the application and the data. Tables,
types, constraints, and normalization decide what the database can store
and how reliably. This lecture covers the core schema decisions and the
discipline of referential integrity.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Design tables with the right types
2. Apply primary and foreign keys
3. Enforce constraints at the database level
4. Normalize without over-normalizing
5. Use timestamps and soft deletes consistently

---

## 1. Tables and Types

A table is a set of rows with a fixed shape. The column types are the
contract: an integer is an integer, a timestamp is a timestamp. Choosing
the right type prevents bad data from entering. The roadmap's exit test:
"the schema is designed before the application."

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

## 2. Keys

The primary key identifies a row; the foreign key links rows across
tables. A foreign key enforces referential integrity — a row cannot
reference a row that does not exist. The roadmap's exit test: "foreign
keys enforce referential integrity."

## 3. Constraints

Constraints are the database's own rules: NOT NULL, UNIQUE, CHECK, and
the keys. Enforcing rules in the database, not just the application,
prevents bad data from every entry point. The roadmap's exit test:
"constraints are enforced at the database level."

## 4. Normalization

Normalization removes redundancy: each fact is stored once. A user's name
lives in the users table, not repeated in every message. Over-normalizing
adds joins for no benefit; the discipline is to normalize the facts and
denormalize only what is measured.

## 5. Timestamps and Soft Deletes

Every table carries created_at and updated_at. Soft deletes use a
deleted_at column instead of deleting rows — history is preserved and
recoverable. The roadmap's rule: "never hard-delete user data."

## Common Mistakes

- Wrong column types (text for dates, floats for money).
- No foreign keys (orphan rows).
- Constraints only in the application.
- Over-normalizing (join-heavy queries).
- Hard-deleting user data.

## Key Takeaways

1. The schema is the contract between app and data.
2. Foreign keys enforce referential integrity.
3. Constraints live in the database, not just the app.
4. Normalize facts; denormalize only what is measured.
5. Timestamps and soft deletes preserve history.