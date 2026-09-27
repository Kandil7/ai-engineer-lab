# Migrations and Schema Evolution Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| Migration | Versioned script that changes schema (or data) reversibly |
| Revision | Unique id of one migration file in the chain |
| Revision chain | Ordered list of migrations Alembic applies |
| `alembic_version` | One-row table recording the applied revision |
| Upgrade | Applying a migration forward (`upgrade()`) |
| Downgrade | Reversing a migration (`downgrade()`) |
| Autogenerate | Alembic draft comparing models to live DB |
| Expand-contract | Three-step pattern for zero-downtime constraint changes |
| Expand step | Additive change old code tolerates (nullable column) |
| Contract step | Constraint tightening after backfill (NOT NULL, unique) |
| Backfill | Data migration populating new columns for existing rows |
| Data migration | Migration changing row content, not shape |
| Idempotent migration | Safe to re-run; second run is a no-op |
| Chunked update | Batched UPDATE by key range to avoid lock/bloat |
| Hand-edit | Ad-hoc DDL in production; unreviewed and unrepeatable |
| Recreate | Drop + create schema; destroys data and lineage |
| Schema drift | Models and deployed database disagree |
| `alembic check` | CI guard detecting model/DB drift |
| Lineage key | Immutable ref (`book/page`) tying index entries to sources |
| `source_ref` | The lineage column; never dropped or rewritten |
| Derived store | Rebuildable index (vector DB) storing refs, not content |
| Index rebuild | Re-reading sources and re-embedding through lineage refs |
| IntegrityError | DB-level constraint violation (duplicate key, NOT NULL) |
| Mixed-version deploy | Old and new code both live during expand window |
| Rollback path | Known downgrade revision + reversibility of data steps |
| Dual-write | Writing old and new columns during a rename migration |
| Linear chain | Single migration lineage; branching only via `merge` |
| Applied migration | Migration recorded in `alembic_version`; immutable |

---

## Detailed Definitions

### Migration and revision chain
A migration is reviewed, ordered code for schema change with `upgrade()`/`downgrade()`. Alembic records the applied revision in `alembic_version`; the chain is the deployed schema's full history and the recovery path.

### Expand → backfill → contract
The zero-downtime sequence: add nullable column (old code safe), idempotent backfill, then enforce the constraint once old code is drained. Each step must keep both old and new code working.

### Data migration
Content change as code (backfills, folds). Must be idempotent, chunked by key range, and honest in `downgrade()` about reversibility.

### Autogenerate and `alembic check`
`--autogenerate` drafts the migration from model/DB differences — always read it. `alembic check` fails CI when models drift from the deployed schema.

### Lineage and derived stores
`source_ref` is immutable identity; index entries store it and join back to sources. Rebuilds re-read sources and re-embed — they never rewrite lineage keys. Migrations must never touch the lineage column without proving every ref still resolves.

### Testing migrations
The CI ritual: upgrade to head, seed data, downgrade + re-upgrade, prove constraints. A `downgrade()` that is `pass` is unproven.

### Applied migrations are immutable
Once recorded in `alembic_version`, a file is history; corrections are new migrations. Editing applied migrations makes environments irreconcilable.

### Mixed-version deploy
The expand window where old and new code coexist. Every intermediate schema must serve both; contract steps run only after the old code is gone.
