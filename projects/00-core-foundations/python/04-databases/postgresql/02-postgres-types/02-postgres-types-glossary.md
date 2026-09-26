# Postgres 02: Type System — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| numeric | Exact decimal type for money | Decimal("19.99") |
| serial/bigserial | Auto-incrementing id backed by a sequence | primary keys |
| timestamptz | Timezone-aware instant stored as UTC | created_at columns |
| timestamp | Wall-clock reading with no zone | shop opening hours |
| UUID | 128-bit globally unique id | public API ids |
| Array type | Native list column (text[], int[]) | tags, roles |
| Type mapping | Postgres-to-Python value contract per driver | psycopg3 table |

---

## Alphabetical Glossary

### Array type

**Definition:** Native Postgres list columns (`text[]`, `int[]`). Right for
small fixed-shape lists; wrong for anything that joins — those stay tables.

**Example:**
```sql
tags text[] DEFAULT '{}'  -- roles, flags; not order lines
```

**Related concepts:** Normalization, JSONB

---

### numeric

**Definition:** Exact fixed-point decimal. The money type: arithmetic that
rounds like accounting, not like floating point.

**Example:**
```python
Decimal("19.99") + Decimal("0.01")  # Decimal("20.00"), exactly
```

**Related concepts:** float8, Type mapping

---

### serial/bigserial

**Definition:** Shorthand creating an integer column fed by a sequence.
Convenient auto-ids; prefer `GENERATED ... AS IDENTITY` in new schemas.

**Example:**
```sql
id bigserial PRIMARY KEY  -- sequence-backed, gap-tolerant
```

**Related concepts:** UUID, Primary key

---

### timestamp

**Definition:** Date-time with no timezone — a wall-clock reading. Correct
only for zone-free civil times; wrong for event instants.

**Example:**
```sql
opens_at time  -- "09:00", no zone claimed
```

**Related concepts:** timestamptz

---

### timestamptz

**Definition:** Timezone-aware instant stored as UTC, displayed per session
zone. The default for every logged or created instant.

**Example:**
```python
# psycopg3 returns aware datetimes; naive input raises
```

**Related concepts:** timestamp

---

### Type mapping

**Definition:** The per-driver contract translating column types to language
values (int/Decimal/str/aware-datetime/UUID/dict). Schema and code meet here.

**Example:**
```python
# numeric -> Decimal, never float: the mapping enforces the money rule
```

**Related concepts:** numeric, psycopg3

---

### UUID

**Definition:** 128-bit unique identifier, unguessable and shard-safe.
Public ids; internal joins usually stay on integers.

**Example:**
```sql
public_id uuid DEFAULT gen_random_uuid()
```

**Related concepts:** serial/bigserial

---

## Related Concepts

- **CHECK constraints**: honest validation replacing arbitrary varchar limits
- **JSONB**: semi-structured payloads (topic 03)
- **Sequences**: gap-tolerant counters behind serial ids

## Key Takeaways

1. Exactness is a type choice, not a hope.
2. Instants carry zones; wall clocks don't.
3. The mapping table binds schema to code.
