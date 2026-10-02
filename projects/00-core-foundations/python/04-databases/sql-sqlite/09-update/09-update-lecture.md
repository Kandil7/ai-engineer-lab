# MySQL Lecture 09: Updating Data

## 🎯 Topic Overview

Updates change existing truth, which makes them riskier than inserts: the same missing `WHERE` that deletes everything also rewrites everything. This lecture covers `UPDATE` — single and multi-column sets, join-driven updates, conditional `CASE` logic, and the habits (preview, `rowcount`, transactions) that keep rewrites safe.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Update rows with `UPDATE ... SET ... WHERE`
2. Set multiple columns in one statement
3. Reference other tables in an update
4. Write conditional updates with `CASE`
5. Verify updates with `rowcount` inside a transaction

## Prerequisites

- `WHERE` filtering (Lecture 06).
- Transactions: commit and rollback (Lecture 02 patterns).

---

## 1. Introduction

This lecture covers updating data in MySQL using Python's sqlite3 as a learning companion. An update is a read plus a write: the `WHERE` selects the victims, the `SET` changes them. Respect both halves.

---

## 2. Core Concepts

### 1. UPDATE Syntax

`UPDATE users SET age = 31 WHERE id = 1;` modifies existing rows.

```python
cur = conn.execute("UPDATE users SET age = ? WHERE id = ?", (31, 1))
print("updated:", cur.rowcount)
conn.commit()
```

### 2. Multiple Columns

`UPDATE users SET age = 31, city = 'NYC' WHERE id = 1;` updates several columns at once.

One statement, one transaction, one round-trip. Splitting the same row's changes across statements is slower and can leave the row half-updated on failure.

### 3. UPDATE with JOIN

UPDATE can reference data from other tables using JOIN syntax.

```sql
UPDATE users SET plan = plans.name
FROM plans WHERE users.plan_id = plans.id AND plans.tier = 'pro';
```

(Dialect syntax varies — MySQL uses `UPDATE ... JOIN`, Postgres/SQLite use `UPDATE ... FROM`.) The join determines *which* rows change, so preview it as a `SELECT` first.

### 4. Conditional Updates

Use `CASE` expressions for different values per row in a single UPDATE.

```sql
UPDATE users SET tier = CASE WHEN age >= 65 THEN 'senior' ELSE 'standard' END;
```

One pass over the table instead of N statements — and atomic, where N statements would not be.

### 5. Safe-update discipline

```python
with sqlite3.connect("app.db") as conn:
    victims = conn.execute("SELECT id FROM users WHERE plan = 'legacy'").fetchall()
    print("will update:", len(victims))
    cur = conn.execute("UPDATE users SET plan = 'standard' WHERE plan = 'legacy'")
    assert cur.rowcount == len(victims)
# commit on clean exit, rollback on exception
```

Preview, assert `rowcount`, and let the context manager decide commit vs rollback.

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

### UPDATE without WHERE
Rewrites every row. The most expensive typo in SQL.

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

1. `SET` lists every changed column; `WHERE` lists every affected row.
2. Missing `WHERE` rewrites the whole table — preview as `SELECT`.
3. `CASE` puts conditional logic in one atomic statement.
4. `rowcount` verifies the update hit what you intended.
5. Related updates belong in one transaction.

## Self-Check Questions

1. What happens with `UPDATE users SET age = 31` and no `WHERE`?
2. Why update several columns in one statement rather than several?
3. When is `CASE` better than multiple `UPDATE` statements?
4. How do you verify an update before committing?
5. Why do join-driven updates need a `SELECT` preview?

## Further Reading / Connections

- Next: Lecture 10, Dropping Tables.
- SQL Fundamentals 03 (writes) and 11 (transactions).
- Exercise: `09-update.py`.
