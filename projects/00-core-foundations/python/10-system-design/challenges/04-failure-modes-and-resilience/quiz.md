# Challenge 04 — Quiz: Failure Modes and Resilience

1. A failure worth retrying is classified as:
   - A) permanent  (B) transient  (C) silent  (D) partial
2. A worker killed mid-job is which class:
   - A) transient  (B) partial  (C) permanent  (D) silent
3. A stale index that raises no error is:
   - A) transient  (B) silent  (C) fine  (D) permanent
4. A bulkhead isolates failure by:
   - A) retrying  (B) capping concurrency per dependency  (C) caching  (D) logging
5. A timeout should be checked:
   - A) after the call  (B) before starting work that cannot finish  (C) never  (D) in tests only
6. Under total dependency failure the product must:
   - A) guess  (B) refuse honestly (503)  (C) cache forever  (D) restart
7. A cascading failure is amplified by:
   - A) backoff  (B) unbounded retries  (C) bulkheads  (D) timeouts
8. The FMEA table records per failure mode:
   - A) the author  (B) detection, blast radius, recovery  (C) the cost  (D) the language

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
