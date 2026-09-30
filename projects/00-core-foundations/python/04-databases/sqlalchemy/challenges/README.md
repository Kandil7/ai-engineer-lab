# 04-databases/sqlalchemy — Challenge Sets

Practice sets follow [`PRACTICE_SPEC.md`](../../../PRACTICE_SPEC.md).

| Challenge | Topic | Skills |
|---|---|---|
| `11-migrations-alembic/` | [Migrations and Schema Evolution](../11-migrations-alembic/) | revision chains, expand-backfill-contract, lineage-preserving rebuild |

## Running

```powershell
python -m pytest 04-databases/sqlalchemy/challenges/<name>/test_challenge.py -q
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 04-databases/sqlalchemy/challenges/<name>/test_challenge.py -q
```
