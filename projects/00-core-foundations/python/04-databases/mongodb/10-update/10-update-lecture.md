# MongoDB Lecture 10: Updating Documents

## 🎯 Topic Overview

Updates rewrite existing truth, so they inherit the delete discipline — preview the filter, verify the count — plus their own operators: `$set`, `$unset`, `$inc`, array updates, and upserts. This lecture covers targeted rewrites and the retry-safe patterns they enable.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Update one document with `update_one` and many with `update_many`
2. Apply `$set/$unset/$inc/$push/$pull` correctly
3. Use upserts for retry-safe writes
4. Verify with `matched_count`/`modified_count`
5. Avoid whole-document replacement bugs

## Prerequisites

- Filters (Lectures 05–06).
- The preview-then-write discipline (Lecture 09).

---

## 1. Introduction

MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents. This lecture covers updating documents with Python using PyMongo.

An update is a filter plus a mutation. The filter selects the victims; the update document changes them. Respect both halves: a wrong filter rewrites the wrong documents, and a replacement-style update drops fields you meant to keep.

---

## 2. Core Concepts

### 1. update_one

`db.users.update_one({'name': 'Alice'}, {'$set': {'age': 26}})` updates first match.

```python
result = db["users"].update_one({"_id": uid}, {"$set": {"age": 26}})
print(result.matched_count, result.modified_count)
```

`matched_count` vs `modified_count` differ when the document already holds the value — matched but unmodified is normal, not an error.

### 2. update_many

`db.users.update_many({'age': {'$lt': 18}}, {'$set': {'status': 'minor'}})` updates all matches.

Preview the filter as a `find` first; bulk rewrites without a preview are how whole collections get relabeled.

### 3. Update Operators

`$set` (set field), `$unset` (remove field), `$inc` (increment), `$push` (add to array), `$pull` (remove from array).

```python
db["users"].update_one(
    {"_id": uid},
    {
        "$set": {"status": "active"},
        "$inc": {"logins": 1},
        "$push": {"tags": "returning"},
    },
)
```

`$inc` is atomic — concurrent increments do not lose counts, unlike read-modify-write in Python. Array operators with `$each` and `$slice` bound array growth.

### 4. Upsert

`update_one(filter, update, upsert=True)` inserts if no document matches, updates otherwise.

```python
db["users"].update_one(
    {"email": "a@x.com"},
    {"$setOnInsert": {"created": now}, "$set": {"last": now}},
    upsert=True,
)
```

`$setOnInsert` separates creation-only fields from every-write fields — the canonical idempotent-write shape for retries and replays.

### 5. Replacement vs operators

Passing a bare document (no `$` operators) *replaces* the whole document except `_id`. Almost always a bug when `$set` was intended. Lint for update documents without operators.

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

### Replacement instead of $set
A bare document replaces everything. Use operators.

### Read-modify-write counters
Two concurrent readers both increment from the same value; one increment is lost. Use `$inc`.

---

## 4. Best Practices

1. Preview filters as `find` before bulk updates.
2. Use operators, never bare replacement documents.
3. Use `$inc` for counters.
4. Upsert with `$setOnInsert` for retry-safe writes.
5. Check `matched_count`/`modified_count` in tooling.

---

## 5. Practice Exercises

### Exercise 1: Verified Update
Update one document by `_id` and assert both counts.

### Exercise 2: Atomic Counter
Increment a counter from 10 concurrent workers with `$inc` and prove no loss.

### Exercise 3: Idempotent Upsert
Write an upsert keyed by email that is safe to run twice, with distinct create vs update fields.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| `update_one/_many` | First vs all matches |
| Operators | `$set/$unset/$inc/$push/$pull` |
| Upsert | Insert-or-update with `$setOnInsert` |
| Counts | `matched` vs `modified` |
| Replacement | Bare documents replace — usually a bug |

## Key Takeaways

1. Preview filters before bulk rewrites.
2. Operators mutate; bare documents replace.
3. `$inc` makes counters concurrency-safe.
4. Upserts plus `$setOnInsert` are the idempotent-write shape.
5. Verify with both counts.

## Self-Check Questions

1. When do `matched_count` and `modified_count` differ?
2. Why is read-modify-write wrong for counters?
3. What distinguishes `$set` from a bare update document?
4. How does `$setOnInsert` make an upsert idempotent?
5. What must you preview before `update_many`?

## Further Reading / Connections

- Next: Lecture 11, Aggregation Pipeline.
- Lecture 04 (inserts) for the write-error taxonomy.
- Exercise: `10-update.py`.
