# SQL 01: Relational Model — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Relation (table) | Named set of rows sharing a schema | messages table |
| Row (tuple) | One fact: a value per column | one message |
| Primary key | Unique, non-null row identifier | id column |
| Foreign key | Column referencing another table's key | conversation_id |
| NULL | Absence of value — not zero, not empty string | missing summary |
| Set thinking | SQL operates on sets; order is never assumed | no ORDER BY, no order |
| Schema | The structure contract: tables, columns, constraints | migrations encode it |

---

## Alphabetical Glossary

### Foreign key

**Definition:** A column whose values reference a primary key elsewhere,
declaring the relationship the database enforces.

**Example:**
```sql
conversation_id INTEGER REFERENCES conversations(id)
```

**Related concepts:** Primary key, Relation

---

### NULL

**Definition:** The absence of a value. Propagates through comparisons
(`NULL = NULL` is not true) — the source of three-valued-logic bugs.

**Example:**
```sql
WHERE summary IS NULL  -- never = NULL
```

**Related concepts:** Three-valued logic, IS NULL

---

### Primary key

**Definition:** The column (or columns) uniquely identifying each row, never
null. The anchor for foreign keys, joins, and ORM identity maps.

**Example:**
```sql
id INTEGER PRIMARY KEY
```

**Related concepts:** Foreign key, UUID

---

### Relation (table)

**Definition:** A named set of rows with a fixed schema. Sets have no order —
any assumed ordering without ORDER BY is a latent bug.

**Example:**
```sql
CREATE TABLE messages (...);  -- the set; rows are its members
```

**Related concepts:** Row, Schema

---

### Row (tuple)

**Definition:** A single member of a relation: one value per column. The
unit of INSERT, UPDATE, DELETE, and ORM identity.

**Example:**
```python
# one eval score = one row in eval_scores
```

**Related concepts:** Relation, Primary key

---

### Schema

**Definition:** The structural contract of a database: tables, columns,
types, keys, constraints. Versioned through migrations, never by hand.

**Example:**
```python
# Alembic revisions are the schema's git history
```

**Related concepts:** DDL, Migrations

---

### Set thinking

**Definition:** Reasoning in whole sets instead of row-by-row loops. SQL's
power and its learning curve: describe the set you want, not the iteration.

**Example:**
```sql
UPDATE messages SET read = TRUE WHERE conversation_id = 7;  -- one set, no loop
```

**Related concepts:** Relation, Aggregation

---

## Related Concepts

- **Three-valued logic**: TRUE/FALSE/UNKNOWN filtering semantics (topic 05)
- **Normalization**: organizing facts to avoid duplication
- **Migrations**: schema as versioned code (DevMate week 4)

## Key Takeaways

1. Tables are sets; rows are facts; keys are the wiring.
2. NULL is absence — compare with IS, never =.
3. No ORDER BY means no order, ever.
