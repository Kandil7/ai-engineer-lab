# MongoDB Lecture 03: Working with Collections

## 🎯 Topic Overview

Collections are where documents live and where most operational decisions attach: creation options, capped behavior for logs, listing, and dropping. This lecture covers the collection lifecycle with PyMongo.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Create collections implicitly and explicitly with options
2. Use capped collections for fixed-size logs and queues
3. List collections with `list_collection_names()`
4. Drop a collection and understand its finality
5. Compare a collection to a relational table

## Prerequisites

- Databases in MongoDB (Lecture 02).
- What a document is (Lecture 01).

---

## 1. Introduction

MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents. This lecture covers working with collections with Python using PyMongo.

A collection is roughly a table without a fixed schema. The differences that matter are creation semantics (lazy), capped collections (fixed-size, ordered), and the lack of server-side schema enforcement by default.

---

## 2. Core Concepts

### 1. Creating Collections

Collections are created implicitly on first insert: `db.create_collection('users')` or explicitly with options.

```python
db.create_collection("users")  # explicit, default options
db.create_collection("events", capped=True, size=1024 * 1024)  # capped: 1 MB
db["logs"].insert_one({"msg": "boot"})  # implicit on first write
```

Explicit creation is for options (capped, validation rules); otherwise let the first insert create it.

### 2. Capped Collections

Fixed-size collections that maintain insertion order and automatically remove oldest documents.

Capped collections are the log/queue primitive: bounded disk, natural insertion order, no manual cleanup. They cannot be sharded by default and documents cannot grow beyond their allocation — size them for the retention window.

### 3. Listing Collections

`db.list_collection_names()` returns all collection names in the current database.

```python
print(db.list_collection_names())
```

System collections (`system.*`) appear; filter them in tooling output.

### 4. Dropping Collections

`db.users.drop()` removes a collection and all its documents permanently.

Like database drops, this is final. In migrations, dropping a collection is a reviewed, backed-up operation — not a REPL experiment.

### 5. Collection vs table

A table enforces one schema on every row; a collection holds whatever documents arrive. The application (or schema validation rules) owns shape discipline. Indexes, by contrast, work the same way: declared per collection, serving the same query shapes.

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

### Growing documents in a capped collection
Updates that grow a document fail in capped collections. Size documents once, or do not cap.

### Assuming schema enforcement
Without validation rules, any shape inserts. Add `$jsonSchema` validation once the shape stabilizes.

---

## 4. Best Practices

1. Create explicitly only when options (capped, validation) are needed.
2. Use capped collections for bounded logs and queues.
3. Verify with `list_collection_names()` after setup.
4. Gate drops behind confirmation and backups.
5. Add schema validation once shapes stabilize.

---

## 5. Practice Exercises

### Exercise 1: Implicit vs Explicit
Create one collection by insert and one by `create_collection` with a capped option; compare their stats.

### Exercise 2: Capped Log
Write 10k log lines to a 1 MB capped collection and show the oldest are evicted while order holds.

### Exercise 3: Safe Drop
Write a drop helper that refuses collections not prefixed `tmp_` without `confirm=True`.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| Creation | Lazy, or explicit with options |
| Capped | Fixed-size, ordered, self-evicting |
| Listing | `list_collection_names()` |
| Dropping | Permanent; gate and back up |
| Validation | Opt-in `$jsonSchema` for shape discipline |

## Key Takeaways

1. Collections are schema-flexible tables; creation is lazy.
2. Capped collections are the bounded-log primitive.
3. Drops are final — confirm and back up.
4. Validation rules, not hope, keep shapes consistent.

## Self-Check Questions

1. What creates a collection?
2. When must creation be explicit?
3. What evicts from a capped collection, and what cannot change there?
4. How do you verify setup created what you expected?
5. Where does shape discipline live without a fixed schema?

## Further Reading / Connections

- Next: Lecture 04, Inserting Documents.
- Lecture 12 (`12-mongo-vs-sql`) for schema-flexibility costs.
- Exercise: `03-collection.py`.
