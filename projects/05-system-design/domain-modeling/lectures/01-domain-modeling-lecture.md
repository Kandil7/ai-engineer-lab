# Lecture 01: Domain-Driven Design and Domain Modeling

## Topic Overview

Every system that outgrows CRUD eventually hits the same wall: the database
tables were never the model, and the business rules that were "temporarily"
scattered across controllers, scripts, and SQL triggers can no longer be
found, let alone changed safely. Domain-Driven Design is the discipline of
putting the model back at the center: one ubiquitous language shared with
domain experts, entities and value objects with honest equality semantics,
aggregates as consistency boundaries whose roots enforce every invariant,
domain events for the rules that span aggregates, and bounded contexts so
two teams never silently share a type they both need to change. This lecture
teaches those mechanics on a real domain — the Athar Islamic-knowledge
corpus (`projects/04-ai-engineering/athar-lab/`)
and its entity-resolution layer (`projects/04-ai-engineering/arabic-nlp/08-arabic-entity-resolution/`)
— and audits the resulting model with nine executable rules. Claims labeled
FACT were verified at the cited path in this repository; everything else is
stated as general practice from the DDD literature (Evans 2003, Vernon 2013).

**Duration:** 3-4 hours
**Difficulty:** Intermediate
**Prerequisites:** Python dataclasses and type hints; the component-contracts
material in `projects/00-core-foundations/python/10-system-design/01-component-contracts`
helps but is not required; the Arabic NLP entity-resolution lecture
(`projects/04-ai-engineering/arabic-nlp/08-arabic-entity-resolution/`) supplies
the worked examples this lecture models

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Explain** why the ubiquitous language is an engineering tool, not a
   naming preference, and detect placeholder names that hide domain concepts
2. **Distinguish** entities from value objects by identity and equality
   semantics, and implement each with the right Python mechanism
3. **Draw** aggregate boundaries so every invariant has exactly one
   responsible root, and reject invariants parked on members
4. **Replace** an anemic root's setters with intention-revealing methods
   that enforce the invariants at the boundary
5. **Model** cross-aggregate rules as past-tense domain events consumed
   idempotently, never as one distributed transaction
6. **Declare** bounded-context relationships explicitly — shared kernel or
   anti-corruption layer — instead of letting one type drift across contexts
7. **Shape** repositories as intent-revealing collection interfaces, not
   table access with filter dicts
8. **Compose** domain rules with the Specification pattern so complex
   predicates stay testable and reusable
9. **Recognize** when a service does not need a domain model at all, and
   keep DTOs at the boundary from becoming the model
10. **Audit** a declarative model description against the nine DDD rules and
    interpret every finding

---

## Key Concepts

### 1. The Ubiquitous Language Is the Interface

A ubiquitous language is the single, rigorously defined vocabulary that
domain experts and developers use for the model — the same words in
conversation, in class names, in method names, in commit messages. It is an
interface in the engineering sense: when a name changes, every implementation
of it must change, and a silent drift between the spoken word and the code
word is a compile error you cannot see.

The failure mode is placeholder vocabulary. A type named `DataItem`,
`Info`, `Manager`, or `Helper` carries no domain meaning, so every discussion
about it must be translated before it can be reasoned about. The
entity-resolution track already learned this lesson the hard way: the
domain expert says "a narration" (a report attributed to a narrator through
a chain of transmission), never "a data item."

**FACT:** the exercise's BAD pack names a member of the `Passage` aggregate
`DataItem` (`exercises/01-domain-modeling.py`, rule DDD007), and the rule
fires. The GOOD pack names the same concept `Narration` — the word the
domain expert actually says — and the rule stays silent.

The practical test: read your type and method names aloud in a sentence
with a domain expert. If the sentence needs translation, the language is
not ubiquitous yet.

### 2. Entities and Value Objects: Identity versus Equality

The first modeling cut every class needs is mechanical, not aesthetic:
does this thing have identity that survives a change of attributes?

| | Entity | Value object |
|---|---|---|
| Identity | Yes — a stable id | No — attributes are the whole thing |
| Equality | By identity only | By all attributes |
| Mutation | May change over life | Immutable, always |
| Examples (this repo) | `Passage` (passage_id), `Narrator` (narrator_id) | `SourceLocation`, `AyahReference`, `NormalizedText` |

An entity is the same thing through change: a narrator's display name is
corrected, but it is still the same narrator. A value object is its
attributes or it is nothing: a `SourceLocation` of `(b1, page 12, v1)` is
equal to every other `SourceLocation` with those attributes, and there is
no "same location, different identity" state to speak of.

**FACT:** Athar's `SourceLocation` is a frozen dataclass —
`projects/04-ai-engineering/athar-lab/contracts.py:33-46`:

```python
@dataclass(frozen=True)
class SourceLocation:
    """Where a passage physically lives in the source corpus."""

    book_id: str
    page: int
    source_version: str
    path: Optional[str] = None  # original file path, for provenance

    def __post_init__(self) -> None:
        if not self.book_id:
            raise ValueError("book_id must not be empty")
        if self.page < 1:
            raise ValueError(f"page must be >= 1, got {self.page}")
```

Frozen gives value-object semantics for free: equality is attribute
equality (`dataclass(frozen=True)` generates `__eq__` from fields),
immutability is enforced by the runtime, and the object is hashable so it
can sit in sets and dict keys.

The Python default for entities is the opposite: a plain `@dataclass` with
a mutable body compares by attribute. That default is a trap. Two `Narration`
objects with the same text but different `narration_id`s are different
narrations; attribute equality collapses them, and every cache, dedupe, and
`in` check built on that equality is then wrong. The fix is an explicit
`__eq__` (or `eq=False` plus your own) that compares identity only.

The two anti-patterns the audit catches:

- **DDD002:** a value object that declares an identity field (`entity_id`,
  a surrogate `id`) is an entity in disguise. Either it is an entity — model
  it as one — or the reference belongs on the aggregate root that owns it.
- **DDD003:** an entity compared by attribute equality. Identity is the
  contract; attributes change.

### 3. Value Objects: Illegal State Is Impossible State

Value objects are not just immutable records; they are the place where
"simple" facts carry their own correctness. The rule from the DDD
literature, operationalized in this repo: **parse, don't validate** —
construct the value object at the boundary and raise immediately, so an
invalid value object cannot exist anywhere downstream.

**FACT:** Athar's `Passage` enforces its two-text discipline in
`__post_init__` (`athar-lab/contracts.py:69-75`):

```python
def __post_init__(self) -> None:
    if not self.passage_id:
        raise ValueError("passage_id must not be empty")
    if not self.original.strip():
        raise ValueError("original text must not be empty")
    if not self.searchable.strip():
        raise ValueError("searchable text must not be empty")
```

Every `Passage` in the system has both texts. No caller, no later layer, no
"final check before write" is needed, because the state that would need
that check cannot be constructed. `SourceLocation` does the same for
`book_id` and `page` (`contracts.py:42-46`): losing either is a correctness
bug, and the contract makes losing one impossible rather than merely
discouraged.

Contrast with validation that lives far from the object: a `payload: str`
field "that should never be empty," checked by one of five controllers, with
the other four having been rewritten last quarter. The value object moved
the invariant to the only place every path to the data must pass through:
construction.

### 4. Aggregates: Consistency Boundaries, Not Clusters

An aggregate is a graph of objects treated as one unit for data changes,
with exactly one **aggregate root** — the only member outside callers are
allowed to hold or reference. The root is the transaction boundary: a
change to any member of the aggregate happens inside one local transaction
that begins and ends at the root, and the whole aggregate is loaded and
saved as a whole.

The size rule is the one people get wrong in both directions: an aggregate
should be as small as it can be while still protecting its invariants, and
no larger. Every invariant that could live in a neighboring aggregate
should move there — cross-aggregate invariants cannot be protected by one
transaction anyway (section 7), so pretending they can only buys a
distributed monolith.

**FACT:** the exercise's GOOD pack draws the Athar citation boundary
correctly (`exercises/01-domain-modeling.py`, `MODEL_GOOD`):

```text
Passage (aggregate root)
├── fields: passage_id, book_id, page, original, searchable
├── operations: ingest, attach_narration, extend_isnad
├── invariants: page_at_least_one, both_texts_present,
│               narration_belongs_to_exactly_one_passage,
│               isnad_is_an_ordered_chain
├── Narration (entity, member) — narration_id, text
└── Isnad    (entity, member) — isnad_id, chain
```

`Narration` and `Isnad` are reachable only through their `Passage`. They
carry no invariants of their own; the rules about "a narration belongs to
exactly one passage" and "the isnad chain is ordered" are declared on the
root, because only the root can guarantee them for every caller.

References across aggregates are by identity, never by object graph: a
`Passage` stores `book_id`, not a live `Book`. The repository loads the
neighbor only when a use case actually needs it (section 6). This keeps
aggregates small, transactional, and independently evolvable.

### 5. Invariants Belong on the Root, Enforced at the Boundary

An invariant is a rule that must hold for every instance at every stable
point in time: "page ≥ 1," "a narration belongs to exactly one passage,"
"the alias table reflects every committed merge." DDD's placement rule has
one sentence: **the aggregate root is the only place an invariant may be
declared, and the root enforces it in the methods that change state.**

Two failure modes, both executable in the audit:

- **DDD001 — the anemic root.** The root exposes `set_book_id`,
  `set_page`, `set_original` and declares no invariants. Setters are
  pass-throughs: they accept whatever the caller hands them, so the "model"
  enforces nothing and every rule about a valid `Passage` now lives in
  whichever callers happen to remember it. The fix is intention-revealing
  methods — `ingest`, `attach_narration`, `extend_isnad` — that validate
  preconditions and preserve the invariants as they change state.

- **DDD004 — the invariant on a member.** An invariant declared on
  `Narration`, a member of `Passage`, has no one responsible for it:
  members can be replaced, constructed directly, or reached through paths
  the root never sees. Move the rule to the root's methods.

**FACT:** Athar already enforces the boundary in code. The demo in
`exercises/01-domain-modeling.py` constructs a `Passage` through its root:

```text
construct page 0      -> rejected: page must be >= 1, got 0
attach n-1 to p1      -> ok (1 narration)
attach n-1 to p2      -> rejected: narration n-1 already belongs to passage b1:p3:0
root exposes a setter -> False (DDD001 finds none)
```

The second rejection is the aggregate boundary doing its job: a narration
already attached to one passage cannot silently appear under another,
because `attach_narration` is the only way in, and it checks.

### 6. Factories and Repositories: the Two Legitimate Ways In and Out

Objects enter the world through **factories** and leave/re-enter through
**repositories**. Both exist so that callers never see half-built or
storage-shaped objects.

A factory is a function or method that produces a valid aggregate, applying
all invariants. **FACT:** Athar's `make_passage`
(`projects/04-ai-engineering/athar-lab/contracts.py:90-110`) is the pattern:

```python
def make_passage(
    book_id: str,
    page: int,
    text: str,
    source_version: str,
    passage_index: int,
    path: Optional[str] = None,
) -> Passage:
    """Build a Passage from raw page text, applying the two-text discipline."""
    original = text.strip()
    return Passage(
        passage_id=f"{book_id}:p{page}:{passage_index}",
        location=SourceLocation(
            book_id=book_id, page=page, source_version=source_version, path=path
        ),
        original=original,
        searchable=normalize_arabic(original),
    )
```

One call from raw page text to a fully valid `Passage`: the searchable text
is derived (never normalized in place of the original — the two-text
discipline), the id is composed from domain identity, and the location's
invariants already ran inside `SourceLocation.__post_init__`. No caller
can produce a `Passage` that skipped normalization, because no caller
constructs `Passage` directly for ingestion.

A repository is the aggregate's collection interface — the illusion of an
in-memory collection of aggregates, persisted behind it. Two rules make it
a domain-facing interface rather than a DAL:

- **Intent-revealing queries.** `passages_of_book(book_id)` states its
  rule at the call site; `find_by({"book_id": ...})` states a filter shape
  and pushes the intent back to every caller. **DDD009** fires on the
  latter.
- **One repository per aggregate root**, not per table. The repository
  loads whole aggregates; it never returns a bare member (`Narration`
  without its `Passage`) to outside code.

**FACT:** the GOOD pack's repositories follow both rules —
`PassageRepository.passages_of_book`, `CanonicalEntityRepository.pending_merge_candidates` —
while the BAD pack's `PassageRepo.find_by(filters: dict)` trips DDD009.

### 7. Domain Events Are Records, Not Instructions

Rules that span aggregates cannot be transactions — two aggregate roots
cannot share one local transaction without coupling their schemas and
lifecycles into a distributed lock. The alternative is eventual consistency
through **domain events**: the aggregate that owns the fact records what
happened, and the other side reacts.

Two disciplines make this safe, and both are enforced by the audit and the
runnable demo:

**Past tense, always.** An event is a record of something that already
happened: `NarrationLinked`, `PassageIngested`, `EntityMerged`,
`MergeDecisionCommitted`. A command-shaped name (`PublishNarration`) reads
as an instruction to perform the action — and on an at-least-once transport,
every redelivery re-issues that instruction. **DDD006** fires on
command-shaped event names. The rule the exercise implements: the first
word is not a command verb, or the final word is past tense
(`MergeDecisionCommitted` starts with a verb *word* but ends in a past
participle — it is a record).

**Idempotent consumers.** At-least-once delivery plus retries means every
consumer *will* see a duplicate. **FACT:** the exercise's
`IdempotentConsumer` demonstrates the required shape:

```text
Domain event EntityMerged delivered twice (queue is at-least-once):
    first delivery        -> applied (alias table updated)
    redelivery            -> suppressed (event already applied)
    alias updates applied -> 1 (not 2)
```

The consumer stores the event id before applying the side effect; the
second delivery is a no-op. This is the same idempotency discipline the
Reliability track teaches for queues and HTTP retries — here it is the
load-bearing half of cross-aggregate consistency, not an optional hardening.

The GOOD pack's `MergeDecision` declares exactly this mechanism:

```python
{
    "name": "alias_table_reflects_committed_merge",
    "scope": "cross-aggregate",
    "mechanism": "domain-event",
}
```

while the BAD pack's `Narration` tries to enforce a cross-aggregate rule
as a single transaction (`mechanism: single-transaction`) — **DDD005**,
critical, because the mechanism cannot work across two roots.

### 8. Bounded Contexts and Context Mapping

A bounded context is an explicit boundary within which a ubiquitous
language is consistent. "Passage" inside the citation context means the
retrievable unit with both texts; the catalog context's unit of publishing
and the resolution context's matching keys are different models that must
not be forced into one type. Outside a context, the same word may mean
something else — that is not a bug, it is why the boundaries exist.

When two contexts must share a type, the relationship is declared, not
assumed. The two declarations the audit accepts:

- **Shared kernel:** both contexts own the type together, change requires
  both sides' consent, and the type is deliberately minimal. Athar's
  `EntityId` is the working example: catalog, citation, and resolution all
  speak it, and the GOOD pack declares `boundary_relationship: "shared-kernel"`.
- **Anti-corruption layer:** one context translates at its edge so its
  model is never polluted by the other's. Use it when one side must not
  bend, or when the external model is a vendor's.

**DDD008** fires when a type appears in two or more contexts with no
declaration. The BAD pack's `EntityId` (`contexts: ["catalog", "citation"]`,
`boundary_relationship: None`) is exactly that silent coupling: the day
citation wants to change the id format, catalog breaks with no warning and
no negotiation.

The broader context map — customer-supplier, conformist, and the rest —
follows the same principle: every relationship between contexts is a
named contract. This lecture's audit enforces the two that matter most for
a single-team codebase; the full catalog is in the glossary.

### 9. Specifications: Composable Domain Rules

A specification is a domain rule packaged as an object: it answers
"is this candidate acceptable?" and — crucially — can be combined with
other specifications by `and`, `or`, and `not` without exploding into
nested boolean spaghetti. Rules that read like the domain expert's policy
stay testable in isolation and reusable across use cases.

**FACT:** the exercise implements the pattern as composable classes
(`exercises/01-domain-modeling.py`, `Specification`, `_AllOf`, `_AnyOf`,
`_Not`, `MeetsScore`, `NotVetoed`) and demonstrates the merge policy the
resolution context actually runs:

```text
Specification: auto_merge = (score >= 0.92) AND (veto is absent)
    h-1/h-2  score 0.97  no veto        -> auto-merge
    h-3/h-4  score 0.88  no veto        -> review
    h-5/h-6  score 0.95  year-conflict  -> review
    same rule inverted for the review queue: NOT ((score >= 0.92) AND (veto is absent))
```

The inversion matters: the review queue is not a second policy, it is the
complement of the first. With specifications, that is one line, and the two
queues provably partition the candidate space. With scattered
`if score >= ... and not veto` conditionals in two modules, the partition
is a hope.

The placement rule: specifications are domain objects, not utilities. They
live in the domain layer with the entities and value objects they judge,
and they are named in the ubiquitous language — `MeetsScore`, not
`check_h`.

### 10. The Anemic Domain Model Anti-Pattern

The anemic domain model looks like a model and behaves like a bag of
getters and setters: dataclasses or Pydantic rows with public fields,
business logic in services that set those fields freely, invariants either
absent or re-checked far away. It is the default outcome of building
"models" as serialization schemas, and the audit names its signature:
**setters on the root, no invariants** (DDD001).

The cost is not aesthetic. With setters, any code path can construct an
invalid state; the rules that used to live in one method now live in
whoever calls the setters, and a new caller can skip them silently. With
intention-revealing methods, the API itself documents what may happen:
`attach_narration` exists, `set_passage_id` does not, and the compiler
plus the type checker surface every attempt.

The honest counterpoint is proportionality (section 13): a service that
genuinely is CRUD over rows does not need rich methods; it needs the rows.
The anti-pattern is not "using dataclasses" — it is "putting the domain's
rules nowhere while pretending the dataclasses are the model."

### 11. Domain Types at the Boundary: DTOs Are Not the Model

Every service has a boundary — HTTP schemas, queue payloads, file rows —
and those boundary types are DTOs: data transfer objects, shaped for the
wire, owned by neither the domain nor the database. They are necessary.
They become a problem only when they are the only types the system has.

**FACT:** DevMate's API boundary is a clean DTO set —
`projects/04-ai-engineering/devmate/src/devmate/llm/schemas.py:10-126`
defines `LLMRequest`, `LLMResponse`, `RAGContext`, `RAGRequest`,
`AskRequest`, `IngestResponse`, and the rest as Pydantic `BaseModel`s.
Pydantic validation at the edge is right: reject malformed input before it
enters. The modeling question is what happens next. If `RAGResponse` is
passed straight through services and into the retrieval layer's decisions,
the DTO has become the model, and the wire format now owns the domain's
shape. The domain layer — entities, value objects, specifications, the
rules from sections 2–9 — sits between the DTO and the storage, translating
in both directions.

The same line applies to storage shapes. **FACT:** DevMate's chunker's
`Document` (`ingest/chunker.py:15-29`) is a
pipeline record — `id`, `content`, `metadata`, `embedding` — and it is
correctly *not* Athar's `Document` (`athar-lab/contracts.py:49-56`, a book
with stable identity). Two models, one word, two contexts: bounded-context
discipline applied without a framework.

### 12. Identity: Natural Keys, Synthetic Keys, Equality

Entities need ids, and the choice of id is a modeling decision with
operational consequences:

- **Natural keys** derive from the domain's own identity: content hashes,
  book:page:index compositions. They make ingestion idempotent for free —
  re-running with the same content upserts rather than duplicates.
- **Synthetic keys** are issued by the system (surrogate UUIDs). They are
  right when the natural identity is unstable, unknown at creation time,
  or when two things that "look the same" must still be tracked
  separately — which is precisely what entity resolution is for.

**FACT:** both patterns appear in this repo, with intent stated. Athar's
`make_passage` composes a natural id — `f"{book_id}:p{page}:{passage_index}"`
(`contracts.py:101`) — so re-ingesting the same book yields the same
passage ids. DevMate's chunker derives a deterministic content id —
`md5(f"{source}:{position}:{content[:100]}")`, 32 hex digits
(`ingest/chunker.py:40-49`) — so re-indexing the same file overwrites the
same Qdrant points. Neither id contains meaning that the domain does not
put there; neither is a database sequence leaking upward.

The equality rule from section 2 closes the loop: entities compare by
these ids, value objects by attributes. Confusing the two — comparing
entities by content — is DDD003, and it breaks exactly where synthetic
ids matter: two distinct narrations with identical text are still two
narrations, and dedupe must not merge them.

### 13. Cross-Aggregate Consistency: the Full Shape

Section 7 gave the event mechanics; here is the complete pattern for a
rule that spans aggregates, with each piece named:

1. **Own the fact.** The aggregate where the fact originates enforces its
   local invariants and, on commit, records a past-tense domain event in
   the same local transaction (the outbox discipline from the Reliability
   track: publication atomic with the write).
2. **Deliver at-least-once.** The event travels through a queue or table
   drain that may duplicate.
3. **React idempotently.** The consuming aggregate applies its side
   effect keyed by the event id; duplicates are suppressed.
4. **Accept convergence, not simultaneity.** Between publish and apply,
   the two aggregates are briefly inconsistent. That window is the price
   of not sharing a transaction; what must be bounded — and published as
   an SLA — is its duration.

**FACT:** the exercise demonstrates the consumer half end to end
(`IdempotentConsumer`, demo output in section 7): two deliveries, one
alias-table update. The GOOD pack declares the mechanism
(`mechanism: "domain-event"`) on the `MergeDecision` invariant
`alias_table_reflects_committed_merge`; the BAD pack attempts the same
class of rule as one transaction inside `Narration` and trips DDD005.

The Reliability track owns the transport mechanics — idempotency keys,
outboxes, DLQs. This track owns the modeling half: which aggregate owns
the fact, what the event is named, and which invariant waits for it.

### 14. When Not to Model: Proportionality

DDD is expensive. Ubiquitous language sessions, aggregate design, event
disciplines — all of it is overhead that pays for itself only where the
domain is complex enough to need it. The literature's own guidance, and
this lecture's: use it where rules are dense, change is frequent, and
mistakes are expensive; skip it where the service is CRUD.

```text
Needs a domain model                Does not need one
─────────────────────────────       ─────────────────────────────
Athar citation + resolution         Config tables, feature flags
  (chains, invariants, merges)        (rows and getters)
Order lifecycle / billing           File upload proxy
  (state transitions, money)          (pass-through)
Policy engines, matching rules     Health/status endpoints
  (specifications everywhere)         (read-only DTOs)
```

A healthy small service may hold a thin domain layer — a few value objects
at construction, a couple of specifications — without full aggregate
discipline. What it must not do is pretend its DTOs are a model while
business rules accrete in controllers. Either model the rules or admit the
service is CRUD; the middle state, "anemic model with rules in five
services," is where the wall from the Topic Overview lives.

### 15. Worked Scenario: One Narrator Merge, End to End

The resolution context of the Athar stack — the part that turns many
surface forms of a narrator's name into one canonical entity — exercises
every concept above in one flow.

**Contexts and boundary.** Resolution owns `Narrator` (aggregate root:
display, aliases, era), `MergeCandidate` (value object: the scored pair),
and `MergeDecision` (entity: append-only audit of what was committed).
Catalog and citation speak `EntityId` — the declared shared kernel
(DDD008's GOOD answer). Resolution never hands its `MergeDecision` type
across the boundary untranslated; the other contexts get ids and events.

**The local rule.** A `MergeDecision` is append-only: corrections are
reversals, never edits. That is an invariant on the root —
`decisions_are_append_only`, enforced in the `commit`/`reverse`
operations, never in a setter (section 5).

**The cross-aggregate rule.** "The alias table reflects every committed
merge" spans `MergeDecision` and `Narrator`. It is declared with
`scope: cross-aggregate`, `mechanism: domain-event` (section 7): commit
records `MergeDecisionCommitted` (past tense, DDD006-clean); the
`Narrator` side consumes it idempotently and records the alias.

**The policy.** Auto-merge versus human review is the specification from
section 9: `(score >= 0.92) AND (veto is absent)`, inverted for the review
queue. The spec is a domain object; the thresholds live next to the
vocabulary that named them.

**The audit.** The GOOD pack encodes this model and raises zero findings
across all nine rules; the BAD pack — anemic `Passage`, `DataItem`,
cross-aggregate single transaction, command-shaped event, undeclared
shared `EntityId`, `find_by(filters)` — raises nine. That contrast is the
lecture's closing argument: the rules are mechanical, the model is
checkable, and the difference between the two packs is every concept in
sections 1–13 applied.

---

## Common Mistakes to Avoid

### 1. Setters on the Aggregate Root (DDD001)

```python
# ❌ BAD: any caller can bypass every rule about a valid passage
passage.set_page(0)
passage.set_original("")
# (no invariants declared anywhere)

# ✅ GOOD: the operation validates; invalid states are unconstructible
passage = make_passage(book_id="b1", page=1, text=text, ...)
passage.attach_narration(n1)   # checks single-passage ownership
```

### 2. An Identity Field on a Value Object (DDD002)

```python
# ❌ BAD: "EntityKey" is an entity in disguise
@dataclass(frozen=True)
class EntityKey:
    entity_id: str  # identity on a value object
    surface: str


# ✅ GOOD: the value carries attributes; identity lives on the entity/root
@dataclass(frozen=True)
class SurfaceForm:
    surface: str
    script_hint: str
```

### 3. Entities Compared by Attributes (DDD003)

```python
# ❌ BAD: dataclass default equality — two narrations with the same text collapse
@dataclass
class Narration:
    narration_id: str
    text: str


# ✅ GOOD: identity is the equality contract
@dataclass(eq=False)
class Narration:
    narration_id: str
    text: str

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Narration) and self.narration_id == other.narration_id
```

### 4. Cross-Aggregate Rules as One Transaction (DDD005)

```python
# ❌ BAD: two roots, one transaction — couples schemas and lifecycles
with db.transaction():
    decision = load_merge_decision(id)
    narrator = load_narrator(decision.right_id)
    narrator.aliases.append(decision.left_id)  # other aggregate, same txn

# ✅ GOOD: own the fact, publish the record, react idempotently
decision.commit()  # local txn records EntityMerged
# consumer (at-least-once, deduped by event id):
narrator.record_alias(event.left_id)
```

### 5. Command-Shaped Domain Events (DDD006)

```python
# ❌ BAD: an instruction — redelivery re-orders the action
publish_event("PublishNarration", {...})

# ✅ GOOD: a record — redelivery re-reads a fact
publish_event("NarrationPublished", {...})
```

### 6. Table Access Disguised as a Repository (DDD009)

```python
# ❌ BAD: filter shape leaks storage mechanics; intent lives in the caller
repo.find_by({"book_id": book_id, "page": {"$gte": 1}})

# ✅ GOOD: the query names the domain rule
repo.passages_of_book(book_id)
```

---

## Best Practices

1. **Name every type and method in the domain expert's words**; treat a
   placeholder (`DataItem`, `Manager`, `Helper`) as a defect, not a draft
2. **Decide entity versus value object first** — identity and equality
   semantics before fields and methods
3. **Make value objects frozen** and enforce their invariants in
   `__post_init__`; construct, never mutate
4. **Give entities explicit identity equality** — `eq=False` plus an
   `__eq__` over the id — never the dataclass attribute default
5. **Draw aggregates around invariants**, one root each, as small as the
   rules allow and no smaller
6. **Reference across aggregates by id**, never by holding the neighbor's
   object; load through repositories when the use case needs it
7. **Declare every invariant on the root** and enforce it in the state
   change; no setters on aggregates
8. **Route construction through factories** that produce valid aggregates
   from raw input (`make_passage`)
9. **One repository per aggregate root**, with intent-revealing queries;
   never return a bare member to outside code
10. **Name events in the past tense** and consume them idempotently by
    event id; declare `mechanism: domain-event` for cross-aggregate rules
11. **Declare every cross-context type** as shared kernel or behind an
    anti-corruption layer; undeclared sharing is a latent breaking change
12. **Keep specifications as domain objects** — composable, named in the
    ubiquitous language, testable alone
13. **Keep DTOs at the boundary**; translate in and out; never let a wire
    schema be the only model
14. **Choose ids deliberately** — natural keys where the domain owns the
    identity, synthetic keys where resolution and tracking demand them
15. **Be proportional** — full discipline where rules are dense, a thin
    layer or none where the service is genuinely CRUD

---

## Practice Exercises

### Exercise 1: Run the Nine-Rule Audit
Using `exercises/01-domain-modeling.py`, run the built-in BAD pack and
match every one of the nine findings to its rule, severity, and the model
line that caused it. Then run the GOOD pack and confirm zero findings.
Explain, for DDD005 and DDD008 specifically, what production incident the
finding predicts.

### Exercise 2: Break the GOOD Pack on Purpose
Copy the GOOD pack's `Passage` definition and add
`setters: ["set_page"]`, removing its invariants. Re-run the audit,
confirm DDD001 fires, then restore the pack. Next, rename the event
`MergeDecisionCommitted` to `CommitMergeDecision` and confirm DDD006
fires — then explain why the past-tense rule exists for at-least-once
transports.

### Exercise 3: Drive the Aggregate Boundary
Using the `Passage` class in the exercise, attach narration `n-1` to
passage A, then attempt to attach the same narration to passage B.
Confirm the root rejects it. Write the one-line invariant statement a
reviewer would check in a PR to keep that guarantee.

### Exercise 4: Prove the Consumer Is Idempotent
Run the `IdempotentConsumer` with the same `EntityMerged` event id three
times and confirm the alias table advanced exactly once. Then remove the
seen-set guard and confirm three updates — the bug DDD006 plus a
non-idempotent consumer produces in production.

### Exercise 5: Audit Your Own Service's Types
List every type in your current service. Mark each as entity, value
object, or DTO. Find one DTO that leaks into business logic, one entity
with attribute equality, and one rule that belongs on an aggregate root
but lives in a controller. For each, state the one-sentence fix — the
same review this lecture's audit automates.

---

## Summary

Domain modeling is the discipline of making the model executable and
auditable:

1. **The ubiquitous language is an interface.** Placeholder names are
   compile errors you cannot see; name types after what the expert says.
2. **Entities have identity; value objects have attributes.** Equality
   semantics follow the cut; frozen dataclasses and explicit `__eq__` are
   the Python mechanisms.
3. **Value objects make illegal state unconstructible.** Invariants live in
   construction (`__post_init__`), not in distant validators.
4. **Aggregates are consistency boundaries with one root.** Invariants are
   declared on the root, enforced by intention-revealing methods, and
   never parked on members.
5. **Factories and repositories are the only ways in and out.** Valid
   objects on the way in; intent-revealing, aggregate-shaped access on the
   way out.
6. **Cross-aggregate rules are past-tense events with idempotent
   consumers.** One transaction cannot span two roots; eventual consistency
   with a bounded, published convergence window can.
7. **Shared types across contexts are declared** — shared kernel or ACL —
   or they are a silent coupling waiting for a breaking change.
8. **Specifications compose domain policies** so the review queue is the
   inversion of the auto-merge rule, not a second copy of it.
9. **DTOs stay at the boundary.** Pydantic schemas validate the wire; they
   do not get to be the model.
10. **Proportionality is part of the craft.** The audit's nine rules apply
    where the domain is complex enough to have rules worth enforcing —
    and the first rule of modeling is knowing when not to model.

**Next lecture:** event-driven consistency end to end — outbox layouts,
consumer lag budgets, and reconciliation jobs — taking this lecture's
domain events onto the transport the Reliability track already hardened.
