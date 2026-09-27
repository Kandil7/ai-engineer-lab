# Data Engineering 02: Schemas and Contracts

## 🎯 Topic Overview

A schema is the contract between a pipeline and its consumers. It declares
what fields exist, their types, which are required, and what values are
valid. For Athar, the `Document`/`Passage`/`SourceLocation` contracts are
the schema — and enforcing them at the boundary is what prevents silent
data corruption. This lecture covers schema design, validation, and
evolution.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Design a schema that declares types, required fields, and constraints
2. Validate data at the pipeline boundary, not deep inside logic
3. Enforce invariants (book_id non-empty, page >= 1) structurally
4. Evolve a schema without breaking consumers (additive changes, versioning)
5. Distinguish schema validation from business validation

---

## 1. What a Schema Declares

A schema declares: the field set, each field's type, which fields are
required, and the constraints on values. The Athar contracts do exactly
this: `SourceLocation` requires a non-empty `book_id` and `page >= 1`;
`Passage` requires non-empty `original` and `searchable`. A schema that
does not state its invariants is a wish, not a contract.

```python
# The contract in code: invalid data cannot even be constructed
@dataclass(frozen=True)
class SourceLocation:
    book_id: str
    page: int

    def __post_init__(self) -> None:
        if not self.book_id:
            raise ValueError("book_id must not be empty")
        if self.page < 1:
            raise ValueError(f"page must be >= 1, got {self.page}")
```

## 2. Validate at the Boundary

Validation belongs where data enters the system: the file reader, the API
request, the pipeline input. Validating deep inside business logic means
corrupt data has already traveled halfway through the system. The boundary
rejects bad input once; everything downstream can assume the contract holds.

## 3. Structural Invariants

The strongest validation is structural: make it impossible to construct an
invalid object. The `__post_init__` checks in the contracts do this — a
`SourceLocation` with an empty book_id cannot exist, so no downstream code
needs to check for it. This is stronger than validating at runtime because
the invalid state is unrepresentable.

## 4. Schema Evolution

Schemas change. The rules: additive changes (new optional fields) are safe;
removing or retyping fields breaks consumers. Version the schema
(`source_version`) so old and new data coexist and consumers know which
shape they hold. Never mutate a schema in place — add a version, migrate,
then retire the old one.

## 5. Schema vs Business Validation

Schema validation checks shape: types, required fields, constraints.
Business validation checks meaning: is this page number in range for this
book, does this passage belong to this source. Keep them separate — schema
validation is mechanical and cheap; business validation is domain logic
that changes with the corpus.

## Common Mistakes

- Validating deep inside logic instead of at the boundary.
- Schemas without stated invariants (empty book_id slips through).
- Breaking consumers with non-additive schema changes.
- Confusing schema validation with business validation.

## Key Takeaways

1. A schema states types, required fields, and constraints.
2. Validate at the boundary; assume the contract downstream.
3. Structural invariants beat runtime checks.
4. Evolve additively, version explicitly.