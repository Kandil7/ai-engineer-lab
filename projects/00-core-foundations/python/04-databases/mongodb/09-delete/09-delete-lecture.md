# MongoDB Lecture 09: Deleting Documents

## 🎯 Topic Overview

Deletion destroys by default, so it gets the strictest habits: targeted filters, `deleted_count` verification, and the soft-delete alternative. This lecture covers `delete_one`, `delete_many`, whole-collection clears, and the return values that prove what happened.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Delete one document with `delete_one`
2. Delete by filter with `delete_many`
3. Clear a collection while keeping it
4. Verify with `deleted_count`
5. Choose hard vs soft delete deliberately

## Prerequisites

- Filters (Lectures 05–06).
- What `rowcount` verification means (SQL analogues).

---

## 1. Introduction

MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents. This lecture covers deleting documents with Python using PyMongo.

The rule for this topic: never run a delete you have not already run as a `find`. The filter is the whole safety story.

---

## 2. Core Concepts

### 1. delete_one

`db.users.delete_one({'name': 'Alice'})` deletes the first matching document.

```python
result = db["users"].delete_one({"_id": user_id})
assert result.deleted_count == 1   # prove it hit
```

Deleting by `_id` is the precise case; deleting by a non-unique filter removes an arbitrary first match — usually a bug.

### 2. delete_many

`db.users.delete_many({'age': {'$lt': 18}})` deletes all matching documents.

```python
preview = db["users"].count_documents({"age": {"$lt": 18}})
print("about to delete:", preview)
result = db["users"].delete_many({"age": {"$lt": 18}})
print("deleted:", result.deleted_count)
```

Preview with `count_documents`, then compare with `deleted_count`. A mismatch means the data moved under you.

### 3. Delete All

`db.users.delete_many({})` removes all documents but keeps the collection.

The empty filter `{}` matches everything — the most dangerous two characters in the driver. Some teams ban bare `{}` in deletes by linting for it.

### 4. Return Value

`result.deleted_count` shows how many documents were deleted.

Zero when you expected one is a signal, not a success: wrong id, wrong filter, or a concurrent delete. Assert the count in tooling and tests.

### 5. Soft delete alternative

Add `{"active": True}` and filter on it instead of removing. History survives and "undelete" is an update — at the cost of filtering every query and complicating unique indexes. Use it for audit/retention requirements; hard-delete for true erasure.

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

### Bare `{}` filter in delete_many
Empties the collection. Preview first, assert `deleted_count` after.

### Deleting by non-unique filter with delete_one
Removes an arbitrary match. Delete by `_id` when precision matters.

---

## 4. Best Practices

1. Preview every delete as a `find`/`count_documents` first.
2. Assert `deleted_count` in scripts and tests.
3. Delete by `_id` for precision.
4. Ban bare `{}` deletes in shared tooling.
5. Choose soft vs hard delete by retention requirements.

---

## 5. Practice Exercises

### Exercise 1: Verified Delete
Delete one document by `_id`, asserting `deleted_count == 1`.

### Exercise 2: Bulk Purge
Preview, delete, and verify a date-bounded purge, reporting all three numbers.

### Exercise 3: Soft Delete
Add an `active` flag migration and rewrite two queries to respect it.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| `delete_one` | First match; prefer `_id` filters |
| `delete_many` | All matches; preview first |
| `{}` | Matches everything — handle with care |
| `deleted_count` | Proof of what happened |
| Soft delete | History at the cost of perpetual filtering |

## Key Takeaways

1. Preview as find, then delete.
2. `deleted_count` is the verification, not a formality.
3. Bare `{}` empties the collection.
4. Delete by `_id` for precision.
5. Soft vs hard is a retention decision.

## Self-Check Questions

1. What does `delete_many({})` do?
2. How do you verify a delete hit what you intended?
3. Why is deleting by a non-unique filter risky with `delete_one`?
4. When is soft delete right, and what does it cost?
5. What guard belongs around `{}` in shared tooling?

## Further Reading / Connections

- Next: Lecture 10, Updating Documents.
- SQL analogues: sqlite Lecture 08.
- Exercise: `09-delete.py`.
