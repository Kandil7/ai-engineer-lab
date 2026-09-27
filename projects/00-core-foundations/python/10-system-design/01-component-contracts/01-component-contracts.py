"""
Component Contracts - System Design Exercises
==============================================
Topics: contracts between components, explicit interfaces, versioning,
producer/consumer agreement, schema evolution at service boundaries,
contract testing at the system level.

Why this matters for AI engineering:
    An Athar pipeline is four services agreeing on shapes: the importer
    produces records, the indexer consumes them, /search serves them,
    /answer cites them. When the contract between them is implicit
    (shared dict, "same team"), every change is a cross-team incident.
    This file makes contracts explicit: named schemas, version fields,
    compatibility rules, and the compatibility test that fails before
    deployment when a producer breaks a consumer.

Environment note:
    Pure standard library. Runnable offline.

Run:      python 01-component-contracts.py
Verify:   python 01-component-contracts.py --verify
Reference: https://microservices.io/patterns/contract-test.html
"""

from __future__ import annotations

import copy
import json
import sys
from dataclasses import dataclass, field

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


# ============================================================
# 1. What a component contract is
# ============================================================
# A contract is the DOCUMENTED, TESTED agreement between producer and
# consumer. It has four parts:
#   1. Shape       - fields, types, nullability (the schema)
#   2. Semantics   - what each field MEANS (book is canonical title,
#                    page is 1-based physical page in that edition)
#   3. Invariants  - what is always true (source_ref unique; text nonempty)
#   4. Version     - what changed and how consumers migrate
# Shape alone is a wire format. The contract is shape + meaning + rules.

print("1. the four parts of a contract")
print("   shape      fields/types/nullability")
print("   semantics  what each field means")
print("   invariants what is always true")
print("   version    what changed + migration path")
print()


# ============================================================
# 2. The Athar record contract
# ============================================================


@dataclass(frozen=True)
class RecordContract:
    """The agreement between importer and indexer."""

    name: str
    version: str
    required: dict[str, str] = field(default_factory=dict)  # field -> semantic type
    invariants: tuple[str, ...] = ()
    deprecated: tuple[str, ...] = ()


ATHAR_V1 = RecordContract(
    name="athar.record",
    version="1.0",
    required={
        "id": "str, unique, immutable",
        "book": "str, canonical Arabic title",
        "page": "int, 1-based, physical page in edition",
        "text": "str, verbatim NFC, never normalized",
    },
    invariants=("source_ref == f'{book}/p{page}'", "text.strip() != ''"),
    deprecated=(),
)

ATHAR_V2 = RecordContract(
    name="athar.record",
    version="2.0",
    required={
        "id": "str, unique, immutable",
        "book": "str, canonical Arabic title",
        "page": "int, 1-based, physical page in edition",
        "text": "str, verbatim NFC, never normalized",
        "edition": "str, edition label; default 'default'",  # NEW
    },
    invariants=("source_ref == f'{book}/p{page}'", "text.strip() != ''"),
    deprecated=(),  # v1 records lacking edition are backfilled, not broken
)

print("2. the Athar record contract")
print(f"   v1 fields: {sorted(ATHAR_V1.required)}")
print(f"   v2 fields: {sorted(ATHAR_V2.required)}")
print()


# ============================================================
# 3. Compatibility rules - what changes break consumers
# ============================================================
# Change type        Compatible?  Who migrates
# ------------------------------------------------------------
# add optional field   YES        nobody (consumer may ignore)
# add required field   NO         producer ships default first
# remove field         NO         deprecate 2 versions, then remove
# change field meaning NO         new field name + deprecation
# tighten invariant    MAYBE      depends if consumers relied on gap
# rename field         NO         dual-write, migrate consumers, drop


def classify_change(old: RecordContract, new: RecordContract) -> str:
    """Return 'compatible', 'breaking', or 'needs-migration'."""
    removed = set(old.required) - set(new.required)
    added = set(new.required) - set(old.required)
    added_required = {f for f in added if "optional" not in new.required[f]}
    changed = {
        f for f in set(old.required) & set(new.required) if old.required[f] != new.required[f]
    }
    if removed or changed:
        return "breaking"
    if added_required:
        return "needs-migration"
    return "compatible"


print("3. compatibility classification")
print(f"   v1 -> v2 : {classify_change(ATHAR_V1, ATHAR_V2)} (added required 'edition')")

V2_OPTIONAL = RecordContract(
    name="athar.record",
    version="2.1",
    required=dict(ATHAR_V2.required),
    invariants=ATHAR_V2.invariants,
    deprecated=("edition_migrated_at",),
)
V2_OPTIONAL.required["edition_migrated_at"] = "ts, optional, backfill marker"
print(f"   v2 -> v2.1 (added optional): {classify_change(ATHAR_V2, V2_OPTIONAL)}")

V3_REMOVED = RecordContract(
    name="athar.record",
    version="3.0",
    required={"id": "str, unique, immutable", "text": "str"},
    invariants=(),
)
print(f"   v2 -> v3 (fields removed): {classify_change(ATHAR_V2, V3_REMOVED)}")
print()


# ============================================================
# 4. Contract test at the system level
# ============================================================
# The producer's serializer must satisfy the consumer's expectation.
# This runs in CI for BOTH sides: producer CI proves it emits the
# contract; consumer CI proves it tolerates every supported version.


def validate_payload(payload: dict, contract: RecordContract) -> list[str]:
    """Check a payload against the contract. Empty list = contract holds."""
    problems = []
    for fname, semantic in contract.required.items():
        if fname not in payload:
            # fields whose semantic says 'optional' are tolerated
            if "optional" in semantic:
                continue
            problems.append(f"missing required field: {fname} ({semantic})")
    for inv in contract.invariants:
        if inv == "text.strip() != ''":
            if not str(payload.get("text", "")).strip():
                problems.append("invariant violated: text is empty")
        if inv == "source_ref == f'{book}/p{page}'":
            ref = payload.get("source_ref")
            expected = f"{payload.get('book')}/p{payload.get('page')}"
            if ref is not None and ref != expected:
                problems.append(f"invariant violated: source_ref {ref!r} != {expected!r}")
    return problems


def producer_emits_v1() -> dict:
    """What the current importer emits (v1 shape)."""
    return {
        "id": "r1",
        "book": "بخاري",
        "page": 5,
        "text": "نص",
        "source_ref": "بخاري/p5",
    }


print("4. system-level contract test")
good = producer_emits_v1()
print(f"   v1 payload vs v1 contract : {validate_payload(good, ATHAR_V1) or 'CLEAN'}")
print(f"   v1 payload vs v2 contract : {validate_payload(good, ATHAR_V2)}")
print(f"   (v1 producer fails v2 consumer until edition is shipped)")
print()


# ============================================================
# 5. The migration path - how v1 producers reach v2
# ============================================================
# The safe sequence for adding a REQUIRED field:
#   step 1: producer emits the new field with a default  (v2 optional)
#   step 2: consumers read it when present (tolerate both)
#   step 3: backfill historical rows
#   step 4: contract tightens: field becomes required (v2 final)
# At every step BOTH old and new versions must work.


def producer_emits_v2_transitional() -> dict:
    """Producer upgraded to emit edition with default."""
    rec = producer_emits_v1()
    rec["edition"] = "default"
    return rec


print("5. migration path for a new required field")
rec2 = producer_emits_v2_transitional()
print(f"   transitional payload vs v2 : {validate_payload(rec2, ATHAR_V2) or 'CLEAN'}")
print("   sequence: emit-with-default -> consumers read -> backfill -> require")
print()


# ============================================================
# 6. Contract storage and discoverability
# ============================================================
# Contracts must live where both teams find them: versioned JSON files
# (or protobuf/JSON Schema), referenced by the services' repos. A dict
# in someone's head is not a contract.


def write_contract_json(contract: RecordContract) -> str:
    """Serialize a contract to JSON for the shared contract repo."""
    return json.dumps(
        {
            "name": contract.name,
            "version": contract.version,
            "required": contract.required,
            "invariants": list(contract.invariants),
            "deprecated": list(contract.deprecated),
        },
        ensure_ascii=False,
        indent=2,
    )


print("6. contract as a versioned artifact")
print(write_contract_json(ATHAR_V2))
print()


# ============================================================
# 7. Self-verification
# ============================================================


def _verify() -> bool:
    checks: list[tuple[str, bool]] = []
    checks.append(
        ("v1 payload satisfies v1 contract", validate_payload(producer_emits_v1(), ATHAR_V1) == [])
    )
    checks.append(
        (
            "v1 payload FAILS v2 contract (edition missing)",
            any("edition" in p for p in validate_payload(producer_emits_v1(), ATHAR_V2)),
        )
    )
    checks.append(
        (
            "v2 payload satisfies v2 contract",
            validate_payload(producer_emits_v2_transitional(), ATHAR_V2) == [],
        )
    )
    checks.append(
        (
            "add-required classified as needs-migration",
            classify_change(ATHAR_V1, ATHAR_V2) == "needs-migration",
        )
    )
    checks.append(
        (
            "add-optional classified as compatible",
            classify_change(ATHAR_V2, V2_OPTIONAL) == "compatible",
        )
    )
    checks.append(
        ("remove-field classified as breaking", classify_change(ATHAR_V2, V3_REMOVED) == "breaking")
    )
    checks.append(
        (
            "invariant: empty text detected",
            validate_payload({"id": "x", "text": "  "}, ATHAR_V1) != [],
        )
    )
    checks.append(
        (
            "invariant: bad source_ref detected",
            validate_payload(
                {"id": "x", "book": "b", "page": 3, "text": "t", "source_ref": "wrong"}, ATHAR_V1
            )
            != [],
        )
    )
    ok = True
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    return ok


if __name__ == "__main__":
    if "--verify" in sys.argv:
        print("Verification:")
        sys.exit(0 if _verify() else 1)
    print("Verification (python 01-component-contracts.py --verify):")
    _verify()
