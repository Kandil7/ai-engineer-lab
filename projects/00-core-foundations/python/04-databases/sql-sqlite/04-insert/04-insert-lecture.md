# MySQL Lecture 04: Inserting Data

## 🎯 Topic Overview

Writing data is where the application meets the database, and it is also where injection, lost writes, and slow bulk loads live. This lecture covers `INSERT` — single rows, many rows, parameters instead of string formatting, and copying between tables — with the sqlite3 patterns that keep writes safe and fast.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Write a correct single-row `INSERT INTO`
2. Bulk-insert with `executemany`
3. Use parameterized queries (`?`) to prevent SQL injection
4. Copy data with `INSERT INTO ... SELECT`
5. Commit reliably and handle write errors

## Prerequisites

- Tables and constraints (Lecture 03).
- The `with sqlite3.connect(...)` pattern (Lecture 02).

---

## 1. Introduction

This lecture covers inserting data in MySQL using Python's sqlite3 as a learning companion. Reads can be retried; a bad write is permanent. So writes get the strictest habits: parameters, commits, and error handling.

---

## 2. Core Concepts

### 1. INSERT INTO

`INSERT INTO users (name, age) VALUES ('Alice', 30);` adds a single row.

```python
with sqlite3.connect(":memory:") as conn:
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
    cur = conn.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
    print(cur.lastrowid)  # the generated id
```

`lastrowid` returns the auto-generated key, which the caller usually needs for the next step.

### 2. Multiple Rows

`cursor.executemany('INSERT INTO users (name, age) VALUES (?, ?)', data)` inserts many rows efficiently.

`executemany` sends one statement shape with many parameter sets. It is dramatically faster than a loop of `execute` calls and keeps the code to one line. For very large loads, wrap it in an explicit transaction so the whole batch commits at once.

### 3. Parameterized Queries

Use `?` placeholders instead of string formatting to prevent SQL injection.

Parameters do two jobs: they keep user input as data (never code), and they let the engine reuse the statement plan. There is no case where string-formatting values into SQL is acceptable.

### 4. INSERT INTO SELECT

`INSERT INTO archive SELECT * FROM users WHERE age > 65;` copies data between tables.

This is the archiving and backfill pattern: the selection runs inside the database, so no rows cross to Python. Match the column lists explicitly rather than `SELECT *` so a schema change does not silently misalign the copy.

### 5. Know what happened: rowcount and RETURNING

```python
cur = conn.execute("UPDATE users SET age = 31 WHERE name = ?", ("Alice",))
print(cur.rowcount)  # rows affected — 0 means the WHERE matched nothing
```

A write that affects zero rows is usually a bug (wrong id, wrong predicate), not a success. Check `rowcount` for writes that must hit.

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

### Inserting one row at a time in a loop
A Python loop of single inserts is the slowest correct way to load data. Use `executemany`, and for huge loads a single transaction.

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

1. Single rows use `INSERT INTO ... VALUES (?, ?)`; never format values in.
2. `executemany` is the bulk path; wrap big loads in one transaction.
3. `lastrowid` and `rowcount` tell you what the write actually did.
4. `INSERT INTO ... SELECT` moves data without round-tripping through Python.
5. Commit is what makes a write durable — closing without it loses the rows.

## Self-Check Questions

1. What two jobs do `?` placeholders do?
2. Why is a loop of single `execute` inserts slow, and what replaces it?
3. What does `rowcount == 0` after an UPDATE usually mean?
4. Why list columns explicitly in `INSERT INTO ... SELECT`?
5. What is lost when you close a connection without committing?

## Further Reading / Connections

- Next: Lecture 05, Selecting Data.
- SQL Fundamentals 03 (writes) and 13 (injection).
- Exercise: `04-insert.py`.
