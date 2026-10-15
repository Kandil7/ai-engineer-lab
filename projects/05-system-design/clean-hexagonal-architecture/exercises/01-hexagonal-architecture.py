"""
Exercise 01: Hexagonal Architecture Layer Checker
=================================================
Check the inward-only dependency rule the way a reviewer would: run the
eight HEX rules from Lecture 01 against a module pack and flag domain
imports of technical packages, application imports of concrete adapters,
outward infrastructure links, leaky port signatures, incomplete port
implementations, multi-responsibility step names, hardcoded models and
URLs, and application code reaching for infrastructure without a seam.

The demo runs the rules against two built-in packs: a BAD pack that trips
every rule, and a GOOD pack that must raise zero findings. It then runs
one AnswerQuestion use case against two Retriever adapters with identical
results asserted. No network. No GPU. No vector store.

Prerequisites:
    Python 3.11+ standard library only. No third-party packages.

Usage:
    python exercises/01-hexagonal-architecture.py
    python exercises/01-hexagonal-architecture.py path/to/modules.json
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

_SOURCE_TEXT = Path(__file__).read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# 1. Models
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """One rule violation in one module pack."""

    severity: str
    code: str
    line: int
    message: str


@dataclass
class ModuleSpec:
    """Declarative description of one module for the HEX rules."""

    name: str
    layer: str
    imports: list[str]
    implements: tuple[str, ...] = ()
    methods: tuple[str, ...] = ()
    has_config_seam: bool = False


@dataclass
class Analysis:
    """All findings for one module pack."""

    source: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "critical")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")


# ---------------------------------------------------------------------------
# 2. Marker-based line resolution
# ---------------------------------------------------------------------------


def _declared_line(label: str, marker: str) -> int:
    """Resolve a finding line by scanning this file for '# LABEL:marker'."""
    needle = f"# {label}:{marker}"
    for i, text in enumerate(_SOURCE_TEXT.splitlines(), start=1):
        if needle in text:
            return i
    return 0


# ---------------------------------------------------------------------------
# 3. Rule constants
# ---------------------------------------------------------------------------

TECHNICAL_PACKAGES = (
    "torch",
    "qdrant_client",
    "fastapi",
    "sqlalchemy",
    "transformers",
    "numpy",
    "requests",
)

PORT_SIGNATURE_LEAKS = (
    "torch",
    "QdrantClient",
    "qdrant_client",
    "fastapi",
    "sqlalchemy",
    "transformers",
    "numpy",
    "requests",
)

REQUIRED_RETRIEVER_METHODS = frozenset({"retrieve"})

RESPONSIBILITY_KEYWORDS = frozenset(
    {
        "chunk",
        "embed",
        "rerank",
        "train",
        "evaluate",
        "ingest",
        "tokenize",
        "retrieve",
        "generate",
        "upsert",
        "normalize",
    }
)

HARDCODED_TOKENS = (
    "gpt-",
    "bert-",
    "all-MiniLM",
    "text-embedding-",
    "http://",
    "https://",
    "localhost",
    ":6333",
)


def _method_names(methods: tuple[str, ...]) -> set[str]:
    names: set[str] = set()
    for raw in methods:
        head = raw.split("(", 1)[0].strip()
        head = head.split()[-1] if head else ""
        head = head.split(".")[-1].strip()
        if head:
            names.add(head)
    return names


def _responsibility_hits(name: str) -> list[str]:
    lowered = name.lower()
    return sorted(k for k in RESPONSIBILITY_KEYWORDS if k in lowered)


# ---------------------------------------------------------------------------
# 4. The eight HEX rules
# ---------------------------------------------------------------------------


def check_hex001(module: ModuleSpec) -> Finding | None:
    """Domain must not import technical packages."""
    if module.layer != "domain":
        return None
    for imp in module.imports:
        base = imp.split(".")[0]
        if base in TECHNICAL_PACKAGES or imp in TECHNICAL_PACKAGES:
            return Finding(
                severity="critical",
                code="HEX001",
                line=_declared_line("BAD", "HEX001"),
                message=f"domain module '{module.name}' imports '{imp}'",
            )
    return None


def check_hex002(module: ModuleSpec) -> Finding | None:
    """Application must depend on ports, not concrete adapters."""
    if module.layer != "application":
        return None
    for imp in module.imports:
        if "adapter" in imp.lower():
            return Finding(
                severity="critical",
                code="HEX002",
                line=_declared_line("BAD", "HEX002"),
                message=f"application module '{module.name}' imports adapter '{imp}'",
            )
    return None


def check_hex003(module: ModuleSpec) -> Finding | None:
    """Application must not depend outward on infrastructure packages."""
    if module.layer != "application":
        return None
    for imp in module.imports:
        if imp.startswith("infrastructure.") and "adapter" not in imp.lower():
            return Finding(
                severity="critical",
                code="HEX003",
                line=_declared_line("BAD", "HEX003"),
                message=f"application module '{module.name}' reaches outward to '{imp}'",
            )
    return None


def check_hex004(module: ModuleSpec) -> Finding | None:
    """Port signatures must not leak infrastructure types."""
    for raw in module.methods:
        for token in PORT_SIGNATURE_LEAKS:
            if token in raw:
                return Finding(
                    severity="critical",
                    code="HEX004",
                    line=_declared_line("BAD", "HEX004"),
                    message=f"port signature in '{module.name}' leaks '{token}': {raw}",
                )
    return None


def check_hex005(module: ModuleSpec) -> Finding | None:
    """A Retriever claim must carry the required methods."""
    if "Retriever" not in module.implements:
        return None
    names = _method_names(module.methods)
    missing = sorted(REQUIRED_RETRIEVER_METHODS - names)
    if missing:
        return Finding(
            severity="critical",
            code="HEX005",
            line=_declared_line("BAD", "HEX005"),
            message=f"'{module.name}' claims Retriever but lacks {missing}",
        )
    return None


def check_hex006(module: ModuleSpec) -> Finding | None:
    """Pipeline step names must carry one responsibility."""
    hits = _responsibility_hits(module.name)
    if len(hits) >= 2:
        return Finding(
            severity="warning",
            code="HEX006",
            line=_declared_line("BAD", "HEX006"),
            message=f"step '{module.name}' spans {hits}; split it",
        )
    return None


def check_hex007(module: ModuleSpec) -> Finding | None:
    """Model names and URLs belong in config, not in logic."""
    for raw in module.methods:
        lowered = raw.lower()
        for token in HARDCODED_TOKENS:
            if token.lower() in lowered:
                return Finding(
                    severity="warning",
                    code="HEX007",
                    line=_declared_line("BAD", "HEX007"),
                    message=f"'{module.name}' hardcodes '{token}': {raw}",
                )
    return None


def check_hex008(module: ModuleSpec) -> Finding | None:
    """Application code touching infra needs a config seam."""
    if module.layer != "application":
        return None
    if module.has_config_seam:
        return None
    for imp in module.imports:
        if imp.startswith("infra.") and "adapter" not in imp.lower():
            return Finding(
                severity="warning",
                code="HEX008",
                line=_declared_line("BAD", "HEX008"),
                message=f"'{module.name}' uses '{imp}' without a config seam",
            )
    return None


RULES = (
    check_hex001,
    check_hex002,
    check_hex003,
    check_hex004,
    check_hex005,
    check_hex006,
    check_hex007,
    check_hex008,
)


def analyze(modules: list[ModuleSpec], source: str) -> Analysis:
    """Run all eight rules over every module in order."""
    analysis = Analysis(source=source)
    for module in modules:
        for rule in RULES:
            found = rule(module)
            if found is not None:
                analysis.findings.append(found)
    return analysis


# ---------------------------------------------------------------------------
# 5. Built-in packs: BAD trips all eight, GOOD stays clean
# ---------------------------------------------------------------------------

PACK_BAD: list[ModuleSpec] = [
    ModuleSpec(
        name="passage",
        layer="domain",
        imports=["torch"],
        methods=("validate(text: str) -> bool",),
    ),  # BAD:HEX001
    ModuleSpec(
        name="answer_service",
        layer="application",
        imports=["adapters.QdrantRetriever"],
        methods=("run(query: str) -> str",),
        has_config_seam=True,
    ),  # BAD:HEX002
    ModuleSpec(
        name="ingest_job",
        layer="application",
        imports=["infrastructure.db"],
        methods=("save(doc: str) -> None",),
        has_config_seam=True,
    ),  # BAD:HEX003
    ModuleSpec(
        name="qdrant_port",
        layer="application",
        imports=[],
        implements=("Retriever",),
        methods=("retrieve(store: QdrantClient) -> list",),
        has_config_seam=True,
    ),  # BAD:HEX004
    ModuleSpec(
        name="sparse_index",
        layer="application",
        imports=[],
        implements=("Retriever",),
        methods=("search(query: str) -> list",),
        has_config_seam=True,
    ),  # BAD:HEX005
    ModuleSpec(
        name="chunk_and_embed",
        layer="pipeline",
        imports=[],
        methods=("run(ctx: dict) -> dict",),
        has_config_seam=True,
    ),  # BAD:HEX006
    ModuleSpec(
        name="draft_step",
        layer="application",
        imports=[],
        methods=("load(model='gpt-4o-mini')",),
        has_config_seam=True,
    ),  # BAD:HEX007
    ModuleSpec(
        name="ask_handler",
        layer="application",
        imports=["infra.qdrant"],
        methods=("run(query: str) -> str",),
        has_config_seam=False,
    ),  # BAD:HEX008
]

PACK_GOOD: list[ModuleSpec] = [
    ModuleSpec(
        name="passage",
        layer="domain",
        imports=["dataclasses"],
        methods=("validate(text: str) -> bool",),
    ),
    ModuleSpec(
        name="citation_rule",
        layer="domain",
        imports=["dataclasses"],
        implements=("CitationPolicy",),
        methods=("check(passages: list) -> bool",),
    ),
    ModuleSpec(
        name="answer_question",
        layer="application",
        imports=["domain.ports"],
        methods=("run(query: str) -> str",),
        has_config_seam=True,
    ),
    ModuleSpec(
        name="memory_store",
        layer="application",
        imports=["domain.ports"],
        implements=("Retriever",),
        methods=("retrieve(query: str) -> list",),
        has_config_seam=True,
    ),
    ModuleSpec(
        name="chunk_sections",
        layer="pipeline",
        imports=[],
        methods=("run(ctx: dict) -> dict",),
        has_config_seam=True,
    ),
    ModuleSpec(
        name="embed_texts",
        layer="pipeline",
        imports=[],
        methods=("run(ctx: dict) -> dict",),
        has_config_seam=True,
    ),
]


# ---------------------------------------------------------------------------
# 6. Ports demo: one use case, two adapters, identical results
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Passage:
    """Shared plain record flowing across the Retriever port."""

    pid: str
    book: str
    section: str
    text: str


class Retriever(Protocol):
    """Port returning candidate passages for a query."""

    def retrieve(self, query: str, limit: int) -> list[Passage]: ...


def _score(query: str, text: str) -> int:
    tokens = query.lower().split()
    lowered = text.lower()
    return sum(1 for t in tokens if t and t in lowered)


def _rank(passages: list[Passage], query: str, limit: int) -> list[Passage]:
    scored = [(p, _score(query, p.text)) for p in passages]
    scored.sort(key=lambda item: (-item[1], item[0].pid))
    return [p for p, _ in scored[:limit]]


class InMemoryRetriever:
    """List-scan fake used for fast tests."""

    def __init__(self, passages: list[Passage]) -> None:
        self._passages = list(passages)

    def retrieve(self, query: str, limit: int) -> list[Passage]:
        if not query.strip():
            return []
        return _rank(self._passages, query, limit)


class SimulatedQdrantRetriever:
    """Paged deterministic stand-in for the real store adapter."""

    def __init__(self, passages: list[Passage], page_size: int = 1) -> None:
        self._passages = list(passages)
        self._page_size = max(1, page_size)

    def retrieve(self, query: str, limit: int) -> list[Passage]:
        if not query.strip():
            return []
        seen: list[Passage] = []
        for start in range(0, len(self._passages), self._page_size):
            page = self._passages[start : start + self._page_size]
            seen.extend(page)
        return _rank(seen, query, limit)


@dataclass
class Answer:
    """Result of the AnswerQuestion use case."""

    text: str
    citations: list[str]
    passage_ids: list[str]


class AnswerQuestion:
    """Orchestrate retrieve, check, draft, cite, and track."""

    def __init__(self, retriever: Retriever) -> None:
        self._retriever = retriever

    def run(self, query: str, limit: int = 2) -> Answer:
        passages = self._retriever.retrieve(query, limit)
        if not passages:
            return Answer(
                text="I have no supporting passage.", citations=[], passage_ids=[]
            )
        top = passages[0]
        text = f"Answer drawn from {top.book} {top.section}: {top.text}"
        citations = [f"{p.book} {p.section} [{p.pid}]" for p in passages]
        return Answer(
            text=text, citations=citations, passage_ids=[p.pid for p in passages]
        )


SEED_PASSAGES = [
    Passage(
        pid="b1:p1:0",
        book="Book of Prayer",
        section="Ch.1",
        text="prayer begins with intention and praise",
    ),
    Passage(
        pid="b1:p2:0",
        book="Book of Prayer",
        section="Ch.2",
        text="charity purifies wealth and intention",
    ),
    Passage(
        pid="b2:p1:0",
        book="Book of Fasting",
        section="Ch.1",
        text="fasting teaches patience and gratitude",
    ),
]


def run_ports_demo() -> tuple[Answer, Answer]:
    """Run one use case against both adapters and assert equality."""
    first = AnswerQuestion(InMemoryRetriever(SEED_PASSAGES)).run("prayer intention", 2)
    second = AnswerQuestion(SimulatedQdrantRetriever(SEED_PASSAGES, page_size=1)).run(
        "prayer intention", 2
    )
    assert first == second, f"adapters diverged: {first!r} != {second!r}"
    return first, second


# ---------------------------------------------------------------------------
# 7. Demo, self-check, and JSON file mode
# ---------------------------------------------------------------------------


def _print_analysis(analysis: Analysis) -> None:
    print(
        f"--- {analysis.source}: {len(analysis.findings)} findings "
        f"({analysis.critical_count} critical, {analysis.warning_count} warning)"
    )
    for finding in analysis.findings:
        print(
            f"{finding.code} [{finding.severity}] line {finding.line}: {finding.message}"
        )


def _self_check(bad: Analysis, good: Analysis) -> None:
    codes = sorted(f.code for f in bad.findings)
    expected = [f"HEX{i:03d}" for i in range(1, 9)]
    assert codes == expected, f"BAD pack must trip {expected}, got {codes}"
    assert len(bad.findings) == 8, f"BAD pack must trip 8, got {len(bad.findings)}"
    assert bad.critical_count == 5, f"BAD critical must be 5, got {bad.critical_count}"
    assert bad.warning_count == 3, f"BAD warning must be 3, got {bad.warning_count}"
    assert not good.findings, f"GOOD pack must be clean, got {good.findings}"
    for rule in RULES:
        assert callable(rule)


def _load_modules_from_json(path: str) -> list[ModuleSpec]:
    raw = Path(path).read_text(encoding="utf-8-sig")
    data = json.loads(raw)
    items = data.get("modules", data) if isinstance(data, dict) else data
    modules: list[ModuleSpec] = []
    for entry in items:  # type: ignore[union-attr]
        modules.append(
            ModuleSpec(
                name=str(entry.get("name", "unknown")),
                layer=str(entry.get("layer", "application")),
                imports=list(entry.get("imports", [])),
                implements=tuple(entry.get("implements", ())),
                methods=tuple(entry.get("methods", ())),
                has_config_seam=bool(entry.get("has_config_seam", False)),
            )
        )
    return modules


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        modules = _load_modules_from_json(argv[1])
        analysis = analyze(modules, source=argv[1])
        _print_analysis(analysis)
        return 1 if analysis.findings else 0
    bad = analyze(PACK_BAD, source="PACK_BAD")
    good = analyze(PACK_GOOD, source="PACK_GOOD")
    _print_analysis(bad)
    _print_analysis(good)
    if not good.findings:
        print("GOOD pack clean")
    first, second = run_ports_demo()
    print(
        f"ports demo identical: {first.passage_ids == second.passage_ids} "
        f"ids={','.join(first.passage_ids)}"
    )
    _self_check(bad, good)
    print("self-check ok: BAD trips HEX001-HEX008, GOOD zero, ports identical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
