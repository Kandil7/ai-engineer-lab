# MySQL Lecture 08: Deleting Data

## 🎯 Topic Overview

Deletion is the only operation that destroys information by default, which makes it the operation with the strictest habits. This lecture covers `DELETE` — targeted removal, what `TRUNCATE` does differently, how foreign keys constrain deletion, and the soft-delete pattern that keeps history while hiding rows.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Delete specific rows with `DELETE ... WHERE`
2. Distinguish `DELETE` from `TRUNCATE`
3. Predict foreign-key behavior (`CASCADE`, `RESTRICT`) on delete
4. Implement soft deletes with an `is_active` flag
5. Preview a delete with `SELECT` before running it

## Prerequisites

- `WHERE` filtering (Lecture 06).
- Foreign keys (SQL Fundamentals 01–02).

---

## 1. Introduction

This lecture covers deleting data in MySQL using Python's sqlite3 as a learning companion. The rule for this whole topic: never run a `DELETE` you have not already run as a `SELECT`.

---

## 2. Core Concepts

### 1. DELETE Syntax

`DELETE FROM users WHERE id = 5;` removes specific rows. Always use WHERE!

```python
# Preview first
doomed = conn.execute("SELECT id, name FROM users WHERE id = ?", (5,)).fetchall()
print("about to delete:", doomed)
# Then delete
cur = conn.execute("DELETE FROM users WHERE id = ?", (5,))
print("deleted:", cur.rowcount)
conn.commit()
```

`rowcount` confirms the delete hit what you expected. Zero rows deleted when you expected one is a signal, not a success.

### 2. DELETE vs TRUNCATE

DELETE removes rows (rollable, triggers fire). TRUNCATE removes all rows (faster, can't roll back).

In SQLite there is no `TRUNCATE`; `DELETE FROM t` without `WHERE` is the equivalent. The distinction matters on MySQL/Postgres: `TRUNCATE` is DDL-like, resets identity counters, and cannot be rolled back in some engines.

### 3. Foreign Key Impact

ON DELETE CASCADE removes children. ON DELETE RESTRICT blocks deletion.

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
```

Choose per relationship: cascade for owned children (order lines), restrict for shared references (a customer with invoices). Note SQLite enforces foreign keys only with `PRAGMA foreign_keys = ON`.

### 4. Soft Delete Pattern

Add `is_active BOOLEAN DEFAULT 1` and filter with `WHERE is_active = 1`.

Soft deletes preserve history and make "undelete" trivial, at the cost of filtering every query and complicating unique constraints. Use them when regulations or audits require retention; use hard deletes when the data must truly be gone (privacy erasure).

### 5. Deleting in batches

```sql
DELETE FROM events WHERE created_at < '2023-01-01' LIMIT 10000;
```

Large deletes in one statement hold locks and bloat the transaction log. Loop bounded deletes until `rowcount` is zero.

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

### DELETE without WHERE
One missing predicate empties the table. Preview as SELECT, and consider requiring `LIMIT` or a rowcount assertion in tooling.

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

1. Preview every `DELETE` as a `SELECT` first.
2. `DELETE` is transactional and trigger-aware; `TRUNCATE` is fast and final.
3. Foreign-key actions decide whether children vanish or block the delete.
4. Soft deletes preserve history; hard deletes honor erasure.
5. Batch large deletes to bound locks and log growth.

## Self-Check Questions

1. What does `rowcount` tell you after a `DELETE`, and when is 0 a problem?
2. When is `CASCADE` right and when is `RESTRICT` right?
3. Why does SQLite need `PRAGMA foreign_keys = ON`?
4. What does a soft delete cost on every future query?
5. Why delete old rows in bounded batches?

## Further Reading / Connections

- Next: Lecture 09, Updating Data.
- SQL Fundamentals 03 (safe writes) and 11 (transactions).
- Exercise: `08-delete.py`.
