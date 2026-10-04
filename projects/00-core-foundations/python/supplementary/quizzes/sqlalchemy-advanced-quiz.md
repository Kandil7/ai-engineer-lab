# SQLAlchemy Advanced Quiz

## Topic Overview
This quiz covers the advanced SQLAlchemy toolkit: the N+1 problem and eager loading strategies (selectinload, joinedload, lazy="raise"), async SQLAlchemy (AsyncSession, aiosqlite, run_sync), advanced patterns (hybrid properties, TypeDecorator, events, window functions), database testing (transactional tests, savepoints), and the repository pattern.

**Difficulty:** Intermediate to Advanced
**Questions:** 20
**Time:** ~25 minutes
**Passing Score:** 70% (14/20)

---

## Questions

### Question 1 [Easy]
**10 projects each have 5 experiments. With default lazy loading, how many queries run if you print `len(project.experiments)` for every project?**

A) 1
B) 6
C) 11
D) 50

**Correct Answer:** C
**Explanation:** The classic N+1: 1 query loads the projects, then each of the 10 projects triggers 1 child query → 11 total. 50 (D) would be every experiment fetched individually; 6 (B) and 1 (A) misstate the lazy behavior.

---

### Question 2 [Easy]
**Same listing as Q1, but with `selectinload(Project.experiments)`. How many queries now?**

A) 3
B) 2
C) 1
D) 11

**Correct Answer:** B
**Explanation:** selectinload adds exactly ONE extra `WHERE project_id IN (...)` query: 1 for parents + 1 for all children = 2, regardless of N. 1 (C) is the joinedload claim; 11 (D) is the unfixed N+1.

---

### Question 3 [Easy]
**What does this code print?**

```python
class StrictProject(Base):
    experiments: Mapped[list["Experiment"]] = relationship(lazy="raise")


p = session.get(StrictProject, 1)
try:
    _ = p.experiments
except InvalidRequestError:
    print("lazy blocked")
```

A) `[]` — the empty collection is returned
B) `InvalidRequestError` is printed
C) The list of experiments is printed
D) `lazy blocked`

**Correct Answer:** D
**Explanation:** `lazy="raise"` makes any unloaded relationship access raise `InvalidRequestError`; the except clause catches it and prints `lazy blocked`. The exception itself is not printed (B) and the access never returns data (A, C).

---

### Question 4 [Easy]
**Which engine event lets you count executed statements for N+1 detection?**

A) `before_cursor_execute`
B) `after_commit`
C) `engine_created`
D) `session_begin`

**Correct Answer:** A
**Explanation:** `before_cursor_execute` fires before every cursor execution — wrap it in a counter to measure round trips. The others fire at commit (B), engine construction (C), or session start (D) and do not see every statement.

---

### Question 5 [Easy]
**In async SQLAlchemy, what must precede every database call?**

A) `async with`
B) `await`
C) `yield`
D) `run_sync`

**Correct Answer:** B
**Explanation:** Every DB operation on an AsyncSession/AsyncEngine is a coroutine and must be `await`ed. `async with` (A) is for context-manager lifecycle, `run_sync` (D) is the bridge for sync code, and `yield` (C) is unrelated.

---

### Question 6 [Easy]
**What does the repository pattern abstract away?**

A) Persistence/DB access behind an interface
B) HTTP routing
C) Business rules
D) UI rendering

**Correct Answer:** A
**Explanation:** A repository is the seam between application logic and persistence: services depend on the interface, never the engine/session. Business rules (C) belong to services, routing (B) to the web layer, rendering (D) to views.

---

### Question 7 [Medium]
**Without `.unique()`, how many times does a project with 3 experiments appear in this result?**

```python
projects = session.scalars(select(Project).options(joinedload(Project.experiments))).all()
```

A) 1
B) 0
C) 3 — once per experiment row
D) The query raises an error

**Correct Answer:** C
**Explanation:** A collection JOIN fans out: one parent row per child, so the project repeats once per experiment (row duplication). `.unique()` collapses back to one row per parent. 2.0 `scalars()` does not apply it automatically.

---

### Question 8 [Medium]
**What does `join_transaction_mode="create_savepoint"` achieve in tests?**

A) Creates a separate database connection per test
B) Nests the session's writes in a savepoint inside the outer transaction, so one outer rollback discards everything
C) Disables transactions for the test
D) Commits each statement immediately

**Correct Answer:** B
**Explanation:** The session begins a SAVEPOINT inside the test's outer transaction; code under test commits to the savepoint, and the outer `rollback()` still discards all of it. It does not open new connections (A), disable transactions (C), or auto-commit (D).

---

### Question 9 [Medium]
**Why is `StaticPool` used here?**

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine("sqlite+aiosqlite://", poolclass=StaticPool)
```

A) It creates a new connection per query
B) It enables thread pooling
C) It connects to a file-backed database
D) It pins one connection so every session shares the same in-memory DB

**Correct Answer:** D
**Explanation:** With in-memory SQLite, each connection would get its own empty DB; StaticPool pins a single connection so all sessions see the same database. It is the opposite of per-query connections (A) and irrelevant to threads (B) or files (C).

---

### Question 10 [Medium]
**What is TRUE about this code?**

```python
async with AsyncSessionLocal() as session:
    session.add(Prediction(model="bert", latency_ms=7))
    await session.commit()
```

A) `commit()` must be awaited, and the context manager closes the session (rolling back on exception)
B) `commit()` is synchronous
C) `add()` must be awaited
D) This raises because the session is not bound to an engine

**Correct Answer:** A
**Explanation:** On AsyncSession every DB operation is a coroutine — `add()` is sync staging, `commit()` is awaited. `async with` guarantees close and rollback on exception. The engine binding happens inside the factory (D wrong); `add()` is not a coroutine (C wrong).

---

### Question 11 [Medium]
**What does a TypeDecorator's `bind_processor` do?**

A) Converts DB values to Python on read
B) Defines the SQL type name
C) Converts Python values to DB format on write
D) Validates column values

**Correct Answer:** C
**Explanation:** `bind_processor` runs on the way IN (Python → DB, e.g., float32 array → bytes); `result_processor` (A) runs on the way OUT. The type name comes from `impl` (B); validation is `@validates`'s job (D).

---

### Question 12 [Medium]
**Where does the expression side of a hybrid_property matter?**

A) Only in Python attribute code
B) Only at flush time
C) Only for column defaults
D) In SQL expressions — `where()`, `order_by()`, `group_by()` compile it to SQL

**Correct Answer:** D
**Explanation:** The `@is_leader.expression` side gives the property a SQL form usable in statements; the plain property body is the Python form for instances. Without the expression side, filtering would fail — the flush (B) and defaults (C) are unrelated.

---

### Question 13 [Medium]
**What does this WHERE clause compile to?**

```python
@hybrid_property
def is_leader(self) -> bool:
    return self.score >= 0.90


@is_leader.expression
def is_leader(cls):
    return cls.score >= 0.90


stmt = select(Experiment).where(Experiment.is_leader)
```

A) `WHERE 1 = 1`
B) `WHERE is_leader`
C) `WHERE score >= 0.90`
D) It raises `TypeError` — hybrids cannot be filtered

**Correct Answer:** C
**Explanation:** The expression-side function body `cls.score >= 0.90` becomes the SQL predicate. There is no `is_leader` column (B wrong), and the hybrid is explicitly filterable when the expression side is defined (A, D wrong).

---

### Question 14 [Medium]
**In a transactional test, what does `outer.rollback()` do?**

A) Discards all test writes — including the code under test's — in one action
B) Commits the test data
C) Drops all tables
D) Disposes the engine

**Correct Answer:** A
**Explanation:** With the session joined via savepoint mode, one rollback of the test's outer transaction undoes everything, so tests stay isolated. It is the opposite of committing (B), does not drop schema (C), and does not dispose the engine (D).

---

### Question 15 [Medium]
**What does `@runtime_checkable` add to a Protocol?**

A) Static type checking only
B) Runtime `isinstance()` support for structurally-matching objects
C) Automatic SQL generation
D) Faster query execution

**Correct Answer:** B
**Explanation:** By default Protocols are static-only: the type checker understands them but `isinstance()` fails. `@runtime_checkable` makes structural matching usable at runtime — e.g., asserting a repository object satisfies the Protocol. SQL (C) and speed (D) are unrelated.

---

### Question 16 [Hard]
**What happens at the `print` here?**

```python
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async with AsyncSessionLocal() as session:
    row = await session.get(Prediction, 1)
    await session.commit()
    print(row.latency_ms)  # loaded before commit
```

A) A new SELECT is triggered to refresh the attribute
B) It raises `MissingGreenlet`
C) It raises `DetachedInstanceError`
D) It prints the cached value with no SQL

**Correct Answer:** D
**Explanation:** `expire_on_commit=False` keeps attribute values after commit, so the print uses the loaded cache — no extra round trip. With the default `True`, (A) would happen (an awaited context is needed, which is exactly what (B) hints at without the option). The session is still open, so not detached (C).

---

### Question 17 [Hard]
**What rank does the 0.84 experiment get?**

```python
rank = func.row_number().over(partition_by=Experiment.model, order_by=Experiment.score.desc())

# For model "bert": scores 0.91, 0.84, 0.97
```

A) 3
B) 1
C) 0
D) NULL

**Correct Answer:** A
**Explanation:** `row_number()` numbers rows within the "bert" partition by score descending: 0.97 → 1, 0.91 → 2, 0.84 → 3. Ranking starts at 1, not 0 (C), and NULL (D) applies to aggregate-style windows, not row_number.

---

### Question 18 [Hard]
**Why do repository WRITE methods `flush()` but never `commit()`?**

A) `flush()` is faster than `commit()`
B) `commit()` is deprecated in SQLAlchemy 2.0
C) Commits belong at the transaction boundary (the service); the repository joins the caller's unit of work
D) `flush()` invalidates the session, so commit is unsafe

**Correct Answer:** C
**Explanation:** The repo participates in whatever transaction is active; committing inside it would end the caller's unit of work early and break all-or-nothing batches. Performance (A) is not the reason, commit is not deprecated (B), and flush does not invalidate the session (D).

---

### Question 19 [Hard]
**What is this pattern for?**

```python
def _count_sync(session):
    return len(list(session.scalars(select(Prediction.id)).all()))


count = await session.run_sync(_count_sync)
```

A) Replacing `await` with synchronous code everywhere
B) Running inherently-synchronous ORM code inside the AsyncSession via the greenlet bridge
C) Connecting to a second database
D) Committing from synchronous code

**Correct Answer:** B
**Explanation:** `run_sync` executes a plain sync function in a greenlet that presents the AsyncSession, so legacy/sync ORM helpers work without blocking the event loop. It is a bridge, not a replacement for async (A), has nothing to do with extra databases (C), and does not change commit ownership (D).

---

### Question 20 [Hard]
**Two workers both load the experiment (version=2), both modify the score, both commit. What happens to the second commit?**

```python
@event.listens_for(Experiment, "before_update")
def _bump(mapper, connection, target):
    target.version += 1


# UPDATE ... SET score=..., version=3 WHERE id=1 AND version=2
```

A) It silently overwrites the first worker's change
B) Version becomes 4
C) The UPDATE matches 0 rows — the conflict is detected (e.g., rowcount == 0 → raise)
D) It raises `IntegrityError`

**Correct Answer:** C
**Explanation:** The optimistic-lock UPDATE filters on the version each worker loaded. The first commit flips version to 3; the second UPDATE with `WHERE version=2` matches nothing, so `rowcount == 0` reveals the stale write. Nothing overwrites silently (A), the version never becomes 4 (B), and this is not a uniqueness violation (D).

---

## Answer Key

| Question | Answer |
|----------|--------|
| 1 | C |
| 2 | B |
| 3 | D |
| 4 | A |
| 5 | B |
| 6 | A |
| 7 | C |
| 8 | B |
| 9 | D |
| 10 | A |
| 11 | C |
| 12 | D |
| 13 | C |
| 14 | A |
| 15 | B |
| 16 | D |
| 17 | A |
| 18 | C |
| 19 | B |
| 20 | C |

---

## Score Tracking

| Score Range | Level |
|-------------|-------|
| 18-20 | Expert - You've mastered advanced SQLAlchemy! |
| 14-17 | Proficient - Solid understanding, review the async and testing chapters |
| 10-13 | Developing - Good foundation, re-read eager loading and N+1 |
| 6-9 | Beginner - Review the repository pattern and transaction boundaries |
| 0-5 | Novice - Start with the eager loading lecture |

---

*Quiz created for AI Engineer Lab - Python Foundations*
