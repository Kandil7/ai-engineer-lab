# Challenge 02 — Quiz: Queues and Workflows

1. A queue broker's delivery guarantee you must assume is:
   - A) exactly-once  (B) at-least-once  (C) never  (D) ordered
2. Idempotency is achieved with:
   - A) locks  (B) a natural key + insert-if-absent  (C) retries  (D) timeouts
3. Exponential backoff with jitter prevents:
   - A) data loss  (B) retry storms  (C) OOM  (D) schema drift
4. A permanent error should be:
   - A) retried  (B) dead-lettered immediately  (C) ignored  (D) logged only
5. The dead-letter queue is for:
   - A) slow jobs  (B) jobs that exhausted retries  (C) old code  (D) backups
6. An unbounded job result history causes:
   - A) speed  (B) memory growth  (C) correctness  (D) nothing
7. The attempt cap exists to:
   - A) slow things down  (B) bound work and route failures to the DLQ  (C) save money  (D) pass tests
8. Backpressure means:
   - A) more workers  (B) producers slow when consumers saturate  (C) compression  (D) caching

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
