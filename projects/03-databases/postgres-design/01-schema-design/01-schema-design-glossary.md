# PostgreSQL 01: Schema Design — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Schema | The contract between app and data | tables, types, constraints |
| Primary key | Identifies a row | id UUID PRIMARY KEY |
| Foreign key | Links rows across tables | user_id REFERENCES users |
| Constraint | The database's own rule | NOT NULL, UNIQUE, CHECK |
| Referential integrity | No orphan references | FK enforced |
| Normalization | Each fact stored once | user name in users |
| Soft delete | deleted_at instead of deletion | history preserved |

---

## Alphabetical Glossary

### Constraint

**Definition:** The database's own rule: NOT NULL, UNIQUE, CHECK, and the
keys. Enforced in the database, not just the application.

**Example:**
```sql
email TEXT UNIQUE NOT NULL
```

**Related concepts:** Referential integrity

---

### Foreign key

**Definition:** A column that references a row in another table. Enforces
referential integrity — no orphan references.

**Example:**
```sql
user_id UUID REFERENCES users(id)
```

**Related concepts:** Referential integrity, Primary key

---

### Normalization

**Definition:** Removing redundancy so each fact is stored once. Normalize
the facts; denormalize only what is measured.

**Example:**
```sql
-- user name lives in users, not repeated in messages
```

**Related concepts:** Schema

---

### Primary key

**Definition:** The column that identifies a row uniquely. The anchor of
every reference.

**Example:**
```sql
id UUID PRIMARY KEY
```

**Related concepts:** Foreign key

---

### Referential integrity

**Definition:** The guarantee that a row cannot reference a row that does
not exist. Enforced by foreign keys.

**Example:**
```sql
-- a message's user_id must exist in users
```

**Related concepts:** Foreign key

---

### Schema

**Definition:** The contract between the application and the data: tables,
types, constraints, and relationships.

**Example:**
```sql
CREATE TABLE users (...);
```

**Related concepts:** Normalization

---

### Soft delete

**Definition:** A deleted_at column instead of deleting rows. History is
preserved and recoverable.

**Example:**
```sql
deleted_at TIMESTAMPTZ
```

**Related concepts:** Schema

---

## Related Concepts

- **Indexes**: the schema's access paths (topic 02)
- **Migrations**: the schema evolves through migrations (topic 03)
- **Connection pooling**: the schema is served through a pool (topic 04)

## Key Takeaways

1. The schema is the contract between app and data.
2. Foreign keys enforce referential integrity.
3. Constraints live in the database, not just the app.
4. Normalize facts; denormalize only what is measured.
5. Timestamps and soft deletes preserve history.