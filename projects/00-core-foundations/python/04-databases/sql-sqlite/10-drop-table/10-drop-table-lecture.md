# MySQL Lecture 10: Dropping Tables

## 🎯 Topic Overview

Dropping a table is the most final DDL operation: the definition and every row vanish together. This lecture covers `DROP TABLE`, how `TRUNCATE` differs, the `DROP` vs `TRUNCATE` vs `DELETE` decision, and the foreign-key and migration discipline that keeps drops from destroying production.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Drop a table with `DROP TABLE` and understand its finality
2. Empty a table with `TRUNCATE` while keeping its structure
3. Choose correctly between `DROP`, `TRUNCATE`, and `DELETE`
4. Handle foreign-key references before dropping
5. Gate drops behind backups and migrations

## Prerequisites

- Tables and constraints (Lecture 03).
- The delete discipline (Lecture 08).

---

## 1. Introduction

This lecture covers dropping tables in MySQL using Python's sqlite3 as a learning companion. Dropping is a design decision with a delete attached; treat it as a migration, not a query.

---

## 2. Core Concepts

### 1. DROP TABLE

`DROP TABLE users;` permanently removes table and data. Irreversible!

```sql
DROP TABLE IF EXISTS temp_import;   -- safe in scripts
```

`IF EXISTS` keeps re-runnable scripts from failing. There is no undo; the only recovery is a backup.

### 2. TRUNCATE TABLE

`TRUNCATE TABLE users;` removes all rows but keeps table structure.

`TRUNCATE` is fast because it deallocates rather than deleting row by row, but it typically cannot be rolled back and does not fire row triggers. SQLite has no `TRUNCATE` — `DELETE FROM t` is the equivalent.

### 3. DROP vs TRUNCATE vs DELETE

DROP removes table+data. TRUNCATE removes data only. DELETE removes rows with WHERE.

| Operation | Removes | Rollback | Triggers | Speed |
|---|---|---|---|---|
| `DROP TABLE` | table + data | no | no | instant |
| `TRUNCATE` | all rows | usually no | no | fast |
| `DELETE` | matched rows | yes | yes | row-by-row |

### 4. Foreign Keys

Cannot DROP a table referenced by a FOREIGN KEY without dropping constraints first.

The engine refuses because the reference would dangle. Drop dependents first, or alter them to remove the reference — in a migration, in order, reviewed.

### 5. The safe-drop checklist

1. Back up the data (`SELECT ... INTO backup` or a dump).
2. Confirm no application code references the table.
3. Drop dependents or their constraints first.
4. Run the drop inside a reviewed migration, never ad-hoc on production.

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

### Dropping without a backup
The table is gone and so is the data. Back up first, always.

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

1. `DROP TABLE` removes definition and data with no undo.
2. `TRUNCATE` empties fast but skips rollback and triggers.
3. `DELETE` is the only row-selective, transactional removal.
4. Foreign keys must be resolved before a drop.
5. Drops belong in backed-up, reviewed migrations.

## Self-Check Questions

1. What is unrecoverable about `DROP TABLE`?
2. When is `TRUNCATE` right and when is `DELETE` right?
3. Why does the engine refuse to drop a referenced table?
4. What backup step precedes any production drop?
5. Why does SQLite lack `TRUNCATE`, and what replaces it?

## Further Reading / Connections

- Next: Lecture 11, Joining Tables.
- SQL Fundamentals 02 (DDL) for migration discipline.
- Exercise: `10-drop-table.py`.
