# Skills Mastery Map — Athar Mastery Criteria

> The anchor document for the `00-core-foundations/python/` module: the six
> professional skills (from the Athar skills table) mapped to every topic that
> teaches them, the Athar application, and the mastery evidence you must be
> able to produce. New topics built for this map are marked **[NEW]**.

---

## How to use this map

1. Pick a skill row. Work through its **Topics** in order.
2. Each topic is a directory with a runnable `.py` exercise (run with `--verify`),
   a detailed lecture, and a glossary.
3. Check yourself against the **Mastery evidence** column - it is the acceptance
   test for the skill, applied to a real Athar-style pipeline.
4. Prove it with the **Practice** challenge set (Bronze/Silver/Gold) linked in
   each section — Silver and Gold carry measured guards a naive solution fails.
5. The skill is *done* when you can produce the evidence, not when you have read
   the lectures.

---

## 1. Production Python — Python الإنتاجي

**What to learn:** data types, Unicode, iterators/generators, exceptions, typing,
asyncio, profiling, dependency management.

**Athar application:** write an importer that reads Arabic texts in batches
instead of loading them all into memory, and fails with a clear message on a
corrupt record.

**Mastery evidence:** processes a large file with bounded memory; one corrupt
record produces one error naming the line number and reason; valid records are
unaffected.

| Sub-skill | Topics | Notes |
|---|---|---|
| Data types & collections | `01-core-python/basics/07-data-types`, `13-lists`–`16-dictionaries`, `advanced/49-collections-toolkit` | foundations |
| **Unicode & Arabic text** | **[NEW]** `02-advanced-python/35-unicode-and-arabic-text` | normalization, harakat, presentation forms, digit folding, the batch importer |
| Iterators & generators | `02-advanced-python/02-generators`, `30-iterators-protocols-deep`, `01-core-python/functions/24-iterators` | lazy pipelines |
| Exceptions | `01-core-python/functions/30-try-except`, `advanced/47-exceptions-advanced` | typed errors, fail-loud policy |
| Typing | `02-advanced-python/05-type-hints`, `23-typing-advanced` | Protocols, generics |
| Asyncio | `02-advanced-python/04-async-await`, `22-asyncio-advanced` | concurrent I/O |
| Profiling & memory | `02-advanced-python/25-profiling-and-optimization`, `24-memory-and-gc`, `01-core-python/advanced/52-memory-and-performance` | measure first |
| Dependency management | `01-core-python/advanced/39-pip`, `40-virtualenv`, `02-advanced-python/27-packaging-and-distribution`, `39-poetry`, `40-uv` | environments, lockfiles |

**The importer pattern lives in [NEW] topic 35's section 9** — batch streaming,
typed `ImportRecordError` with line numbers, and the `on_error` quarantine hook.

**Practice:** [`02-advanced-python/challenges/35-unicode-and-arabic-text/`](02-advanced-python/challenges/35-unicode-and-arabic-text/) —
Bronze normalization, Silver O(n) dedup with a comparison budget, Gold
streaming import under an 8 MB `tracemalloc` ceiling.

---

## 2. Maintainable Code — كتابة كود قابل للصيانة

**What to learn:** separation of responsibilities, interfaces, dependency
injection, config, logging, code review.

**Athar application:** separate parser from normalizer from indexer from API;
never let an endpoint do everything.

**Mastery evidence:** you can replace the search engine without touching the
reference-validation rules (and the validator's tests pass unchanged).

| Sub-skill | Topics | Notes |
|---|---|---|
| **Separation of concerns, interfaces, DI, config, logging** | **[NEW]** `02-advanced-python/36-separation-of-concerns` | the layered pipeline, Protocols, composition root, frozen config, spy-double proof, engine-swap test |
| **Code review & refactoring** | **[NEW]** `02-advanced-python/37-code-review-and-refactoring` | review lenses, smell measurement, extract-method, strategy-over-conditional, lock tests, four-part comments |
| ABCs & patterns | `02-advanced-python/08-abc`, `20-patterns`, `26-design-patterns-advanced` | pattern vocabulary |
| Logging | `02-advanced-python/19-logging`, `01-core-python/advanced/44-logging` | library-grade logging |
| Config & CLI | `01-core-python/advanced/46-cli-and-config`, `05-web-frameworks/fastapi/50-configuration` | settings objects |
| Quality tooling | `02-advanced-python/28-code-quality-tooling` | ruff, mypy in CI |

**The engine-swap test lives in [NEW] topic 36's section 7** — identical
validation errors across two search backends is the mechanical proof.

**Practice:** [`02-advanced-python/challenges/36-separation-of-concerns/`](02-advanced-python/challenges/36-separation-of-concerns/) —
Bronze DI wiring, Silver spy-guarded call budgets (normalize once per record),
Gold a new engine with a structural decoupling proof.

**Practice:** [`02-advanced-python/challenges/20-patterns/`](02-advanced-python/challenges/20-patterns/) —
Bronze provider adapter, Silver comparison-budgeted observer bus, Gold
probe-budgeted strategy router.

---

## 3. Testing — الاختبارات

**What to learn:** unit, integration, contract, regression, and data tests.

**Athar application:** test that the original text, the book, and the page never
get lost through the pipeline.

**Mastery evidence:** rerunning the ingest never produces duplicates; 20 known
failure cases never return.

| Sub-skill | Topics | Notes |
|---|---|---|
| Unit testing | `02-advanced-python/18-unit-testing`, `01-core-python/advanced/45-testing-with-pytest` | pure, fast, offline |
| **Full test taxonomy** | **[NEW]** `02-advanced-python/38-test-strategy-contract-regression` | unit/integration/contract/regression/data in one pipeline; provenance test; idempotent rerun; golden known-failure cases |
| DB testing | `04-databases/sqlalchemy/09-testing-with-db` | hermetic temp stores |
| API testing | `05-web-frameworks/fastapi/20-testing`, `42-security-testing` | endpoint contracts |
| Testing style in practice | `PRACTICE_SPEC.md` (module root) | falsifiable guards, no wall-clock asserts |

**The provenance + idempotency + known-failure trio lives in [NEW] topic 38's
sections 2–5** — byte-for-byte text/book/page assertions, double-ingest row
count, and the `KF-01…` regression fixtures.

**Practice:** [`02-advanced-python/challenges/38-test-strategy-contract-regression/`](02-advanced-python/challenges/38-test-strategy-contract-regression/) —
Bronze invariant checker, Silver idempotent ingest under a comparison budget,
Gold the regression gate with mutation detection and exact call budgets. Also
[`02-advanced-python/challenges/37-code-review-and-refactoring/`](02-advanced-python/challenges/37-code-review-and-refactoring/)
for lock tests and structural budgets.

---

## 4. Databases — قواعد البيانات

**What to learn:** SQL, transactions, indexes, migrations, EXPLAIN, backups.

**Athar application:** make PostgreSQL the record of books, editions, and
permissions — not the vector DB — as the source of truth.

**Mastery evidence:** you can modify a book edition and rebuild the index without
losing the link to the source.

| Sub-skill | Topics | Notes |
|---|---|---|
| SQL | `04-databases/sql-fundamentals/` (14 topics), `sql-sqlite/` | DDL, DML, joins, windows |
| Transactions | `sql-fundamentals/11-transactions`, `postgresql/05-transactions-mvcc` | ACID, isolation |
| Indexes & EXPLAIN | `sql-fundamentals/10-indexes-and-plans`, `14-query-optimization`, `postgresql/04-indexes-postgres` | prove plans changed |
| **Migrations** | **[NEW]** `04-databases/sqlalchemy/11-migrations-alembic` | revision chains, expand-backfill-contract, idempotent data migrations, lineage-preserving edits |
| **Backups** | **[NEW]** `04-databases/postgresql/07-backup-and-restore` | verify-by-restore, RPO/RTO, PITR, 3-2-1, derived index excluded |
| ORM & repositories | `sqlalchemy/01`–`10` | models, sessions, repository pattern |
| Vector stores | `vector-stores/` (8 topics) | embeddings, hybrid search |

**The lineage criterion lives in [NEW] topic 11's section 5** (migrations) and
**[NEW] backup topic's section 5** (index is derived, rebuilt not restored).

**Practice:** [`04-databases/sqlalchemy/challenges/11-migrations-alembic/`](04-databases/sqlalchemy/challenges/11-migrations-alembic/) —
Bronze revision chains, Silver expand-backfill-contract with mixed-version
safety, Gold a lineage-preserving rebuild under statement and memory budgets.
And [`04-databases/postgresql/challenges/07-backup-and-restore/`](04-databases/postgresql/challenges/07-backup-and-restore/) —
verify-by-restore with content-drift detection and point-in-time recovery.

---

## 5. Backend and APIs — Backend وAPIs

**What to learn:** HTTP, request validation, auth, pagination, timeouts, rate
limits, async I/O.

**Athar application:** build `/search` and `/sources/{id}` before `/answer`.

**Mastery evidence:** a documented, tested API; the user never sees a source they
are not authorized to see.

| Sub-skill | Topics | Notes |
|---|---|---|
| HTTP & routing | `05-web-frameworks/fastapi/01`–`08` | request/response lifecycle |
| Request validation | `05-request-body`, `26-pydantic-v2-deep` | schemas at the boundary |
| Auth & authz | `12-security`, `13-jwt-auth`, `14-oauth2`, `38-auth-deep`, `39-oauth2-oidc`, `40-authorization` | never leak unauthorized sources |
| Pagination & filtering | `28-pagination-and-filtering` | bounded responses |
| Timeouts & resilience | `47-resilience-patterns`, `30-idempotency-and-retries` | bounded waits, retries |
| Rate limits & API security | `41-api-security`, `42-security-testing`, `04-databases/redis/04-rate-limiting` | per-identity limits |
| Async I/O | `21-async`, `32-async-endpoints-deep`, `33-database-async` | concurrent handling |
| Docs & clients | `31-openapi-and-clients`, `27-api-versioning` | OpenAPI as contract |

*(Backend was the best-covered skill; the gaps it had — timeout/rate-limit
discipline and authorization-as-contract — are reinforced by [NEW] system-design
topics 01 and 04.)*

---

## 6. System Design — System design

**What to learn:** component contracts, queues, caching, consistency, failure
modes, ADRs.

**Athar application:** draw the text journey from source to index, and the
question journey to the answer.

**Mastery evidence:** you can explain what happens if a worker fails or the
index becomes older than the source.

| Sub-skill | Topics | Notes |
|---|---|---|
| **Component contracts** | **[NEW]** `10-system-design/01-component-contracts` | four-part contracts, compatibility classes, migration path, system-level contract tests |
| **Queues & workflows** | **[NEW]** `10-system-design/02-queues-and-workflows` | job lifecycle, at-least-once, idempotency, backoff, DLQ, bounded workers |
| **Consistency & staleness** | **[NEW]** `10-system-design/03-consistency-and-staleness` | source-of-truth vs derived, drift/version stamps, cache TTL/invalidation, read-your-writes, staleness state machine |
| **Failure modes & resilience** | **[NEW]** `10-system-design/04-failure-modes-and-resilience` | failure taxonomy, FMEA-lite, timeouts, cascading failure, bulkheads, degradation ladder |
| **ADRs** | **[NEW]** `10-system-design/05-architecture-decision-records` | ADR format, threshold test, status lifecycle, enforcement links |
| Caching (implementation) | `05-web-frameworks/fastapi/34-caching-strategies`, `04-databases/redis/03-caching-patterns` | cache mechanics |
| Queues (implementation) | `fastapi/35-background-jobs`, `redis/05-pubsub-and-streams`, `redis/07-session-and-queues` | real brokers |
| Resilience (implementation) | `fastapi/47-resilience-patterns` | tenacity, circuit breakers |
| End-to-end architecture | `08-mlops/09-pipeline-orchestration`, `08-mlops/16-case-study-e2e`, `09-genai/23-case-study-rag-service` | full pipelines |

**The mastery answer lives in [NEW] topic 04's section 7** (designed stories for
worker failure and stale index) and **topic 03's section 7** (the staleness
state machine + rebuild path).

**Practice:** all five sets in [`10-system-design/challenges/`](10-system-design/challenges/) —
contracts with a rolling-upgrade simulation, queues with retry/DLQ accounting,
consistency with versioned apply, resilience with bulkheads and a degradation
ladder, and the ADR lifecycle with an immutability guard.

---

## Cross-skill capstone checklist

When you can do all of the following against a real or simulated Athar corpus,
the map is complete:

1. **Import** a large Arabic corpus in batches; quarantine one corrupt record
   with its line number; memory stays bounded. (Skill 1, topic 35)
2. **Swap the search engine** and the reference-validation rules and their tests
   are untouched. (Skill 2, topic 36)
3. **Prove** text/book/page survive byte-for-byte; reruns produce zero
   duplicates; the known-failure suite holds. (Skill 3, topic 38)
4. **Migrate** the schema (add `edition`), edit a book, rebuild the index —
   every `source_ref` still resolves. (Skill 4, topics 11 + backup)
5. **Serve** `/search` and `/sources/{id}` with authz; unauthorized sources are
   never visible; the API is documented and tested. (Skill 5, fastapi track)
6. **Explain** — with detections and runbooks — what happens when a worker dies
   mid-job and when the index drifts behind the source. (Skill 6, topics 02–04)
7. **Record** the source-of-truth decision as an accepted ADR with its
   enforcement link. (Skill 6, topic 05)

---

*Created for the Athar mastery criteria. All [NEW] topics ship with runnable,
self-verifying exercises (`--verify`) in the established three-file format.*
