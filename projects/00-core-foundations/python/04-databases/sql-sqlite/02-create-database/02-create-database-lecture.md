# MySQL Lecture 02: Creating and Managing Databases

## 🎯 Topic Overview

Every environment problem in database work traces back to this topic done carelessly: connecting to the wrong file, assuming a database exists, or deleting what you meant to keep. MySQL creates databases explicitly with `CREATE DATABASE`; sqlite3 creates them implicitly the moment you connect. Understanding both models — and the sqlite3 idioms that stand in for `USE` and `DROP DATABASE` — is the foundation every later lecture assumes.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Create new databases using CREATE DATABASE
2. Select and switch between databases with USE
3. Drop databases safely with DROP DATABASE
4. List available databases
5. Understand sqlite3 vs MySQL database creation differences

## Prerequisites

- Python installed and runnable (Core Python 02).
- Basic file-path concepts (absolute vs relative).

---

## 1. Introduction

This lecture covers creating and managing databases in MySQL using Python's sqlite3 as a learning companion.

In MySQL, a server holds many databases; you create, select, and drop them with SQL. In sqlite3, one file is one database; connecting to a path creates it, and there is no server-level catalogue. The mapping below lets you practice every MySQL concept with a local file.

---

## 2. Core Concepts

### 1. CREATE DATABASE

In MySQL, databases are created explicitly: `CREATE DATABASE mydb;`. In sqlite3, databases are created automatically when you connect: `sqlite3.connect('mydb.db')`.

```python
import sqlite3

# This creates a database file if it doesn't exist
conn = sqlite3.connect("mydatabase.db")
print("Database created (or opened) successfully!")
conn.close()
```

Use `IF NOT EXISTS` in MySQL (`CREATE DATABASE IF NOT EXISTS mydb;`) so re-running a script is safe. In sqlite3, connecting is idempotent by construction — the call either opens or creates.

### 2. USE Database

In MySQL, `USE mydb;` selects which database to operate on. In sqlite3, you select the database at connection time — you can't switch databases without creating a new connection.

```python
# sqlite3 equivalent of USE: open a second connection to the other file
sales = sqlite3.connect("sales.db")
archive = sqlite3.connect("archive.db")
```

### 3. DROP DATABASE

`DROP DATABASE mydb;` permanently removes a database. In sqlite3, you simply delete the .db file.

```python
# For sqlite3, dropping a database means closing the connection
# and deleting the file
conn.close()
import os

os.remove("mydatabase.db")
print("Database deleted.")
```

Dropping is irreversible. In production the safe pattern is backup-then-drop, and in MySQL `DROP DATABASE IF EXISTS` avoids failing scripts mid-migration.

### 4. SHOW DATABASES

`SHOW DATABASES;` lists all databases on the MySQL server. In sqlite3, this doesn't apply — each .db file is a separate database. The equivalent inspection is listing the directory, or in SQLite attaching multiple files and querying `PRAGMA database_list;`.

```python
conn = sqlite3.connect("mydatabase.db")
print(conn.execute("PRAGMA database_list;").fetchall())
conn.close()
```

### 5. Connection hygiene: context managers

Every connection you open must close, even on error. The `with` statement on a sqlite3 connection commits-or-rolls-back and keeps ownership clear:

```python
with sqlite3.connect("mydatabase.db") as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS t (id INTEGER PRIMARY KEY)")
# exits cleanly, transaction committed
```

---

## 3. Common Mistakes

### Forgetting to close connections
```python
# WRONG
conn = sqlite3.connect('test.db')
# ... work ...
# conn never closed!

# RIGHT
conn = sqlite3.connect('test.db')
try:
    # ... work ...
finally:
    conn.close()
```

### Using reserved words as database names
```python
# WRONG
conn = sqlite3.connect("select.db")  # 'select' is a reserved word

# RIGHT
conn = sqlite3.connect("my_select_data.db")
```

### Deleting the wrong file
A relative path resolves against the working directory, not the script. Confirm with an absolute path before `os.remove`, or you will delete a file you did not mean to.

---

## 4. Best Practices

1. Use descriptive database names
2. Always close connections when done
3. Use in-memory databases for testing
4. Handle database creation errors
5. Use IF NOT EXISTS / IF EXISTS for safety

---

## 5. Practice Exercises

### Exercise 1: Create and Connect
Create a new database file, connect to it, create a simple table, insert data, query it, and close the connection.

### Exercise 2: Error Handling
Write a function that attempts to connect to a database and handles FileNotFoundError or sqlite3.OperationalError gracefully.

### Exercise 3: Multiple Databases
Create two separate database files, insert data into each, and prove they are independent by querying both.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| CREATE DATABASE | Explicit in MySQL, automatic in sqlite3 |
| USE | Switch databases in MySQL, set at connect in sqlite3 |
| DROP DATABASE | Permanent deletion — use with extreme caution |
| SHOW DATABASES | List available databases |
| Cleanup | Always close connections to avoid corruption |

## Key Takeaways

1. MySQL manages databases explicitly; sqlite3 maps one file to one database.
2. Connecting in sqlite3 is idempotent create-or-open.
3. "Dropping" a sqlite file means close-then-delete; verify the path first.
4. Use context managers so connections close even on error.
5. In-memory databases (`:memory:`) are the right tool for tests.

## Self-Check Questions

1. What happens when you connect to a nonexistent sqlite3 path?
2. How do you "USE" a different database in sqlite3?
3. Why is `IF NOT EXISTS` important in re-runnable setup scripts?
4. What must happen before deleting a sqlite database file?
5. Why are in-memory databases preferred for tests?

## Further Reading / Connections

- Next: Lecture 03, Creating Tables.
- `PRAGMA database_list` and `ATTACH DATABASE` for multi-file SQLite work.
- Exercise: `02-create-database.py`.
