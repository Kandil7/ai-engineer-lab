# PostgreSQL Schema Design

Relational database schema for the AI Engineer Lab and ThanaweyaGPT platform.
Covers users, courses, chat sessions, messages, and embedding metadata.

---

## Schema Overview

### Core Tables

| Table        | Purpose                              | Key Relationships     |
| ------------ | ------------------------------------ | --------------------- |
| `users`      | User accounts and profiles           | → sessions, courses   |
| `courses`    | Educational course definitions       | → modules, enrollments|
| `modules`    | Course modules/units                 | → lessons             |
| `lessons`    | Individual learning content          | → messages            |
| `sessions`   | Chat sessions between user and AI    | → messages            |
| `messages`   | Individual chat messages             | → sessions            |
| `enrollments`| User-course enrollment records       | → users, courses      |
| `embeddings` | Embedding metadata for RAG           | → lessons, messages   |

### Schema Design Principles

1. **UUIDs for primary keys** — prevents enumeration, supports distributed systems
2. **Timestamps on every table** — `created_at`, `updated_at` with triggers
3. **Soft deletes** — `deleted_at` column, never hard-delete user data
4. **JSONB for flexible metadata** — course settings, user preferences, message metadata
5. **Referential integrity** — foreign keys with appropriate ON DELETE behavior

---

## Migration Strategy

Migrations live in `projects/03-databases/postgres-design/migrations/` and follow a
sequential naming convention:

```
001_create_users.sql
002_create_courses.sql
003_create_sessions.sql
...
```

### Rules

- Each migration is **idempotent** where possible (CREATE IF NOT EXISTS)
- Every migration has a **down** counterpart in a `rollback/` subdirectory
- Migrations are run in order; never reorder after they've been applied
- Test migrations against a fresh database before applying to shared environments

### Applying Migrations

```bash
# Direct psql
psql -h localhost -p 5432 -U fslab -d fslab -f migrations/001_create_users.sql

# Via Docker
docker exec -i fslab-postgres psql -U fslab -d fslab < migrations/001_create_users.sql
```

---

## Indexing Approach

### Primary Indexes

- **B-tree** on all foreign keys (default, auto-created)
- **B-tree** on `created_at` for time-range queries
- **GIN** on JSONB columns for metadata searches
- **Unique** on `users.email`

### Composite Indexes

```sql
-- Chat history: messages by session, ordered by time
CREATE INDEX idx_messages_session_time ON messages (session_id, created_at);

-- Course lookup: modules by course, ordered by position
CREATE INDEX idx_modules_course_position ON modules (course_id, position);

-- Active enrollments: user + status filter
CREATE INDEX idx_enrollments_user_status ON enrollments (user_id, status);
```

### Full-Text Search

```sql
-- Turkish/Arabic content search
CREATE INDEX idx_lessons_search ON lessons USING GIN (
  to_tsvector('simple', coalesce(title, '') || ' ' || coalesce(content, ''))
);
```

---

## Connection Pooling

Use **pgxpool** (Go) or **asyncpg** (Python) for connection pooling:

| Setting             | Value    | Rationale                      |
| ------------------- | -------- | ------------------------------ |
| Min connections     | 2        | Always ready for requests      |
| Max connections     | 10       | Sufficient for local dev       |
| Max idle time       | 5 min    | Release unused connections     |
| Connection timeout  | 10 sec   | Fail fast if DB unreachable    |
| Statement timeout   | 30 sec   | Prevent runaway queries        |

---

## Getting Started

```bash
# Start PostgreSQL
docker compose -f infra/docker/docker-compose.yml up -d postgres

# Apply all migrations
for f in projects/03-databases/postgres-design/migrations/*.sql; do
  psql -h localhost -p 5432 -U fslab -d fslab -f "$f"
done

# Verify schema
psql -h localhost -p 5432 -U fslab -d fslab -c "\dt"
```
