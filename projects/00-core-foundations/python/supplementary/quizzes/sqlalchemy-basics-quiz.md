# SQLAlchemy Basics Quiz

## Topic Overview
SQLAlchemy is the de-facto Python ORM toolkit: Core (SQL expression language, schema, connections) and ORM (declarative mapped classes, sessions, relationships). This quiz covers the fundamentals: Core vs ORM, declarative models, the session lifecycle, relationships (one-to-many, many-to-many, self-referential), and 2.0-style querying with `select()`.

**Difficulty:** Beginner to Intermediate
**Questions:** 20
**Time:** ~25 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Easy]
**What does SQLAlchemy Core provide?**

A) Only the high-level ORM with no raw SQL support
B) Only an async driver for SQLite
C) A low-level SQL toolkit: schema metadata, SQL expression language, engine/connection handling
D) A replacement for the database itself

**Correct Answer:** C
**Explanation:** Core is the foundation — tables, columns, `select()` expressions, engines, and connections. The ORM (A) is built on top of Core. Core is not a database (D) and async drivers are a separate concern (B).

---

### Question 2 [Easy]
**What does this code output?**

```python
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str] = mapped_column(default="researcher")


# The table is created. Which statement about the schema is TRUE?
```

A) `id` is nullable
B) `name` is nullable
C) `role` gets its default from the database at INSERT time
D) `role` gets its default in Python at flush time

**Correct Answer:** D
**Explanation:** A plain `default=` is a Python-side default: SQLAlchemy fills it at flush time, so no database default exists. `server_default` would be the DB-level variant (C). `Mapped[str]` means NOT NULL (B wrong) and the primary key `id` is implicitly NOT NULL (A wrong).

---

### Question 3 [Easy]
**Which import builds a 2.0-style SELECT statement?**

A) `from sqlalchemy import select`
B) `from sqlalchemy.orm import Query`
C) `from sqlalchemy import raw`
D) `from sqlalchemy import query`

**Correct Answer:** A
**Explanation:** In 2.0, `select()` from `sqlalchemy` is the one statement API. `Query` (B) is the legacy 1.x API. There is no `raw`/`query` import (C, D).

---

### Question 4 [Easy]
**When does this code actually send the INSERT to the database?**

```python
session.add(User(name="ada"))
session.commit()
```

A) Immediately when `add()` is called
B) Never, unless you call `session.flush()` explicitly
C) At `commit()`, which first flushes pending changes
D) Only when the session is closed

**Correct Answer:** C
**Explanation:** `add()` only stages the object in the session's unit of work. `commit()` flushes (emits the INSERT) and then commits the transaction. `flush()` alone (B) emits SQL without committing, but commit always flushes first. Nothing is sent at `add()` time (A).

---

### Question 5 [Easy]
**In a one-to-many relationship, where does the foreign key live?**

A) In the child table
B) In the parent table
C) In a separate association table
D) In the session

**Correct Answer:** A
**Explanation:** The child holds the FK column pointing at the parent's PK; the parent just exposes a collection. An association table (C) is for many-to-many, not one-to-many.

---

### Question 6 [Easy]
**What is a Session in SQLAlchemy?**

A) The transactional workspace (unit of work) that tracks objects and flushes changes
B) A database connection
C) A table definition
D) A query result set

**Correct Answer:** A
**Explanation:** A Session is the unit-of-work: it tracks loaded objects, stages adds, and flushes on commit. It is not itself a connection (B) — it borrows connections from the engine — and it is neither a schema object (C) nor a result set (D).

---

### Question 7 [Medium]
**What does this column declaration produce?**

```python
nickname: Mapped[str | None] = mapped_column()
```

A) A NOT NULL `str` column
B) A `str` column with an empty-string default
C) A column that cannot be queried
D) A nullable `str` column

**Correct Answer:** D
**Explanation:** The `| None` union makes the column nullable in the generated DDL; `Mapped[str]` without the union is NOT NULL (A). It has no default (B) and is perfectly queryable (C).

---

### Question 8 [Medium]
**What is `cascade="all, delete-orphan"` used for?**

A) Any relationship, including many-to-many
B) Making the FK `ON DELETE CASCADE` at the database level
C) One-to-many: children are deleted when the parent is deleted, and children removed from the collection are deleted too
D) Preventing deletes on the relationship entirely

**Correct Answer:** C
**Explanation:** `delete-orphan` is only valid for one-to-many: deleting the parent cascades, and removing a child from the collection orphans it (deletes it). It is forbidden on many-to-many (A). It is ORM-level behavior, not DDL (B) — the database knows nothing unless `ON DELETE` is set separately.

---

### Question 9 [Medium]
**What does this code output?**

```python
users = session.scalars(select(User)).all()
print(type(users[0]).__name__)
```

A) `User`
B) `Row`
C) `Select`
D) `tuple`

**Correct Answer:** A
**Explanation:** `scalars()` unwraps single-column results, so selecting the full entity yields `User` objects. `execute()` + `.all()` would yield `Row`s (B, D) for projections. `Select` (C) is the statement, not the result.

---

### Question 10 [Medium]
**What is the purpose of `back_populates`?**

A) It creates the reverse relationship automatically without naming it
B) It enables lazy loading on both sides
C) It fills the child table's FK column values
D) It wires two explicit relationship sides of ONE relationship so both stay in sync

**Correct Answer:** D
**Explanation:** `back_populates="attr"` names the counterpart attribute on the other class, keeping both directions in sync — append to `author.books` and `book.author` updates immediately. `backref` (A) is the implicit shorthand. `back_populates` has nothing to do with FK values (C) or lazy strategy (B).

---

### Question 11 [Medium]
**In a many-to-many relationship, what does `secondary=` name?**

A) The child table
B) The parent table
C) The association table holding the FK pair
D) A secondary connection pool

**Correct Answer:** C
**Explanation:** `relationship("Tag", secondary=book_tag, ...)` names the association table; SQLAlchemy inserts/removes the pair rows automatically. The child class (A) is the first argument, not `secondary`.

---

### Question 12 [Medium]
**What happens in this join?**

```python
stmt = select(Experiment).join(EvalMetric)
```

A) The ON clause is inferred from the foreign key between the two tables
B) It fails because no ON clause is given
C) It produces a cross join
D) It requires `outerjoin()` to work

**Correct Answer:** A
**Explanation:** `join()` infers the ON condition from the FK relationship. You override with an explicit ON when multiple FK paths exist (B wrong). It is an inner join, not a cross join (C), and outerjoin (D) is a different statement.

---

### Question 13 [Medium]
**What is `remote_side` for, and on which side of a self-referential relationship does it go?**

A) The collection side; names the child's PK
B) The many-to-one side; names the column the FK points TO
C) Either side; it is optional sugar
D) The association table; defines its columns

**Correct Answer:** B
**Explanation:** For self-referential relationships (a class related to itself), `remote_side="PromptTemplate.id"` on the many-to-one side tells SQLAlchemy which column is the target, otherwise direction is ambiguous. It is required for self-references (C wrong) and irrelevant to association tables (D).

---

### Question 14 [Medium]
**What does this code output?**

```python
rows = session.execute(select(Experiment.model, func.count()).group_by(Experiment.model)).all()
```

A) A list of `Experiment` objects
B) A single row with the total count
C) An error because there is no JOIN
D) A list of rows, each `(model, count)` — one per distinct model

**Correct Answer:** D
**Explanation:** `execute()` returns `Row`s for projections: one row per group (per distinct model), with the model and its count. No ORM object exists here (A), and without `group_by` you would get one row (B). A JOIN is not required for `func.count()` (C).

---

### Question 15 [Medium]
**What is the difference between `backref` and `back_populates`?**

A) They are identical; the names are interchangeable
B) `backref` implicitly creates the reverse side; `back_populates` explicitly names both sides
C) `back_populates` works only on many-to-many
D) `backref` requires a join table

**Correct Answer:** B
**Explanation:** `backref="parent"` creates the reverse attribute implicitly in one line; `back_populates` requires declaring both sides explicitly. Explicit wiring is preferred for clarity and works on all relationship kinds (C, D wrong).

---

### Question 16 [Hard]
**What does this code do?**

```python
user = session.get(User, 1)
session.commit()
print(user.role)
```

A) Prints the value cached at load time; no SQL is sent
B) Raises `DetachedInstanceError`
C) Raises `AttributeError`
D) Triggers a new SELECT to refresh `role`, because commit expires attributes by default

**Correct Answer:** D
**Explanation:** With the default `expire_on_commit=True`, commit marks loaded attributes expired, so the next access refreshes from the DB — an extra round trip. Not detached (B) because the session is still open. The cache-only behavior (A) requires `expire_on_commit=False`.

---

### Question 17 [Hard]
**What happens on the second commit here?**

```python
session.add(User(id=1, name="a"))
session.commit()
session.add(User(id=1, name="b"))
session.commit()
```

A) Two rows with the same PK are inserted
B) `IntegrityError` is raised at the second commit's flush
C) A `ValueError` is raised at `add()`
D) The second row silently overwrites the first

**Correct Answer:** B
**Explanation:** Adding a second object with the same PK makes the flush emit a conflicting INSERT, raising `IntegrityError` at commit time. Nothing silently overwrites (D), duplicates are impossible (A), and `add()` itself does not check PKs (C).

---

### Question 18 [Hard]
**Which session lifecycle stage correctly describes a DETACHED instance?**

A) In the session, pending, not yet flushed
B) In the session, persistent, with a database row
C) Was associated with a session that has been closed — attributes remain readable but new DB access requires re-attaching
D) Never had a session; created and immediately usable

**Correct Answer:** C
**Explanation:** Detached = persistent before, session closed. Loaded attribute values remain readable, but lazy loads and refreshes fail. Pending (A) and persistent (B) are pre-close states; a fresh object is transient (D).

---

### Question 19 [Hard]
**What does this statement's execution order look like?**

```python
stmt = (
    select(Experiment.model, func.count(EvalMetric.id))
    .join(EvalMetric, EvalMetric.experiment_id == Experiment.id)
    .where(Experiment.status == "done")
    .group_by(Experiment.model)
)
```

A) The count includes rows that do not match `status == "done"`
B) JOIN → WHERE → GROUP BY → project (count computed per group after filtering)
C) WHERE → JOIN → GROUP BY
D) GROUP BY → JOIN → WHERE

**Correct Answer:** B
**Explanation:** SQL order is FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT/projection. Filtering happens BEFORE grouping, so only "done" experiments are counted per model (A wrong). The other orderings (C, D) misstate SQL semantics.

---

### Question 20 [Hard]
**Why does keyset (cursor) pagination beat `OFFSET` pagination at scale?**

A) `OFFSET` makes the database read and discard all skipped rows each page; keyset jumps directly past the last-seen cursor via the index
B) Keyset pagination is simpler to implement
C) Keyset works without indexes
D) `OFFSET` cannot be combined with `ORDER BY`

**Correct Answer:** A
**Explanation:** `OFFSET m` forces the DB to scan and discard m rows per page — O(m + n) per page. Keyset (`WHERE id > :last ORDER BY id LIMIT n`) uses the index to start at the cursor: O(page_size), and pages stay stable as new rows arrive. Keyset requires a unique sort column (C wrong) and is not simpler (B). `OFFSET` works with `ORDER BY` (D wrong) — it just degrades.

---

## Answer Key

| Question | Answer |
|----------|--------|
| 1 | C |
| 2 | D |
| 3 | A |
| 4 | C |
| 5 | A |
| 6 | A |
| 7 | D |
| 8 | C |
| 9 | A |
| 10 | D |
| 11 | C |
| 12 | A |
| 13 | B |
| 14 | D |
| 15 | B |
| 16 | D |
| 17 | B |
| 18 | C |
| 19 | B |
| 20 | A |

---

## Score Tracking

| Score Range | Level |
|-------------|-------|
| 18-20 | Expert - You've mastered SQLAlchemy basics! |
| 14-17 | Proficient - Solid understanding, review eager loading and async |
| 10-13 | Developing - Good foundation, re-read the session lifecycle |
| 6-9 | Beginner - Review declarative models and relationships |
| 0-5 | Novice - Start with the Core vs ORM lecture |

---

*Quiz created for AI Engineer Lab - Python Foundations*
