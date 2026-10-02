# MongoDB Lecture 07: Sorting Results

## 🎯 Topic Overview

Unordered reads return whatever is cheapest, which looks stable until it changes. Sorting makes "top N", leaderboards, and pages deterministic. This lecture covers sort direction, multi-field sorts, sort-with-limit, and the index rule that keeps sorts fast.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Sort ascending (`1`) and descending (`-1`)
2. Sort by multiple fields with mixed directions
3. Combine sort with limit for top-N queries
4. Explain why sorts need supporting indexes at scale
5. Detect in-memory sort overflow in `explain()`

## Prerequisites

- `find` and cursors (Lecture 05).
- What an index is (Lecture 12 companion).

---

## 1. Introduction

MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents. This lecture covers sorting results with Python using PyMongo.

Sort is a cursor modifier: it composes with filter, limit, and skip. The order you chain them reads naturally — filter, sort, then take — and the engine plans accordingly.

---

## 2. Core Concepts

### 1. Basic Sort

`db.users.find().sort('age', 1)` ascending. `sort('age', -1)` descending.

```python
oldest_first = db["users"].find().sort("age", -1)
```

`1` and `-1` are the only directions; there is no natural-order sort beyond `$natural`, which reflects storage order and is not a query contract.

### 2. Multiple Fields

`db.users.find().sort([('age', 1), ('name', -1)])` sorts by multiple fields.

Later fields break ties from earlier ones. The canonical leaderboard shape is `(score DESC, _id ASC)` — score first, id as the deterministic tiebreaker.

### 3. Sort with Limit

`db.users.find().sort('age', -1).limit(5)` returns top 5 oldest users.

Sort-then-limit lets the engine keep only N winners instead of sorting everything — but only with a supporting index does it avoid the full sort. This is the top-N pattern behind feeds and leaderboards.

### 4. Sort and Index

Sorting on indexed fields is significantly faster.

An index on `(age DESC)` serves the sort directly; without it, the engine sorts in memory with a 32 MB limit per stage, spilling or failing beyond that. `explain()` shows `SORT` vs `IXSCAN` — the former is the warning.

### 5. Sort stability and pagination

Sorts are only stable with a unique tiebreaker. Paginating a sorted query without one skips and repeats rows across pages; end every sort key list with `_id`.

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

### Sorting without an index at scale
The in-memory sort cap fails large result sets. Index the sort keys.

### Paginating a non-unique sort
Ties reorder across pages. Always end with `_id`.

---

## 4. Best Practices

1. End every sort with a unique tiebreaker (`_id`).
2. Index sort keys; verify with `explain()`.
3. Pair sort with limit for top-N.
4. Prefer `(score DESC, _id ASC)` for leaderboards.
5. Never rely on natural order.

---

## 5. Practice Exercises

### Exercise 1: Top-N
Seed 100 users, return the 5 oldest with a single sort+limit, then prove an index removes the `SORT` stage.

### Exercise 2: Tiebreaker
Show page drift on a non-unique sort, then fix it with `_id`.

### Exercise 3: Compound Sort
Build a `(status ASC, created_at DESC)` sort with a matching compound index.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| Direction | `1` ascending, `-1` descending |
| Multi-field | List of pairs; tiebreaker last |
| Top-N | Sort + limit; index-backed |
| Index | Serves the sort; `explain()` proves it |
| Stability | Unique tiebreaker or pages drift |

## Key Takeaways

1. Directions are `1`/`-1`, per field, composable.
2. Top-N is sort+limit on an index.
3. In-memory sorts cap at 32 MB per stage.
4. Unique tiebreakers stabilize sorts and pages.
5. Natural order is not a contract.

## Self-Check Questions

1. How do you sort age down and name up in one query?
2. Why does top-N still need an index?
3. What fails when a sort exceeds 32 MB?
4. Why end sort keys with `_id`?
5. How does `explain()` distinguish an indexed sort?

## Further Reading / Connections

- Next: Lecture 08, Limiting and Skipping.
- Lecture 12 (`12-mongo-vs-sql`) for index types.
- Exercise: `07-sort.py`.
