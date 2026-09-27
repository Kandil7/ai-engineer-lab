# Data Engineering 02: Schemas and Contracts — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Schema | Field set, types, required fields, constraints | Passage contract |
| Contract | The enforceable agreement between pipeline and consumers | dataclass invariants |
| Boundary validation | Rejecting bad input where it enters the system | file reader, API |
| Structural invariant | Invalid state made unrepresentable | __post_init__ checks |
| Schema evolution | Changing schemas without breaking consumers | additive + versioned |
| source_version | Version tag on data rows | provenance + compat |
| Business validation | Domain-meaning checks, separate from shape | page-in-range |

---

## Alphabetical Glossary

### Boundary validation

**Definition:** Rejecting invalid input where it enters the system — the
file reader, API request, or pipeline input. Everything downstream assumes
the contract holds.

**Example:**
```python
# reject bad rows at read time, not halfway through the pipeline
```

**Related concepts:** Schema, Structural invariant

---

### Business validation

**Definition:** Domain-meaning checks: is this page in range, does this
passage belong to this source. Separate from mechanical schema validation.

**Example:**
```python
# page 500 in a 300-page book: business rule, not schema
```

**Related concepts:** Schema, Boundary validation

---

### Contract

**Definition:** The enforceable agreement between a pipeline and its
consumers: what fields exist, their types, and their invariants.

**Example:**
```python
# Passage requires non-empty original and searchable
```

**Related concepts:** Schema, Structural invariant

---

### Schema

**Definition:** The declaration of a data shape: field set, types, required
fields, constraints. A schema without stated invariants is a wish.

**Example:**
```python
# SourceLocation: book_id str, page int >= 1
```

**Related concepts:** Contract, Schema evolution

---

### Schema evolution

**Definition:** Changing a schema over time. Additive changes are safe;
removing or retyping fields breaks consumers. Version and migrate.

**Example:**
```python
# add optional field -> new version -> migrate -> retire old
```

**Related concepts:** source_version, Schema

---

### source_version

**Definition:** A version tag on data rows identifying which schema and
source produced them. Enables coexistence of old and new shapes.

**Example:**
```python
# "v1" vs "v2": consumers know which shape they hold
```

**Related concepts:** Schema evolution, Provenance

---

### Structural invariant

**Definition:** An invariant enforced by construction — invalid state is
unrepresentable. Stronger than runtime checks because the bad state cannot
exist.

**Example:**
```python
# __post_init__ raises on empty book_id: it cannot be constructed
```

**Related concepts:** Contract, Boundary validation

---

## Related Concepts

- **Provenance**: source_version is part of it (topic 06)
- **Idempotency**: contracts make upserts keyed and safe (topic 03)
- **Validation**: mechanical shape checks vs domain meaning

## Key Takeaways

1. Schemas state types, required fields, and constraints.
2. Validate at the boundary; assume the contract downstream.
3. Structural invariants beat runtime checks.
4. Evolve additively, version explicitly.