# MongoDB Lecture 05: Querying Documents

## 🎯 Topic Overview

Reading in MongoDB is filter-plus-shape: `find` selects documents, projection selects fields, and cursors stream the rest. This lecture covers `find`, `find_one`, projection, and the cursor discipline that keeps large reads from eating memory.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Filter with `find()` and fetch one with `find_one()`
2. Shape output with projection (include/exclude fields)
3. Iterate cursors without materializing huge results
4. Distinguish `None` (no match) from an empty cursor
5. Print nested documents readably

## Prerequisites

- Documents and collections (Lectures 01–03).
- Inserted data to query (Lecture 04).

---

## 1. Introduction

MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents. This lecture covers querying documents with Python using PyMongo.

A query has three parts: which documents (filter), which fields (projection), and how many in what order (sort/limit, Lectures 07–08). This lecture covers the first two; the cursor is the vehicle for all of them.

---

## 2. Core Concepts

### 1. find()

`db.users.find()` returns all documents. `db.users.find({'age': 25})` filters results.

```python
for doc in db["users"].find({"age": {"$gte": 18}}):
    print(doc["name"])
```

`find` returns a cursor, not a list — iteration streams from the server. Calling `list()` on it materializes everything, which is the OOM footgun for large collections.

### 2. find_one()

`db.users.find_one({'name': 'Alice'})` returns the first matching document or None.

Use it for by-id and by-unique-key lookups. A `None` result means "no match", distinct from an empty cursor — check explicitly rather than letting `None["field"]` raise later.

### 3. Projection

`db.users.find({}, {'name': 1, '_id': 0})` includes/excludes specific fields.

```python
# only names, no _id, no other fields over the wire
names = db["users"].find({}, {"name": 1, "_id": 0})
```

Projection is both a bandwidth and a secrecy control: password hashes and tokens should never leave the database unless the caller needs them. Note `_id` is included by default and must be excluded explicitly.

### 4. Pretty Printing

Use `pprint` from pprint module for readable output of nested documents.

```python
from pprint import pprint
pprint(db["users"].find_one({"name": "Alice"}))
```

For JSON output (APIs, logs), serialize with `bson.json_util`, not `json.dumps` directly — `ObjectId` and dates need it.

### 5. Cursor discipline

```python
cursor = db["users"].find({}).batch_size(100)
for doc in cursor:
    process(doc)   # bounded memory, streaming
```

Set `batch_size` for large scans, `limit()` for top-N, and never `list()` an unbounded cursor. Cursors time out server-side if idle — process steadily or use `no_cursor_timeout` with explicit close.

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

### list() on an unbounded cursor
Materializing millions of documents OOMs the client. Stream, batch, or limit.

### Forgetting _id in projection
`{"name": 1}` still returns `_id`. Exclude it explicitly when the consumer must not see it.

---

## 4. Best Practices

1. Project only needed fields; exclude `_id` when it must not leak.
2. Stream with cursors; reserve `list()` for bounded results.
3. Check `find_one` for `None` before dereferencing.
4. Serialize with `json_util` at boundaries.
5. Set `batch_size` on large scans.

---

## 5. Practice Exercises

### Exercise 1: Filter and Project
Insert 20 users, query adults projecting only names, and assert `_id` is absent.

### Exercise 2: Streaming Count
Count a large collection twice — once with `list()`, once by iteration — and compare peak memory.

### Exercise 3: None Handling
Write a `get_user_or_404` helper that maps `find_one` `None` to a clean not-found error.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| `find` | Filtered cursor, streamed |
| `find_one` | First match or `None` |
| Projection | Include/exclude; `_id` needs explicit exclusion |
| Cursors | Stream; never `list()` unbounded |
| Output | `pprint` for humans, `json_util` for machines |

## Key Takeaways

1. Filters select documents; projection selects fields.
2. Cursors stream — materialize only bounded results.
3. `find_one` returns `None` on miss; check it.
4. Projection is a bandwidth and secrecy control.
5. Serialize `ObjectId` at every boundary.

## Self-Check Questions

1. What is the difference between a cursor and a list of documents?
2. How do you exclude `_id` from projected output?
3. Why is `list()` on an unbounded cursor dangerous?
4. What does `find_one` return on no match, and how should callers handle it?
5. When is `json_util` required instead of plain `json`?

## Further Reading / Connections

- Next: Lecture 06, Query Operators.
- Lectures 07–08 (sort/limit) complete the read path.
- Exercise: `05-find.py`.
