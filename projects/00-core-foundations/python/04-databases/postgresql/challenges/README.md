# 04-databases/postgresql — Challenge Sets

Practice sets follow [`PRACTICE_SPEC.md`](../../../PRACTICE_SPEC.md).

| Challenge | Topic | Skills |
|---|---|---|
| `07-backup-and-restore/` | [Backup and Restore](../07-backup-and-restore/) | verify-by-restore, content-drift detection, point-in-time recovery |

## Running

```powershell
python -m pytest 04-databases/postgresql/challenges/<name>/test_challenge.py -q
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 04-databases/postgresql/challenges/<name>/test_challenge.py -q
```
