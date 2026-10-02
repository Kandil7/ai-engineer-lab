# MySQL Lecture 03: Creating Tables

## 🎯 Topic Overview

A table is where design becomes durable: column names, types, and constraints decide what data can exist and how fast it can be found. Getting the table right is cheaper than fixing it later, because every row written under a bad schema inherits the mistake. This lecture covers `CREATE TABLE` — columns, SQLite types, constraints, keys, and auto-generated ids — with sqlite3 as the runnable companion.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Write a correct `CREATE TABLE` with columns, types, and constraints
2. Choose SQLite types (INTEGER, TEXT, REAL, BLOB) and know their MySQL counterparts
3. Declare `PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`, and `FOREIGN KEY`
4. Use `AUTOINCREMENT`/`INTEGER PRIMARY KEY` for generated ids
5. Apply `IF NOT EXISTS` so setup scripts are re-runnable

## Prerequisites

- Databases vs files (Lecture 02).
- What a primary key is (SQL Fundamentals 01).

---

## 1. Introduction

This lecture covers creating tables in MySQL using Python's sqlite3 as a learning companion. A table is defined once and read millions of times, so the definition deserves the care: every constraint you declare is a bug you will never debug.

---

## 2. Core Concepts

### 1. CREATE TABLE Syntax

`CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER);` defines columns, types, and constraints.

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id   INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age  INTEGER CHECK (age >= 0)
        )
        """
    )
```

`IF NOT EXISTS` makes the statement safe to re-run. Without it, a second setup run crashes.

### 2. Data Types

INTEGER, TEXT, REAL, BLOB (sqlite3). MySQL adds VARCHAR, FLOAT, DATE, TIMESTAMP, ENUM, etc.

SQLite uses type affinity rather than rigid types: declaring `VARCHAR(255)` is accepted and stored as TEXT affinity. The practical rule is to use the four native types and let the affinity system do its job.

### 3. Constraints

PRIMARY KEY, NOT NULL, UNIQUE, FOREIGN KEY, CHECK, DEFAULT.

Constraints are enforced by the engine on every write, which is exactly where enforcement belongs — application code forgets, the database does not.

```python
conn.execute(
    """
    CREATE TABLE orders (
        id      INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        total   REAL NOT NULL DEFAULT 0.0,
        email   TEXT UNIQUE
    )
    """
)
```

### 4. AUTOINCREMENT

Automatically generates unique IDs. In sqlite3: `id INTEGER PRIMARY KEY AUTOINCREMENT`.

Plain `INTEGER PRIMARY KEY` already auto-assigns `max(id)+1`; `AUTOINCREMENT` additionally guarantees ids are never reused. Use it when external systems reference your ids.

### 5. A complete table script

```python
SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    email      TEXT UNIQUE NOT NULL,
    age        INTEGER CHECK (age >= 0),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
"""

with sqlite3.connect("app.db") as conn:
    conn.executescript(SCHEMA)
```

A schema script plus `executescript` is the smallest honest migration: version it, review it, run it in order.

---

## 3. Common Mistakes

### Forgetting to commit
Always commit after INSERT, UPDATE, or DELETE:
```python
# WRONG
cursor.execute("INSERT ...")
conn.close()  # Changes lost!

# RIGHT
cursor.execute("INSERT ...")
conn.commit()
conn.close()
```

### SQL Injection vulnerability
Never use string formatting for SQL queries:
```python
# WRONG - string concatenation is dangerous
name_input = "Alice' OR '1'='1"
query = "SELECT * FROM users WHERE name = '" + name_input + "'"
# Executes: SELECT * FROM users WHERE name = 'Alice' OR '1'='1'

# RIGHT - parameterized queries are safe
cursor.execute("SELECT * FROM users WHERE name = ?", (name_input,))
```

### Not handling errors
Always wrap database operations in try/except/finally:
```python
try:
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
except sqlite3.Error as e:
    print(f"Error: {e}")
    if conn:
        conn.rollback()
finally:
    if conn:
        conn.close()
```

### Declaring no constraints
A table with no `NOT NULL`, no keys, and no checks accepts garbage. The constraint list is the cheapest test suite you will ever write.

---

## 4. Best Practices

1. Always use **parameterized queries** to prevent SQL injection
2. **Commit** only when all operations succeed - use transactions
3. **Close connections** with try/finally or context managers
4. **Validate input** before database operations
5. Use **appropriate indexes** for query performance
6. **Test with in-memory databases** before using real ones

---

## 5. Practice Exercises

### Exercise 1: Basic Operations
Write code that connects to an in-memory database, creates a table, inserts 5 sample rows, queries them, and properly cleans up.

### Exercise 2: Advanced Queries
Using the same table, write queries that filter with WHERE, sort with ORDER BY, and limit results with LIMIT.

### Exercise 3: Error Handling
Write a function that executes any SQL query safely with error handling and always closes the connection.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| Syntax | Standard SQL patterns work across databases |
| Safety | Parameterized queries prevent SQL injection |
| Transactions | Commit saves changes, rollback undoes them |
| Error Handling | Always use try/except/finally
| Cleanup | Close connections to free resources

## Key Takeaways

1. `CREATE TABLE` defines columns, types, and constraints in one statement.
2. SQLite affinity accepts MySQL-style types; use the four native affinities.
3. `IF NOT EXISTS` keeps setup scripts re-runnable.
4. `INTEGER PRIMARY KEY` auto-generates ids; `AUTOINCREMENT` adds no-reuse.
5. Constraints are enforced on every write — declare them, don't trust callers.

## Self-Check Questions

1. What does `IF NOT EXISTS` protect against?
2. Which types are native to SQLite, and what happens to `VARCHAR(255)`?
3. When is `AUTOINCREMENT` needed beyond plain `INTEGER PRIMARY KEY`?
4. Give one constraint for each of: identity, presence, uniqueness, range.
5. Why is a schema script better than ad-hoc DDL?

## Further Reading / Connections

- Next: Lecture 04, Inserting Data.
- SQL Fundamentals 02 (DDL) for constraints in depth.
- Exercise: `03-create-table.py`.
