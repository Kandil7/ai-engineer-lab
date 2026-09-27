# System Design Lecture 03: Consistency and Staleness

## Topic Overview

The skills map asks the question directly: *what happens when the index becomes older than the source?* If the answer is "retrieval silently serves old text", the system has an unmodeled failure state. This lecture models it: one source of truth per fact, everything else derived and therefore *allowed to lag* — but with the lag measured (version stamps), bounded (staleness states), visible (alerts), and recoverable (rebuild). Caches get the same treatment: TTL as honest staleness, invalidation as best-effort freshness, and read-your-writes so a user who just edited a record actually sees the edit. The payoff is the Athar design in which a stale index is a *known state with a runbook*, not corrupted citations nobody can explain.

The theme: **staleness is not a bug to eliminate — it is a quantity to measure, bound, and recover from.**

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Name the single source of truth for each fact and justify what is derived.
2. Use version stamps to compute drift mechanically.
3. Implement cache-aside with TTL and event invalidation, and state each one's staleness contract.
4. Explain read-your-writes and implement the cheap version.
5. Design the staleness state machine (healthy → stale → degraded → broken) with thresholds.
6. Reject out-of-order updates by version, preventing lost-update corruption.
7. Explain the rebuild path and why only derived stores have one.

---

## Prerequisites

| Need | Where |
|---|---|
| Component contracts | `10-system-design/01-component-contracts/` |
| Queues (events, redelivery) | `10-system-design/02-queues-and-workflows/` |
| Migrations & lineage | `04-databases/sqlalchemy/11-migrations-alembic` |
| Backup & derived stores | `04-databases/postgresql/07-backup-and-restore` |

---

## 1. One source of truth per fact

Every fact — a book's title, a page's text, a user's permission — has exactly one authoritative store. For Athar: **PostgreSQL** holds books, editions, pages, permissions. The **vector index** and any search cache are *derived*: they can be rebuilt from Postgres at any time.

The test for "is this derived?": *can we delete it and rebuild it from the truth?* If yes, it is a derived store and eventual consistency is acceptable. If no, you have invented a second source of truth, and the two will disagree — the classic dual-write corruption. This decision belongs in an ADR (topic 05).

## 2. Version stamps: staleness as a number

Feelings don't page anyone at 3 a.m.; numbers do. Every write to the source bumps a version; the derived store records the version it reflects:

```python
drift = source.version - index.built_from_version
```

`drift == 0` is current; `drift == 3` means three writes are invisible in retrieval. This number is the alert, the dashboard panel, and the recovery trigger. Without it, "is the index stale?" is unanswerable until a user notices wrong citations.

## 3. Cache-aside: TTL and invalidation

**Cache-aside** is the standard read path: check cache → hit returns; miss loads from source, populates cache. Two invalidation styles with different contracts:

| Style | Freshness | Cost | Failure mode |
|---|---|---|---|
| **TTL** (expire after N s) | bounded staleness | trivial | serves data ≤ N seconds old |
| **Event** (invalidate on write) | near-fresh | write hook needed | lost invalidation = stale forever |

TTL is *honest*: it states its staleness bound. Event invalidation is *best-effort*: it works until a write hook fails. Production systems use both — TTL as the safety net, events for freshness. The exercise measures the cache's hit/miss behavior across expiry and invalidation.

Cache keys matter: a cached answer without its version stamp is an untraceable stale value.

## 4. Read-your-writes

The user-visible bug of eventual consistency: *I edited the record, refreshed, and see the old version.* Read-your-writes (RYW) guarantees a writer sees their own writes immediately. The cheap implementation: for the writing session, read from the source of truth (or skip the cache) — other sessions may continue reading the derived view.

```python
if writer_session:
    return source.rows[key]  # your own write, from truth
return cache.get(key, ...)  # others: cache is fine
```

For Athar: after an editor corrects a page, the editor's next `/search` must see the correction even if the vector index has not been updated.

## 5. The staleness state machine

The mastery question's answer is a designed state machine:

| State | Drift | Response |
|---|---|---|
| **healthy** | 0 | serve normally |
| **stale** | ≤ threshold (e.g. 5) | alert + incremental catch-up |
| **degraded** | ≤ broken threshold | serve with staleness warning, or serve source-backed only |
| **broken** | unbounded | full rebuild from source; treat as incident |

The thresholds are product decisions: how stale may retrieval be before the answer is a lie? For a scholarly citation system, the tolerance is low — a citation quoting a superseded page is a correctness failure, so `degraded` should be loud.

The **recovery path is always rebuild** — because the index is derived (section 1). That is the deep link between the backup lecture (index not backed up as truth) and this one (index rebuilt on drift).

## 6. Out-of-order updates and lost updates

Queues redeliver (topic 02); incremental index updates can arrive out of order. Applying an old update after a new one silently corrupts the index. The fix is the same version discipline applied per update:

```python
if update_version <= index.built_from_version:
    return False  # stale event: ignore
```

This is the *compare-and-set* pattern at the state level: only monotonic versions advance the derived store. Combined with idempotent handlers, it makes the event pipeline safe under at-least-once and reordering.

## 7. The Athar answer to "index older than source"

The complete designed answer — the mastery criterion:

1. **Detection**: `drift = source.version - index.built_from_version`, monitored continuously.
2. **Bound**: staleness state machine with thresholds; `degraded` triggers a product response (warning banner or source-backed answers).
3. **Recovery**: rebuild job re-derives the index from Postgres through lineage refs (`source_ref`); version stamp advances to source's.
4. **Prevention**: versioned incremental updates (reject out-of-order), idempotent jobs, write hooks for cache invalidation.
5. **Verification**: post-rebuild invariant checks (topic 38: no-loss, provenance intact).

## 8. Best-practice checklist

| Practice | Payoff |
|---|---|
| One source of truth per fact | consistency is fixable by rebuild |
| Version stamps on source and derived | drift is a number, not a feeling |
| TTL as the safety net under events | bounded staleness even when hooks fail |
| Read-your-writes for editors | no "my edit vanished" reports |
| Staleness states with thresholds | designed responses, not surprises |
| Rebuild runbook for derived stores | drift is recoverable by definition |
| Compare-and-set version updates | reordering cannot corrupt the index |
| Alert on drift, DLQ depth, job age | degradation visible before loss |
| Staleness documented in contracts | consumers know the freshness they get |

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Two stores both "authoritative" | pick one; make the other derived/rebuildable |
| No version stamps | drift is invisible until users complain |
| Event invalidation without TTL | add TTL as the safety net |
| Cached value with no version | can't reason about freshness |
| Writer reads stale cache | read-your-writes for the writing session |
| Out-of-order index updates applied | version check, reject stale |
| Index backed up as if it were truth | it's derived; rebuild from source |
| "Consistency later" | the dual-write bug is the cost |

---

## Mastery Check

You can claim this topic when you can:

1. State which of your stores are truth vs derived for every fact.
2. Compute drift for a system and set thresholds that page someone.
3. Design the exact answer to "the index is older than the source" — detection, bound, recovery.
4. Prove a writer's own read sees their write while other readers may lag.
5. Show that a late, out-of-order update cannot corrupt the index.

---

## Next Steps

- What happens when the worker dies mid-rebuild: `04-failure-modes-and-resilience/`.
- Record the truth/derived decision: `05-architecture-decision-records/`.
- Rebuild mechanics and lineage: `04-databases/sqlalchemy/11-migrations-alembic`.
