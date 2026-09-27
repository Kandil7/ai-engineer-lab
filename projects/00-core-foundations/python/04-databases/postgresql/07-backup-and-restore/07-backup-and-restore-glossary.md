# Backup and Restore Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| Backup | A copy of the system that can be restored to a usable state |
| Restore | Applying a backup to recreate the database |
| Restore drill | Scheduled rehearsal: restore + verify + measure timing |
| Verification | Comparison proving restored data matches the source |
| Logical dump | Schema+data serialized to re-runnable SQL (pg_dump) |
| Physical backup | Copy of the data files themselves (pgBackRest base) |
| pg_dump / pg_restore | Postgres logical dump/restore tools |
| WAL | Write-Ahead Log: every change recorded before data files |
| WAL archiving | Shipping WAL segments to durable storage |
| PITR | Point-in-Time Recovery: replay WAL to a target second |
| `recovery_target_time` | Timestamp stopping the WAL replay |
| Base backup | Full physical copy WAL replay starts from |
| RPO | Recovery Point Objective: max data loss tolerated |
| RTO | Recovery Time Objective: max downtime tolerated |
| 3-2-1 rule | 3 copies, 2 media types, 1 offsite |
| Offsite copy | Backup in a different physical location |
| Checksum (sha256) | Hash proving a dump file is intact |
| Truncated dump | Partial dump file; must fail verification |
| Source of truth | The store whose data is authoritative |
| Derived store | Rebuildable store (vector index) not backed up as primary |
| Lineage ref | `source_ref` key tying derived entries to sources |
| Runbook | Executable incident procedure with measured steps |
| Read-only mode | Stopping writes during recovery |
| Retention policy | How long backups/WAL segments are kept |
| Scratch instance | Temporary database used for restore drills |
| Spot-check | Sampled content comparison during verification |
| Config/secrets reference | Pointer to vault-held secrets, backed up as text |

---

## Detailed Definitions

### Backup vs verified backup
A backup is only as good as its last successful restore. Verification = restore into a scratch instance and compare row counts plus content spot-checks with the source. An unverified dump is a file, not a backup.

### Logical vs physical backup
Logical (`pg_dump`) serializes SQL — portable, selective, slower to restore. Physical (pgBackRest base backup + WAL) copies data files — fast, tied to the same major version. Choose by RTO.

### WAL and PITR
Postgres writes changes to the Write-Ahead Log before data files. Archiving WAL turns a base backup into a timeline: `recovery_target_time` replays to any second, so a 14:32 loss recovers to 14:31.

### RPO and RTO
RPO = how much data you can lose; RTO = how fast you must recover. They are business numbers that select the mechanism: nightly dump (24 h RPO) vs continuous WAL shipping (seconds).

### 3-2-1 rule
Three copies on two media types with one offsite — the standard defense against accidental deletion, media failure, and site loss.

### Full backup surface
Beyond data: migration files + version state (schema history), config/secret references (secrets in a vault), and a runbook. The vector index is *derived* — rebuilt from sources through lineage refs, not restored as primary.

### Disaster runbook
The rehearsed incident path: stop writes → restore verified dump → replay WAL → verify → resume → root-cause. Written from drill measurements, not invented during the incident.

### Corruption detection
Truncated or partial dumps must fail verification (comparison-based checks and checksums). "The restore command exited 0" is not evidence.

### Source of truth vs derived store
Postgres (books, editions, permissions, lineage) is authoritative and backed up. Vector indexes are derived and rebuilt. Treating the index as truth is the classic recoverability mistake.
