# MySQL Lecture 12: Set Operations with UNION

## 🎯 Topic Overview

Some questions span tables with the same shape: employees plus contractors, this year's orders plus last year's archive. `UNION` stacks result sets vertically where `JOIN` widens them horizontally. This lecture covers `UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT`, and the column-compatibility rules that make set operations work.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Combine result sets with `UNION` and `UNION ALL`
2. Choose correctly between deduplicating and preserving duplicates
3. Use `INTERSECT` and `EXCEPT` for overlap and difference
4. Align column counts and types across branches
5. Sort the combined result correctly

## Prerequisites

- `SELECT` basics (Lecture 05).
- What duplicates mean for counts (SQL Fundamentals 04–06).

---

## 1. Introduction

This lecture covers set operations with union in MySQL using Python's sqlite3 as a learning companion. If a join answers "side by side", a union answers "one list after another".

---

## 2. Core Concepts

### 1. UNION

`SELECT name FROM employees UNION SELECT name FROM contractors;` combines results, removing duplicates.

```python
rows = conn.execute(
    "SELECT name FROM employees UNION SELECT name FROM contractors ORDER BY name"
).fetchall()
```

`UNION` (distinct) sorts-and-deduplicates, which costs. Use it when duplicates across the branches are possible and wrong.

### 2. UNION ALL

`SELECT name FROM employees UNION ALL SELECT name FROM contractors;` — keeps duplicates, faster.

When the branches cannot overlap (different years, different regions), `UNION ALL` skips the dedup pass and is strictly better. Default to `ALL` unless you need dedup.

### 3. INTERSECT / EXCEPT

INTERSECT returns common rows. EXCEPT returns rows in first but not second query.

```sql
SELECT user_id FROM signups
INTERSECT
SELECT user_id FROM purchasers;   -- signed up AND purchased

SELECT user_id FROM signups
EXCEPT
SELECT user_id FROM purchasers;   -- signed up but never purchased
```

`EXCEPT` is the set-difference behind churn and funnel analysis.

### 4. UNION Rules

Same number of columns. Compatible data types. ORDER BY applies to final result.

```sql
SELECT name, email FROM employees
UNION
SELECT name, NULL AS email FROM contractors
ORDER BY name;   -- one ORDER BY, at the end, by output position or alias
```

Column *names* in the output come from the first branch; align types explicitly with casts when engines differ.

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

### UNION when you meant UNION ALL (or vice versa)
Dedup by default hides real duplicates; `ALL` preserves duplicates you did not want. Choose deliberately.

### ORDER BY inside a branch
Only the final `ORDER BY` is meaningful. Put it last.

---

## 4. Best Practices

1. Always use **parameterized queries** to prevent SQL injection
2. **Commit** only when all operations succeed - use transactions
3. **Close connections** with try/finally or context managers
4. **Validate input** before database operations
5. **Use appropriate indexes** for query performance
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

1. `UNION` stacks result sets and deduplicates; `UNION ALL` skips the dedup.
2. Default to `ALL` when branches cannot overlap.
3. `INTERSECT` finds overlap; `EXCEPT` finds difference.
4. Branches must align in column count and compatible types.
5. One `ORDER BY`, at the end, applies to the combined result.

## Self-Check Questions

1. When is `UNION ALL` strictly better than `UNION`?
2. How do you find users who signed up but never purchased?
3. Why must branches have the same number of columns?
4. Where does `ORDER BY` go in a union, and what can it reference?
5. Why do output column names come from the first branch?

## Further Reading / Connections

- SQL Fundamentals 04–06 for the set semantics behind unions.
- Exercise: `12-union.py`.
