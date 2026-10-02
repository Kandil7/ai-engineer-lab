# MongoDB Lecture 11: Aggregation Pipeline

## 🎯 Topic Overview

The aggregation pipeline is MongoDB's answer to `GROUP BY` on steroids: documents flow through stages — match, group, sort, shape — each transforming the stream. This lecture covers the core stages, accumulator functions, stage ordering for performance, and the `$lookup` join equivalent.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Compose a pipeline of `$match/$group/$sort/$project` stages
2. Aggregate with `$sum/$avg/$min/$max/$push`
3. Order stages for performance (`$match` first)
4. Reshape output with `$project`
5. Join collections with `$lookup` and know its cost

## Prerequisites

- `find` filters (Lectures 05–06).
- What `GROUP BY` does (SQL Fundamentals 06).

---

## 1. Introduction

MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents. This lecture covers aggregation pipeline with Python using PyMongo.

A pipeline is a list of stage documents. Documents enter the first stage; each stage's output feeds the next. Thinking in streams — what each stage receives and emits — is the whole skill.

---

## 2. Core Concepts

### 1. Aggregate Method

`db.users.aggregate([{'$match': ...}, {'$group': ...}])` processes documents through a pipeline.

```python
pipeline = [
    {"$match": {"age": {"$gte": 18}}},
    {"$group": {"_id": "$city", "count": {"$sum": 1}, "avg_age": {"$avg": "$age"}}},
    {"$sort": {"count": -1}},
]
for doc in db["users"].aggregate(pipeline):
    print(doc)
```

### 2. $match Stage

Filters documents (like find). Should be first stage for performance.

Early `$match` shrinks the stream before expensive stages run, and it can use indexes — a `$match` buried after a `$group` cannot. Filter first is the pipeline's prime directive.

### 3. $group Stage

Groups documents by a key. Supports accumulators: `$sum`, `$avg`, `$min`, `$max`, `$push`.

```python
{"$group": {"_id": "$city", "users": {"$push": "$name"}, "n": {"$sum": 1}}}
```

`_id` in `$group` is the group key (confusingly named — it is not the document id). Grouping by `None` aggregates the whole collection into one document.

### 4. $sort and $project

`$sort` reorders documents. `$project` includes/excludes/shapes fields in output.

```python
{"$project": {"name": 1, "adult": {"$gte": ["$age", 18]}, "_id": 0}}
```

`$project` computes derived fields inline — the pipeline's equivalent of `SELECT` expressions. Project early to slim documents before heavy stages.

### 5. $lookup and stage ordering

`$lookup` left-joins another collection. It is the escape hatch for referenced data, with join-like cost — prefer embedding for read-hot relations (Lecture 12) and reserve `$lookup` for genuinely separate entities.

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

### $match after $group
Filtering after grouping processes (and groups) documents you will discard. Match first.

### Unbounded $push accumulators
Pushing thousands of elements into one group document can exceed the 16 MB document limit. Bound or paginate.

---

## 4. Best Practices

1. `$match` first, always.
2. Project early to slim the stream.
3. Group by indexed keys where possible.
4. Bound `$push` accumulations.
5. Reserve `$lookup` for truly separate entities.

---

## 5. Practice Exercises

### Exercise 1: City Stats
Group users by city with count and average age, sorted by count desc.

### Exercise 2: Stage Reorder
Run a `$group`-then-`$match` pipeline and a `$match`-then-`$group` version; compare with `explain()`.

### Exercise 3: Lookup Join
Join orders to users with `$lookup`, then rewrite with embedding and compare.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| Pipeline | Ordered stages, stream in/out |
| `$match` | Filter first for index use |
| `$group` | Keyed aggregation with accumulators |
| `$project` | Shape and derive fields |
| `$lookup` | Join escape hatch, priced like one |

## Key Takeaways

1. Think in streams: each stage's output feeds the next.
2. `$match` first or pay for discarded work.
3. `_id` in `$group` is the group key.
4. Bound accumulators under the 16 MB limit.
5. Embedding beats `$lookup` for read-hot relations.

## Self-Check Questions

1. Why must `$match` come first?
2. What does `_id` mean inside `$group`?
3. How do you compute a derived boolean in `$project`?
4. What breaks when `$push` accumulates unboundedly?
5. When is `$lookup` appropriate despite its cost?

## Further Reading / Connections

- Next: Lecture 12, Mongo vs SQL.
- SQL Fundamentals 06 (GROUP BY) for the relational analogue.
- Exercise: `11-aggregation.py`.
