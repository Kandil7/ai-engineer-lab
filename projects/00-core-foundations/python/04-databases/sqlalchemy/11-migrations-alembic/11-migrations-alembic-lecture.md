# Databases Lecture 11: Migrations and Schema Evolution (Alembic)

## Topic Overview

Every schema eventually changes: an edition column arrives, a source table splits, an index rebuilds. The question is never *whether* the schema changes but *how the change travels to production* — hand-edited SQL with no history, a recreate that deletes the corpus, or a migration file that is reviewed, ordered, reversible, and testable. For a reference system the stakes are concrete: the vector index joins back to the source through a lineage key, and a careless schema change severs that join silently. This lecture covers Alembic's model (revision chains, upgrade/downgrade), the expand-contract pattern for zero-downtime changes, data migrations, and the discipline that keeps source linkage intact while books, editions, and indexes evolve.

The theme: **schema change is code — reviewed, reversible, and lineage-preserving.**

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why versioned migrations beat hand-edits and recreate scripts.
2. Read and write Alembic revisions with correct upgrade/downgrade pairs.
3. Apply the expand-backfill-contract sequence for NOT NULL and renames.
4. Write idempotent data migrations and know when they belong in code vs SQL.
5. Test migrations in CI (upgrade, downgrade, re-upgrade, constraint proof).
6. Preserve index-to-source lineage across schema changes (the mastery criterion).
7. Handle the operational reality: `alembic check`, migration review, and never editing applied migrations.

---

## Prerequisites

| Need | Where |
|---|---|
| SQL DDL/DML | `04-databases/sql-fundamentals/02-ddl-schema` |
| Indexes | `04-databases/sql-fundamentals/10-indexes-and-plans` |
| SQLAlchemy models | `04-databases/sqlalchemy/02-declarative-models` |
| Transactions | `04-databases/sql-fundamentals/11-transactions` |

---

## 1. The three ways a schema changes (only one survives audit)

**Hand-edit in production** works until two environments disagree, until nobody remembers which column was added when, until the rollback is a shrug. **Drop and recreate** preserves neither data nor lineage — and for a RAG catalog, the lineage *is* the product's correctness. **Versioned migrations** are Python/SQL scripts with an ordered revision id, an `upgrade()` that applies, and a `downgrade()` that reverses. Alembic records the applied revision in a one-row `alembic_version` table, so every environment knows exactly where it stands.

The migration chain is a *durable artifact*: it is reviewed in the same PR as the model change, it is the recovery path after a bad deploy, and it is the diff that explains why production looks the way it does six months later.

## 2. The revision chain

Alembic's mechanics are exactly what the exercise builds in ~40 lines:

```python
def upgrade():
    op.add_column("sources", sa.Column("edition", sa.Text()))


def downgrade():
    op.drop_column("sources", "edition")
```

- **One migration per PR**, named after the change ("add edition column"), never "fix".
- **Linear chain** unless you have a real branching need (`alembic merge` for the rare case).
- **`upgrade()` and `downgrade()` are a pair.** A `downgrade()` that is `pass` is a lie that surfaces during the incident you need it.
- **Never edit an applied migration.** The bytes of an applied file are part of the deployed system's history; a correction is a *new* migration.

`alembic revision --autogenerate` compares your SQLAlchemy models to the live database and drafts the script. It is a draft: read every generated file, fix operation order, and notice what it cannot detect (data shape, backfills).

## 3. Expand → backfill → contract

Adding a NOT NULL column to a populated table is the classic production outage: the `ALTER` fails or locks the table while old code still inserts rows without the column. The safe sequence is three migrations:

1. **Expand** — add the column as NULLable. Old code keeps writing; new code starts writing values. The system runs in mixed mode safely.
2. **Backfill** — a data migration filling existing rows (`UPDATE sources SET edition = 'default' WHERE edition IS NULL`). Make it **idempotent** (a `WHERE NULL` guard) so re-running is safe.
3. **Contract** — once every row is populated and old code is gone, enforce the constraint (`NOT NULL`, unique index, rename).

The same pattern covers renames (add new column → dual-write → switch reads → drop old) and table splits. The rule of thumb: **at every intermediate step, both the old and the new code version must work.** If a step breaks old code, it is not an expand step.

## 4. Data migrations

Schema migrations change shape; data migrations change content. They belong in migration files when the *data* must change to keep the system consistent (backfills, repartitioning, folding legacy spellings), and in application code when the change is ongoing business logic (normalization at ingest).

Rules for data migrations:

- **Idempotent**: re-running must be a no-op. Guard with a `WHERE` clause or a version marker.
- **Chunked**: a single `UPDATE` over ten million rows locks and bloats; batch by primary key ranges.
- **Logged**: print/log progress per chunk so a stalled migration is observable.
- **Reversible in spirit**: `downgrade()` for a data migration is often the inverse UPDATE — but if the pre-image is lost, say so in the docstring rather than pretending.

## 5. Testing migrations

A migration that has never been tested downward is unproven. The four-move check (which the exercise's `_verify()` implements):

1. **Upgrade to head** on a scratch database → reaches the expected revision.
2. **Insert representative data** (including the tricky rows).
3. **Downgrade one step, re-upgrade** → the schema round-trips and data survives where promised.
4. **Prove the constraints** — a duplicate insert raises `IntegrityError`, a NOT NULL violation raises, etc.

In CI this runs against a temp sqlite (fast, semantic DDL subset) and/or a disposable Postgres container (full fidelity). The cheap part matters: run it on every PR so a broken `downgrade()` is caught while the author still remembers what they meant.

## 6. The lineage criterion: rebuild the index without losing the source

The skills-map criterion: *modify a book edition and rebuild the index without losing the linkage.* The contract that makes it possible:

- **`source_ref` is immutable identity** (`bukhari/p5`). Content edits are `UPDATE`s; the identity never changes and is never recycled.
- **Index entries store `source_ref`, not content.** The vector index is a *derived* store; its entries join back through the lineage key. A rebuild re-reads sources and re-embeds — it never rewrites the keys.
- **Migrations must never drop or rewrite the lineage column.** A migration that touches `source_ref` must prove in its test that every pre-migration ref resolves post-migration.

The exercise proves the mechanical version: update text in place, re-read every row through `source_ref`, and assert the row count is unchanged and the target ref resolves. If a future migration can break that assertion, the test says so before production does.

## 7. Alembic in the workflow

```bash
alembic revision --autogenerate -m "add edition column"
alembic upgrade head
alembic downgrade -1
alembic history
alembic check       # model/DB drift detection (Alembic 1.13+)
```

Operational habits:

- **Migration files review as carefully as code** — they run against the data that is the business.
- **Pair model change + migration in one PR** so `alembic check` stays clean.
- **Deploy order**: migration first (expand direction), then code that needs it; contract migrations only after old code is fully drained.
- **Rollback plan**: know which revision to downgrade to, and whether the data migration's effects are reversible, *before* deploying.

## 8. Best-practice checklist

| Practice | Payoff |
|---|---|
| Versioned migration files | auditable history, repeatable deploys |
| One migration per PR, descriptive name | reviewable, bisectable |
| `downgrade()` always implemented | rollback exists when needed |
| Expand → backfill → contract | zero-downtime, mixed-version safe |
| Idempotent data migrations | re-runs are safe |
| Never edit applied migrations | history stays truthful |
| Migrations tested (up/down/up + constraints) | broken reversals caught in CI |
| Lineage columns immutable | index rebuilds never orphan entries |
| Index stores refs, not content | derived stores stay rebuildable |
| `alembic check` in CI | model drift caught immediately |

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| `NOT NULL` added in one step on live data | expand → backfill → contract |
| `downgrade(): pass` | implement it or state why impossible |
| Edited an already-applied migration | write a follow-up migration instead |
| One giant backfill UPDATE | chunk by primary key, log progress |
| Drop + recreate to "clean up" | migration chain; recreate destroys lineage |
| Index rebuilt from content hashes | store `source_ref`; rebuild re-reads sources |
| Autogenerated migration committed unread | review generated scripts line by line |
| Model changed, migration forgotten | `alembic check` in CI |

---

## Mastery Check

You can claim this topic when you can:

1. Change a book edition and rebuild the index with every `source_ref` still resolving.
2. Write an expand-backfill-contract sequence and explain why each step is safe with old code running.
3. Downgrade one step and re-upgrade with data intact.
4. Prove a unique constraint raises on duplicate insert after migration.
5. Explain why an applied migration is never edited.

---

## Next Steps

- Backup and restore the migrated database: `04-databases/postgresql/07-backup-and-restore`.
- Source-of-truth patterns for derived indexes: `10-system-design/03-consistency-and-staleness`.
- Repository patterns around evolving models: `04-databases/sqlalchemy/10-repository-pattern`.
