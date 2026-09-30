# Challenge 03 — Quiz: Consistency and Staleness

1. The store that is authoritative for a fact is called:
   - A) the cache  (B) the source of truth  (C) the index  (D) the replica
2. A derived store differs from the source when:
   - A) never  (B) drift > 0  (C) always  (D) at midnight
3. TTL in a cache provides:
   - A) strong consistency  (B) a bounded staleness window  (C) speed only  (D) durability
4. Event invalidation is best-effort because:
   - A) it is slow  (B) hooks can fail  (C) caches are small  (D) of TTL
5. Read-your-writes means:
   - A) faster reads  (B) a writer's next read sees their own write  (C) replication  (D) caching
6. A late queue event must not overwrite a newer one; the fix is:
   - A) locking  (B) per-key version stamps  (C) retries  (D) batching
7. The recovery path for a stale derived index is:
   - A) restart  (B) rebuild from the source of truth  (C) drop it  (D) wait
8. The staleness state "degraded" should trigger:
   - A) nothing  (B) a designed product response (warning or source-backed)  (C) an outage  (D) a restart

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
