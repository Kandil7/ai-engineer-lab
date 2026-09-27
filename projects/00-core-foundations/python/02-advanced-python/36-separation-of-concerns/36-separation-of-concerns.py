"""
Separation of Concerns - Advanced Python Exercises
===================================================
Topics: single responsibility, protocols/interfaces, dependency injection,
configuration objects, logging, layered pipeline (parser -> normalizer ->
validator -> indexer -> API).

Why this matters for AI engineering:
    An Athar-style RAG system mixes four hard-to-change concerns in one
    request: parsing source texts, normalizing Arabic, validating
    references (book/page/sanad rules), and searching an index. When they
    live in one function you cannot replace the search engine without
    re-testing the reference rules. This file builds a layered pipeline
    where each layer has one job and is wired by dependency injection, so
    the searcher is a Protocol you can swap while the validator - and its
    tests - stay untouched.

Environment note:
    Pure standard library (dataclasses, abc, logging, typing).

Run:      python 36-separation-of-concerns.py
Verify:   python 36-separation-of-concerns.py --verify
Reference: https://docs.python.org/3/library/typing.html#typing.Protocol
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable, Protocol, runtime_checkable

if hasattr(__import__("sys").stdout, "reconfigure"):
    __import__("sys").stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]

logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("athar.pipeline")


# ============================================================
# 1. Configuration - one object, no globals, no env guessing
# ============================================================
# Config is data. Read it once at startup, pass it down explicitly.
# A function that reads os.environ deep inside is untestable: you cannot
# run two configurations in one process.


@dataclass(frozen=True)
class PipelineConfig:
    """Immutable settings the whole pipeline reads."""

    strict_pages: bool = True
    min_text_length: int = 3
    default_index_backend: str = "memory"


config = PipelineConfig()
print(f"1. config: strict_pages={config.strict_pages} min_text={config.min_text_length}")
print()


# ============================================================
# 2. Layer 1 - the parser: bytes/lines in, RawRecord out
# ============================================================
# One job: turn untrusted input into a structure. It does NOT decide
# what a valid reference is (that is the validator) and does NOT know
# about search (that is the indexer).


@dataclass
class RawRecord:
    record_id: str
    book: str
    page: str
    text: str


class ParseError(ValueError):
    """Input could not be parsed at all (as opposed to invalid)."""


def parse_line(line: str, line_no: int) -> RawRecord:
    """Parse one JSONL line. Only structure - never semantics."""
    try:
        obj = json.loads(line)
    except json.JSONDecodeError as exc:
        raise ParseError(f"line {line_no}: invalid JSON: {exc.msg}") from exc
    if not isinstance(obj, dict):
        raise ParseError(f"line {line_no}: expected object")
    missing = [k for k in ("id", "book", "page", "text") if k not in obj]
    if missing:
        raise ParseError(f"line {line_no}: missing {', '.join(missing)}")
    return RawRecord(str(obj["id"]), str(obj["book"]), str(obj["page"]), str(obj["text"]))


print("2. parser: raw line -> RawRecord (structure only)")
print(f"   {parse_line('{"id": "a1", "book": "bukhari", "page": "5", "text": "نص"}', 1)}")
print()


# ============================================================
# 3. Layer 2 - the normalizer: text in, clean text out
# ============================================================
# One job: make text comparable and searchable. It never raises for
# "wrong content" - that is the validator's call. It is a pure function:
# same input, same output, no I/O, no config reads.


HARAKAT = set(range(0x064B, 0x0653)) | {0x0670}


def normalize_text(text: str) -> str:
    """Strip diacritics and collapse whitespace. Pure and total."""
    import unicodedata

    text = unicodedata.normalize("NFKC", text)
    text = "".join(ch for ch in text if ord(ch) not in HARAKAT)
    return " ".join(text.split())


print("3. normalizer: pure function, no side effects")
print(f"   normalize_text('مُحَمَّد   الرسول') -> {normalize_text('مُحَمَّد   الرسول')!r}")
print()


# ============================================================
# 4. Layer 3 - the validator: business rules, swappable by config
# ============================================================
# One job: decide whether a record is semantically valid. The rules are
# THE asset of a reference system; they must not import search, storage,
# or HTTP. Notice this layer has zero dependencies on layers 1/2 outputs
# beyond the plain dataclass.


@dataclass
class ValidatedRecord:
    record_id: str
    book: str
    page: int
    text: str
    search_key: str


class ValidationError(ValueError):
    """A record is structurally fine but violates reference rules."""


def validate_record(raw: RawRecord, cfg: PipelineConfig) -> ValidatedRecord:
    """Apply reference rules. Returns a validated record or raises."""
    if not raw.text.strip():
        raise ValidationError(f"{raw.record_id}: empty text")
    if len(raw.text.strip()) < cfg.min_text_length:
        raise ValidationError(f"{raw.record_id}: text too short")
    if cfg.strict_pages:
        try:
            page = int(raw.page)
        except ValueError as exc:
            raise ValidationError(f"{raw.record_id}: page not numeric: {raw.page!r}") from exc
        if page <= 0:
            raise ValidationError(f"{raw.record_id}: page must be positive, got {page}")
    else:
        page = int(raw.page) if raw.page.strip().lstrip("-").isdigit() else 0
    return ValidatedRecord(
        record_id=raw.record_id,
        book=raw.book,
        page=page,
        text=raw.text.strip(),
        search_key=normalize_text(raw.text),
    )


print("4. validator: reference rules isolated from everything else")
try:
    validate_record(RawRecord("x1", "bukhari", "-3", "نص صالح"), config)
except ValidationError as exc:
    print(f"   rejected: {exc}")
print()


# ============================================================
# 5. Layer 4 - the indexer behind a Protocol (THIS is the seam)
# ============================================================
# A Protocol defines the contract any search backend must satisfy. The
# pipeline depends on the Protocol, never on a concrete engine. Swapping
# the engine is one line of wiring; the validator is not even imported
# by the engine, so its rules cannot break.


@runtime_checkable
class SearchIndex(Protocol):
    """Contract: anything that can be indexed and queried."""

    def add(self, record: ValidatedRecord) -> None: ...
    def search(self, query: str, limit: int = 5) -> list[ValidatedRecord]: ...


class InMemoryIndex:
    """Implementation A: naive substring matching over a dict."""

    def __init__(self) -> None:
        self._records: dict[str, ValidatedRecord] = {}

    def add(self, record: ValidatedRecord) -> None:
        self._records[record.record_id] = record

    def search(self, query: str, limit: int = 5) -> list[ValidatedRecord]:
        q = normalize_text(query)
        hits = [r for r in self._records.values() if q in r.search_key]
        return hits[:limit]


class PrefixIndex:
    """Implementation B: prefix matching - deliberately different engine."""

    def __init__(self) -> None:
        self._by_prefix: dict[str, list[ValidatedRecord]] = {}

    def add(self, record: ValidatedRecord) -> None:
        key = record.search_key[:3] if len(record.search_key) >= 3 else record.search_key
        self._by_prefix.setdefault(key, []).append(record)

    def search(self, query: str, limit: int = 5) -> list[ValidatedRecord]:
        q = normalize_text(query)
        key = q[:3] if len(q) >= 3 else q
        return self._by_prefix.get(key, [])[:limit]


# Liskov check at runtime: both implementations satisfy the Protocol
print("5. indexer Protocol: both engines satisfy the contract")
print(f"   InMemoryIndex is SearchIndex: {isinstance(InMemoryIndex(), SearchIndex)}")
print(f"   PrefixIndex   is SearchIndex: {isinstance(PrefixIndex(), SearchIndex)}")
print()


# ============================================================
# 6. Dependency injection - the assembler is the only place that
#    knows concrete classes
# ============================================================
# The pipeline takes its collaborators as constructor arguments. Test
# code injects fakes; production injects real engines. No isinstance
# checks, no if-else backend selection inside business logic.


class Pipeline:
    """Orchestrates layers without owning any of them."""

    def __init__(self, index: SearchIndex, cfg: PipelineConfig) -> None:
        self._index = index
        self._cfg = cfg

    def ingest(self, lines: Iterable[str]) -> dict[str, list[str]]:
        """Parse -> validate -> index. Returns per-line error report."""
        errors: list[str] = []
        imported = 0
        for line_no, line in enumerate(lines, start=1):
            if not line.strip():
                continue
            try:
                raw = parse_line(line, line_no)
                validated = validate_record(raw, self._cfg)
            except (ParseError, ValidationError) as exc:
                errors.append(str(exc))
                log.warning("skipping record: %s", exc)
                continue
            self._index.add(validated)
            imported += 1
        return {"imported": [str(imported)], "errors": errors}

    def search(self, query: str, limit: int = 5) -> list[dict[str, object]]:
        """Query the index - endpoint code stays a one-liner."""
        return [
            {"id": r.record_id, "book": r.book, "page": r.page, "text": r.text}
            for r in self._index.search(query, limit)
        ]


def make_pipeline(engine: str = "memory") -> Pipeline:
    """Composition root: the ONLY place naming concrete classes."""
    index: SearchIndex = InMemoryIndex() if engine == "memory" else PrefixIndex()
    return Pipeline(index, config)


print("6. dependency injection: composition root wires the graph")
pipe = make_pipeline("memory")
result = pipe.ingest(
    [
        '{"id": "r1", "book": "bukhari", "page": "1", "text": "إنما الأعمال بالنيات"}',
        '{"id": "r2", "book": "bukhari", "page": "2", "text": "الدين النصيحة"}',
        '{"id": "r3", "book": "bukhari", "page": "x", "text": "سجل معطوب"}',
    ]
)
print(f"   ingest report: {result}")
print(f"   search 'الدين' -> {pipe.search('الدين')}")
print()


# ============================================================
# 7. THE MASTERY TEST - swap the engine, rules untouched
# ============================================================
# Skills-map criterion: "replace the search engine without touching the
# reference validation rules." We run the identical input through both
# engines and the identical validation outcomes come out.


def run_both_engines(lines: list[str]) -> dict[str, dict[str, object]]:
    """Same input, two engines, identical validation semantics."""
    out: dict[str, dict[str, object]] = {}
    for engine in ("memory", "prefix"):
        pipe = make_pipeline(engine)
        report = pipe.ingest(lines)
        out[engine] = {"errors": report["errors"], "hits": pipe.search("الدين", limit=5)}
    return out


print("7. mastery test: swap engine -> validation rules unchanged")
demo_lines = [
    '{"id": "a", "book": "bukhari", "page": "1", "text": "الدين النصيحة"}',
    '{"id": "b", "book": "bukhari", "page": "-9", "text": "صفحة سالبة"}',
]
comparison = run_both_engines(demo_lines)
print(f"   memory engine : errors={comparison['memory']['errors']}")
print(f"   prefix engine : errors={comparison['prefix']['errors']}")
print(f"   error sets equal: {comparison['memory']['errors'] == comparison['prefix']['errors']}")
print()


# ============================================================
# 8. Logging - structured, levelled, and replaceable
# ============================================================
# Rules: libraries log through a named logger and never configure
# handlers; the application configures logging once at startup. Never
# print() in library code - it cannot be silenced, redirected, or tested.

log.setLevel(logging.INFO)
log.info("pipeline ready: engine=%s", config.default_index_backend)
print("8. logging: named loggers, configured once, never print() in libs")
print()


# ============================================================
# 9. Self-verification
# ============================================================


class SpyIndex:
    """A test double proving the pipeline never reaches around the Protocol."""

    def __init__(self) -> None:
        self.added: list[str] = []
        self.queries: list[str] = []

    def add(self, record: ValidatedRecord) -> None:
        self.added.append(record.record_id)

    def search(self, query: str, limit: int = 5) -> list[ValidatedRecord]:
        self.queries.append(query)
        return []


def _verify() -> bool:
    checks: list[tuple[str, bool]] = []

    checks.append(("normalizer is pure", normalize_text("مُحَمَّد") == normalize_text("محمد")))

    try:
        validate_record(RawRecord("v", "b", "-1", "نص"), PipelineConfig(strict_pages=True))
        checks.append(("validator rejects negative page", False))
    except ValidationError:
        checks.append(("validator rejects negative page", True))

    loose = PipelineConfig(strict_pages=False, min_text_length=1)
    ok = validate_record(RawRecord("v", "b", "-1", "نص طويل بما فيه"), loose).page == -1
    checks.append(("loose config accepts (config-driven rules)", ok))

    checks.append(
        (
            "both engines are SearchIndex",
            isinstance(InMemoryIndex(), SearchIndex) and isinstance(PrefixIndex(), SearchIndex),
        )
    )

    spy = SpyIndex()
    p = Pipeline(spy, config)
    p.ingest(['{"id": "s1", "book": "b", "page": "1", "text": "نص سليم"}'])
    p.search("نص")
    checks.append(
        ("pipeline talks only to the Protocol", spy.added == ["s1"] and spy.queries == ["نص"])
    )

    comp = run_both_engines(demo_lines)
    checks.append(
        (
            "engine swap leaves validation identical",
            comp["memory"]["errors"] == comp["prefix"]["errors"],
        )
    )

    ok = True
    for name, passed in checks:
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")
        ok = ok and passed
    return ok


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        print("Verification:")
        sys.exit(0 if _verify() else 1)
    print("Verification (python 36-separation-of-concerns.py --verify):")
    _verify()
