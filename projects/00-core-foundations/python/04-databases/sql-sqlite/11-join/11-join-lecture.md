# MySQL Lecture 11: Joining Tables

## 🎯 Topic Overview

Real data is normalized — spread across tables that must be reassembled at query time. Joins are that reassembly, and they are where row counts silently multiply, aggregates silently inflate, and missing rows silently vanish. This lecture covers inner, outer, and self joins with the cardinality discipline that keeps them honest.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Write `INNER JOIN` for matched rows only
2. Preserve unmatched rows with `LEFT JOIN`
3. Relate a table to itself with a self-join
4. Alias tables to disambiguate shared column names
5. Detect and prevent join fan-out before aggregating

## Prerequisites

- `SELECT` and `WHERE` (Lectures 05–06).
- Primary and foreign keys (SQL Fundamentals 01).

---

## 1. Introduction

This lecture covers joining tables in MySQL using Python's sqlite3 as a learning companion. A join is a row-matching operation: every row on one side pairs with every matching row on the other. Understanding what "matching" produces — especially when it produces more rows than you started with — is the whole subject.

---

## 2. Core Concepts

### 1. INNER JOIN

`SELECT * FROM users INNER JOIN orders ON users.id = orders.user_id;` — matching rows only.

```python
rows = conn.execute(
    """
    SELECT users.name, orders.total
    FROM users INNER JOIN orders ON users.id = orders.user_id
    """
).fetchall()
```

Unmatched rows on either side disappear. That is correct when you want "users with orders" and a bug when you wanted "all users and their orders if any".

### 2. LEFT JOIN

`SELECT * FROM users LEFT JOIN orders ON users.id = orders.user_id;` — all users, even without orders.

Missing matches produce NULLs. Filter them (`WHERE orders.id IS NULL`) and the same query becomes the anti-join: "users with no orders".

### 3. RIGHT JOIN

`SELECT * FROM users RIGHT JOIN orders ON users.id = orders.user_id;` — all orders, even without users.

SQLite does not implement `RIGHT JOIN`; swap the table order and use `LEFT JOIN`. Prefer `LEFT JOIN` everywhere for portability.

### 4. Self-Join

`SELECT e.name, m.name FROM employees e JOIN employees m ON e.manager_id = m.id;`

The same table appears twice under different aliases. Self-joins model hierarchies and pairs: managers, referrals, consecutive events.

### 5. Join cardinality and fan-out

A one-to-many join multiplies rows: one user with five orders becomes five rows. Aggregating after the fan-out (`SUM(orders.total)` alongside user columns) overcounts unless you aggregate before joining or count distinct keys.

```python
# aggregate first, then join — the fan-out-safe shape
rows = conn.execute(
    """
    SELECT u.name, t.total
    FROM users u LEFT JOIN (
        SELECT user_id, SUM(total) AS total FROM orders GROUP BY user_id
    ) t ON t.user_id = u.id
    """
).fetchall()
```

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

### Forgetting the ON clause
A join without a condition is a `CROSS JOIN`: every row times every row. Always write the predicate.

### Aggregating after a fan-out join
Sums and counts inflate. Aggregate first, join second.

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

1. `INNER JOIN` keeps matches; `LEFT JOIN` preserves the left side.
2. SQLite has no `RIGHT JOIN` — swap sides and use `LEFT JOIN`.
3. Aliases disambiguate shared columns and enable self-joins.
4. Fan-out multiplies rows; aggregate before joining.
5. `LEFT JOIN ... IS NULL` finds orphans.

## Self-Check Questions

1. When does an `INNER JOIN` silently drop rows you wanted?
2. How do you find users with no orders?
3. Why does `SUM` after a one-to-many join overcount?
4. How do you write a self-join for employees and managers?
5. Why prefer `LEFT JOIN` over `RIGHT JOIN` for portability?

## Further Reading / Connections

- Next: Lecture 12, Set Operations with UNION.
- SQL Fundamentals 07 (joins in depth).
- Exercise: `11-join.py`.
