# Advanced Python Lecture 38: Test Strategy — Unit, Integration, Contract, Regression, Data Tests

## Topic Overview

A test suite is a portfolio of bets about what will break. Unit tests bet on logic; integration tests bet on wiring; contract tests bet on other teams; regression tests bet on history; data tests bet on the corpus. Teams that only write unit tests discover schema drift in production; teams that only write end-to-end tests discover a bug with no idea which layer caused it. This lecture builds one test of each type against a miniature ingest pipeline, anchored on the three Athar mastery criteria: **text/book/page never lost through the pipeline, reruns never duplicate, and known failure cases never return.** By the end you know exactly which test type answers which question, where it runs, and what it cannot catch.

The theme: **each test type pays for a distinct failure mode — portfolio, don't duplicate.**

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Place tests in the pyramid by scope, dependencies, and cadence.
2. Write pure unit tests that pin rules in milliseconds.
3. Write hermetic integration tests that assert end state across layers.
4. Write contract tests that fail before a producer's schema drift reaches production.
5. Pin bugs as regression cases with golden fixtures.
6. Write data/pipeline invariants (no loss, no phantom, provenance intact, rerun-safe).
7. State what each test type *cannot* catch — the reason the others exist.

---

## Prerequisites

| Need | Where |
|---|---|
| pytest basics | `45-testing-with-pytest-lecture.md`, `18-unit-testing-lecture.md` |
| Pipeline layering | `36-separation-of-concerns-lecture.md` |
| Normalization and provenance | `35-unicode-and-arabic-text-lecture.md` |
| Failure typing | `47-exceptions-advanced-lecture.md` |

---

## 1. The pyramid, and why the shape is not dogma

```
        /\       E2E          few, slow, real deps      nightly
       /  \      Integration  wiring, hermetic          every PR
      /    \     Unit+Contract pure, fast               every save
     /______\
```

The shape encodes cost and diagnosability. Unit tests are cheap and localize failures to one rule. End-to-end tests are expensive and, when they fail, tell you *something* is wrong but not where. The middle layer — integration and contract — is where most real bugs in a pipeline live: handoffs between layers.

| Type | Scope | Dependencies | Speed | Cadence |
|---|---|---|---|---|
| Unit | one rule | none | < 1ms | every save |
| Contract | producer/consumer schema | none | < 1ms | every PR |
| Integration | layer wiring | temp store/files | < 100ms | every PR |
| Regression | pinned bugs | fixtures | varies | every PR |
| Data | corpus invariants | real corpus | seconds+ | post-ingest |

The balance is a portfolio rule: many unit tests (they pay per rule), enough integration tests (they pay per handoff), one contract test per boundary, and a regression entry per production bug forever.

## 2. Unit tests — one rule, no I/O

Unit tests answer "is this rule correct?" They are pure, offline, and fast enough to run on every save. In the ingest pipeline the two core rules are parsing (does `parse_line` build the right `source_ref` and fold digits?) and storage semantics (does `insert` reject a duplicate?).

What unit tests **cannot** catch: anything involving a second component. A unit test on `parse_line` and a unit test on `Store.insert` can both pass while the *wiring* between them drops the `text` field. That is exactly what integration tests are for.

Anti-patterns: asserting on mock internals (you are testing your fake), tautologies, and tests that reach the network. A unit test that needs a live store is an integration test wearing a costume.

## 3. Integration tests — the wiring, still hermetic

Integration tests answer "do the layers hand off correctly?" The two that encode the Athar criteria:

**Provenance survives** — the strongest data-protection test in a reference pipeline:

```python
assert r1.text == "النص الأصلي"  # byte-for-byte
assert r1.book == "bukhari"
assert r1.page == 1
assert r1.source_ref == "bukhari/p1"
```

Byte-for-byte comparison on the *stored* text, not a normalized form. If the pipeline normalizes for search, the verbatim text must still be intact — that is what the citation will quote.

**Rerun is idempotent** — the skills-map criterion "reruns never produce duplicates":

```python
first = ingest(lines, store)  # {"imported": 1, "skipped_duplicates": 0}
second = ingest(lines, store)  # {"imported": 0, "skipped_duplicates": 1}
assert len(store.rows) == 1
```

Hermetic means: a temporary store of the same shape (a temp sqlite file standing in for Postgres), no shared state between tests, no network. Real-dependency integration tests exist too — they are the nightly tier.

What integration tests cannot catch: drift from a *third party* (a producer's schema change), and production-only semantics (real Postgres locking, real vector-store recall).

## 4. Contract tests — the boundary between producers and consumers

When another team (or another service, or last year's export script) produces the data you consume, the schema is a **contract**. A contract test asserts the *shape* a consumer depends on: required fields, types, nullability.

```python
REQUIRED_FIELDS = {"id": "str", "book": "str", "page": "int-like", "text": "str"}


def contract_payload_matches_consumer_schema(payload) -> list[str]: ...
```

Key properties:

- It lives **with the consumer's expectations** and runs against **the producer's real serializer** (or a recorded golden payload). When the producer drops a field, the consumer's CI fails — before production does.
- It asserts shape, not content. Content correctness belongs to the producer's own tests.
- One contract test per boundary is enough; the cost is in maintenance, not volume.

This is the test type that turns "the importer changed and our citations silently broke" into a red build on the wrong-looking PR.

## 5. Regression tests — pin every bug forever

The rule is mechanical: **every production bug gets a failing test first, then the fix.** The suite accumulates into the "20 known failure cases that never return" of the skills map.

```python
KNOWN_FAILURE_CASES = [
    ("KF-01", '{"id": "", ...}', "reject: empty id"),
    ("KF-02", '{"id": "a", "page": "0", ...}', "reject: page zero"),
    ("KF-03", '{"id": "a", "page": "١٢", ...}', "accept after digit fold"),
]
```

Three disciplines make regression tests durable:

1. **Store the case as data** (golden fixture JSONL), not inline strings that drift with code refactors.
2. **Name the expected outcome**, including which failure mode ("reject: page zero") so a future reader knows *why* the case exists.
3. **Include the acceptance cases too** (KF-03: Arabic-Indic digits must keep working) — regressions break happy paths as often as edges.

Note the KF-03 lesson: it pins the digit-folding behavior from topic 35. Cross-topic behaviors are exactly what regression suites protect.

## 6. Data and pipeline tests — corpus-level invariants

Data tests are about **totals and identity**, not one record. They run after an ingest batch, over the real corpus:

| Invariant | Failure it catches |
|---|---|
| No loss (every source id stored) | silent drops in a batch |
| No phantom (no stored id outside source) | double-processing, wrong joins |
| Text non-empty in store | blank-field validation hole |
| Provenance carried (`source_ref` starts with book) | citation breakage |
| Idempotent rerun | duplicate index growth |

```python
def data_invariants_hold(before, after) -> list[str]:
    lost = source_ids - stored_ids  # "lost records: [...]"
    phantom = stored_ids - source_ids  # "phantom records: [...]"
```

The value of reporting *violations as strings* rather than a boolean: a post-ingest job can log exactly which records broke the invariant and quarantine them, instead of a red/green that hides the scope.

Data tests cannot be the first line of defense — by the time they run, the bad batch exists. They are the *detection net*: catch it before the index is served.

## 7. The complete Athar test portfolio

Mapping the skills map to test types:

| Criterion | Test type | Example assertion |
|---|---|---|
| Text/book/page never lost | integration + data | `r1.text == "النص الأصلي"` (byte-for-byte) |
| Reruns never duplicate | integration | second ingest reports `skipped_duplicates: 1` |
| 20 failure cases never return | regression | `KF-01..KF-20` all hold |
| Engine swap keeps rules | unit + contract (topic 36) | validation errors identical across engines |
| Producer schema stable | contract | required fields present, types right |

## 8. Best-practice checklist

| Practice | Payoff |
|---|---|
| One type per failure mode | no duplicate bets, clear diagnosis |
| Pure unit tests, run on save | instant feedback on rule changes |
| Hermetic integration (temp store) | wiring bugs caught without infra |
| Contract tests per boundary | cross-team drift fails in CI |
| Bugs become named regression cases | history cannot repeat silently |
| Data invariants post-ingest | corpus damage detected before serving |
| Byte-for-byte provenance assertions | citations cannot degrade |
| Golden fixtures as data files | cases survive refactors |
| Markers (`unit`, `regression`, `data`) | run the right tier at the right time |

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Only unit tests; wiring bugs reach prod | add integration tests per handoff |
| Only E2E tests; failures undiagnosable | add unit + integration tiers |
| Contract test asserts content not shape | keep it to required fields/types |
| Bug fixed without a test | regression rule: test first, fix second |
| Regression cases as inline strings | store as golden JSONL fixtures |
| Data test asserts a boolean | report violation lists for quarantine |
| Normalized text asserted | assert verbatim text for provenance |
| Network in "unit" tests | fake the boundary; unit tests run offline |
| Tests share a store | fresh temp store per test (hermetic) |

---

## Mastery Check

You can claim this topic when you can:

1. Write the byte-for-byte provenance test and run it against a modified pipeline that drops `text` — and see it fail.
2. Run the same ingest twice and prove no duplicates via the store's row count.
3. Add a 21st known-failure case as data and see it fail before the fix, pass after.
4. Write a contract test that fails when a producer drops a required field.
5. State, for each test type, one bug it catches that the others cannot.

---

## Next Steps

- Wire these markers into CI in `28-code-quality-tooling-lecture.md`.
- System-level contracts: `10-system-design/01-component-contracts/`.
- Data quality at ingestion scale: `04-databases/sqlalchemy/11-migrations-alembic/`.
