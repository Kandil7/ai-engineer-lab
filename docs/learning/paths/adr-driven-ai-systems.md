# Learning Path: ADR-Driven AI Systems Engineering

**Last updated:** 2026-10-14

**Goal:** build engineering judgment for designing, building, and operating AI systems.
Design patterns are learned as decisions that solved a real problem inside one project,
never as a memorized catalogue. Every decision is recorded as an ADR, and the ADR log is
the backbone of the learning rather than an afterthought.

**Primary project:** `projects/04-ai-engineering/devmate`
**Application target:** Athar, the Arabic AI platform (external repo `Athar-Lab`)

---

## Why decisions instead of a pattern list

A pattern name is not knowledge. "We use Adapter because the sources differ" becomes
knowledge only when you can also state what you rejected, what the choice cost, and what
would make you reverse it. The ADR format forces all three. See `templates/adr.template.md`
and the live log in `docs/decisions/`.

The rule that governs this entire path: **do not advance to the next layer before the
current one has produced a runnable artifact.** A layer you cannot run is a layer you
have only read about.

This path is complementary to `docs/learning/paths/system-design.md`, which covers
distributed infrastructure (scaling, caching, queues, microservices). This path covers
application architecture, design decisions, and the deterministic/probabilistic split
that is specific to AI systems.

---

## Milestones

### 1. Layer 1: Programming Fundamentals (Week 1)

The foundation that makes the rest readable, testable, and extendable.

- Type hints and `typing`: `Optional`, `Literal`, `Protocol`, `TypeVar`, `Generic`, `Annotated`
- Dataclasses versus Pydantic, and when each is the right tool
- A custom exception hierarchy instead of bare `Exception`
- Context managers (`with`) for every resource that must be released
- Iterators and generators, especially for streaming and large documents
- Concurrency: `asyncio`, `ThreadPoolExecutor`, `ProcessPoolExecutor`
- Testing: pytest fixtures, parametrize, mocks, integration tests
- Packaging: `pyproject.toml`, entry points, dependency groups
- Structured logging: `structlog`, or `logging` with a JSON formatter
- Configuration: `.env`, `pydantic-settings`, layered configs

**Module contract.** Every module must answer three questions: what are its inputs, what
are its outputs, and what side effects are permitted. A `chunk_document()` function should
be near-pure: take a `Document`, return `list[Chunk]`, touch neither the database nor Qdrant.

**Artifact:** one module under `projects/00-core-foundations/python/` with a typed public
surface, a custom exception, and a passing test.

### 2. Layer 2: Clean Code and SOLID (Week 2)

- Names describe intent, not implementation
- One function, one responsibility
- No bare dictionaries passed between layers; pass models
- No mixing I/O with business logic
- Business logic is never duplicated; it lives in a service or domain function
- Side effects are declared and visible: database, network, filesystem, LLM call
- Every module has exactly one reason to change

| Principle | Wrong | Right |
| --- | --- | --- |
| Single Responsibility | One service that scrapes, cleans, writes to the DB, and embeds | Separate fetcher, cleaner, repository, embedder |
| Open/Closed | `if source == "x": ... elif source == "y": ...` | A `SourceAdapter` protocol with one implementation per source |
| Liskov Substitution | An adapter raises an unexpected exception | Every adapter returns the same `RawDocument` contract |
| Interface Segregation | One huge interface for every service | Separate `Fetcher`, `Parser`, `Embedder`, `Retriever` |
| Dependency Inversion | A service constructs its own client | A service receives a `VectorStore` protocol |

**Artifact:** refactor one existing DevMate module so the business logic is testable with
the I/O faked, and record what you rejected in an ADR.

### 3. Layer 3: Hexagonal Architecture, Ports and Adapters (Week 3)

Chosen over pure Clean Architecture because it is practical and directly applicable to AI
systems. The layering:

```text
interfaces   FastAPI routes, CLI, workers
application  use cases and orchestration
domain       entities and business rules, pure
infrastructure  database, Qdrant, vLLM, MinIO, external APIs
```

Dependency direction: `interfaces -> application -> domain`, with `infrastructure`
implementing the ports that `application` declares.

The domain knows nothing about Qdrant, vLLM, or FastAPI. The application knows the use
case but not the implementation details. The infrastructure implements the ports.

**Artifact:** one use case in DevMate expressed behind a port, with the real adapter and a
fake adapter both satisfying it under the same contract test.

### 4. Layer 4: Design Patterns as Decisions (Week 4)

Only the patterns that actually appear in this stack. Each one earns its place by a
problem you have already hit.

| Pattern | Use it when | Instance here |
| --- | --- | --- |
| Repository | Isolating persistence | Document and chunk repositories |
| Adapter | Unifying different sources | Shamela, PDF, YouTube sources |
| Strategy | Swapping an algorithm without changing callers | Dense, hybrid, and graph retrievers |
| Factory | Building objects from config | `create_vector_store(settings)` |
| Builder | Assembling a complex request | Retrieval request builder |
| Pipeline / Chain | Ordered stages | clean, chunk, embed, index |
| Template Method | Fixed steps, varying details | Base ingestion pipeline |
| Observer / Events | Reacting to an occurrence | `DocumentIngested` triggers indexing and evaluation |
| Circuit Breaker | Shielding from a failing external service | LLM API or embedding service |
| Retry with backoff | Transient failure | Qdrant or a model download |
| Unit of Work | Coordinating a transaction | Saving a document with its chunks and embeddings |
| Specification | Complex filtering | Retrieval filters by date, source, topic |
| Facade | Simplifying a subsystem | `RAGService` hiding retrieval, rerank, generation |
| Proxy / Cache | Cutting cost and latency | Cached embeddings and responses |
| Mapper | Separating DTO from domain | API model to domain entity |

**The rule for this layer:** never apply a pattern speculatively. The trigger is a real
second use case or a real third variation, not the anticipation of one. A pattern with
one caller is speculative generality.

**Artifact:** one pattern applied with an ADR that names the alternative you rejected and
the cost you accepted.

### 5. Layer 5: AI and LLM System Design (Week 5-6)

This is where AI systems diverge from ordinary backends: they contain probabilistic
components.

```text
Deterministic layer   auth, permissions, validation, storage, workflows, citations
Probabilistic layer   query understanding, retrieval ranking, generation, classification
```

Never make the LLM responsible for logic that must be deterministic. Whether a user may
see a book is an authorization decision, not a generation decision.

**RAG pipeline shape:**

```text
Query -> Validate -> Rewrite / Expand -> Hard Metadata Filters
      -> Hybrid Retrieval -> Rerank -> Context Construction
      -> Prompt Assembly -> LLM Generation -> Citation Verification
      -> Response -> Trace + Evaluation
```

**Decisions to record, with a starting recommendation each:**

| Decision | Recommendation |
| --- | --- |
| Model access | Local first, cloud fallback for hard cases |
| Prompt management | Files plus versioning plus a registry, never hardcoded |
| Structured output | Pydantic plus validation plus retry |
| Context construction | Hierarchical, following document structure, not top-k alone |
| Citations | IDs in the context plus post-generation verification |
| Guardrails | Layered: rules first, then a classifier |
| Evaluation | Offline, online, and human; start offline |
| Cost control | Caching, model routing, batching |

**Artifact:** one retrieval change in DevMate, measured before and after on the frozen
golden set.

### 6. Layer 6: Evaluation Discipline (Week 7)

- Every real bug becomes a regression test
- Every prompt change passes the eval set
- Every retrieval change is measured with Recall@k and MRR
- Every model change is measured on the same frozen eval set
- An "improvement" without before and after numbers is not accepted

Live example already in this repo: ADR-0009 records that the offline harness reported
Hit@5 1.000 from fixtures while the first live baseline measured 0.900, and it names the
two indexing defects behind the gap. That is the discipline this milestone teaches.

**Artifact:** a live eval report under `evaluations/rag/reports/` plus an ADR citing the
measured numbers.

### 7. Layer 7: Production and LLMOps (Week 8)

- Health checks, readiness and liveness probes
- Structured logging with request IDs
- Metrics: latency, error rate, token usage, retrieval hit rate
- Tracing from request to retrieved chunks to LLM response
- Rate limiting and authentication
- Secrets management, never in code
- Backups and disaster recovery
- Alembic migrations for PostgreSQL
- CI: lint, type check, tests, eval smoke test, Docker build
- Deployment: Docker Compose first, Kubernetes only when required

**Artifact:** one service deployable from a clean machine with a health check that an
operator can trust.

---

## The per-feature cycle

Do not start writing code at random. For every feature, run this cycle:

1. Write the user story
2. Write the acceptance criteria
3. Draw the data flow
4. Name the domain models
5. Name the interfaces and ports
6. Write the failing tests first
7. Implement the minimum
8. Run the tests
9. Add observability
10. Write the ADR
11. Review the code as if someone else wrote it

---

## Ten questions before any code

1. What is the real problem?
2. What is the simplest solution that satisfies it?
3. What will change around this system?
4. What must be deterministic?
5. What may be probabilistic?
6. What will be hard to change later?
7. How do I know the solution worked?
8. What fails first under load?
9. What is the data contract?
10. What is the failure mode?

---

## The daily exercise

After every session, write into `docs/decisions/` or `docs/learning/`:

- What did I build?
- Why did I choose this solution?
- What were the alternatives?
- What are the tradeoffs?
- How did I prove it works?
- What would I change if the requirements changed?

This exercise is worth more than another course, because it converts knowledge into
engineering judgment.

---

## Definition of done

A project is not done when a demo runs. It is done when:

- It runs from a clean machine
- Every new source enters through an adapter
- Every chunk and embedding carries a version
- Every answer has verifiable citations
- Every change passes the eval suite
- Every important decision has an ADR
- Every failure has a log, a metric, and an alert
- The system can be explained without opening the code

---

## Links

- Related paths: `docs/learning/paths/system-design.md`,
  `docs/learning/paths/rag-qdrant.md`, `docs/learning/paths/fastapi-ai-services.md`
- ADR practice: `projects/00-core-foundations/python/10-system-design/05-architecture-decision-records`
- ADR template: `templates/adr.template.md`
- Live decision log: `docs/decisions/`
- Worked example of measured discipline:
  `docs/decisions/0009-fix-indexing-scope-before-chunk-tuning.md`
- Active project: `projects/04-ai-engineering/devmate`
