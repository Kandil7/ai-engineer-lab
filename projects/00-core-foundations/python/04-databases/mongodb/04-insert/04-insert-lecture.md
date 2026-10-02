# MongoDB Lecture 04: Inserting Documents

## 🎯 Topic Overview

Writes are where data enters the system, and the choices — one vs many, ordered vs unordered, client-generated vs server-generated `_id` — decide both speed and failure behavior. This lecture covers `insert_one`, `insert_many`, `_id` semantics, and bulk-write ordering.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Insert one document with `insert_one` and read the generated `_id`
2. Bulk-insert with `insert_many` and interpret partial results
3. Choose ordered vs unordered bulk writes by failure semantics
4. Decide when to supply `_id` vs letting the server generate it
5. Handle duplicate-key and write errors

## Prerequisites

- Collections (Lecture 03) and the document model (Lecture 01).
- What `_id`/`ObjectId` is.

---

## 1. Introduction

MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents. This lecture covers inserting documents with Python using PyMongo.

Every insert assigns an `_id`; every bulk insert chooses what happens when one document fails. The defaults are safe for learning and wrong for production bulk loads, which is why this lecture exists.

---

## 2. Core Concepts

### 1. insert_one

`db.users.insert_one({'name': 'Alice', 'age': 25})` inserts a single document and returns InsertOneResult.

```python
result = db["users"].insert_one({"name": "Alice", "age": 25})
print(result.inserted_id)  # the _id, generated or supplied
```

### 2. insert_many

`db.users.insert_many([doc1, doc2])` inserts multiple documents efficiently and returns InsertManyResult.

```python
result = db["users"].insert_many([{"name": "Bob"}, {"name": "Cleo"}], ordered=False)
print(result.inserted_ids)
```

One round-trip for the batch instead of N — the same bulk discipline as SQL `executemany`.

### 3. The _id Field

Every document requires a unique `_id` field. Auto-generated as ObjectId if omitted.

Supply `_id` when the id is meaningful (a natural key, an idempotent operation id); otherwise let the server generate it. Client-supplied ids enable idempotent retries: re-inserting the same `_id` fails fast instead of duplicating.

### 4. Ordered vs Unordered

Ordered inserts stop on first error. Unordered continues with remaining documents.

```python
# ordered=True (default): aborts the batch at the first failure
# ordered=False: inserts everything insertable, reports the failures
```

Bulk loads use `ordered=False` so one bad document does not discard ten thousand good ones; the errors come back in the result for handling.

### 5. Write concern and errors

Duplicate `_id` raises `DuplicateKeyError`; validation failures raise `WriteError`. Catch them per bulk result rather than letting one poison the whole import — and for critical writes, use majority write concern so the data survives a failover.

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

### Ordered bulk loads in production imports
One malformed document aborts the batch. Use `ordered=False` and handle the error list.

### Ignoring duplicate-key errors on retry
A retried insert with a client-supplied `_id` raises `DuplicateKeyError` — which means "already done", not "failed". Treat it as success.

---

## 4. Best Practices

1. Bulk-insert with `insert_many`, unordered for imports.
2. Supply `_id` for idempotent operations; generate otherwise.
3. Handle `DuplicateKeyError` as already-done on retry.
4. Use majority write concern for critical writes.
5. Validate shapes before the batch, not after.

---

## 5. Practice Exercises

### Exercise 1: Round-Trip
Insert one document, read it back by `_id`, and assert equality.

### Exercise 2: Unordered Bulk
Insert 1000 documents with 3 deliberate duplicates, unordered, and report inserted vs failed counts.

### Exercise 3: Idempotent Retry
Write an insert helper keyed by client-supplied `_id` that is safe to call twice.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| `insert_one` | One doc, returns its `_id` |
| `insert_many` | Batched; unordered for imports |
| `_id` | Unique always; meaningful ids enable idempotency |
| Errors | `DuplicateKeyError`/`WriteError`, handled per batch |
| Concern | Majority for data that must survive failover |

## Key Takeaways

1. One round-trip per batch, not per document.
2. Unordered bulk continues past bad documents.
3. Client-supplied `_id` makes retries idempotent.
4. Duplicate-key on retry means already-done.
5. Critical writes use majority concern.

## Self-Check Questions

1. What does `inserted_id` give you that the input dict lacks?
2. When is `ordered=False` correct?
3. How does a client-supplied `_id` make an insert idempotent?
4. What two error types must a bulk import handle?
5. Why does write concern matter on failover?

## Further Reading / Connections

- Next: Lecture 05, Querying Documents.
- Lecture 10 (updates/upserts) for the retry-safe write.
- Exercise: `04-insert.py`.
