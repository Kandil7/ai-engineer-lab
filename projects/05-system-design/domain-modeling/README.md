# Domain-Driven Design — Domain Modeling

The ubiquitous language, entities and value objects, aggregates with roots
that enforce their invariants, repositories and factories, past-tense
domain events with idempotent consumers, bounded contexts with declared
shared kernels, and specifications — modeled on the Athar
Islamic-knowledge corpus and its entity-resolution layer, then audited by
nine executable rules (DDD001–DDD009). Every FACT claim below was verified
at the cited path before this track was written.

---

## Architecture: Where the Rules Live

```
            domain expert's words
                   │  (ubiquitous language)
                   ▼
        ┌─────────────────────┐
        │   bounded context   │◄──── shared kernel / ACL declared
        └──────────┬──────────┘        (DDD008)
                   │
        ┌──────────▼──────────┐
        │  aggregate root     │──── intention-revealing methods
        │  (Passage, Book,    │     enforce every invariant
        │   Narrator, ...)    │     (DDD001, DDD004)
        └────┬──────────┬─────┘
             │ contains │ references by id
      ┌──────▼───┐  ┌───▼────────────┐
      │ members  │  │ other roots    │── domain event (past tense,
      │ (no in-  │  │ via repository │   idempotent consumer)
      │ variants)│  │ (intent-named) │   (DDD005, DDD006, DDD009)
      └──────────┘  └────────────────┘

  value objects: immutable, attribute equality, invariants at
  construction (frozen dataclass + __post_init__)
```

Each box blocks a different modeling failure. The lecture teaches why
omitting any of them moves the rules into callers, controllers, or hope.

---

## Track Contents

| File | What it covers |
|------|----------------|
| `lectures/01-domain-modeling-lecture.md` | 15 sections: ubiquitous language, entities vs value objects, parse-don't-validate construction, aggregates and roots, invariant placement, factories and repositories, domain events, bounded contexts and context mapping, specifications, the anemic-model anti-pattern, DTO discipline, identity keys, cross-aggregate consistency, proportionality, and the narrator-merge worked scenario |
| `lectures/01-domain-modeling-glossary.md` | 36-term quick-reference table plus detailed definitions, each with code from Athar, DevMate, or the audit exercise |
| `quizzes/01-domain-modeling-quiz.md` | 15 questions (5 Easy, 7 Medium, 3 Hard) with inline answers and explanations, score tracking, answer key |
| `exercises/01-domain-modeling.py` | Offline rule engine: 9 DDD rules over a model description (BAD trips all 9, GOOD raises zero) plus runnable components — composable specifications, an aggregate root enforcing invariants at the boundary, an idempotent event consumer |
| `README.md` | This page |

---

## What Is Grounded (FACT)

Verified at the cited paths before this track was written:

- **Athar's contracts are the worked value objects and aggregate:**
  `SourceLocation` is a frozen dataclass with construction-time invariants
  (`projects/04-ai-engineering/athar-lab/contracts.py:33-46`);
  `Passage` enforces the two-text discipline in `__post_init__`
  (`contracts.py:69-75`); `make_passage` is the factory applying it all
  from raw page text (`contracts.py:90-110`), composing a natural id
  `book_id:pN:index` (`contracts.py:101`).
- **Entity resolution supplies the cross-context model:** `EntityId`,
  `MergeCandidate`, `MergeDecision`, canonical ids, and the alias table
  are taught in `projects/04-ai-engineering/arabic-nlp/08-arabic-entity-resolution/`
  (lecture sections 6–9); this track models them as aggregates and
  events rather than re-teaching resolution.
- **DevMate's boundary is DTOs, not a model:** the Pydantic set
  `LLMRequest`/`RAGRequest`/`AskResponse`/`IngestResponse` lives at
  `projects/04-ai-engineering/devmate/src/devmate/llm/schemas.py:10-126`;
  the chunker's `Document` pipeline record with a deterministic md5
  natural key is at `ingest/chunker.py:15-29` and `:40-49`. Neither is a
  domain model; the lecture uses both to teach where the domain layer
  would sit.
- **The audit is executable and deterministic:** the exercise's BAD pack
  trips all nine rules (5 critical, 4 warning) and the GOOD pack raises
  zero; reruns are identical, the demo needs no network, and file mode
  accepts a model description as JSON (BOM-safe).

Sources: the DDD literature this lecture operationalizes is Eric Evans,
*Domain-Driven Design: Tackling Complexity in the Heart of Software*
(2003), and Vaughn Vernon, *Domain-Driven Design Distilled* (2013) —
named as the canon, not vendored. No `source-index` entry exists for
either book yet; the repo-grounded claims above are the verifiable half.

---

## Complements (Not Duplicates)

This track owns **model shape and rule placement**. Adjacent territory
already taught elsewhere:

- `system-design.contracts` (knowledge-registry) — four-part component
  contracts with compatibility and migration:
  `projects/00-core-foundations/python/10-system-design/01-component-contracts`.
  Interface contracts between components; this track's contracts are the
  invariants *inside* one component's domain layer.
- `arabic-nlp.*` entity resolution
  (`projects/04-ai-engineering/arabic-nlp/08-arabic-entity-resolution/`) —
  matching, scoring, canonization, and merge mechanics. This track takes
  its `Narrator`/`MergeDecision` types as modeling input and does not
  repeat the resolution algorithm.
- The Reliability track (`projects/06-devops/reliability/`) —
  idempotency keys, outboxes, and DLQs as *transport* mechanics. This
  track's domain events sit on that transport; the consumer half
  demonstrated here (`IdempotentConsumer`) is the modeling-side
  complement of REL006.
- `system-design.failure-modes` — failure taxonomy and runbooks;
  this track's failures are modeling defects (DDD001–DDD009) that the
  audit catches before runtime.

---

## Verification

Run from the repository root:

```powershell
python -m py_compile projects\05-system-design\domain-modeling\exercises\01-domain-modeling.py
python projects\05-system-design\domain-modeling\exercises\01-domain-modeling.py
powershell -NoProfile -ExecutionPolicy Bypass -File tests\repo-structure\validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tests\knowledge\validate.ps1
```

Expected: compile exits 0; the demo exits 0 with the BAD pack tripping all
9 DDD rules (5 critical, 4 warning) and the GOOD pack raising zero
findings; both validators exit 0. The exercise is stdlib-only, offline,
and deterministic — reruns are identical.

---

*AI Engineer Lab — System Design track, domain-modeling lane.*
