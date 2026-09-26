# SQLAlchemy 06: Eager Loading — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| N+1 | 1 query for parents + N per-parent queries via lazy access | 101 queries for 100 rows |
| Lazy loading | Default: relationship SQL fires on attribute access | p.experiments triggers query |
| selectinload | Eager strategy: parents, then children via IN (2 stmts) | collections default |
| joinedload | Eager strategy: one JOINed statement, rows duplicate | many-to-one refs |
| subqueryload | Eager strategy via subquery (legacy niche) | inherited code only |
| Query-count test | Assertion capping statements per endpoint | CI performance gate |
| lazy= | Per-relationship default loading strategy | model-level policy |

---

## Alphabetical Glossary

### joinedload

**Definition:** Eager loading via SQL JOIN in a single statement. Parent rows
duplicate per child — safe for many-to-one, explosive for large one-to-many.

**Example:**
```python
select(Project).options(joinedload(Project.owner))
```

**Related concepts:** selectinload, N+1

---

### lazy=

**Definition:** Relationship-level default loading: `select` (lazy),
`selectin` (eager IN), `joined` (eager JOIN), `raise` (forbid implicit IO).
Policy in the model, overridable per query.

**Example:**
```python
experiments: Mapped[list["Experiment"]] = relationship(lazy="selectin")
```

**Related concepts:** Lazy loading, selectinload

---

### Lazy loading

**Definition:** Default ORM behavior: related collections load on first
attribute access, one query each. Convenient, and the N+1 factory.

**Example:**
```python
p.experiments  # innocent line, one query per project in a loop
```

**Related concepts:** N+1, selectinload

---

### N+1

**Definition:** The performance defect: 1 query for N parents plus 1 per
parent for children. Endpoint latency scales with row count; fixed by eager
loading, proven by statement counts.

**Example:**
```python
# 100 projects -> 101 statements; selectinload -> 2
```

**Related concepts:** Lazy loading, Query-count test

---

### Query-count test

**Definition:** A test asserting the statement ceiling of an endpoint via an
event listener. Turns "fast" from an observation into a gate.

**Example:**
```python
assert len(queries) <= 2  # N+1 cannot silently return
```

**Related concepts:** N+1, selectinload

---

### selectinload

**Definition:** Eager strategy issuing a second statement with `WHERE
parent_id IN (...)`. No duplication, no cartesian products — the collection
default.

**Example:**
```python
select(Project).options(selectinload(Project.experiments))
```

**Related concepts:** joinedload, lazy=

---

### subqueryload

**Definition:** Eager strategy via a subquery load. Largely superseded by
selectinload; encountered in inherited code, rarely chosen new.

**Example:**
```python
# know it on sight; prefer selectinload for new code
```

**Related concepts:** selectinload, joinedload

---

## Related Concepts

- **EXPLAIN**: proves the fixed plan, not just the count (PG04)
- ** cartesian products**: the joinedload-on-collections failure mode
- **Registry listings**: DevMate week-4 endpoints guarded by these tests

## Key Takeaways

1. Lazy by default, eager by decision.
2. Strategy follows relationship shape.
3. Counts in CI, or it regresses.
