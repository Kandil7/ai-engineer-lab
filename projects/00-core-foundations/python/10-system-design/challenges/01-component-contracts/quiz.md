# Challenge 01 — Quiz: Component Contracts

1. A contract's four parts are:
   - A) name, version, size, hash  (B) shape, semantics, invariants, version  (C) input, output, error, log  (D) class, method, field, doc
2. Adding a required field is:
   - A) compatible  (B) needs-migration  (C) breaking  (D) invisible
3. Adding an optional field is:
   - A) compatible  (B) needs-migration  (C) breaking  (D) illegal
4. The safe order to introduce a required field is:
   - A) require, backfill  (B) emit-default, consumers-tolerate, backfill, require  (C) one deploy  (D) rename first
5. Semantic drift means:
   - A) a missing field  (B) same shape, different meaning  (C) a typo  (D) a slow query
6. A validator should report:
   - A) the first problem only  (B) every violation  (C) nothing  (D) a boolean
7. Where should the shared contract live?
   - A) in one team's head  (B) a versioned artifact both teams read  (C) Slack  (D) in tests only
8. A producer-side contract test catches:
   - A) performance  (B) schema drift before production  (C) UI bugs  (D) flaky tests

**Answers:** 1-B, 2-B, 3-A, 4-B, 5-B, 6-B, 7-B, 8-B
