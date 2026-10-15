"""
Exercise 01: Domain-Driven Design and Domain Modeling
=====================================================
Audit a declarative domain model the way a reviewer would: run the nine DDD
rules from Lecture 01 against a model description and flag an anemic
aggregate root, value objects that carry identity, entities compared by
attribute equality, invariants parked on the wrong member, cross-aggregate
rules squeezed into one transaction, command-shaped domain events,
ubiquitous-language violations, types shared across contexts with no
declared boundary, and repositories that still speak in filter dicts.

The demo runs the rules against two built-in descriptions: a BAD
Athar-shaped model (Book, Section, Passage, Narration, Isnad, Narrator,
Scholar, EntityId, MergeCandidate) that trips all nine rules, and a GOOD
one that must raise zero findings. It then exercises the modeling
components the lecture teaches - composable specifications, an aggregate
root enforcing its invariant at the boundary, and an idempotent event
consumer - all against offline fixtures. No network.

Prerequisites:
    Python 3.11+ standard library only. No third-party packages.

Usage:
    python exercises/01-domain-modeling.py
    python exercises/01-domain-modeling.py path/to/model.json
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

_SOURCE_TEXT = Path(__file__).read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# 1. Models
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """One rule violation in one model description."""

    severity: str
    code: str
    line: int
    message: str


@dataclass
class Analysis:
    """All findings for one model description."""

    source: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "critical")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")


# ---------------------------------------------------------------------------
# 2. Model access and marker-based line resolution
# ---------------------------------------------------------------------------


def _types(model: dict) -> list[dict]:
    entries = model.get("types")
    return (
        [t for t in entries if isinstance(t, dict)] if isinstance(entries, list) else []
    )


def _repositories(model: dict) -> list[dict]:
    entries = model.get("repositories")
    return (
        [r for r in entries if isinstance(r, dict)] if isinstance(entries, list) else []
    )


def _events(model: dict) -> list[dict]:
    entries = model.get("events")
    return (
        [e for e in entries if isinstance(e, dict)] if isinstance(entries, list) else []
    )


def _declared_line(label: str, code: str) -> int:
    """Resolve a finding's line by scanning this file for '# LABEL:CODE'."""
    needle = f"# {label}:{code}"
    for number, line in enumerate(_SOURCE_TEXT.splitlines(), start=1):
        if needle in line:
            return number
    return 0


_CAMEL_RE = re.compile(r"[A-Z]+(?![a-z])|[A-Z][a-z]*|[a-z]+")


def _words(name: str) -> list[str]:
    """Split CamelCase or snake_case into words: PublishNarration -> 2 words."""
    return [w for w in _CAMEL_RE.findall(name or "") if w]


# Names a command uses. A domain event that starts with one of these is an
# instruction ("PublishNarration"), not a record of something that happened.
_COMMAND_VERBS = frozenset(
    {
        "add",
        "apply",
        "approve",
        "archive",
        "assign",
        "attach",
        "canonize",
        "close",
        "compute",
        "create",
        "decide",
        "defer",
        "delete",
        "detach",
        "embed",
        "execute",
        "generate",
        "ingest",
        "label",
        "link",
        "merge",
        "notify",
        "open",
        "publish",
        "rebuild",
        "record",
        "register",
        "reject",
        "remove",
        "request",
        "restore",
        "retrieve",
        "run",
        "save",
        "score",
        "send",
        "set",
        "split",
        "start",
        "stop",
        "sync",
        "tombstone",
        "trigger",
        "update",
        "validate",
    }
)

# Irregular past-tense forms, for events whose last word does not end in -ed.
_PAST_FORMS = frozenset({"built", "done", "kept", "ran", "sent", "shown"})

# Placeholder vocabulary no domain expert ever says out loud.
_BANNED_NAMES = frozenset(
    {
        "Data",
        "DataItem",
        "DataObject",
        "Generic",
        "Info",
        "Information",
        "Misc",
        "Miscellaneous",
        "Temp",
        "Thing",
    }
)
_BANNED_SUFFIXES = ("Helper", "Manager", "Util", "Utils")

# Fields that name a value object's own identity. References to *other*
# entities (left_id, book_id) are foreign keys and are not what DDD002 means.
_IDENTITY_FIELDS = frozenset({"id", "entity_id", "entityid", "guid", "pk", "uuid"})

# Table-shaped repository vocabulary: the query names the mechanics, not intent.
_TABLE_METHODS = frozenset(
    {
        "find",
        "find_all",
        "find_by",
        "filter",
        "get_all",
        "list_all",
        "query",
        "search_by",
        "select",
        "where",
    }
)

# Boundary declarations that make one type shared across contexts legitimate.
_DECLARED_BOUNDARIES = frozenset({"anti-corruption-layer", "shared-kernel"})


# ---------------------------------------------------------------------------
# 3. Rules (DDD001 - DDD009)
# ---------------------------------------------------------------------------


def check_anemic_root(model: dict, label: str, findings: list[Finding]) -> None:
    """DDD001: an aggregate root with setters and no invariants enforces nothing."""
    for t in _types(model):
        if t.get("kind") != "aggregate" or not t.get("root"):
            continue
        setters = [str(s) for s in t.get("setters") or []]
        if setters and not t.get("invariants"):
            findings.append(
                Finding(
                    severity="critical",
                    code="DDD001",
                    line=_declared_line(label, "DDD001"),
                    message=(
                        f"Aggregate root '{t.get('name')}' exposes setters "
                        f"({', '.join(setters)}) while declaring no invariants. "
                        "Any caller can bypass the rules; move the rules onto the "
                        "root and replace setters with intention-revealing methods "
                        "that enforce them."
                    ),
                )
            )


def check_value_object_identity(
    model: dict, label: str, findings: list[Finding]
) -> None:
    """DDD002: a value object with an identity field is an entity in disguise."""
    for t in _types(model):
        if t.get("kind") != "value":
            continue
        for field_name in t.get("fields") or []:
            if str(field_name).strip().lower() in _IDENTITY_FIELDS:
                findings.append(
                    Finding(
                        severity="warning",
                        code="DDD002",
                        line=_declared_line(label, "DDD002"),
                        message=(
                            f"Value object '{t.get('name')}' declares identity "
                            f"field '{field_name}'. Value objects are immutable and "
                            "compared by their attributes; an id-named field makes "
                            "it an entity in disguise - model an entity, or keep "
                            "the reference on the aggregate root."
                        ),
                    )
                )
                break


def check_entity_equality(model: dict, label: str, findings: list[Finding]) -> None:
    """DDD003: entities compared by attribute equality break identity semantics."""
    for t in _types(model):
        if t.get("kind") != "entity":
            continue
        compared = str(t.get("compared_by") or "").strip().lower()
        if compared in {"attribute", "attributes", "fields", "value", "values"}:
            findings.append(
                Finding(
                    severity="critical",
                    code="DDD003",
                    line=_declared_line(label, "DDD003"),
                    message=(
                        f"Entity '{t.get('name')}' is compared by attribute "
                        "equality. Two entities are equal only when their identities "
                        "are equal; attribute comparison breaks caching, dedupe, and "
                        "collection behavior the moment a display field changes."
                    ),
                )
            )


def check_invariant_on_member(model: dict, label: str, findings: list[Finding]) -> None:
    """DDD004: an invariant on a non-root member has no one responsible for it."""
    for t in _types(model):
        if t.get("root"):
            continue
        aggregate = t.get("aggregate")
        invariants = t.get("invariants") or []
        if aggregate and invariants:
            names = ", ".join(
                str(i.get("name", "?")) for i in invariants if isinstance(i, dict)
            )
            findings.append(
                Finding(
                    severity="critical",
                    code="DDD004",
                    line=_declared_line(label, "DDD004"),
                    message=(
                        f"Invariant '{names}' is declared on '{t.get('name')}', a "
                        f"member of aggregate '{aggregate}'. Members can be replaced "
                        "or reached through any path; the aggregate root is the only "
                        "place that can guarantee the rule for every caller."
                    ),
                )
            )


def check_cross_aggregate_transaction(
    model: dict, label: str, findings: list[Finding]
) -> None:
    """DDD005: a cross-aggregate rule cannot hold inside one transaction."""
    for t in _types(model):
        for inv in t.get("invariants") or []:
            if not isinstance(inv, dict):
                continue
            if inv.get("scope") != "cross-aggregate":
                continue
            if str(inv.get("mechanism") or "").strip().lower() == "domain-event":
                continue
            findings.append(
                Finding(
                    severity="critical",
                    code="DDD005",
                    line=_declared_line(label, "DDD005"),
                    message=(
                        f"Cross-aggregate invariant '{inv.get('name')}' is enforced "
                        f"inside aggregate '{t.get('name')}' as a single transaction. "
                        "Two aggregates cannot share a transaction; publish a domain "
                        "event and let the other side react idempotently (Reliability "
                        "track, idempotency section)."
                    ),
                )
            )


def check_event_naming(model: dict, label: str, findings: list[Finding]) -> None:
    """DDD006: a domain event named as a command is an instruction, not a record.

    A final word in past tense decides it: 'MergeDecisionCommitted' starts with
    a verb *word* but records what happened, while 'PublishNarration' ends in
    its object and orders every consumer to act again on redelivery.
    """
    for event in _events(model):
        name = str(event.get("name") or "")
        words = _words(name)
        if not words or words[0].lower() not in _COMMAND_VERBS:
            continue
        if words[-1].lower().endswith("ed") or words[-1].lower() in _PAST_FORMS:
            continue
        findings.append(
            Finding(
                severity="warning",
                code="DDD006",
                line=_declared_line(label, "DDD006"),
                message=(
                    f"Domain event '{name}' is named as a command. Events record "
                    "what happened in past tense (NarrationPublished); a "
                    "present-tense name tells every consumer to perform the "
                    "action again on redelivery."
                ),
            )
        )


def check_ubiquitous_language(model: dict, label: str, findings: list[Finding]) -> None:
    """DDD007: placeholder names hide the concept the model exists to express."""
    named = [(str(t.get("name") or ""), "type") for t in _types(model)]
    named += [(str(r.get("name") or ""), "repository") for r in _repositories(model)]
    for name, kind in named:
        if name in _BANNED_NAMES or name.endswith(_BANNED_SUFFIXES):
            findings.append(
                Finding(
                    severity="warning",
                    code="DDD007",
                    line=_declared_line(label, "DDD007"),
                    message=(
                        f"{kind.capitalize()} '{name}' violates the ubiquitous "
                        "language: the domain expert says 'a narration', not "
                        "'a data item'. Placeholder names (DataItem, Info, Manager, "
                        "Helper) hide the concept the model exists to express."
                    ),
                )
            )


def check_shared_context_type(model: dict, label: str, findings: list[Finding]) -> None:
    """DDD008: a type shared across contexts with no declared boundary is coupling."""
    for t in _types(model):
        contexts = [str(c) for c in t.get("contexts") or []]
        if len(contexts) < 2:
            continue
        boundary = str(t.get("boundary_relationship") or "").strip().lower()
        if boundary in _DECLARED_BOUNDARIES:
            continue
        findings.append(
            Finding(
                severity="critical",
                code="DDD008",
                line=_declared_line(label, "DDD008"),
                message=(
                    f"Type '{t.get('name')}' is shared across contexts "
                    f"{contexts} with no shared-kernel or anti-corruption-layer "
                    "declaration. Two contexts silently coupled by one type drift "
                    "apart until neither side can change safely."
                ),
            )
        )


def check_repository_shape(model: dict, label: str, findings: list[Finding]) -> None:
    """DDD009: a table-shaped repository leaks storage mechanics to callers."""
    for repo in _repositories(model):
        for method in repo.get("methods") or []:
            if not isinstance(method, dict):
                continue
            name = str(method.get("name") or "")
            params = [str(p) for p in method.get("params") or []]
            raw_dict = any(p.strip().endswith("dict") for p in params)
            if not raw_dict and name not in _TABLE_METHODS:
                continue
            findings.append(
                Finding(
                    severity="warning",
                    code="DDD009",
                    line=_declared_line(label, "DDD009"),
                    message=(
                        f"Repository '{repo.get('name')}' method '{name}' takes a "
                        "raw filter shape instead of intent. A repository is the "
                        "aggregate's collection interface: name the query after "
                        "intent (passages_of_book) so the rule is visible at the "
                        "call site."
                    ),
                )
            )


# ---------------------------------------------------------------------------
# 4. Analysis entry point
# ---------------------------------------------------------------------------


def analyze_model(model: dict, label: str) -> Analysis:
    """Run every DDD rule against one model description."""
    name = model.get("name")
    source = f"{label} pack ({name})" if name else f"{label} pack"
    analysis = Analysis(source=source)

    check_anemic_root(model, label, analysis.findings)
    check_value_object_identity(model, label, analysis.findings)
    check_entity_equality(model, label, analysis.findings)
    check_invariant_on_member(model, label, analysis.findings)
    check_cross_aggregate_transaction(model, label, analysis.findings)
    check_event_naming(model, label, analysis.findings)
    check_ubiquitous_language(model, label, analysis.findings)
    check_shared_context_type(model, label, analysis.findings)
    check_repository_shape(model, label, analysis.findings)

    analysis.findings.sort(key=lambda f: (f.code, f.line))
    return analysis


def render(analysis: Analysis) -> str:
    """Format one analysis for the terminal."""
    lines = [f"Model description: {analysis.source}"]
    if not analysis.findings:
        lines.append("  No findings. 0 critical, 0 warning.")
        return "\n".join(lines)
    for f in analysis.findings:
        where = f"line {f.line}" if f.line else "line -"
        lines.append(f"  {f.code}  {f.severity:<8}  {where:<9}  {f.message}")
    lines.append(
        f"  {len(analysis.findings)} findings: "
        f"{analysis.critical_count} critical, {analysis.warning_count} warning"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 5. Sample model descriptions used for the demo
# ---------------------------------------------------------------------------

MODEL_BAD: dict = {
    "name": "athar-monolith-legacy",
    "contexts": ["catalog", "citation"],
    "types": [
        {
            "name": "Passage",
            "kind": "aggregate",
            "root": True,
            "contexts": ["citation"],
            "fields": ["passage_id", "book_id", "page", "original", "searchable"],
            "compared_by": "identity",
            "setters": ["set_book_id", "set_page", "set_original"],  # BAD:DDD001
            "invariants": [],
        },
        {
            "name": "DataItem",  # BAD:DDD007
            "kind": "entity",
            "root": False,
            "aggregate": "Passage",
            "contexts": ["citation"],
            "fields": ["item_id", "payload"],
            "compared_by": "attributes",  # BAD:DDD003
            "setters": ["set_payload"],
            "invariants": [
                {
                    "name": "payload_not_empty",
                    "scope": "aggregate",
                    "mechanism": "aggregate-root",
                },  # BAD:DDD004
            ],
        },
        {
            "name": "EntityKey",
            "kind": "value",
            "root": False,
            "contexts": ["citation"],
            "fields": ["entity_id", "surface"],  # BAD:DDD002
            "invariants": [],
        },
        {
            "name": "Narration",
            "kind": "aggregate",
            "root": True,
            "contexts": ["citation"],
            "fields": ["narration_id", "passage_id", "text"],
            "compared_by": "identity",
            "setters": [],
            "invariants": [
                {
                    "name": "narration_belongs_to_exactly_one_passage",
                    "scope": "aggregate",
                    "mechanism": "aggregate-root",
                },
                {
                    "name": "canonical_entity_has_at_least_one_alias",
                    "scope": "cross-aggregate",
                    "mechanism": "single-transaction",
                    "enforced_in": "Narration",
                },  # BAD:DDD005
            ],
        },
        {
            "name": "EntityId",
            "kind": "value",
            "root": False,
            "contexts": ["catalog", "citation"],
            "fields": ["value"],
            "boundary_relationship": None,  # BAD:DDD008
            "invariants": [],
        },
        {
            "name": "Scholar",
            "kind": "entity",
            "root": True,
            "contexts": ["catalog"],
            "fields": ["scholar_id", "display"],
            "compared_by": "identity",
            "setters": [],
            "invariants": [],
        },
    ],
    "events": [
        {"name": "PublishNarration", "context": "citation"},  # BAD:DDD006
        {"name": "NarrationLinked", "context": "citation"},
    ],
    "repositories": [
        {
            "name": "PassageRepo",
            "context": "citation",
            "methods": [
                {"name": "find_by", "params": ["filters: dict"]},  # BAD:DDD009
                {"name": "narrations_by_narrator", "params": ["narrator_id: str"]},
            ],
        },
    ],
}

MODEL_GOOD: dict = {
    "name": "athar-domain",
    "contexts": ["catalog", "citation", "resolution"],
    "types": [
        {
            "name": "Book",
            "kind": "aggregate",
            "root": True,
            "contexts": ["catalog"],
            "fields": ["book_id", "title", "source_version"],
            "compared_by": "identity",
            "setters": [],
            "operations": ["rename", "retire_edition"],
            "invariants": [
                {
                    "name": "book_id_not_empty",
                    "scope": "aggregate",
                    "mechanism": "aggregate-root",
                },
                {
                    "name": "title_not_empty",
                    "scope": "aggregate",
                    "mechanism": "aggregate-root",
                },
            ],
        },
        {
            "name": "Section",
            "kind": "entity",
            "root": False,
            "aggregate": "Book",
            "contexts": ["catalog"],
            "fields": ["section_id", "ordinal", "heading"],
            "compared_by": "identity",
            "setters": [],
            "invariants": [],
        },
        {
            "name": "Passage",
            "kind": "aggregate",
            "root": True,
            "contexts": ["citation"],
            "fields": ["passage_id", "book_id", "page", "original", "searchable"],
            "compared_by": "identity",
            "setters": [],
            "operations": ["ingest", "attach_narration", "extend_isnad"],
            "invariants": [
                {
                    "name": "page_at_least_one",
                    "scope": "aggregate",
                    "mechanism": "aggregate-root",
                },
                {
                    "name": "both_texts_present",
                    "scope": "aggregate",
                    "mechanism": "aggregate-root",
                },
                {
                    "name": "narration_belongs_to_exactly_one_passage",
                    "scope": "aggregate",
                    "mechanism": "aggregate-root",
                },
                {
                    "name": "isnad_is_an_ordered_chain",
                    "scope": "aggregate",
                    "mechanism": "aggregate-root",
                },
            ],
        },
        {
            "name": "Narration",
            "kind": "entity",
            "root": False,
            "aggregate": "Passage",
            "contexts": ["citation"],
            "fields": ["narration_id", "text"],
            "compared_by": "identity",
            "setters": [],
            "invariants": [],
        },
        {
            "name": "Isnad",
            "kind": "entity",
            "root": False,
            "aggregate": "Passage",
            "contexts": ["citation"],
            "fields": ["isnad_id", "chain"],
            "compared_by": "identity",
            "setters": [],
            "invariants": [],
        },
        {
            "name": "AyahReference",
            "kind": "value",
            "root": False,
            "contexts": ["citation"],
            "fields": ["surah", "ayah"],
            "invariants": [],
        },
        {
            "name": "NormalizedText",
            "kind": "value",
            "root": False,
            "contexts": ["citation"],
            "fields": ["original", "normalized", "normalizer_version"],
            "invariants": [],
        },
        {
            "name": "Narrator",
            "kind": "aggregate",
            "root": True,
            "contexts": ["resolution"],
            "fields": ["narrator_id", "display", "aliases", "era"],
            "compared_by": "identity",
            "setters": [],
            "operations": ["record_alias", "link_work"],
            "invariants": [
                {
                    "name": "display_not_empty",
                    "scope": "aggregate",
                    "mechanism": "aggregate-root",
                },
                {
                    "name": "canonical_entity_has_at_least_one_alias",
                    "scope": "aggregate",
                    "mechanism": "aggregate-root",
                },
            ],
        },
        {
            "name": "Scholar",
            "kind": "entity",
            "root": True,
            "contexts": ["catalog"],
            "fields": ["scholar_id", "display"],
            "compared_by": "identity",
            "setters": [],
            "invariants": [],
        },
        {
            "name": "EntityId",
            "kind": "value",
            "root": False,
            "contexts": ["catalog", "citation", "resolution"],
            "fields": ["value"],
            "boundary_relationship": "shared-kernel",
            "invariants": [],
        },
        {
            "name": "MergeCandidate",
            "kind": "value",
            "root": False,
            "contexts": ["resolution"],
            "fields": ["left_id", "right_id", "score", "decision"],
            "invariants": [],
        },
        {
            "name": "MergeDecision",
            "kind": "entity",
            "root": True,
            "contexts": ["resolution"],
            "fields": [
                "decision_id",
                "left_id",
                "right_id",
                "decided_by",
                "decided_at",
            ],
            "compared_by": "identity",
            "setters": [],
            "operations": ["commit", "reverse"],
            "invariants": [
                {
                    "name": "decisions_are_append_only",
                    "scope": "aggregate",
                    "mechanism": "aggregate-root",
                },
                {
                    "name": "alias_table_reflects_committed_merge",
                    "scope": "cross-aggregate",
                    "mechanism": "domain-event",
                },
            ],
        },
    ],
    "events": [
        {"name": "NarrationLinked", "context": "citation"},
        {"name": "PassageIngested", "context": "citation"},
        {"name": "EntityMerged", "context": "resolution"},
        {"name": "AliasRecorded", "context": "resolution"},
        {"name": "MergeDecisionCommitted", "context": "resolution"},
    ],
    "repositories": [
        {
            "name": "PassageRepository",
            "context": "citation",
            "methods": [
                {"name": "passages_of_book", "params": ["book_id: str"]},
                {"name": "narrations_by_narrator", "params": ["narrator_id: str"]},
            ],
        },
        {
            "name": "CanonicalEntityRepository",
            "context": "resolution",
            "methods": [
                {"name": "pending_merge_candidates", "params": []},
                {"name": "canonical_entity", "params": ["entity_id: str"]},
            ],
        },
    ],
}


# ---------------------------------------------------------------------------
# 6. Modeling components
# ---------------------------------------------------------------------------


class Specification:
    """A named business rule: evaluable, composable with and / or / not."""

    description = "specification"

    def is_satisfied_by(self, candidate) -> bool:
        raise NotImplementedError

    def __and__(self, other: "Specification") -> "Specification":
        return _AllOf(self, other)

    def __or__(self, other: "Specification") -> "Specification":
        return _AnyOf(self, other)

    def __invert__(self) -> "Specification":
        return _Not(self)

    def __repr__(self) -> str:
        return self.description


class _AllOf(Specification):
    def __init__(self, left: Specification, right: Specification) -> None:
        self.left, self.right = left, right
        self.description = f"({left.description}) AND ({right.description})"

    def is_satisfied_by(self, candidate) -> bool:
        return self.left.is_satisfied_by(candidate) and self.right.is_satisfied_by(
            candidate
        )


class _AnyOf(Specification):
    def __init__(self, left: Specification, right: Specification) -> None:
        self.left, self.right = left, right
        self.description = f"({left.description}) OR ({right.description})"

    def is_satisfied_by(self, candidate) -> bool:
        return self.left.is_satisfied_by(candidate) or self.right.is_satisfied_by(
            candidate
        )


class _Not(Specification):
    def __init__(self, inner: Specification) -> None:
        self.inner = inner
        self.description = f"NOT ({inner.description})"

    def is_satisfied_by(self, candidate) -> bool:
        return not self.inner.is_satisfied_by(candidate)


class MeetsScore(Specification):
    def __init__(self, threshold: float) -> None:
        self.threshold = threshold
        self.description = f"score >= {threshold:.2f}"

    def is_satisfied_by(self, candidate) -> bool:
        return candidate.score >= self.threshold


class NotVetoed(Specification):
    description = "veto is absent"

    def is_satisfied_by(self, candidate) -> bool:
        return candidate.veto is None


@dataclass(frozen=True)
class Candidate:
    """Offline stand-in for a merge candidate: pair, score, optional veto."""

    left: str
    right: str
    score: float
    veto: str | None = None


class Narration:
    """Member object: can only reach the world through its aggregate root."""

    def __init__(self, narration_id: str) -> None:
        self.narration_id = narration_id
        self.passage: "Passage | None" = None


class Passage:
    """Aggregate root: construction and attachment are where the rules hold."""

    def __init__(self, passage_id: str, page: int) -> None:
        if page < 1:
            raise ValueError(f"page must be >= 1, got {page}")
        self.passage_id = passage_id
        self.page = page
        self._narrations: list[Narration] = []

    @property
    def narrations(self) -> tuple[Narration, ...]:
        return tuple(self._narrations)

    def attach(self, narration: Narration) -> None:
        if narration.passage is not None:
            raise ValueError(
                f"narration {narration.narration_id} already belongs to passage "
                f"{narration.passage.passage_id}"
            )
        narration.passage = self
        self._narrations.append(narration)


class IdempotentConsumer:
    """Reacts to domain events; a redelivered event is suppressed by key."""

    def __init__(self) -> None:
        self._applied: set[str] = set()
        self.alias_links = 0

    def handle(self, event_id: str) -> str:
        if event_id in self._applied:
            return "suppressed (event already applied)"
        self._applied.add(event_id)
        self.alias_links += 1
        return "applied (alias table updated)"


# ---------------------------------------------------------------------------
# 7. Demos
# ---------------------------------------------------------------------------


def _demo_specification() -> None:
    auto_merge = MeetsScore(0.92) & NotVetoed()
    candidates = [
        Candidate("h-1", "h-2", 0.97, None),
        Candidate("h-3", "h-4", 0.88, None),
        Candidate("h-5", "h-6", 0.95, "year-conflict"),
    ]
    print(f"Specification: auto_merge = {auto_merge.description}")
    for c in candidates:
        verdict = "auto-merge" if auto_merge.is_satisfied_by(c) else "review"
        veto = c.veto or "no veto"
        print(f"    {c.left}/{c.right}  score {c.score:.2f}  {veto:<14} -> {verdict}")
    inverted = ~auto_merge
    print(f"    same rule inverted for the review queue: {inverted.description}")


def _demo_aggregate() -> None:
    print("Aggregate root: rules enforced at the boundary, not by convention")
    try:
        Passage("b1:p3:0", page=0)
    except ValueError as exc:
        print(f"    construct page 0      -> rejected: {exc}")
    p1, p2 = Passage("b1:p3:0", page=3), Passage("b1:p4:0", page=4)
    narration = Narration("n-1")
    p1.attach(narration)
    print(f"    attach n-1 to p1      -> ok ({len(p1.narrations)} narration)")
    try:
        p2.attach(narration)
    except ValueError as exc:
        print(f"    attach n-1 to p2      -> rejected: {exc}")
    print(f"    root exposes a setter -> {hasattr(p1, 'set_page')} (DDD001 finds none)")


def _demo_idempotent_event() -> None:
    consumer = IdempotentConsumer()
    first = consumer.handle("evt-entity-merged-0001")
    second = consumer.handle("evt-entity-merged-0001")
    print("Domain event EntityMerged delivered twice (queue is at-least-once):")
    print(f"    first delivery        -> {first}")
    print(f"    redelivery            -> {second}")
    print(f"    alias updates applied -> {consumer.alias_links} (not 2)")


# ---------------------------------------------------------------------------
# 8. Entry point
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    print("=" * 72)
    print("Exercise 01: Domain-Driven Design and Domain Modeling")
    print("=" * 72)

    if len(argv) > 1:
        path = Path(argv[1])
        if not path.is_file():
            print(f"error: no such model file: {path}", file=sys.stderr)
            return 2
        try:
            # utf-8-sig: Windows editors save JSON with a BOM; plain utf-8 would
            # leave U+FEFF in the text and json.loads would reject it.
            model = json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            print(f"error: {path} is not valid JSON: {exc}", file=sys.stderr)
            return 2
        analysis = analyze_model(model, label="FILE")
        print(render(analysis))
        return 1 if analysis.critical_count else 0

    bad = analyze_model(MODEL_BAD, label="BAD")
    good = analyze_model(MODEL_GOOD, label="GOOD")
    print(render(bad))
    print()
    print(render(good))
    print("-" * 72)

    _demo_specification()
    print()
    _demo_aggregate()
    print()
    _demo_idempotent_event()
    print("-" * 72)
    print(
        f"Demo result: BAD pack raised {bad.critical_count} critical and "
        f"{bad.warning_count} warning findings; GOOD pack raised "
        f"{good.critical_count} critical and {good.warning_count} warning findings."
    )
    print("No network access, no wall-clock dependence: reruns are identical.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
