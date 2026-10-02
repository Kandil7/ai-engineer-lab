# MongoDB Lecture 02: Working with Databases

## 🎯 Topic Overview

In MongoDB there is no `CREATE DATABASE` ceremony: the first write brings the database into existence. That convenience hides real decisions — naming, listing, dropping, and separating environments — that this lecture makes explicit with PyMongo.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Reference a database explicitly with `client["name"]`
2. List databases with `list_database_names()`
3. Drop a database with `drop_database()` and understand its finality
4. Explain why databases appear lazily on first write
5. Separate environments by database name

## Prerequisites

- Connecting with `MongoClient` (Lecture 01).
- What a database vs a collection is.

---

## 1. Introduction

MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents. This lecture covers working with databases with Python using PyMongo.

Unlike MySQL's explicit `CREATE DATABASE` or sqlite's file-per-database, MongoDB databases are namespaces that materialize on first use. The lecture maps each management operation to its PyMongo call.

---

## 2. Core Concepts

### 1. Creating Databases

In MongoDB, databases are created implicitly on first use: `db = client['mydb']`.

```python
db = client["mydb"]  # reference; nothing created yet
db["users"].insert_one({"name": "Alice"})  # first write creates db + collection
```

Referencing alone creates nothing — a typo in the name silently targets an empty database. Verify with a list call after setup scripts.

### 2. Listing Databases

`client.list_database_names()` returns all database names on the server.

```python
print(client.list_database_names())
```

System databases (`admin`, `local`, `config`) always appear; filter them when presenting to users or when asserting setup state in tests.

### 3. Dropping Databases

`client.drop_database('mydb')` permanently deletes a database and all its collections.

There is no recycle bin and no transaction around it. In tooling, gate drops behind an explicit `--confirm` flag plus a backup; in tests, prefer unique-per-run database names over dropping shared ones.

### 4. Database References

Use `db = client.get_database('mydb')` or `db = client['mydb']` syntax.

`get_database` accepts options (codec, read preference) for that handle; the bracket form uses the client's defaults. Pick one style per codebase — the bracket form reads best in application code.

### 5. Environments by name

```python
db = client[os.environ.get("MONGO_DB", "myapp_dev")]
```

`myapp_dev`, `myapp_test`, `myapp` — the database name is configuration, and tests get a fresh name per run so they never touch shared state.

---

## 3. Common Mistakes

### Not handling ObjectId serialization
ObjectId is not JSON serializable by default. Use bson.json_util for proper serialization:
```python
from bson import json_util
import json

# Serialize a document with ObjectId
json.dumps(doc, default=json_util.default)
```

### Using implicit database references
Explicit syntax is clearer and less error-prone:
```python
# OK but implicit
col = client.mydb.users

# Better - explicit
col = client["mydb"]["users"]
```

### Targeting a typo'd database
Because creation is lazy, `client["mydb "]` (trailing space) silently works on an empty database. Assert expected collections exist after setup.

### Dropping the wrong database
`drop_database` takes a name string — parameterize it from config, never interpolate user input, and never run it against production without a backup.

---

## 4. Best Practices

1. Reference databases explicitly with `client["name"]`.
2. Derive the database name from env per environment.
3. Verify setup with `list_database_names()` / `list_collection_names()`.
4. Gate drops behind confirmation and backups.
5. Use per-run database names in tests.

---

## 5. Practice Exercises

### Exercise 1: Create by Writing
Reference a new database, insert one document, and show it appears in `list_database_names()`.

### Exercise 2: Safe Drop
Write a function that drops a database only when its name starts with `test_` and a `confirm=True` flag is passed.

### Exercise 3: Env Separation
Load the database name from env with a `_dev` default and assert the test suite never touches the dev database.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| Creation | Lazy, on first write |
| Listing | `list_database_names()`; filter system DBs |
| Dropping | Permanent; gate and back up |
| Reference | Explicit `client["name"]` |
| Environments | Name per env from config |

## Key Takeaways

1. Databases materialize on first write — referencing creates nothing.
2. Lazy creation makes typos silent; verify after setup.
3. Drops are final; confirm, back up, restrict by name.
4. One name per environment, from env, keeps tests isolated.

## Self-Check Questions

1. What creates a MongoDB database?
2. Why can a typo'd database name go unnoticed?
3. What must happen before `drop_database` in tooling?
4. How do `get_database` and `client["name"]` differ?
5. Why do tests use per-run database names?

## Further Reading / Connections

- Next: Lecture 03, Working with Collections.
- Exercise: `02-databases.py`.
