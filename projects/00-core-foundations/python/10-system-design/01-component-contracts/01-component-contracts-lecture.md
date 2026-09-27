# System Design Lecture 01: Component Contracts

## Topic Overview

A distributed text pipeline is a set of promises between components: the importer promises the shape of a record, the indexer promises what retrieval returns, the API promises what a citation contains. When those promises are implicit — a shared dict, a "same team" assumption, a Slack message — every change becomes a coordinated deployment and every mismatch becomes a data-loss incident discovered by a user. This lecture makes the promises explicit: the four parts of a contract, compatibility rules that classify every schema change, the migration path for adding fields, and the contract tests that fail in CI before a producer breaks a consumer. For Athar, the record contract (`id/book/page/text` + lineage) is the artifact that makes "text, book, page never get lost" enforceable.

The theme: **shape is a wire format; a contract is shape plus meaning plus invariants plus a version.**

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. Write a four-part component contract (shape, semantics, invariants, version).
2. Classify a schema change as compatible, needs-migration, or breaking.
3. Plan the migration path for a new required field (emit-default → consume → backfill → require).
4. Write system-level contract tests for producer and consumer sides.
5. Store contracts as versioned artifacts both teams can find.
6. Explain why implicit contracts turn every change into a coordinated deploy.

---

## Prerequisites

| Need | Where |
|---|---|
| Contract testing basics | `02-advanced-python/38-test-strategy-contract-regression-lecture.md` |
| Protocols / interfaces | `02-advanced-python/36-separation-of-concerns-lecture.md` |
| Dataclasses | `02-advanced-python/06-dataclasses-lecture.md` |

---

## 1. What a contract is (and is not)

A **contract** is the documented, tested agreement between a producer and a consumer of data or behavior. It has four parts:

1. **Shape** — fields, types, nullability. This is the wire format; it is necessary but insufficient.
2. **Semantics** — what each field *means*: `book` is the canonical Arabic title, `page` is the 1-based physical page *in that edition*. Two services can agree on `int page` and still disagree on whether page 0 exists.
3. **Invariants** — what is always true: `source_ref == f"{book}/p{page}"`, `text` is non-empty and verbatim NFC. Invariants are what make downstream reasoning possible.
4. **Version** — what changed and how consumers migrate. Without it, "is this payload OK?" has no answer.

The discipline: **a shape without semantics is a guess shared by two codebases.** The dict in your head is not a contract; the JSON file in the shared contract repo, tested by both sides, is.

## 2. Compatibility rules

Not all schema changes are equal. The classification (which the exercise implements mechanically):

| Change | Class | Why |
|---|---|---|
| Add optional field | **compatible** | consumers ignore what they don't know |
| Add required field | **needs-migration** | old producers emit nothing; consumers break |
| Remove field | **breaking** | consumers that read it break immediately |
| Change field meaning | **breaking** | same name, different semantics is the worst case |
| Rename field | **breaking** | treat as remove + add; dual-write first |
| Tighten invariant | **maybe breaking** | depends on whether consumers relied on the gap |

The key insight: **adding is safe if and only if the new thing is optional at first.** Required additions are migrations, not edits.

## 3. The migration path for a new required field

The exercise adds `edition` to the record. The safe sequence:

1. **Emit with default** — the producer starts sending `edition: "default"` for everything. Old consumers ignore it. This is a v2-transitional contract.
2. **Consumers read when present** — new consumers use the field; old producers' absence is tolerated during the window.
3. **Backfill history** — a data migration fills the field for existing rows.
4. **Require it** — the contract tightens: `edition` is now required. Any producer that skipped step 1 now fails the contract test.

At **every** step, both old and new versions must work. That is the same expand→backfill→contract shape as the schema migrations lecture, because it is the same problem one layer up: rolling upgrades.

## 4. Contract tests at the system level

Two directions, both in CI:

**Producer side** — assert that what the producer emits satisfies the contract:

```python
validate_payload(producer_emits_v1(), ATHAR_V1) == []  # v1 emits valid v1
validate_payload(producer_emits_v1(), ATHAR_V2) != []  # v1 does NOT satisfy v2
```

The second assertion is the valuable one: it proves the version boundary is real. A producer that silently emits v1 while consumers demand v2 is caught at CI, not at 3 a.m.

**Consumer side** — assert that the consumer tolerates every *supported* version. A consumer that crashes on a missing `edition` is not ready to roll out during step 2.

When a payload violates an **invariant** (empty `text`, broken `source_ref`), the failure must name which invariant broke and with what values — the same "clear message" discipline as the importer.

## 5. Contracts as artifacts

Contracts live where both teams can find them: versioned JSON files (or JSON Schema, Protobuf, OpenAPI components) in a shared repo, with a test on each side that executes the validation. The serialized form in the exercise is the pattern:

```json
{
  "name": "athar.record",
  "version": "2.0",
  "required": {"id": "str, unique, immutable", ...},
  "invariants": ["source_ref == f'{book}/p{page}'", "text.strip() != ''"],
  "deprecated": []
}
```

Rules: contracts are **reviewed like code** (a change here is a cross-team event); versions follow semantic versioning where minor = compatible additions and major = breaking; and deprecations are listed explicitly for at least one full version before removal.

## 6. Why implicit contracts fail in AI pipelines

The failure is specific to systems where the *data is the product*:

- **Silent field loss** — an importer refactor drops `book` from the dict; the indexer stores citations as `?/p5`; no error raises because dicts don't enforce keys. A contract test would have raised at CI.
- **Semantic drift** — `page` starts meaning PDF page instead of physical edition page; retrieval returns correct-looking wrong citations. Only semantics in the contract catch this.
- **Normalization divergence** — one component stores normalized text, another expects verbatim; the citation quotes folded letters. The `text` semantic ("verbatim NFC, never normalized") prevents it.

Each of these is invisible to shape-only checking and caught by contract tests.

## 7. Best-practice checklist

| Practice | Payoff |
|---|---|
| Four-part contract (shape+semantics+invariants+version) | disagreement surfaces early |
| Classify every change before shipping | compatible vs migration vs breaking is explicit |
| New required fields via emit-default → backfill → require | rolling upgrades never break |
| Contract tests on producer AND consumer CI | drift caught at build, not at 3 a.m. |
| Versioned contract artifacts | both teams find the same truth |
| Deprecate for one full version before removal | consumers get a migration window |
| Invariant failures name the rule and values | debugging is reading one log line |
| Semantic fields documented in the contract | "page means what?" has one answer |

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Shape checked, semantics undocumented | write the meaning next to the field |
| Required field added in one deploy | emit-default first, require last |
| Contract lives in one team's code | shared versioned artifact |
| Invariant violated but no named error | validate_payload names the rule |
| Consumers assume fields exist | consumer tolerates supported versions |
| Rename in place | dual-write old+new, migrate, drop old |
| "We'll document it later" | the contract IS the documentation |

---

## Mastery Check

You can claim this topic when you can:

1. Write the four parts of the record contract for a new field.
2. Classify three sample changes (add optional, add required, remove) correctly.
3. Design the four-step migration for a new required field and say why each step is safe.
4. Write both contract tests and see the producer-side version-boundary test fail when it should.
5. Point at the versioned artifact your two services share.

---

## Next Steps

- Async boundaries: `02-queues-and-workflows/`.
- Stale indexes and consistency: `03-consistency-and-staleness/`.
- What breaks when a contract fails at runtime: `04-failure-modes-and-resilience/`.
