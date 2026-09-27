# Test Strategy Glossary

## Quick Reference Table

| Term | One-Line Definition |
|------|-------------------|
| Test pyramid | Portfolio shape: many unit, some integration, few E2E |
| Unit test | Test of one rule in isolation; pure, offline, < 1ms |
| Integration test | Test of layer handoffs using real-shaped, hermetic deps |
| E2E test | Test through the real system; few, slow, nightly |
| Contract test | Test asserting the schema a consumer depends on |
| Schema drift | Producer changes shape without consumer knowing |
| Required fields | Fields a consumer's contract test enforces |
| Regression test | Test pinning a fixed bug so it never returns |
| Known-failure case | Named production bug stored as a golden fixture |
| Golden fixture | Stored test data (JSONL) that survives refactors |
| Characterization test | Test pinning current behavior, quirks included |
| Data test | Corpus-level invariant check after an ingest run |
| Invariant | Condition that must hold over the whole dataset |
| No-loss invariant | Every source record id is present in the store |
| No-phantom invariant | No stored record id that is absent from the source |
| Provenance | The book/page/source lineage attached to every record |
| Idempotent rerun | Re-running ingest produces no duplicates |
| Duplicate suppression | Insert-by-id: second insert reports skipped |
| Hermetic test | No shared state; fresh temp store per test |
| Test double | Fake collaborator (stub, spy, fake) at a contract boundary |
| Stub | Test double returning canned answers |
| Spy | Test double recording calls for later assertion |
| Tautological test | Assertion that cannot fail |
| Marker | pytest label (`unit`, `regression`, `data`) selecting tiers |
| Test tier | Group run at one cadence (save / PR / nightly) |
| Quarantine | Skip-and-report policy for data invariant violations |
| Byte-for-byte assertion | Verbatim comparison protecting stored originals |
| Diagnosability | How precisely a failure points at the broken layer |
| Cadence | How often a test tier runs |

---

## Detailed Definitions

### Test pyramid and tiers
The portfolio shape (many unit → some integration → few E2E) encodes cost and diagnosability. Tiers run at cadences: unit on every save, contract+integration every PR, E2E and data checks nightly/post-ingest.

### Unit test
One rule, no I/O, milliseconds. Pins parsing and rule logic. Cannot catch wiring bugs — that is the integration tier's job.

### Integration test
Layer handoffs with real-shaped but hermetic dependencies (temp sqlite standing in for Postgres). Asserts end state, especially byte-for-byte provenance and rerun idempotence.

### Contract test
Asserts the shape (required fields, types) a consumer depends on, against the producer's serializer or golden payload. Producer schema drift fails the consumer's CI before it reaches production.

### Regression test and known-failure cases
Every production bug becomes a named failing test first, then the fix. Cases live as golden JSONL fixtures. The suite is the "20 known failure cases that never return."

### Data tests and invariants
Corpus-level checks run after ingest: no loss, no phantom records, non-empty text, provenance carried, idempotent rerun. Report violations as strings so operators can quarantine the exact records.

### Provenance
The book/page/source lineage stored on every record. Protected by byte-for-byte assertions on the *verbatim* text — normalized text is for search only.

### Idempotency
Re-running the same ingest produces zero new rows (duplicates reported as skipped). The property that makes backfills and retries safe.

### Hermetic tests
Fresh state per test (temp store, temp dir), no network, no shared globals. Prevents order-dependent flakes and makes parallel CI safe.

### Test doubles
Stubs (canned answers), spies (recorded calls), fakes (working stand-ins). Distinguishable from mocks: assert observable behavior of the unit, not internals of the double.

### Markers and cadence
pytest markers (`unit`, `contract`, `regression`, `data`) select which tier runs when — `pytest -m "not data"` on save, the full suite nightly.
