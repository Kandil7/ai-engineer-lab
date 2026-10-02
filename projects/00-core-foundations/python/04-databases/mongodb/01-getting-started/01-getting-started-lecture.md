# MongoDB Lecture 01: Getting Started with MongoDB

## 🎯 Topic Overview

MongoDB is a NoSQL document database that stores data as JSON-like documents instead of rows and columns. Where a relational table forces every row into the same columns, a MongoDB collection holds documents that share a shape by convention, not by enforcement — flexible when your data evolves, demanding discipline when it does. This lecture covers the document model, the four CRUD operations at a glance, and connecting with PyMongo.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Explain the document model: databases, collections, documents, fields
2. Connect with `MongoClient` and select a database and collection explicitly
3. Name the four CRUD operations and their PyMongo entry points
4. Serialize an `ObjectId` to JSON with `bson.json_util`
5. Compare a document to a relational row

## Prerequisites

- Python dicts, lists, and JSON basics.
- What a database connection is (PostgreSQL 01 or SQLite lectures).

---

## 1. Introduction

MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents. This lecture covers getting started with mongodb with Python using PyMongo.

A document looks like the JSON you already know, with two additions: a mandatory `_id` key and a richer type system (dates, `ObjectId`, decimals). A collection is a group of documents — roughly a table, without the fixed schema.

---

## 2. Core Concepts

### 1. What is MongoDB?

MongoDB is a NoSQL document database that stores data as JSON-like documents instead of rows and columns.

The tradeoff is explicit: schema flexibility and nested data in exchange for giving up joins, foreign keys, and multi-document transactions as the default. It fits catalogs, profiles, logs, and content — data that is read as a whole document.

### 2. Document Model

Documents are Python dicts with key-value pairs. Collections hold documents. Schema is flexible.

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["shop"]
users = db["users"]

users.insert_one({"name": "Alice", "age": 25, "tags": ["pro", "early"]})
```

Nested dicts and arrays are first-class: an address sub-document and a tags array live inside the user document instead of in joined tables.

### 3. CRUD Overview

Create (insert), Read (find), Update (update), Delete (delete) are the four basic operations.

```python
users.insert_one({"name": "Bob", "age": 30})          # create
users.find_one({"name": "Bob"})                        # read
users.update_one({"name": "Bob"}, {"$set": {"age": 31}})  # update
users.delete_one({"name": "Bob"})                      # delete
```

Each operation takes a filter document plus, for writes, an update document. The filter language (`{"age": {"$gte": 18}}`) is shared across read, update, and delete.

### 4. PyMongo Driver

`pip install pymongo` then `from pymongo import MongoClient` to connect.

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
client.admin.command("ping")   # fail fast if no server
db = client["mydb"]
```

`MongoClient` pools connections internally; create one per process and share it. The URI carries host, port, credentials, and options — keep it in env, never in code.

### 5. ObjectId and JSON

Every document carries `_id`, auto-generated as an `ObjectId` when omitted. `ObjectId` encodes a timestamp, machine, process, and counter — roughly time-ordered and globally unique without coordination.

```python
from bson import json_util
import json

doc = users.find_one({"name": "Alice"})
print(json.dumps(doc, default=json_util.default))  # ObjectId-safe JSON
```

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

### Assuming the server exists
`MongoClient` connects lazily; the first operation fails, not the constructor. Ping at startup or set a short `serverSelectionTimeoutMS` so misconfiguration surfaces immediately.

### Treating flexible schema as no schema
Flexibility without validation drifts into incompatible shapes. Use schema validation rules (Lecture 12 companion) once the shape stabilizes.

---

## 4. Best Practices

1. One `MongoClient` per process, shared everywhere.
2. Keep the connection URI in env, with credentials never in code.
3. Use explicit `client["db"]["collection"]` references.
4. Serialize with `bson.json_util` at API boundaries.
5. Validate document shapes once they stabilize.

---

## 5. Practice Exercises

### Exercise 1: Connect and Insert
Connect to a local (or in-memory stand-in) MongoDB, insert a user document with nested address and tags, read it back, and print it as JSON.

### Exercise 2: CRUD Round-Trip
Create, read, update, and delete the same document, asserting the state after each step.

### Exercise 3: ObjectId JSON
Fetch a document and serialize it twice — once naively (observe the failure) and once with `json_util`.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| Document | A dict with `_id`; nested data lives inside |
| Collection | A group of documents; roughly a table |
| CRUD | `insert_*`, `find_*`, `update_*`, `delete_*` share filter syntax |
| PyMongo | One pooled client per process; URI from env |
| ObjectId | Time-ordered unique id; serialize with `json_util` |

## Key Takeaways

1. Documents replace rows; collections replace tables; `_id` replaces the PK.
2. One shared `MongoClient`; explicit `client["db"]["coll"]` references.
3. Filters are shared across find, update, and delete.
4. `ObjectId` is not JSON — serialize at the boundary.
5. Flexibility is a feature; validation is still required.

## Self-Check Questions

1. What are the three levels of the MongoDB data hierarchy?
2. Why is one `MongoClient` per process the right pattern?
3. What fails when you `json.dumps` a raw document, and what fixes it?
4. Which two CRUD operations share the same filter language?
5. When is a document database the wrong choice?

## Further Reading / Connections

- Next: Lecture 02, Working with Databases.
- Lecture 12 (`12-mongo-vs-sql`) for the document-vs-relational decision.
- Exercise: `01-getting-started.py`.
