# Data Engineering 02: Schemas and Contracts

## Topic Overview

A schema is the contract between a pipeline and its consumers. It declares what fields exist, their
types, which are required, and what values are valid. For Athar, the `Document`, `Passage`, and
`SourceLocation` contracts are the schema, and enforcing them at the boundary is what prevents silent
data corruption that would otherwise surface as a wrong answer months later.

This lecture covers schema design, validating at the pipeline boundary, enforcing invariants
structurally so invalid data cannot exist, evolving a schema without breaking consumers, and the
distinction between schema validation and business validation.

The strongest form of schema enforcement is structural: make it impossible to construct an invalid
object. When an empty `book_id` cannot exist as a `SourceLocation`, no downstream code needs to
check for it, and the class of bug is eliminated rather than detected.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Design a schema that declares types, required fields, and constraints.
2. Validate data at the pipeline boundary, not deep inside logic.
3. Enforce invariants structurally so invalid states are unrepresentable.
4. Evolve a schema without breaking consumers (additive, versioned).
5. Distinguish schema validation from business validation.
6. Explain why a schema without stated invariants is only a wish.

## Prerequisites

- Data Engineering 01 (ETL fundamentals) for the stage the schema bounds.
- Basic familiarity with Python dataclasses.

---

## 1. What a Schema Declares

### The four parts

A schema declares the field set, each field's type, which fields are required, and the constraints
on values. The Athar contracts declare all four: `SourceLocation` requires a non-empty `book_id` and
`page >= 1`; `Passage` requires non-empty `passage_id`, `original`, and `searchable`.

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

### The wish

A schema that does not state its invariants is a wish, not a contract. It declares fields but not
what makes them valid, so the constraints exist only in the author's head and are enforced
inconsistently.

### Frozen

The contracts are frozen, so a constructed object cannot be mutated into an invalid state. Immutability
is part of the contract.

## 2. Validate at the Boundary

### The rule

Validation belongs where data enters the system: the file reader, the API request, the pipeline
input. Validating deep inside business logic means corrupt data has already traveled halfway through
the system before it is caught.

### The payoff

The boundary rejects bad input once, and everything downstream can assume the contract holds. This
removes the defensive checks scattered through the code and concentrates them where the data arrives.

### The anti-pattern

Validating in five different places, each slightly differently, is how a constraint gets enforced
inconsistently. One boundary, one check, one source of truth.

## 3. Structural Invariants

### The idea

The strongest validation is structural: make it impossible to construct an invalid object. The
`__post_init__` checks do this. A `SourceLocation` with an empty `book_id` cannot exist, so no
downstream code needs to check for it:

```python
for bad in (
    lambda: SourceLocation("", 1, "v1"),
    lambda: SourceLocation("b1", 0, "v1"),
):
    try:
        bad()
        raise AssertionError("expected ValueError")
    except ValueError:
        pass
```

### Why structural beats runtime

A runtime check must be remembered and applied everywhere. A structural invariant is enforced at
construction, once, and the invalid state is unrepresentable. The bug class is eliminated rather than
detected.

### The cost

Construction raises, so the pipeline must handle the exception at the boundary. That is the correct
place for it, and it is why the boundary validation and the structural invariant work together.

## 4. Schema Evolution

### The rules

- **Additive changes** (new optional fields) are safe: old data and consumers still work.
- **Removing or retyping fields** breaks consumers and requires a migration.

### Versioning

Version the schema (the `source_version` field does this for Athar) so old and new data coexist and
consumers know which shape they hold:

```python
@dataclass(frozen=True)
class SourceLocationV2(SourceLocation):
    path: str | None = None
```

### Never mutate in place

Do not mutate a schema in place. Add a version, migrate, then retire the old one. In-place mutation
is what produces the "works on old data, fails on new data" bug that erodes trust.

## 5. Schema Versus Business Validation

### The distinction

Schema validation checks shape: types, required fields, constraints. Business validation checks
meaning: is this page number in range for this book, does this passage belong to this source.

### Why keep them separate

Schema validation is mechanical and cheap; business validation is domain logic that changes with the
corpus. Mixing them means a domain change requires re-testing the mechanical checks. Keep the
mechanical layer stable and the domain layer explicit.

### The placement

Schema validation at the boundary; business validation in the domain logic that has the context to
judge meaning. Each layer does what it is equipped to do.

## 6. The Audit Trail

### The schema carries provenance

The contracts carry `book_id`, `page`, and `source_version`, which are the provenance the audit trail
needs (Data Engineering 06). A schema that carries provenance makes every row traceable by
construction.

### The link to citation

A RAG answer cites a passage; the passage's provenance resolves to its source. The schema is what
makes that chain possible, which is why the provenance fields are mandatory, not optional.

## Real-World Application

- Enforcing `book_id` non-empty and `page >= 1` so a malformed passage never enters the corpus.
- Validating at the file reader so a corrupted source is rejected once, at the boundary.
- Adding an optional `path` field additively so older data still loads.
- Keeping the schema's provenance fields so every passage can be cited back to its source.

## Common Mistakes

1. **Validating deep inside logic.** Corrupt data travels before it is caught.
2. **Schemas without stated invariants.** Empty `book_id` slips through.
3. **Non-additive schema changes.** Consumers break on new data.
4. **In-place schema mutation.** Old and new data conflict.
5. **Confusing schema and business validation.** A domain change forces a mechanical retest.

## Key Takeaways

1. A schema states types, required fields, and constraints; without invariants it is a wish.
2. Validate at the boundary; assume the contract downstream.
3. Structural invariants make invalid states unrepresentable, which beats runtime checks.
4. Evolve additively and version explicitly; never mutate a schema in place.
5. Keep schema validation (shape) separate from business validation (meaning).

## Self-Check Questions

1. Why is a schema without stated invariants only a wish?
2. What does structural enforcement buy over a runtime check?
3. Which schema changes are safe, and which break consumers?
4. Why must schema and business validation stay separate?
5. Why are the provenance fields mandatory in the schema?

## Further Reading / Connections

- Data Engineering 01 (ETL) and 03 (idempotency) — the pipeline the schema bounds.
- Data Engineering 06 (provenance and versioning) — the fields the schema carries.
- `projects/04-ai-engineering/athar-lab/contracts.py` — the contracts in code.
- RAG System 04 (context construction) — where provenance becomes a citation.
