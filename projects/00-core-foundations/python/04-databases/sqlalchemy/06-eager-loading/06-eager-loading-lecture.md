# Databases (SQLAlchemy) — 06: Eager Loading and the N+1 Problem

## Topic Overview

The N+1 problem is the most common performance defect in ORM-backed services:
list N parents, then lazily fire one query per parent for its children — 101
queries where 2 sufficed. This lecture demonstrates it with measured query
counts, fixes it with the three eager strategies, and locks the fix with an
assertion so it cannot silently regress.

For AI/backend engineers this is the read path of every registry listing, run
explorer, and eval matrix: "one extra query per row" turns a 5 ms endpoint
into a 500 ms one. Query counts are the guard (PRACTICE_SPEC rule 1) — count
SQL statements to prove the N+1 is fixed.

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Reproduce N+1 with lazy loading and count exactly N+1 statements
2. Fix it with `selectinload` and prove 2 statements via an event listener
3. Choose `selectinload` vs `joinedload` vs `subqueryload` deliberately
4. Set `lazy=` strategies per relationship with justification
5. Write a regression test asserting the query count ceiling

## Prerequisites

| Need | Where |
|---|---|
| Declarative models, relationships | `02-declarative-models/`, `04-relationships/` |
| 2.0 select() reads | [05](05-querying-2.0-lecture.md) |
| The runnable exercise | [06-eager-loading.py](06-eager-loading.py) |

## 1. The Bug, Counted

```python
from sqlalchemy import event

queries = []
event.listen(engine, "before_cursor_execute", lambda *a: queries.append(a[2]))

projects = session.scalars(select(Project)).all()
for p in projects:
    print(p.name, len(p.experiments))  # one query PER project: N+1
assert len(queries) == 1 + len(projects)
```

Default relationship loading is lazy: attribute access fires SQL. The event
listener makes the invisible visible — never diagnose ORM performance
without counting statements first.

## 2. The Three Fixes

```python
from sqlalchemy.orm import selectinload, joinedload, subqueryload

# selectinload: 2 statements (parents, then children WHERE parent_id IN ...)
# default choice for collections; no row duplication, no cartesian products
q = select(Project).options(selectinload(Project.experiments))

# joinedload: 1 statement with a JOIN; parent rows duplicate per child —
# fine for many-to-one, dangerous for large one-to-many (row explosion)
q = select(Project).options(joinedload(Project.owner))

# subqueryload: 2 statements via a subquery; niche — legacy alternative
```

Decision rule: collections get `selectinload`; single references get
`joinedload`; `subqueryload` only when inheriting code that already uses it.
Per-relationship `lazy="selectin"` bakes the default into the model; explicit
`.options()` overrides per query. Either way the query-count test from
section 1 stays green.

## 3. Locking the Fix

```python
def test_registry_listing_query_count():
    queries.clear()
    rows = session.scalars(select(Project).options(selectinload(Project.experiments))).all()
    for r in rows:
        _ = len(r.experiments)
    assert len(queries) <= 2  # the N+1 cannot silently return
```

Count assertions belong in CI for every list endpoint. Performance fixes
without regression tests are intentions, not fixes.

## Common Mistakes

- `joinedload` on big one-to-many (cartesian row explosion dwarfs the join saving).
- Eager-loading everything "to be safe" (over-fetching replaces N+1 with 1+giant).
- Counting queries in dev with 3 rows and declaring victory (N+1 hides below ~10).
- `lazy="dynamic"` legacy queries that bypass 2.0 patterns silently.

## DevMate Connection

Week 4 lists conversations with messages and eval runs with scores — both
are one-to-many reads over the exact relationship shape of this lecture.
The API ships with count-asserted tests on its list endpoints, and the SQL
sprint's EXPLAIN pass treats any per-row statement pattern as a defect on
sight.

## Key Takeaways

1. Count statements first; N+1 is measured, not suspected.
2. Collections `selectinload`, references `joinedload`, test the ceiling.
3. The regression test is the fix — everything else is a suggestion.
