"""Pure evaluation metrics for DevMate retrieval and answer properties."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RetrievalScore:
    """Retrieval metrics for one case."""

    case_id: str
    hit_at_1: bool
    hit_at_5: bool
    hit_at_10: bool
    reciprocal_rank: float
    expected: list[str]
    retrieved: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "hit_at_1": self.hit_at_1,
            "hit_at_5": self.hit_at_5,
            "hit_at_10": self.hit_at_10,
            "reciprocal_rank": self.reciprocal_rank,
            "expected": self.expected,
            "retrieved": self.retrieved,
        }


@dataclass
class AnswerPropertyScore:
    """Checkable answer-property results for one prompt golden case."""

    case_id: str
    passed: bool
    checks: dict[str, bool] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "passed": self.passed,
            "checks": self.checks,
            "failures": self.failures,
        }


def _normalize(path: str) -> str:
    return path.replace("\\", "/").strip().lower()


def _source_matches(expected_fragment: str, retrieved_path: str) -> bool:
    """True when a retrieved path contains the expected filename/path fragment."""
    exp = _normalize(expected_fragment)
    got = _normalize(retrieved_path)
    if not exp or not got:
        return False
    # Bare filename (e.g. chunker.py) or full path fragment
    return exp in got or got.endswith(exp) or exp.endswith(got)


def score_retrieval(
    case_id: str,
    expected_context: list[str],
    retrieved_paths: list[str],
) -> RetrievalScore:
    """Score retrieval against expected context fragments.

    A case is a hit at k if any expected fragment appears in the top-k retrieved paths.
    Reciprocal rank uses the first hit position (1-based); 0.0 when no hit in the list.
    """
    expected = list(expected_context)
    retrieved = list(retrieved_paths)

    first_hit_rank = 0
    for idx, path in enumerate(retrieved[:10], start=1):
        if any(_source_matches(exp, path) for exp in expected):
            first_hit_rank = idx
            break

    return RetrievalScore(
        case_id=case_id,
        hit_at_1=first_hit_rank == 1,
        hit_at_5=0 < first_hit_rank <= 5,
        hit_at_10=0 < first_hit_rank <= 10,
        reciprocal_rank=(1.0 / first_hit_rank) if first_hit_rank else 0.0,
        expected=expected,
        retrieved=retrieved,
    )


def _check_forbidden(answer: str, forbidden: list[str]) -> tuple[bool, list[str]]:
    lower = answer.lower()
    hits = [p for p in forbidden if p.lower() in lower]
    return len(hits) == 0, hits


def _mentions_from_properties(props: dict[str, Any]) -> list[str]:
    """Map must_mention_* flags to searchable phrases from expected metadata."""
    explicit = props.get("must_mention_phrases")
    if isinstance(explicit, list) and explicit:
        return [str(x) for x in explicit]
    return []


def _unique_keywords(mention_keywords: list[str] | None, props: dict[str, Any]) -> list[str]:
    keywords = list(mention_keywords or [])
    keywords.extend(_mentions_from_properties(props))
    seen: set[str] = set()
    uniq: list[str] = []
    for kw in keywords:
        key = kw.lower()
        if key not in seen:
            seen.add(key)
            uniq.append(kw)
    return uniq


def _check_forbidden_flag(
    text: str,
    props: dict[str, Any],
    checks: dict[str, bool],
    failures: list[str],
) -> None:
    forbidden = props.get("forbidden_phrases") or []
    if not forbidden:
        return
    ok, hits = _check_forbidden(text, forbidden)
    checks["forbidden_phrases_absent"] = ok
    if not ok:
        failures.append(f"forbidden phrases present: {hits}")


def _check_mentions(
    text: str,
    keywords: list[str],
    checks: dict[str, bool],
    failures: list[str],
) -> None:
    if not keywords:
        return
    lower = text.lower()
    missing = [kw for kw in keywords if kw.lower() not in lower]
    checks["mention_keywords_present"] = not missing
    if missing:
        failures.append(f"missing mention keywords: {missing}")


def _check_citations(
    text: str,
    props: dict[str, Any],
    retrieved_paths: list[str] | None,
    checks: dict[str, bool],
    failures: list[str],
) -> None:
    if not props.get("must_cite_sources"):
        return
    lower = text.lower()
    has_citation = (
        ("[" in text and "]" in text) or "src/" in lower or ".py" in lower or "source" in lower
    )
    if not has_citation and retrieved_paths:
        has_citation = any(_normalize(p).split("/")[-1] in lower for p in retrieved_paths if p)
    checks["has_citation_signal"] = has_citation
    if not has_citation:
        failures.append("must_cite_sources: no citation/path signal in answer")


def _check_tools(
    text: str,
    props: dict[str, Any],
    checks: dict[str, bool],
    failures: list[str],
) -> None:
    expected_tools = props.get("expected_tool_names") or []
    if expected_tools:
        missing_tools = [t for t in expected_tools if t not in text]
        checks["expected_tool_names_present"] = not missing_tools
        if missing_tools:
            failures.append(f"missing tool names: {missing_tools}")

    invent_phrases = ["invented tool", "new tool i added", "additional tools such as"]
    if props.get("must_not_invent_api") and expected_tools:
        ok, hits = _check_forbidden(text, invent_phrases)
        checks["no_invented_tool_claims"] = ok
        if not ok:
            failures.append(f"invented tool claims: {hits}")


def score_answer_properties(
    case_id: str,
    answer: str,
    expected_properties: dict[str, Any],
    mention_keywords: list[str] | None = None,
    retrieved_paths: list[str] | None = None,
) -> AnswerPropertyScore:
    """Score an LLM answer against checkable golden-case properties.

    Offline-safe: no network, no judge model. Semantic groundedness is not
    claimed; only structural checks run here.
    """
    props = dict(expected_properties or {})
    checks: dict[str, bool] = {}
    failures: list[str] = []
    text = answer or ""

    _check_forbidden_flag(text, props, checks, failures)
    _check_mentions(text, _unique_keywords(mention_keywords, props), checks, failures)
    _check_citations(text, props, retrieved_paths, checks, failures)
    _check_tools(text, props, checks, failures)

    if not checks:
        checks["non_empty_answer"] = bool(text.strip())
        if not text.strip():
            failures.append("empty answer")

    passed = all(checks.values()) if checks else False
    return AnswerPropertyScore(
        case_id=case_id,
        passed=passed,
        checks=checks,
        failures=failures,
    )


@dataclass
class EvalSummary:
    """Aggregate metrics across cases."""

    retrieval_cases: int = 0
    retrieval_hit_at_1: int = 0
    retrieval_hit_at_5: int = 0
    retrieval_hit_at_10: int = 0
    retrieval_mrr: float = 0.0
    answer_cases: int = 0
    answer_passed: int = 0
    notes: list[str] = field(default_factory=list)

    @property
    def hit_at_1_rate(self) -> float:
        return self.retrieval_hit_at_1 / self.retrieval_cases if self.retrieval_cases else 0.0

    @property
    def hit_at_5_rate(self) -> float:
        return self.retrieval_hit_at_5 / self.retrieval_cases if self.retrieval_cases else 0.0

    @property
    def hit_at_10_rate(self) -> float:
        return self.retrieval_hit_at_10 / self.retrieval_cases if self.retrieval_cases else 0.0

    @property
    def mean_reciprocal_rank(self) -> float:
        return self.retrieval_mrr / self.retrieval_cases if self.retrieval_cases else 0.0

    @property
    def answer_pass_rate(self) -> float:
        return self.answer_passed / self.answer_cases if self.answer_cases else 0.0


def summarize(
    retrieval_scores: list[RetrievalScore],
    answer_scores: list[AnswerPropertyScore],
) -> EvalSummary:
    summary = EvalSummary(
        retrieval_cases=len(retrieval_scores),
        answer_cases=len(answer_scores),
    )
    for score in retrieval_scores:
        summary.retrieval_hit_at_1 += int(score.hit_at_1)
        summary.retrieval_hit_at_5 += int(score.hit_at_5)
        summary.retrieval_hit_at_10 += int(score.hit_at_10)
        summary.retrieval_mrr += score.reciprocal_rank
    for score in answer_scores:
        summary.answer_passed += int(score.passed)
    return summary


def format_metrics_table(summary: EvalSummary) -> str:
    lines = [
        "Metric                  Value",
        "----------------------  -----",
        f"Retrieval cases         {summary.retrieval_cases}",
        f"Hit@1                   {summary.hit_at_1_rate:.3f} ({summary.retrieval_hit_at_1}/{summary.retrieval_cases})",
        f"Hit@5                   {summary.hit_at_5_rate:.3f} ({summary.retrieval_hit_at_5}/{summary.retrieval_cases})",
        f"Hit@10                  {summary.hit_at_10_rate:.3f} ({summary.retrieval_hit_at_10}/{summary.retrieval_cases})",
        f"MRR                     {summary.mean_reciprocal_rank:.3f}",
        f"Answer cases            {summary.answer_cases}",
        f"Answer pass rate        {summary.answer_pass_rate:.3f} ({summary.answer_passed}/{summary.answer_cases})",
    ]
    for note in summary.notes:
        lines.append(f"Note                    {note}")
    return "\n".join(lines)
