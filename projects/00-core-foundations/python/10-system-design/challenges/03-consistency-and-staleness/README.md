# Challenge 03: Consistency and Staleness — The Stale Index

The Athar vector index is derived; Postgres is truth. Updates arrive from a
queue that redelivers and reorders. Three questions: how stale are we, when is
a cached read acceptable, and how do late events stay harmless?

## 🥉 Bronze — The State Machine (~15 min)

**Task:** Implement `staleness_state(drift, stale_threshold, broken_threshold)`:
`drift == 0` → `"healthy"`; `drift <= stale_threshold` → `"stale"`;
`drift <= broken_threshold` → `"degraded"`; otherwise `"broken"`.

**Signature:**
```python
def staleness_state(drift: int, stale_threshold: int, broken_threshold: int) -> str
```

| Input | Expected |
|---|---|
| `0, 5, 100` | `"healthy"` |
| `3, 5, 100` | `"stale"` |
| `50, 5, 100` | `"degraded"` |
| `500, 5, 100` | `"broken"` |

**Constraints:** thresholds are positive. Any correct mapping passes.

---

## 🥈 Silver — Cache-Aside with TTL (~35 min)

**Task:** Implement `cache_get(cache, key, now, ttl, loader)`: return the cached
value if fresh (`now - stored_at <= ttl`); otherwise call `loader(key)`, store
`(value, now)` in `cache[key]`, and return it. **Evicting `cache[key]` is the
invalidation event** — the next access must load again.

**Signature:**
```python
def cache_get(cache: dict, key: str, now: float, ttl: float, loader) -> dict
```

| Scenario | Expected |
|---|---|
| fresh hit | cached value, loader **not** called |
| expired (`now` past `ttl`) | loader called |
| after eviction | loader called |
| `ttl = 0` | every access loads |

**Constraints:** `now` is an injected clock value — never wall-clock. **Guard
(call counting):** a 20-access timeline (hits, one TTL boundary, one eviction)
must produce exactly **3** loader calls — a no-TTL cache calls once and fails;
a never-caching implementation calls 20 times and fails. **Adversarial case:**
accesses exactly at the TTL boundary and one microsecond under it.

---

## 🥇 Gold — Versioned Apply (~75 min)

**Task:** Implement `apply_events(index, events, applied_versions)` for
redelivered, out-of-order queue events `(version, key, value)`: apply an event
iff `version > applied_versions.get(key, 0)` (per-key monotonic), updating
`index[key] = value` and the stamp; return `{"accepted": int, "rejected": int}`.
And `recover(source, index, applied_versions, source_version)` rebuilding the
index from the source of truth: returns the number of resolvable entries.

**Signature:**
```python
def apply_events(index: dict, events: list[tuple[int, str, dict]],
                 applied_versions: dict[str, int]) -> dict[str, int]
def recover(source: dict, index: dict, applied_versions: dict[str, int],
            source_version: int) -> int
```

| Scenario | Expected |
|---|---|
| shuffled events with late arrivals | final index = max-version-per-key reference |
| duplicate redelivery | rejected, counted |
| `recover` after 3-event drift | index == source, stamps == source_version |
| `[]` events | `{"accepted": 0, "rejected": 0}` |

**Constraints:** 50k events, memory ceiling 8 MB peak (`tracemalloc`) — storing
per-event histories blows it; counters plus the per-key stamps stay flat.
**Guards:** (a) correctness under shuffle + redelivery (naive arrival-order
apply leaves an old value winning and fails); (b) exact accepted/rejected
counts; (c) memory ceiling. **Follow-up:** what breaks first when events arrive
faster than rebuilds? *(Answer: drift grows unbounded — you need incremental
catch-up or a rebuild trigger at the degraded threshold.)*

---

## Running

```bash
python -m pytest 10-system-design/challenges/03-consistency-and-staleness/test_challenge.py -q
$env:CHALLENGE_USE_SOLUTION = "1"
python -m pytest 10-system-design/challenges/03-consistency-and-staleness/test_challenge.py -q
```
