# MongoDB Lecture 06: Query Operators

## 🎯 Topic Overview

Filters are a small language: comparison, logical, element, and regex operators compose into precise predicates. This lecture covers the operator set with PyMongo, plus the performance rule that decides which predicates use indexes.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:
1. Compare with `$gt/$lt/$gte/$lte/$ne/$in`
2. Combine with `$and/$or/$nor/$not`
3. Test shape with `$exists`/`$type`
4. Match strings with `$regex`
5. State which operators use indexes and which scan

## Prerequisites

- `find` and projection (Lecture 05).
- Indexes exist (Lecture 12 companion).

---

## 1. Introduction

MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents. This lecture covers query operators with Python using PyMongo.

Operators nest inside field specs: `{"age": {"$gte": 18, "$lt": 65}}`. Learning to read that nesting — field, then operator, then value — is learning to read every MongoDB query.

---

## 2. Core Concepts

### 1. Comparison Operators

`$gt` (greater than), `$lt` (less than), `$gte`, `$lte`, `$ne` (not equal), `$in` (in list).

```python
db["users"].find({"age": {"$gte": 18, "$lt": 65}, "city": {"$in": ["Cairo", "Alex"]}})
```

`$ne` is the expensive one: "everything but X" rarely uses an index well. Prefer positive predicates when the data allows.

### 2. Logical Operators

`$and` (all conditions), `$or` (any condition), `$nor` (none), `$not` (negation).

```python
db["users"].find({"$or": [{"role": "admin"}, {"age": {"$gt": 65}}]})
```

Top-level comma-separated fields are already an implicit `$and`; reach for explicit `$and` only when the same field needs two constraints that would otherwise collide as dict keys.

### 3. Element Operators

`$exists` (field exists), `$type` (field type check).

```python
db["users"].find({"email": {"$exists": True, "$ne": None}})
```

`$exists` plus `$ne: None` is the "has a real value" test — essential in flexible-schema collections where a field may be missing, null, or present.

### 4. Regex Queries

`db.users.find({'name': {'$regex': '^A'}})` for pattern matching on strings.

Anchor with `^` so the index can serve the prefix; unanchored patterns scan. Case-insensitive regex (`$options: "i"`) cannot use a plain index — use a case-insensitive index or a normalized field.

### 5. Operators and indexes

Equality and range on indexed fields use the index; `$ne`, `$not`, unanchored `$regex`, and `$where` (JavaScript — avoid) generally do not. Design filters so the selective, indexed predicate comes first.

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

### `$ne: None` meaning "exists"
`{"field": {"$ne": None}}` matches documents *missing* the field too. Add `$exists: True` when presence matters.

### Unanchored regex on large collections
A leading wildcard scans every document. Anchor, index, or move the pattern to a search engine.

---

## 4. Best Practices

1. Prefer equality and range on indexed fields.
2. Avoid `$ne`/`$not`/unanchored regex on hot paths.
3. Test presence with `$exists` + `$ne: None`.
4. Put the selective predicate first.
5. Never use `$where` JavaScript in application queries.

---

## 5. Practice Exercises

### Exercise 1: Operator Matrix
Build one query per operator family against a seeded collection and assert the counts.

### Exercise 2: Presence Test
Insert documents with missing, null, and valued emails; write the filter that returns only valued ones.

### Exercise 3: Regex Performance
Compare an anchored vs unanchored regex with `explain()` and record the stage difference.

---

## 6. Summary

| Concept | Key Takeaway |
|---------|-------------|
| Comparison | `$gt/$lt/$gte/$lte/$ne/$in` |
| Logical | `$and/$or/$nor/$not`; top level is implicit `$and` |
| Element | `$exists`/`$type` test shape |
| Regex | Anchor with `^`; index serves prefixes |
| Indexes | Selective indexed predicates first |

## Key Takeaways

1. Filters nest as field → operator → value.
2. `$ne` and unanchored regex rarely use indexes.
3. Presence needs `$exists` plus `$ne: None`.
4. Selective, indexed predicates lead.
5. `$where` JavaScript has no place in app queries.

## Self-Check Questions

1. Why does `$ne: None` also match missing fields?
2. Which regex shape can use an index, and why?
3. How do you express "field exists with a real value"?
4. Why is `$where` avoided?
5. What goes first in a compound filter, and why?

## Further Reading / Connections

- Next: Lecture 07, Sorting Results.
- Lecture 12 (`12-mongo-vs-sql`) for index types.
- Exercise: `06-query.py`.
