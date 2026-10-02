# MongoDB Lecture 08: Limiting and Skipping

## 🎯 Topic Overview

`limit` bounds a result; `skip` pages through it — and `skip` degrades exactly like SQL `OFFSET`. This lecture covers both, the pagination pattern they compose into, and the cursor-based alternative production uses.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Bound results with `limit()`
2. Page with `skip()` + `limit()`
3. Explain why deep `skip` is slow
4. Implement cursor (keyset) pagination with a ranged filter
5. Choose the right pagination for the scale

## Prerequisites

- `find` and sort (Lectures 05, 07).
- Why arbitrary order breaks pages.

---

## 1. Introduction

MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents. This lecture covers limiting and skipping with Python using PyMongo.

Limit is a safety device as much as a feature: every unbounded read is a future OOM. Skip is a convenience that scales poorly. Knowing both — and when to replace skip — is the subject.

---

## 2. Core Concepts

### 1. limit()

`db.users.find().limit(10)` restricts results to a maximum number of documents.

```python
page = list(db["users"].find().sort("_id").limit(10))
```

`limit` composes with sort and filter; the engine can stop early instead of scanning everything.

### 2. skip()

`db.users.find().skip(20)` skips the first N documents.

Skip walks past N documents on every page. Page 1 costs 10 reads; page 10,000 costs 100,000 — the same rescanning disease as SQL `OFFSET`.

### 3. Pagination

`db.users.find().skip(page * size).limit(size)` implements pagination.

```python
def page(n, size=20):
    return list(db["users"].find().sort("_id").skip(n * size).limit(size))
```

Correct for small collections and admin screens; wrong for deep or hot pagination.

### 4. Performance

Skip becomes slow on large datasets. Use cursor-based pagination for production.

```python
# keyset: continue from the last seen _id — no rescanning
def page_after(last_id, size=20):
    return list(db["users"].find({"_id": {"$gt": last_id}}).sort("_id").limit(size))
```

A ranged filter on an indexed, unique key is O(page size) on every page. The client keeps the last id instead of a page number.

### 5. When skip is fine

Small, cold, administrative listings where simplicity beats scale. Even there, cap the page number so a curious `?page=99999` cannot tie up the server.

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

### Unbounded page numbers
Deep skip on a hot endpoint is a self-inflicted DoS. Cap pages or switch to keyset.

### Paginating unsorted results
Without a deterministic sort, pages overlap and skip rows.

---

## 4. Best Practices

1. Always `limit()` reads that feed a page or a loop.
2. Sort deterministically (end with `_id`) before paging.
3. Use keyset pagination for deep or hot pages.
4. Cap page numbers on skip-based endpoints.
5. Index the keyset key.

---

## 5. Practice Exercises

### Exercise 1: Skip Cost
Time page 1 vs page 5000 on a 100k collection and record the ratio.

### Exercise 2: Keyset Rewrite
Convert a skip-based pager to `$gt`-on-`_id` and show constant page cost.

### Exercise 3: Page Cap
Add a max-page guard to a skip endpoint and return 400 beyond it.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| `limit` | Bounds every read |
| `skip` | Simple paging, rescans |
| Pagination | skip+limit, small scale |
| Keyset | Ranged filter, constant cost |
| Guard | Cap pages; sort deterministically |

## Key Takeaways

1. `limit` is a safety device; use it everywhere.
2. `skip` rescans — cost grows with depth.
3. Keyset pagination is O(page size) on every page.
4. Sort deterministically or pages drift.
5. Cap skip-based pages.

## Self-Check Questions

1. Why does page 10,000 cost more than page 1 with skip?
2. How does a `$gt`-on-`_id` filter replace skip?
3. What must the sort contain for stable pages?
4. When is skip acceptable?
5. What guard belongs on a skip endpoint?

## Further Reading / Connections

- Next: Lecture 09, Deleting Documents.
- SQL Fundamentals 14 (keyset vs offset).
- Exercise: `08-limit.py`.
