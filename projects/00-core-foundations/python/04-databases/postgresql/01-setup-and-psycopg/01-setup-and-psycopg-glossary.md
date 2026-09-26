# Postgres 01: Setup and psycopg Connection — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Connection | Network session with the server; capped, must close | 100 max by default |
| DSN | Connection string: scheme, auth, host, port, db, options | postgresql://… |
| Cursor | Handle issuing SQL and fetching rows on a connection | cur.execute(…) |
| Server-side cursor | Named cursor streaming rows; server holds the portal | bulk export |
| Client-side cursor | Default cursor fetching all rows into the client | small reads |
| psycopg3 | Modern Postgres driver (psycopg package, v3 API) | with-block connects |
| max_connections | Server cap on simultaneous sessions | leak = outage |

---

## Alphabetical Glossary

### Client-side cursor

**Definition:** Default cursor type that fetches the full result set into
client memory. Simple and correct for bounded results; OOM risk on big ones.

**Example:**
```python
cur.execute("SELECT * FROM logs LIMIT 100")  # bounded: fine
```

**Related concepts:** Server-side cursor, Connection

---

### Connection

**Definition:** An authenticated network session with Postgres. Limited by
`max_connections`; leaked sessions accumulate into outages.

**Example:**
```python
with psycopg.connect(DSN) as conn:  # closed on every path
```

**Related concepts:** DSN, Cursor, Connection pooling

---

### Cursor

**Definition:** The object that sends SQL over a connection and retrieves
rows. Created per unit of work, closed with its block.

**Example:**
```python
with conn.cursor() as cur:
    cur.execute("SELECT version();")
```

**Related concepts:** Connection, Server-side cursor

---

### DSN

**Definition:** Data Source Name: the connection string encoding who connects
where with what options. Read left to right; secrets from env.

**Example:**
```python
"postgresql://user:pw@host:5432/dbname?sslmode=require"
```

**Related concepts:** Connection

---

### max_connections

**Definition:** Server setting capping simultaneous sessions (default 100).
The reason pools exist and leaks are incidents.

**Example:**
```python
# SHOW max_connections; monitor pg_stat_activity counts against it
```

**Related concepts:** Connection, Connection pooling

---

### psycopg3

**Definition:** The current Postgres Python driver (`psycopg` package):
with-block connections, server-side cursor support, prepared statements.

**Example:**
```python
import psycopg  # v3 import name; psycopg2 is the legacy line
```

**Related concepts:** Cursor, DSN

---

### Server-side cursor

**Definition:** Named cursor where rows stay server-side and page to the
client on fetch. The bulk-data path for exports and ETL.

**Example:**
```python
with conn.cursor(name="export") as cur:  # streams, never materializes
```

**Related concepts:** Client-side cursor, Connection

---

## Related Concepts

- **Connection pooling**: sharing sessions across requests (topic 06)
- **sqlite3 stand-in**: identical connect/cursor semantics, zero setup
- **Alembic**: migration runner above this lifecycle (DevMate week 4)

## Key Takeaways

1. Sessions are scarce: open, work, close — structurally.
2. Cursor type follows result size.
3. The driver is thin; the discipline is the product.
