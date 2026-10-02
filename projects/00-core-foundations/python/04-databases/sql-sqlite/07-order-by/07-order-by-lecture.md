# MySQL Lecture 07: Sorting with ORDER BY

## 🎯 Topic Overview

Unordered query results are not random — they are arbitrary, which is worse, because they look stable until they change. `ORDER BY` is what makes output deterministic, pages stable, and "top N" meaningful. This lecture covers sort direction, multi-column ordering, NULL placement, and why sorting interacts with indexes and pagination.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Sort ascending and descending with `ORDER BY`
2. Order by multiple columns with mixed directions
3. Control NULL placement explicitly
4. Explain why pagination requires `ORDER BY`
5. Use indexes to avoid sort steps

## Prerequisites

- `SELECT` and `WHERE` (Lectures 05–06).
- What an index is (SQL Fundamentals 10).

---

## 1. Introduction

This lecture covers sorting with order by in MySQL using Python's sqlite3 as a learning companion. Without `ORDER BY` the engine returns rows in whatever order is cheapest — valid SQL, useless contract.

---

## 2. Core Concepts

### 1. ORDER BY Basics

`SELECT * FROM users ORDER BY age;` sorts ascending. `ORDER BY age DESC` descending.

```python
rows = conn.execute("SELECT name, age FROM users ORDER BY age DESC, name ASC").fetchall()
```

Direction is per column, not per query: `ORDER BY a DESC, b` sorts `a` descending, `b` ascending.

### 2. Multiple Columns

`ORDER BY last_name ASC, first_name ASC` sorts by last then first name.

Later keys break ties left by earlier ones. The first key should be the coarsest grouping, the last a unique tiebreaker — ideally the primary key, so the order is fully deterministic.

### 3. NULLS Handling

NULLs sort first (ASC) or last (DESC) by default in MySQL.

Defaults differ by engine (PostgreSQL puts NULLs last on ASC by default). State it explicitly — `ORDER BY x ASC NULLS LAST` — whenever NULLs are possible and the consumer cares.

### 4. Index Impact

ORDER BY on indexed columns is significantly faster.

An index on `(last_name, first_name)` serves `ORDER BY last_name, first_name` directly; otherwise the engine sorts in memory (or on disk for large results). `EXPLAIN QUERY PLAN` shows whether a sort step exists.

### 5. Sorting and pagination

A page is only a page with a deterministic order. `ORDER BY id LIMIT 10 OFFSET 20` is stable; `LIMIT 10 OFFSET 20` alone is not. For deep pages, keyset pagination (`WHERE id > ? ORDER BY id LIMIT 10`) replaces the rescanning `OFFSET`.

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

### Paginating without ORDER BY
Pages overlap and skip rows silently. The order is the page's identity.

### Sorting by column position (`ORDER BY 2`)
Positional references break when the select list changes. Name the column.

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

1. No `ORDER BY` means no order guarantee — arbitrary, not random.
2. Direction is per column; end with a unique tiebreaker.
3. State NULL placement explicitly; defaults vary.
4. Pagination without a deterministic order is broken.
5. A matching composite index can eliminate the sort step.

## Self-Check Questions

1. Why is unordered output worse than random output?
2. How do you sort one column up and the next down?
3. Why end a sort key list with the primary key?
4. What does an index on the sort columns save?
5. Why is keyset pagination better than deep `OFFSET`?

## Further Reading / Connections

- Next: Lecture 08, Deleting Data.
- SQL Fundamentals 04 (NULL ordering) and 14 (keyset pagination).
- Exercise: `07-order-by.py`.
