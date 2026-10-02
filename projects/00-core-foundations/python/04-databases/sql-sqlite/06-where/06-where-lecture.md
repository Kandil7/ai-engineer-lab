# MySQL Lecture 06: Filtering with WHERE

## 🎯 Topic Overview

`WHERE` decides which rows survive, and it is where most query bugs live: a missing predicate that rewrites the whole table, a NULL comparison that silently drops rows, a string-formatted value that injects. This lecture covers comparison, logical, and special operators — with parameters, always — and the NULL semantics that make `WHERE` tricky.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Filter rows with comparison operators
2. Combine predicates with `AND`, `OR`, `NOT`
3. Use `IN`, `BETWEEN`, `LIKE`, and `IS NULL`
4. Handle NULL comparisons correctly
5. Parameterize every value in the predicate

## Prerequisites

- `SELECT` basics (Lecture 05).
- What NULL means (SQL Fundamentals 01).

---

## 1. Introduction

This lecture covers filtering with where in MySQL using Python's sqlite3 as a learning companion. Every read-modify and every report starts with a filter; getting the filter wrong means acting on the wrong rows.

---

## 2. Core Concepts

### 1. WHERE Clause

`SELECT * FROM users WHERE age >= 18;` filters rows by conditions.

```python
adults = conn.execute(
    "SELECT name, age FROM users WHERE age >= ?", (18,)
).fetchall()
```

The value travels as a parameter. The day a value is formatted into the string is the day injection becomes possible.

### 2. Comparison Operators

`=` equal, `<>` not equal, `>` greater, `<` less, `>=` / `<=` .

Note `<>` (standard) versus `!=` (accepted almost everywhere). Pick one per codebase.

### 3. Logical Operators

`AND` (all true), `OR` (any true), `NOT` (negation).

`AND` binds tighter than `OR`, exactly like multiplication over addition. Parenthesize mixed expressions explicitly — the bug from relying on precedence is silent and returns plausible-but-wrong rows.

### 4. Special Operators

`IN`, `BETWEEN`, `LIKE`, `IS NULL` for advanced filtering.

```python
# IN with a parameter per element
ids = (1, 2, 3)
placeholders = ",".join("?" for _ in ids)
rows = conn.execute(f"SELECT * FROM users WHERE id IN ({placeholders})", ids).fetchall()

# BETWEEN is inclusive on both ends
# LIKE: % matches any run, _ matches one character
rows = conn.execute("SELECT * FROM users WHERE name LIKE ?", ("A%",)).fetchall()

# IS NULL is the only correct NULL test
rows = conn.execute("SELECT * FROM users WHERE email IS NULL").fetchall()
```

`IN` with an empty list is a syntax error in most engines; guard it or short-circuit in Python.

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

### `= NULL` instead of `IS NULL`
`WHERE email = NULL` is unknown for every row — it matches nothing, ever, with no error.

### Relying on AND/OR precedence
`WHERE a OR b AND c` parses as `a OR (b AND c)`. Parenthesize.

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

1. `WHERE` with parameters is the safe filter; formatting values in is injection.
2. `AND` binds tighter than `OR` — parenthesize mixed logic.
3. `NULL` needs `IS NULL`; `= NULL` matches nothing.
4. `IN` needs one placeholder per element; guard the empty list.
5. `LIKE` patterns: `%` for runs, `_` for single characters.

## Self-Check Questions

1. Why does `WHERE a OR b AND c` surprise people?
2. What does `WHERE email = NULL` return, and why?
3. How do you build an `IN` list safely for 5 values?
4. What is the difference between `%a%` and `a%` in `LIKE`?
5. Why is `BETWEEN` inclusive a date-range footgun?

## Further Reading / Connections

- Next: Lecture 07, Sorting with ORDER BY.
- SQL Fundamentals 05 (advanced filtering, three-valued logic).
- Exercise: `06-where.py`.
