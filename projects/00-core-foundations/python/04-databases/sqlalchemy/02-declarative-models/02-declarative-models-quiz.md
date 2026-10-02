# SQLAlchemy 02: Declarative Models — Quiz

> **Topic Overview**: `DeclarativeBase`, mapped columns, and schema edges.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is `DeclarativeBase`?**
- A) A connection
- B) The 2.0 base class models inherit to declare tables
- C) A migration
- D) A session

<details><summary>Reveal Answer</summary>**B.** Model base.</details>

### Question 2 — Easy
**How do you declare a typed column?**
- A) `Column`
- B) `Mapped[int] = mapped_column(...)`
- C) An attribute
- D) A dict

<details><summary>Reveal Answer</summary>**B.** Typed mapping.</details>

### Question 3 — Medium
**Nullable vs Optional: the rule?**
- A) Same
- B) `nullable=False` with a non-`Optional` type; `Optional` requires `nullable=True`
- C) Always nullable
- D) Never nullable

<details><summary>Reveal Answer</summary>**B.** Types and schema agree.</details>

### Question 4 — Medium
**Python-side vs DB-side defaults?**
- A) Same
- B) Python defaults run in the ORM; DB defaults (`server_default`) run in the database for all writers
- C) DB defaults are slower
- D) Python defaults persist

<details><summary>Reveal Answer</summary>**B.** Two default layers.</details>

### Question 5 — Medium
**What is `__table_args__` for?**
- A) Columns
- B) Table-level constraints (unique composites, checks, indexes)
- C) Sessions
- D) Migrations

<details><summary>Reveal Answer</summary>**B.** Table-level rules.</details>

### Question 6 — Hard
**Why are foreign keys the schema's edges?**
- A) They are not
- B) They declare the graph relationships the database enforces
- C) Speed
- D) Style

<details><summary>Reveal Answer</summary>**B.** Enforced relations.</details>

### Question 7 — Hard
**What does "the database enforces, Python only asks" mean?**
- A) Skip validation
- B) Constraints live in DDL; Python validation is convenience, not guarantee
- C) No constraints
- D) Python enforces

<details><summary>Reveal Answer</summary>**B.** DDL is the guarantee.</details>

### Question 8 — Hard
**Why must the model match the migration?**
- A) Style
- B) Drift between models and schema produces runtime errors and silent misbehavior
- C) Speed
- D) Locking

<details><summary>Reveal Answer</summary>**B.** Single source of truth.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You model declaratively. |
| 5-6 | Review nullability and defaults. |
| < 5 | Re-read the lecture. |
