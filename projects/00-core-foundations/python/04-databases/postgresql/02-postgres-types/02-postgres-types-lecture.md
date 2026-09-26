# Databases — PG02: Postgres Type System

## Topic Overview

Wrong column types are silent performance and correctness bugs: floats where
money needed exactness, `timestamp` where timezones crossed borders,
`varchar(255)` cargo-culted everywhere. This lecture maps Postgres types to
Python values through psycopg3, with the decision rules for each family.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Choose integer, numeric, and float types by exactness requirements
2. Use `timestamptz` by default and explain why `timestamp` loses timezone fights
3. Map each Postgres type to its psycopg3 Python value (and back)
4. Pick text, varchar, char, UUID, boolean, and array types deliberately
5. Reserve JSONB for semi-structured payloads (full treatment in topic 03)

## Prerequisites

| Need | Where |
|---|---|
| DDL and schema basics | `sql-fundamentals/02-ddl-schema/` |
| The runnable exercise | [02-postgres-types.py](02-postgres-types.py) |

## 1. Numbers: Exactness First

`integer`/`bigint` for counts and ids (`serial`/`bigserial` auto-generate
them, backed by sequences). `numeric` for money — exact decimal arithmetic.
`float`/`double precision` for measurements where approximate is honest
(embeddings, sensor readings). The rule is one sentence: money is numeric,
everything measured is float, everything counted is integer.

```python
# psycopg3 mapping: int -> integer/bigint, Decimal -> numeric, float -> float8
from decimal import Decimal

cur.execute("INSERT INTO ledger (amount) VALUES (%s)", (Decimal("19.99"),))
```

## 2. Time: Always With Timezone

`timestamp` stores a wall-clock reading with no zone — two servers in
different zones disagree about what it means. `timestamptz` stores an instant
(a UTC point); display converts to any zone. Default to `timestamptz` for
every created_at, logged_at, and event time; reach for plain `timestamp` only
for zone-free civil times like "shop opens at 09:00". psycopg3 returns aware
`datetime` objects for `timestamptz` — naive datetimes in, errors out.

## 3. Text, UUID, Boolean, Arrays

`text` with a CHECK constraint beats `varchar(n)` cargo-cult limits in
Postgres (identical storage, honest validation). `uuid` for public ids that
must not leak sequence or shard cleanly. `boolean`, never 0/1 integers.
Native arrays (`text[]`) for small fixed-shape lists — tags, roles — with
the warning that arrays don't join, so growing or relational lists stay in
tables.

## 4. The Mapping Table

| Postgres | Python (psycopg3) | Notes |
|---|---|---|
| integer/bigint | int | serial for auto-ids |
| numeric | Decimal | money only |
| float8 | float | measurements |
| text/varchar | str | prefer text + CHECK |
| boolean | bool | never 0/1 ints |
| timestamptz | aware datetime | default for instants |
| uuid | UUID | public ids |
| jsonb | dict/list | topic 03 |

## Common Mistakes

- `float` for money (0.1 + 0.2 != 0.3, now in your ledger).
- `timestamp` across timezones (the 3 a.m. bug).
- `varchar(255)` everywhere (a limit with no reason is tech debt).
- Naive datetimes crashing psycopg3 timestamptz writes.

## DevMate Connection

The week-4 schema lives these decisions: conversation/message ids, UTC
`created_at` columns, cost stored numeric (dollars must add up exactly), and
the `metadata` JSONB column whose full treatment is topic 03 — including the
`meta`-attribute rename the model layer already survived.

## Key Takeaways

1. Money numeric, measurements float, counts integer.
2. `timestamptz` by default; plain `timestamp` almost never.
3. text + CHECK beats arbitrary varchar limits.
4. The mapping table is the contract between schema and code.
