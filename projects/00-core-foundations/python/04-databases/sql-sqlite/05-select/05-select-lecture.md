# MySQL Lecture 05: Selecting Data

## 🎯 Topic Overview

Reading is the most common database operation and the easiest to get subtly wrong: returning too much, ordering nothing, paginating unstably. This lecture covers `SELECT` — projection, `DISTINCT`, aliases, and `LIMIT/OFFSET` — with the discipline that keeps reads correct, lean, and reproducible.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Project explicit columns instead of `SELECT *`
2. Remove duplicates with `DISTINCT`
3. Rename output with column aliases
4. Page results with `LIMIT` and `OFFSET`
5. Fetch results correctly with `fetchone`/`fetchall`/iteration

## Prerequisites

- Tables exist with data in them (Lectures 03–04).
- The `with sqlite3.connect(...)` pattern (Lecture 02).

---

## 1. Introduction

This lecture covers selecting data in MySQL using Python's sqlite3 as a learning companion. A read cannot corrupt data, but it can still be wrong: ambiguous order, unbounded size, and `SELECT *` in production code are the classic read bugs.

---

## 2. Core Concepts

### 1. SELECT Basics

`SELECT * FROM users;` retrieves all columns. `SELECT name, age FROM users;` retrieves specific columns.

Explicit columns document intent, transfer fewer bytes, and survive `ALTER TABLE ADD COLUMN` without changing your output shape. `SELECT *` is for the REPL, not for code.

```python
rows = conn.execute("SELECT name, age FROM users ORDER BY name").fetchall()
for name, age in rows:
    print(name, age)
```

### 2. SELECT DISTINCT

`SELECT DISTINCT city FROM users;` returns unique values, removing duplicates.

`DISTINCT` applies to the whole row, not one column: `SELECT DISTINCT a, b` deduplicates pairs. It costs a sort or hash, so prefer fixing the duplicate source (usually a join) when the list is long.

### 3. Column Aliases

`SELECT name AS full_name FROM users;` renames columns in output using AS.

Aliases matter for computed columns (`SELECT price * qty AS line_total`) and for self-joins where two tables share a column name. Use `row_factory = sqlite3.Row` to read results by alias name.

### 4. LIMIT and OFFSET

`SELECT * FROM users LIMIT 10 OFFSET 20;` supports pagination.

`LIMIT` without `ORDER BY` returns an arbitrary ten rows — fine for a look, wrong for a page. And `OFFSET` rescans skipped rows, so deep pages are slow; keyset pagination (Lecture 07 companion, SQL Fundamentals 14) is the fix at scale.

### 5. Fetching in Python

```python
cur = conn.execute("SELECT name FROM users")
first = cur.fetchone()  # one row or None
rest = cur.fetchall()  # everything remaining
for row in conn.execute("SELECT name FROM users"):  # streaming, no full list
    print(row)
```

`fetchall` on a million-row result builds a million-tuple list. Iterate the cursor for large results.

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

### SELECT * in application code
It couples your code to the table's column order and ships columns (password hashes, tokens) the caller never needed.

### fetchall on unbounded queries
One huge `fetchall` can exhaust memory. Page, filter, or stream.

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

1. Project explicit columns; `SELECT *` is for exploration.
2. `DISTINCT` deduplicates whole rows at a sorting cost.
3. Aliases name computed output and disambiguate joins.
4. `LIMIT` needs `ORDER BY` to be meaningful; `OFFSET` degrades with depth.
5. Stream large results with cursor iteration, not `fetchall`.

## Self-Check Questions

1. Why does `SELECT *` break when a column is added?
2. What does `DISTINCT` deduplicate — a column or a row?
3. Why is `LIMIT 10` without `ORDER BY` not a stable page?
4. When should you iterate a cursor instead of `fetchall`?
5. How do aliases help a self-join?

## Further Reading / Connections

- Next: Lecture 06, Filtering with WHERE.
- SQL Fundamentals 04 (projection) and 14 (pagination at scale).
- Exercise: `05-select.py`.
