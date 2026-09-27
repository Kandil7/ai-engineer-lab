# Consistency and Staleness Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| Source of truth | The one authoritative store for a fact |
| Derived store | Rebuildable store (vector index, cache) that may lag |
| Eventual consistency | Derived store converges to truth over time |
| Version stamp | Monotonic number recording a store's current state |
| Drift | `source.version - derived.built_from_version` (writes invisible) |
| Staleness | How far behind a derived store is |
| Cache-aside | Read pattern: check cache, miss loads source and populates |
| TTL | Time-to-live: cache entry expires after N seconds |
| Event invalidation | Cache entry removed on write (best-effort freshness) |
| Write hook | Code invoked on writes to trigger invalidation |
| Read-your-writes (RYW) | A writer's own reads see their writes immediately |
| Session pinning | Routing a session's reads to the fresher store |
| Staleness state machine | healthy → stale → degraded → broken, by drift |
| Degraded mode | Serving with warnings when drift is significant |
| Rebuild | Full re-derivation of a derived store from the source |
| Incremental update | Partial index update applied per change event |
| Compare-and-set | Apply an update only if its version is newer |
| Lost update | A later write overwritten by an out-of-order older one |
| Out-of-order delivery | Events applied in wrong sequence (queue retries) |
| Idempotency | Re-applying an update produces the same state |
| Invariant check | Post-rebuild verification (no-loss, provenance) |
| Lineage ref | `source_ref` key linking derived entries to sources |
| Freshness contract | Documented staleness bound a consumer can rely on |
| Dual-write | Writing two stores as if both were truth; corruption source |
| Safety net (TTL) | Expiry that bounds staleness when invalidation fails |
| Alert threshold | Drift value that triggers a page |
| Monotonic version | Version that only increases; blocks stale applications |

---

## Detailed Definitions

### Source of truth vs derived
Exactly one store is authoritative per fact (Postgres for Athar's catalog). Derived stores (vector index, caches) are rebuildable from truth — the test: "can we delete it and rebuild?" Duality (two truths) guarantees silent divergence.

### Version stamps and drift
Every write bumps the source version; the derived store records what it reflects. `drift` is a number you can alert on. Unstamped staleness is invisible until a user finds wrong citations.

### Cache-aside, TTL, invalidation
Cache-aside: hit returns, miss loads and populates. TTL gives bounded staleness (honest); event invalidation gives near-freshness (best-effort). Production uses TTL as safety net under events.

### Read-your-writes
A writer's subsequent reads see their own write (read from truth or skip cache for the session). Prevents "my edit vanished" — essential for editors of a scholarly catalog.

### Staleness state machine
healthy (drift 0) → stale (small drift: alert + catch-up) → degraded (serve with warning or source-backed only) → broken (full rebuild, incident). Thresholds are product decisions about how wrong retrieval may be.

### Rebuild path
Derived stores recover by re-deriving from source through lineage refs (`source_ref`). Post-rebuild invariant checks (topic 38) prove no loss and provenance intact.

### Compare-and-set and lost updates
Updates are applied only if their version is newer than the store's. Out-of-order events (from retries) are rejected. Combined with idempotent handlers this makes the pipeline safe under at-least-once.

### Freshness contracts
What a consumer may assume (e.g. "search results may lag writes by ≤ 5 s"). Documented in the component contract; enforced by TTL and monitored by drift.

### Dual-write corruption
Writing two stores as if both were authoritative. The fix is a single truth plus derived rebuildables — recorded as an ADR (topic 05).
