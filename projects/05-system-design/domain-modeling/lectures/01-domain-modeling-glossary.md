# Glossary: Domain-Driven Design and Domain Modeling

Quick-reference table of every term used in Lecture 01, followed by detailed definitions with examples drawn from this repository — Athar's contracts (`projects/04-ai-engineering/athar-lab/contracts.py`), the entity-resolution layer (`projects/04-ai-engineering/arabic-nlp/08-arabic-entity-resolution/`), DevMate's boundary schemas (`projects/04-ai-engineering/devmate/src/devmate/llm/schemas.py`), and the audit exercise (`projects/05-system-design/domain-modeling/exercises/01-domain-modeling.py`). Where a rule is enforced by the exercise, the rule code is named.

## Quick Reference Table

| Term | Definition | Lecture section |
|------|------------|-----------------|
| Aggregate | Cluster of objects treated as one unit for data changes, with one root | 4 |
| Aggregate Root | The only member of an aggregate outside code may reference; the transaction boundary | 4, 5 |
| Anemic Domain Model | A model of getters and setters that enforces no invariants; business rules live elsewhere | 10 |
| Anti-Corruption Layer | Translation boundary so one context's model never pollutes another's | 8 |
| Bounded Context | Explicit boundary within which a ubiquitous language is consistent | 8 |
| Command | An instruction to do something; the counterpart of an event | 7 |
| Consistency Boundary | The scope inside which invariants hold atomically — one aggregate | 4, 13 |
| Context Map | The named relationships between bounded contexts | 8 |
| Conformist | Context relationship where one side adopts the other's model as-is | 8 |
| Customer-Supplier | Context relationship where upstream supplies, downstream's needs negotiate the contract | 8 |
| Domain | The problem space the software addresses — the expert's world | 1 |
| Domain Event | Past-tense record of something that happened in the domain | 7 |
| Domain Layer | The layer holding entities, value objects, specifications, domain services | 11 |
| Domain Model | Code that represents the business concepts and rules | 1 |
| Domain Service | Stateless domain operation that does not belong to one entity | 9 |
| DTO (Data Transfer Object) | Boundary carrier shaped for the wire, owned by neither domain nor storage | 11 |
| Entity | Thing with identity that survives attribute change; equality by identity | 2 |
| Equality Semantics | What "same" means: by identity (entity) or by attributes (value object) | 2 |
| Eventual Consistency | Cross-aggregate convergence after a bounded, published delay | 7, 13 |
| Factory | Function or method that produces a valid aggregate, applying all invariants | 6 |
| Frozen Dataclass | Immutable, hashable, attribute-equality Python record; the value-object default | 2 |
| Identity | What makes a thing the same thing through change | 2 |
| Identity Field | An id attribute; on a value object it signals an entity in disguise (DDD002) | 2 |
| Invariant | Rule that must hold for every instance at every stable point | 4, 5 |
| Intention-Revealing Method | State-change method named for the domain rule it enforces, not the field it writes | 5 |
| Layered Architecture | UI / application / domain / infrastructure, with the domain at the center | 11 |
| Natural Key | Id derived from domain identity (content hash, book:page:index) | 12 |
| Placeholder Name | `DataItem`, `Manager`, `Helper` — vocabulary that hides the concept (DDD007) | 1 |
| Repository | One aggregate root's collection interface; intent-revealing queries only | 6 |
| Shared Kernel | Declared type co-owned by two bounded contexts; changes need both sides' consent | 8 |
| Specification | Composable domain rule object: `and`, `or`, `not` without boolean spaghetti | 9 |
| Synthetic Key | System-issued id (UUID, sequence) used when natural identity is unstable or unknown | 12 |
| Transaction Boundary | The unit of atomic change; in DDD, exactly one aggregate | 4, 13 |
| Two-Text Discipline | Athar's rule: every passage keeps verbatim original plus normalized searchable | 3 |
| Ubiquitous Language | One rigorously shared vocabulary between experts and code | 1 |
| Value Object | Immutable attribute bundle with no identity; equality by all attributes | 2, 3 |

## Detailed Definitions

### Ubiquitous Language

The single vocabulary domain experts and developers use for the model — the same words in conversation, class names, method names, and commits. It functions as an interface: when a name changes, every implementation changes with it, and drift between the spoken word and the code word is an invisible defect.

The audit's test is mechanical. **DDD007** flags placeholder names:

```text
DDD007  warning   Type 'DataItem' violates the ubiquitous language: the
                  domain expert says 'a narration', not 'a data item'.
```

Athar's real vocabulary — passage, narration, isnad, narrator, book, section — is the antidote: every type in the GOOD pack is a word a hadith scholar would recognize.

### Entity

A thing with identity that is the same thing through change. Two entities are equal only when their identities are equal; their attributes may differ wildly. In Athar: a `Passage` with `passage_id = "b1:p12:0"` is one passage whether or not its searchable text was re-normalized last week.

```python
# The equality contract, made explicit (Lecture 01, section 2)
@dataclass(eq=False)
class Narration:
    narration_id: str
    text: str

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Narration) and self.narration_id == other.narration_id
```

**DDD003** fires when an entity compares by attributes instead — the moment a display field changes, caches, dedupe sets, and `in` checks built on that equality all break.

### Value Object

An immutable bundle of attributes with no identity: it is its attributes or it is nothing. Two `SourceLocation(book_id="b1", page=12, source_version="v1")` values are the same location, full stop.

**FACT:** Athar's value objects are frozen dataclasses with construction-time invariants (`projects/04-ai-engineering/athar-lab/contracts.py:33-46`):

```python
@dataclass(frozen=True)
class SourceLocation:
    book_id: str
    page: int
    source_version: str

    def __post_init__(self) -> None:
        if not self.book_id:
            raise ValueError("book_id must not be empty")
        if self.page < 1:
            raise ValueError(f"page must be >= 1, got {self.page}")
```

Frozen gives attribute equality, immutability, and hashability in one mechanism. **DDD002** fires when a value object declares an identity field — it is an entity in disguise, and the model should say so.

### Identity

What makes a thing the same thing through change. Entities carry it; value objects do not. Identity is also an operational choice — natural versus synthetic — with ingestion and dedupe consequences (see Natural Key, Synthetic Key).

The rule that closes the loop: entities compare by identity, value objects by attributes. Confusing the two directions produces DDD002 and DDD003, the audit's identity pair.

### Invariant

A rule that must hold for every instance at every stable point in time: "page ≥ 1," "a narration belongs to exactly one passage," "the alias table reflects every committed merge." DDD's placement rule is absolute: the invariant is declared on the aggregate root and enforced by the root's state-change methods.

The GOOD pack's `Passage` declares four — `page_at_least_one`, `both_texts_present`, `narration_belongs_to_exactly_one_passage`, `isnad_is_an_ordered_chain` — all with `scope: aggregate`, all enforced in the root's operations. **DDD001** fires when a root enforces none (setters, empty invariants); **DDD004** fires when one is parked on a member.

### Aggregate Root

The single entry point to an aggregate. Outside code holds roots and ids, never members. The root enforces the invariants, and the aggregate is the transaction boundary: one unit of atomic change.

**FACT:** the exercise's demo drives the boundary directly:

```text
construct page 0      -> rejected: page must be >= 1, got 0
attach n-1 to p1      -> ok (1 narration)
attach n-1 to p2      -> rejected: narration n-1 already belongs to passage b1:p3:0
root exposes a setter -> False (DDD001 finds none)
```

The second rejection is the boundary working: a narration attached elsewhere cannot silently appear under a new passage.

### Aggregate

The cluster itself — root plus the entities and value objects reachable only through it, loaded and saved as a whole. Size rule: as small as the invariants allow, and no smaller — cross-aggregate invariants cannot be protected by one transaction anyway, so pulling neighbors in only couples what must stay independent.

Athar's citation aggregate: `Passage` (root) containing `Narration` and `Isnad` members; references outward by id (`book_id`), never by object graph.

### Anemic Domain Model

A model that looks like a model and behaves like a bag of getters and setters: data holders with public fields, business rules living in services that set those fields freely. It is the audit's DDD001 signature — setters on the root, no invariants — and its cost is that no single place can guarantee a valid state.

The counterpoint is proportionality: a genuine CRUD service does not need rich methods. The failure mode is the middle state — "models" that are really DTOs while the rules accrete in five controllers.

### DTO (Data Transfer Object)

A boundary carrier shaped for the wire, owned by neither the domain nor the database. Necessary everywhere; a problem only when it becomes the only model.

**FACT:** DevMate's API boundary is a clean DTO set (`src/devmate/llm/schemas.py:10-126`): `LLMRequest`, `RAGRequest`, `AskResponse`, `IngestResponse`, all Pydantic `BaseModel`s. Pydantic validation at the edge is right; the domain layer translates between the DTO and whatever the services actually decide.

### Domain Event

A past-tense record of something that happened: `NarrationLinked`, `PassageIngested`, `EntityMerged`, `MergeDecisionCommitted`. Not an instruction — a command says "do this"; an event says "this happened." That distinction is load-bearing on at-least-once transports: a command-shaped name tells every redelivery to perform the action again (**DDD006**).

### Factory

The function or method that produces a valid aggregate from raw input, applying every invariant on the way. **FACT:** Athar's `make_passage` (`contracts.py:90-110`) composes the id from domain identity, derives the searchable text (never normalizing in place of the original), and lets `SourceLocation.__post_init__` run its checks — one call, no invalid `Passage` possible.

### Repository

One aggregate root's collection interface — the illusion of an in-memory collection, persisted behind it. Two rules: one repository per aggregate root, and intent-revealing queries.

```text
DDD009  warning   Repository 'PassageRepo' method 'find_by' takes a raw
                  filter shape instead of intent ... name the query after
                  intent (passages_of_book).
```

The GOOD pack's `PassageRepository.passages_of_book(book_id)` and `CanonicalEntityRepository.pending_merge_candidates()` are the shape; a `find_by(filters: dict)` is table access wearing a repository's name.

### Specification

A domain rule packaged as an object that answers "is this candidate acceptable?" and composes with `and`, `or`, `not`. **FACT:** the exercise's `MeetsScore` and `NotVetoed` compose the resolution policy:

```text
auto_merge = (score >= 0.92) AND (veto is absent)
review queue = NOT auto_merge
```

The review queue is the inversion of one policy, not a second copy — the partition of candidates is provable rather than hopeful.

### Bounded Context

An explicit boundary within which one ubiquitous language holds. Outside it, the same word may mean something different — "document" is Athar's book identity (`athar-lab/contracts.py:49-56`) and DevMate's chunk record (`ingest/chunker.py:15-29`); two models, one word, two contexts. **FACT:** both types exist in this repository under the same name, deliberately.

### Shared Kernel

A declared boundary relationship: both contexts co-own a deliberately minimal type, and changes require both sides' consent. **FACT:** Athar's `EntityId` is the working example — catalog, citation, and resolution all speak it, and the GOOD pack declares `boundary_relationship: "shared-kernel"`. **DDD008** fires when a type spans contexts with no declaration; the undeclared version is a silent coupling that breaks one side when the other changes.

### Anti-Corruption Layer

The other declared boundary relationship: one context translates at its edge so its model is never polluted by the other's. Use it when one side must not bend — a vendor API, a legacy schema — or when adopting the foreign model outright would leak its accidents into your ubiquitous language.

### Consistency Boundary

The scope inside which invariants hold atomically — in DDD, exactly one aggregate. Cross-aggregate rules cannot live inside it; they move to events and eventual consistency with a bounded convergence window (Lecture 01, sections 7 and 13). **DDD005** fires when a `scope: cross-aggregate` invariant declares `mechanism: single-transaction`, because two roots cannot share a transaction without becoming one aggregate.

### Natural Key

An id derived from the domain's own identity. **FACT:** both patterns in this repo state their intent. Athar's `make_passage` composes `f"{book_id}:p{page}:{passage_index}"` (`contracts.py:101`); DevMate's chunker hashes `f"{source}:{position}:{content[:100]}"` to 32 hex (`ingest/chunker.py:40-49`). Re-running the pipeline upserts the same keys instead of duplicating — ingestion idempotency for free.

### Synthetic Key

A system-issued id (UUID, sequence) used when the natural identity is unstable, unknown at creation, or when two look-alikes must be tracked separately — which is exactly the situation entity resolution exists for. Two surface forms of a narrator's name merge into one canonical `EntityId`; the merge is recorded, not assumed, because the ids were synthetic enough to keep them distinct until a decision said otherwise.

### Two-Text Discipline

Athar's domain rule: every passage keeps its verbatim `original` for display and citation, plus a normalized `searchable` form for matching — and the original is never normalized in place. **FACT:** enforced in `Passage.__post_init__` (`contracts.py:69-75`: both texts non-empty) and applied by `make_passage`, which derives `searchable` via `normalize_arabic(original)`. Losing either text is a correctness bug; the contracts make losing one impossible rather than merely discouraged.

### Intention-Revealing Method

A state-change method named for the domain rule it enforces: `attach_narration`, `retire_edition`, `record_alias`, `commit` — not `set_passage_id`, `update_field`. The GOOD pack's roots expose only operations; the BAD pack's `Passage` exposes `set_book_id`, `set_page`, `set_original` and declares no invariants (DDD001). The method name is where the rule becomes visible at the call site.

### Layered Architecture

The canonical DDD placement: UI on top, application services coordinating, the domain layer holding the model, infrastructure beneath. The rule that makes it work: dependencies point inward — the domain layer depends on nothing outside itself, and everything else depends on it. The lecture's DTO discipline (section 11) is this rule at the boundary: wire schemas translate in and out; they never become the model the domain layer speaks.

## Summary

The table is the map; the definitions are the terrain. Five families run through Lecture 01 — language and naming, identity and equality, aggregates and invariants, events and consistency boundaries, contexts and their declared relationships — and each has one job. The exercise's nine rules (DDD001–DDD009) are their mechanical shadows: every definition above has a rule that fires when the definition is broken. Treat the rules as the backlog and the definitions as the spec they enforce.
