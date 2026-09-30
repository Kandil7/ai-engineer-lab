# Challenge 38 — Quiz: Test Strategy

1. The test type that catches cross-team schema drift is:
   - A) unit  (B) contract  (C) regression  (D) smoke
2. A byte-for-byte assertion on stored text protects:
   - A) speed  (B) provenance/citations  (C) memory  (D) coverage
3. Idempotent ingest means a rerun produces:
   - A) duplicates  (B) zero new rows  (C) errors  (D) slower results
4. A known-failure case should be stored as:
   - A) an inline string  (B) a golden fixture  (C) a comment  (D) a TODO
5. "Validate then parse" on every record violates which budget:
   - A) memory  (B) call count  (C) disk  (D) network
6. The data invariant for "record in source but not store" is called:
   - A) phantom  (B) loss  (C) drift  (D) corruption
7. A tautological test is one that:
   - A) runs fast  (B) cannot fail  (C) covers edges  (D) uses mocks
8. Unit tests should depend on the network:
   - A) always  (B) never  (C) in CI only  (D) on Fridays

**Answers:** 1-B, 2-B, 3-B, 4-B, 5-B, 6-B, 7-B, 8-B
