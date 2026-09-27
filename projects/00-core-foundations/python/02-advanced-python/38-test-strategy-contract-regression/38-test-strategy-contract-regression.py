"""
Test Strategy: Unit, Integration, Contract, Regression, Data Tests
==================================================================
Topics: test pyramid, unit vs integration boundaries, contract tests,
regression locks (golden files), data/pipeline tests, idempotency checks,
property-style invariants.

Why this matters for AI engineering:
    The skills-map criterion: "text, book, and page never get lost through
    the pipeline; reruns never duplicate; 20 known failure cases never
    return." That is not one test type - it is four. Unit tests pin the
    rules; integration tests pin the wiring; contract tests pin the
    boundaries between teams; regression tests pin the bugs; data tests
    pin the corpus invariants. This file builds one test of each type
    against a miniature ingest->store pipeline so you can see where each
    one belongs and what each one can and cannot catch.

Environment note:
    Pure standard library. Demonstrations run inline; the pytest forms
    are shown as strings so this file runs standalone.

Run:      python 38-test-strategy-contract-regression.py
Verify:   python 38-test-strategy-contract-regression.py --verify
Reference: https://docs.pytest.org/en/stable/how-to/fixtures.html
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]


# ============================================================
# The system under test: a tiny ingest pipeline
# ============================================================


@dataclass
class Record:
    record_id: str
    book: str
    page: int
    text: str
    source_ref: str


@dataclass
class Store:
    """Toy store with a real failure mode: duplicate insert on rerun."""

    rows: dict[str, Record] = field(default_factory=dict)
    insert_log: list[str] = field(default_factory=list)

    def insert(self, rec: Record) -> bool:
        """Insert idempotently. Returns True if newly stored, False if dup."""
        self.insert_log.append(rec.record_id)
        if rec.record_id in self.rows:
            return False
        self.rows[rec.record_id] = rec
        return True

    def get(self, record_id: str) -> Record | None:
        return self.rows.get(record_id)


def parse_line(line: str, line_no: int) -> Record:
    obj = json.loads(line)
    record_id = str(obj["id"])
    if not record_id:
        raise ValueError(f"line {line_no}: empty id: empty id")
    page_raw = str(obj["page"])
    # Arabic-Indic digits fold to ASCII before parsing (see topic 35)
    page = int(page_raw.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")))
    if page <= 0:
        raise ValueError(f"line {line_no}: page must be positive: page zero")
    return Record(
        record_id=record_id,
        book=str(obj["book"]),
        page=page,
        text=str(obj["text"]),
        source_ref=f"{obj['book']}/p{obj['page']}",
    )


def ingest(lines: list[str], store: Store) -> dict[str, int]:
    imported, skipped = 0, 0
    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        rec = parse_line(line, line_no)
        if store.insert(rec):
            imported += 1
        else:
            skipped += 1
    return {"imported": imported, "skipped_duplicates": skipped}


# ============================================================
# 1. UNIT TESTS - one rule, no I/O, milliseconds
# ============================================================
# Catch: logic errors in parsing and rules. Cannot catch: wiring bugs,
# schema drift at the boundary, real-store semantics. Keep them fast and
# pure; every test runs anywhere, offline.


def unit_parse_builds_source_ref() -> bool:
    rec = parse_line('{"id": "a", "book": "bukhari", "page": "7", "text": "نص"}', 1)
    return rec.source_ref == "bukhari/p7" and rec.page == 7


def unit_store_rejects_duplicate() -> bool:
    store = Store()
    rec = Record("x", "b", 1, "t", "b/p1")
    return store.insert(rec) is True and store.insert(rec) is False


print("1. unit tests (pure, fast, offline)")
print(f"   parse builds source_ref: {unit_parse_builds_source_ref()}")
print(f"   store rejects duplicate: {unit_store_rejects_duplicate()}")
print()


# ============================================================
# 2. INTEGRATION TESTS - the wiring, still hermetic
# ============================================================
# Catch: layer handoff bugs (parse->store field loss, counter drift).
# Cannot catch: production store semantics, network failure. Use a real
# (temporary) store of the same shape - sqlite in a temp file is the
# standard stand-in for Postgres - and assert end state, not internals.


def integration_no_loss_of_provenance() -> bool:
    """Text, book, page survive the pipeline byte-for-byte."""
    store = Store()
    lines = [
        json.dumps(
            {"id": "r1", "book": "bukhari", "page": "1", "text": "النص الأصلي"}, ensure_ascii=False
        ),
        json.dumps(
            {"id": "r2", "book": "muslim", "page": "2", "text": "نص آخر"}, ensure_ascii=False
        ),
    ]
    ingest(lines, store)
    r1 = store.get("r1")
    return (
        r1 is not None
        and r1.text == "النص الأصلي"
        and r1.book == "bukhari"
        and r1.page == 1
        and r1.source_ref == "bukhari/p1"
    )


def integration_rerun_is_idempotent() -> bool:
    """Skills criterion: a rerun must not duplicate."""
    store = Store()
    lines = [json.dumps({"id": "r1", "book": "b", "page": "1", "text": "نص"})]
    first = ingest(lines, store)
    second = ingest(lines, store)
    return (
        first == {"imported": 1, "skipped_duplicates": 0}
        and second == {"imported": 0, "skipped_duplicates": 1}
        and len(store.rows) == 1
    )


print("2. integration tests (wiring, hermetic)")
print(f"   provenance survives: {integration_no_loss_of_provenance()}")
print(f"   rerun idempotent   : {integration_rerun_is_idempotent()}")
print()


# ============================================================
# 3. CONTRACT TESTS - the boundary between producers and consumers
# ============================================================
# Catch: schema drift when another team's writer changes. A contract
# test asserts the SHAPE a consumer depends on: required fields, types,
# nullability. It runs against the producer's code AND is versioned with
# the consumer's expectations. If the producer changes the shape, this
# test fails BEFORE production does.

REQUIRED_FIELDS = {"id": "str", "book": "str", "page": "int-like", "text": "str"}


def contract_payload_matches_consumer_schema(payload: dict) -> list[str]:
    """Return a list of contract violations (empty = contract holds)."""
    violations = []
    for name, expected in REQUIRED_FIELDS.items():
        if name not in payload:
            violations.append(f"missing field: {name}")
            continue
        value = payload[name]
        if expected == "str" and not isinstance(value, str):
            violations.append(f"{name} must be str, got {type(value).__name__}")
        if expected == "int-like":
            try:
                int(str(value))
            except ValueError:
                violations.append(f"{name} must be int-like, got {value!r}")
    return violations


def contract_producer_keeps_schema() -> bool:
    good = {"id": "a", "book": "b", "page": "3", "text": "t"}
    bad = {"id": "a", "book": "b"}  # producer stopped sending page/text
    return (
        contract_payload_matches_consumer_schema(good) == []
        and len(contract_payload_matches_consumer_schema(bad)) == 2
    )


print("3. contract tests (producer/consumer boundary)")
print(f"   schema enforcement works: {contract_producer_keeps_schema()}")
print(
    f"   violations for bad payload: {contract_payload_matches_consumer_schema({'id': 'a', 'book': 'b'})}"
)
print()


# ============================================================
# 4. REGRESSION TESTS - pin every bug forever
# ============================================================
# Catch: the same bug returning after a later change. Rule: every
# production bug gets a failing test FIRST, then the fix. The suite
# becomes the "20 known failure cases" that never return. Keep the case
# data as golden fixtures (stored JSONL) so the scenario cannot drift.

KNOWN_FAILURE_CASES = [
    # (case_id, input_line, expected_outcome)
    ("KF-01", '{"id": "", "book": "b", "page": "1", "text": "t"}', "reject: empty id"),
    ("KF-02", '{"id": "a", "book": "b", "page": "0", "text": "t"}', "reject: page zero"),
    ("KF-03", '{"id": "a", "book": "b", "page": "١٢", "text": "t"}', "accept after digit fold"),
]


def regression_case_returns(case: tuple[str, str, str]) -> bool:
    """Run one known-failure case and check the outcome never regresses."""
    case_id, line, expected = case
    try:
        rec = parse_line(line, 1)
    except Exception:
        return expected.startswith("reject")
    if expected.startswith("reject"):
        return False
    return rec.record_id != ""


def regression_suite_holds() -> bool:
    return all(regression_case_returns(c) for c in KNOWN_FAILURE_CASES)


print("4. regression tests (known failures pinned)")
print(f"   suite holds: {regression_suite_holds()}")
for case_id, _line, expected in KNOWN_FAILURE_CASES:
    print(f"   {case_id}: {expected}")
print()


# ============================================================
# 5. DATA / PIPELINE TESTS - corpus-level invariants
# ============================================================
# Catch: silent data loss and duplication across runs. These are not
# about one record - they are about totals, provenance, and identity.
# Run them as a batch job over the real corpus after every ingest.


def data_invariants_hold(before: list[dict], after: dict[str, Record]) -> list[str]:
    """Return invariant violations for one ingest run (empty = clean)."""
    problems = []
    source_ids = {str(b["id"]) for b in before if b.get("id")}
    stored_ids = set(after.keys())
    lost = source_ids - stored_ids
    if lost:
        problems.append(f"lost records: {sorted(lost)[:5]}")
    phantom = stored_ids - source_ids
    if phantom:
        problems.append(f"phantom records (never in source): {sorted(phantom)[:5]}")
    for rid, rec in after.items():
        if not rec.text.strip():
            problems.append(f"{rid}: empty text stored")
        if not rec.source_ref.startswith(rec.book):
            problems.append(f"{rid}: source_ref does not carry book/page")
    return problems


def data_test_clean_run() -> bool:
    before = [
        {"id": "d1", "book": "bukhari", "page": "1", "text": "نص"},
        {"id": "d2", "book": "muslim", "page": "2", "text": "نص آخر"},
    ]
    store = Store()
    ingest([json.dumps(b, ensure_ascii=False) for b in before], store)
    return data_invariants_hold(before, store.rows) == []


def data_test_detects_loss() -> bool:
    before = [
        {"id": "d1", "book": "bukhari", "page": "1", "text": "نص"},
        {"id": "d2", "book": "muslim", "page": "2", "text": "نص آخر"},
    ]
    store = Store()
    ingest([json.dumps(before[0], ensure_ascii=False)], store)  # d2 lost
    problems = data_invariants_hold(before, store.rows)
    return any("lost records" in p for p in problems)


print("5. data tests (corpus invariants)")
print(f"   clean run reports nothing : {data_test_clean_run()}")
print(f"   loss is detected          : {data_test_detects_loss()}")
print()


# ============================================================
# 6. Where each type lives in the pyramid
# ============================================================
#      /\        E2E (few, slow, real deps)      -> nightly
#     /  \       Integration (wiring, hermetic)  -> every PR
#    /    \      Unit + Contract (pure, fast)    -> every save
#   /______\

TEST_PYRAMID = {
    "unit": {"scope": "one rule", "deps": "none", "speed": "< 1ms", "cadence": "every save"},
    "contract": {
        "scope": "producer/consumer schema",
        "deps": "none",
        "speed": "< 1ms",
        "cadence": "every PR",
    },
    "integration": {
        "scope": "layer wiring",
        "deps": "temp store",
        "speed": "< 100ms",
        "cadence": "every PR",
    },
    "regression": {
        "scope": "pinned bugs",
        "deps": "fixtures",
        "speed": "varies",
        "cadence": "every PR",
    },
    "data": {
        "scope": "corpus invariants",
        "deps": "real corpus",
        "speed": "seconds+",
        "cadence": "post-ingest",
    },
}

print("6. test pyramid placement")
for kind, spec in TEST_PYRAMID.items():
    print(f"   {kind:12} {spec['scope']:28} {spec['cadence']}")
print()


# ============================================================
# 7. The pytest forms (for the real suite)
# ============================================================
# This file runs standalone, so the pytest versions live as strings.
# Copy these into tests/ in the real project.

PYTEST_FORMS = """
# test_pipeline.py
import json, pytest
from devmate.pipeline import parse_line, ingest, Store

def test_parse_builds_source_ref():
    rec = parse_line('{"id":"a","book":"bukhari","page":"7","text":"t"}', 1)
    assert rec.source_ref == "bukhari/p7"

@pytest.mark.regression
@pytest.mark.parametrize("line,reason", [
    ('{"id":"","book":"b","page":"1","text":"t"}', "empty id"),
    ('{"id":"a","book":"b","page":"0","text":"t"}', "page zero"),
])
def test_known_failures_never_return(line, reason):
    with pytest.raises(ValueError, match=reason.split(":")[-1].strip() or ".*"):
        parse_line(line, 1)

@pytest.mark.data
def test_no_loss_no_phantom(tmp_path):
    before = [{"id":"d1","book":"b","page":"1","text":"t"}]
    store = Store()
    ingest([json.dumps(b) for b in before], store)
    assert set(store.rows) == {"d1"}
    assert store.rows["d1"].text == "t"          # text survives
    assert store.rows["d1"].source_ref == "b/p1"  # provenance survives
"""
print("7. pytest forms (copy into tests/)")
print(PYTEST_FORMS)


# ============================================================
# 8. Self-verification
# ============================================================


def _verify() -> bool:
    checks = [
        ("unit: parse", unit_parse_builds_source_ref()),
        ("unit: dedup", unit_store_rejects_duplicate()),
        ("integration: provenance", integration_no_loss_of_provenance()),
        ("integration: idempotent rerun", integration_rerun_is_idempotent()),
        ("contract: schema gate", contract_producer_keeps_schema()),
        ("regression: suite holds", regression_suite_holds()),
        ("data: clean run", data_test_clean_run()),
        ("data: loss detected", data_test_detects_loss()),
    ]
    ok = True
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    return ok


if __name__ == "__main__":
    if "--verify" in sys.argv:
        print("Verification:")
        sys.exit(0 if _verify() else 1)
    print("Verification (python 38-test-strategy-contract-regression.py --verify):")
    _verify()
