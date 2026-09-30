# 🗄️ Phase 4: Database Integration

76+ files across 7 database technologies, each organized into self-contained topic directories.

## 📋 Directory Structure

Each topic directory contains:
- `NN-topic-name.py` — Exercise (runnable code)
- `NN-topic-name-lecture.md` — Lecture (detailed explanation)
- `NN-topic-name-glossary.md` — Glossary (key terms)

```
04-databases/
├── sql-fundamentals/            # 14 topics: Core SQL concepts
│   ├── 01-relational-model/
│   │   ├── 01-relational-model.py
│   │   └── 01-relational-model-lecture.md
│   └── ... (14 topics)
│
├── sql-sqlite/                  # 12 topics: SQLite exercises
├── postgresql/                  # 7 topics: PostgreSQL exercises + backup/restore
│   ├── 07-backup-and-restore/   # verify-by-restore, PITR, 3-2-1
│   └── challenges/07-backup-and-restore/   # Bronze/Silver/Gold practice set
├── mongodb/                     # 12 topics: MongoDB exercises
├── redis/                       # 8 topics: Caching, pub/sub, sessions
├── sqlalchemy/                  # 11 topics: ORM patterns + migrations
│   ├── 11-migrations-alembic/   # revision chains, expand-backfill-contract
│   └── challenges/11-migrations-alembic/   # Bronze/Silver/Gold practice set
└── vector-stores/               # 8 topics: Embeddings, similarity search
```

## 📚 Technologies

| Technology | Topics | Focus |
|------------|--------|-------|
| **SQL Fundamentals** | 14 | Portable SQL (DDL, DML, joins, subqueries) |
| **SQLite** | 12 | Portable exercises (built-in sqlite3) |
| **PostgreSQL** | 7 | Advanced features (JSONB, indexes, pooling) + backup/restore |
| **MongoDB** | 12 | Document database (dict stand-in) |
| **Redis** | 8 | Caching, pub/sub, distributed locks |
| **SQLAlchemy** | 11 | ORM patterns (Core + ORM) + migrations/Alembic |
| **Vector Stores** | 8 | Embeddings, similarity search |

New in this phase's Athar track: **`postgresql/07-backup-and-restore`**
(verify-by-restore, RPO/RTO, PITR, the derived-index rule) and
**`sqlalchemy/11-migrations-alembic`** (revision chains, expand-backfill-contract,
lineage-preserving rebuilds). Both ship with challenge sets.

## 🚀 Quick Start

```bash
# SQL Fundamentals (no setup needed)
python sql-fundamentals/01-relational-model/01-relational-model.py

# SQLite (no setup needed)
python sql-sqlite/01-getting-started/01-getting-started.py

# PostgreSQL (requires Docker)
docker-compose up -d postgres
python postgresql/01-setup-and-psycopg/01-setup-and-psycopg.py

# MongoDB (uses dict stand-in)
python mongodb/01-getting-started/01-getting-started.py

# Redis (requires Docker)
docker-compose up -d redis
python redis/01-introduction/01-introduction.py

# SQLAlchemy (any database)
python sqlalchemy/01-core-vs-orm/01-core-vs-orm.py

# Vector Stores (embeddings)
python vector-stores/01-vector-search-fundamentals/01-vector-search-fundamentals.py

# Challenge sets (starter fails until solved; solution validates with env var)
python -m pytest sqlalchemy/challenges/11-migrations-alembic/test_challenge.py -q
python -m pytest postgresql/challenges/07-backup-and-restore/test_challenge.py -q
```

## 📝 Notes

- **sql-fundamentals/** teaches portable SQL (works anywhere)
- **sql-sqlite/** uses SQLite as a portable stand-in (no installation)
- **postgresql/** requires real PostgreSQL (Docker recommended)
- **mongodb/** uses Python dicts as stand-ins (no MongoDB needed)
- **redis/** requires Redis server (Docker recommended)
- **sqlalchemy/** covers ORM patterns for any database, plus migrations
- **vector-stores/** covers modern vector database patterns
- **backup/restore** and **migrations** carry the Athar mastery criteria:
  source-of-truth vs derived index, lineage keys, and restore drills

---

*Last updated: September 2026*
