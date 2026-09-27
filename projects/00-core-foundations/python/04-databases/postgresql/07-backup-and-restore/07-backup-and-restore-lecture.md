# Databases Lecture 07: Backup and Restore

## Topic Overview

The backup that matters is not the one that runs at midnight — it is the one that restores at 2 a.m. under pressure. Backups fail in four characteristic ways: they are never verified, they are too coarse-grained for the loss you actually suffer, they omit the config and secrets that make the data usable, or they restore slower than the business can wait. For a scholarly catalog like Athar's, where PostgreSQL is the declared source of truth and the vector index is derived, the backup *is* the corpus's survival. This lecture covers dump/verify/restore as one discipline, RPO/RTO as the design parameters, PITR for modern losses, the 3-2-1 rule, and the disaster runbook you can only write if you have already rehearsed the drill.

The theme: **an unverified backup is not a backup; an unrehearsed restore is a hope.**

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Name the four backup failure modes and design against each.
2. Perform a logical dump and restore, and verify the restore by comparison.
3. Set RPO/RTO and pick a backup strategy that satisfies both.
4. Explain WAL archiving and point-in-time recovery (PITR).
5. Apply the 3-2-1 rule and decide what else must be backed up (and what is derived).
6. Write and rehearse a disaster runbook with measured timings.
7. Detect a corrupt or truncated dump before it is needed.

---

## Prerequisites

| Need | Where |
|---|---|
| SQL fundamentals | `04-databases/sql-fundamentals/` |
| Transactions | `04-databases/sql-fundamentals/11-transactions` |
| Migrations | `04-databases/sqlalchemy/11-migrations-alembic` |
| System consistency | `10-system-design/03-consistency-and-staleness` |

---

## 1. The four failure modes

1. **Never verified.** A dump file exists; nobody has ever restored it. Corrupt encodings, missing tables, and permission gaps surface at the worst moment. Verification is a *restore into scratch + comparison*, automated.
2. **Wrong granularity.** A nightly dump has a 24-hour RPO. If the incident is a bad migration at 14:32, a nightly dump rolls the day back. Granularity must match the loss you can actually afford.
3. **Config/secrets loss.** The data restores; the connection strings, migration state, and model-version pin do not. The system is an orphan. Back up the migration chain and config *references* (the secrets themselves live in a vault).
4. **Too slow.** The restore works but takes 12 hours against a 1-hour RTO. Measure restore time during drills; if it violates RTO, change the method (physical backup, parallel restore, standby).

## 2. Logical dump and restore

A **logical dump** serializes schema + data into a re-runnable form (`pg_dump` for Postgres; `sqlite3.iterdump` in the exercise). It is portable (restores to a different major version), human-readable, and selective (one table, one schema). Its cost: restore is slower than a physical copy.

The restore is only half the operation. **Verification** compares source and restored databases — row counts per table plus content spot-checks (the corpus text must survive byte-for-byte):

```python
problems = verify_restore(src, restored)  # [] means verified
```

Automation rule: the drill runs on a schedule (weekly is common), restores into a scratch instance, verifies, and reports the measured restore time. The report is the backup's real status.

## 3. RPO and RTO: the design parameters

| Concept | Question it answers | Example |
|---|---|---|
| **RPO** (Recovery Point Objective) | How much data may we *lose*? | "24 hours" for read-mostly archives |
| **RTO** (Recovery Time Objective) | How fast must we be *back*? | "1 hour" before revenue impact |

These are business decisions that select the technology:

| Strategy | RPO | RTO | Fits |
|---|---|---|---|
| Nightly logical dump | 24 h | hours | small, read-mostly catalog |
| Hourly dump + WAL archiving | 1 h | minutes | active catalog |
| Continuous WAL shipping | seconds | minutes | mission-critical |
| Sync replica + PITR | ~0 | seconds | zero-loss requirement |

The trap: declaring "we have backups" without stating RPO/RTO. Every backup design must name both numbers and show which mechanism delivers them.

## 4. WAL archiving and point-in-time recovery

Postgres writes every change to the **Write-Ahead Log** before touching data files. Archiving the WAL turns a nightly dump into a *timeline*: the dump is the base, WAL segments are the replay, and `recovery_target_time` stops the replay at any second.

```ini
archive_mode = on
archive_command = 'cp %p /archive/%f'
# recovery:
restore_command = 'cp /archive/%f %p'
recovery_target_time = '2026-08-17 14:31:00'
```

PITR is what makes the 14:32 incident recoverable to 14:31 instead of to midnight. Physical backup tools (pgBackRest, Barman) package base backup + WAL shipping + retention; for a real Athar deployment they are the default choice over cron'd `pg_dump`.

## 5. 3-2-1 and the full backup surface

**3 copies, 2 media types, 1 offsite.** The rule survives because it defends against the three real threats: accidental deletion (another copy), media failure (another medium), site loss (offsite).

But the *data* is only part of what must survive:

| Item | Backed up? | Why |
|---|---|---|
| Data dumps | yes | the corpus |
| WAL archive | if RPO < 24 h | the timeline |
| Migration files + version state | yes | they *are* the schema's history |
| Config and secrets | references only | secrets belong in the vault |
| **Vector index** | **no — derived** | rebuilt from source via lineage refs |
| Restore runbook | yes | with drill results and dates |

The vector index's exclusion is the skills-map logic in action: the index is a derived store keyed by `source_ref`. Backing it up is optional convenience; rebuilding it is the recovery path. The thing that must never be lost is the source of truth and its lineage keys.

## 6. The disaster runbook

The runbook is executable only because the drill measured every step:

1. **Stop writes** (read-only mode) — prevent further corruption.
2. **Restore the last verified dump** into the scratch/production path.
3. **Replay WAL to the target time** (PITR) if RPO requires it.
4. **Verify** counts + content spot-checks (the same comparison as the drill).
5. **Resume**, then root-cause the incident (bad migration → the migration test gap).

The exercise's simulation proves the shape: data wiped, restore from verified dump, verification clean, recovered row count matches. The drill is why step 4 takes seconds instead of being a discovery.

## 7. Corruption detection

A truncated or partially-written dump restores *some* rows and verifies *against* the source — which is exactly why verification must be comparison-based, not "the restore command exited 0". The exercise includes a deliberately truncated dump and proves the verifier catches it. In production, also store dump checksums (`sha256sum`) alongside the file and verify before restore.

## 8. Best-practice checklist

| Practice | Payoff |
|---|---|
| Verify by restore + comparison | backup is proven, not assumed |
| Automate the drill on a schedule | measured restore time, known RTO |
| State RPO/RTO explicitly | technology choice is justified |
| WAL archiving for RPO < 24 h | losses measured in seconds |
| 3-2-1 placement | survives deletion, media, site failures |
| Back up migrations + config refs | restored data is a usable system |
| Treat vector index as derived | recovery path is rebuild, not restore |
| Checksums on dump files | corruption caught before the incident |
| Runbook with measured steps | the 2 a.m. path is rehearsed |
| Backup before every migration | worst case is one migration back |

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| "The backup ran" = "we're safe" | verify by restoring it |
| Nightly dump but need second-level RPO | WAL archiving + PITR |
| Restore never timed | drill it and measure |
| Backups on the same disk as the DB | 3-2-1: separate media, offsite copy |
| Vector index backed up as primary | it's derived; source is truth |
| Secrets in the backup plaintext | vault references only |
| One giant unverified dump file | checksums + scheduled drill |
| Runbook written during the incident | write it from the drill |

---

## Mastery Check

You can claim this topic when you can:

1. Restore a dump into scratch and prove by comparison that it matches the source.
2. Name your system's RPO/RTO and the mechanism that delivers each.
3. Explain the exact steps and measurements in your disaster runbook.
4. Detect a truncated dump with the verifier before it is used.
5. State which of your stores are sources of truth vs derived, and what gets backed up.

---

## Next Steps

- Source-of-truth and consistency in derived indexes: `10-system-design/03-consistency-and-staleness`.
- Failure modes of workers and pipelines: `10-system-design/04-failure-modes-and-resilience`.
- Migration safety before backups: `04-databases/sqlalchemy/11-migrations-alembic`.
