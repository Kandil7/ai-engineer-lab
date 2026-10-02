# Databases — PG02: Postgres Type System

## Topic Overview

Wrong column types are silent performance and correctness bugs: floats where
money needed exactness, `timestamp` where timezones crossed borders,
`varchar(255)` cargo-culted everywhere. This lecture maps Postgres types to
Python values through psycopg3, with the decision rules for each family.

Types are the schema's contract with the application. A money column typed
`float` will eventually produce `0.1 + 0.2 != 0.3` in a ledger; a timestamp
without a zone will eventually place the same instant on two different days for
two different users. The cost of choosing well is a few minutes at design time;
the cost of choosing badly is a migration under pressure.

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

Pass `Decimal`, not `float`, for `numeric` columns — a float literal reintroduces
the inexactness the column was created to avoid. `serial` is convenient, but
prefer `GENERATED ... AS IDENTITY` on new tables: it is standard SQL and cannot
be accidentally bypassed.

## 2. Time: Always With Timezone

`timestamp` stores a wall-clock reading with no zone — two servers in
different zones disagree about what it means. `timestamptz` stores an instant
(a UTC point); display converts to any zone. Default to `timestamptz` for
every created_at, logged_at, and event time; reach for plain `timestamp` only
for zone-free civil times like "shop opens at 09:00". psycopg3 returns aware
`datetime` objects for `timestamptz` — naive datetimes in, errors out.

```python
from datetime import datetime, timezone

now = datetime.now(timezone.utc)  # aware: safe to store
cur.execute("INSERT INTO events (at) VALUES (%s)", (now,))
```

The 3 a.m. bug is the classic failure: a daily job keyed on naive timestamps
runs twice or never across a daylight-saving change. `timestamptz` plus aware
datetimes removes the class.

## 3. Text, UUID, Boolean, Arrays

`text` with a CHECK constraint beats `varchar(n)` cargo-cult limits in
Postgres (identical storage, honest validation). `uuid` for public ids that
must not leak sequence or shard cleanly. `boolean`, never 0/1 integers.
Native arrays (`text[]`) for small fixed-shape lists — tags, roles — with
the warning that arrays don't join, so growing or relational lists stay in
tables.

```sql
CREATE TABLE api_keys (
    id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    label      text NOT NULL CHECK (char_length(label) BETWEEN 1 AND 64),
    scopes     text[] NOT NULL DEFAULT '{}',
    revoked    boolean NOT NULL DEFAULT false,
    created_at timestamptz NOT NULL DEFAULT now()
);
```

`char(n)` pads with spaces — a legacy footgun; avoid it for new columns.

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

Print this table and keep it by the schema. Every mismatch across the boundary
is a bug: a `numeric` read as `float` loses exactness; a `timestamptz` read as
naive loses the zone.

## 5. Real-World Application

DevMate's week-4 schema applies the mapping end to end: conversation and
message ids as server-generated integers, UTC `created_at timestamptz`
columns, cost stored `numeric` so dollars add up exactly, and a `metadata`
JSONB column for the semi-structured remainder. The `meta`-attribute rename
the model layer already survived proves the mapping works in both directions —
choosing the types deliberately is what made the rename safe.

## Common Mistakes

- `float` for money (0.1 + 0.2 != 0.3, now in your ledger).
- `timestamp` across timezones (the 3 a.m. bug).
- `varchar(255)` everywhere (a limit with no reason is tech debt).
- Naive datetimes crashing psycopg3 timestamptz writes.
- `char(n)` padding surprises in comparisons.
- Arrays for relational lists that should be tables (they don't join).

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
5. Pass `Decimal` and aware datetimes; let the driver carry the types.

## Self-Check Questions

1. Why does `0.1 + 0.2 != 0.3` rule out `float` for money?
2. What does `timestamptz` store that `timestamp` does not?
3. Why is `varchar(255)` with no reason tech debt?
4. When is a native array appropriate, and when must the list become a table?
5. What Python values must you pass for `numeric` and `timestamptz`?

## Further Reading / Connections

- Next: PG03, JSONB queries.
- `sql-fundamentals/02-ddl-schema/` for constraint mechanics.
- Exercise: `02-postgres-types.py`.
