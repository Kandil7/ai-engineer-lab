"""DevMate evaluation harness entry point.

Week 2–3 deliverable named to match `make eval` / `eval/README.md`:
`eval/run_ragas.py` — runnable as a module from the DevMate package.

Modes
-----
offline (default)
    Load golden sets, score retrieval from a recorded top-k file (or fixtures),
    score answer properties from recorded answers. No network, no API key.

live
    Retrieve via Qdrant + embeddings, then score retrieval only unless
    `--with-llm` is set (LLM answers require a provider key; never run in CI).

Usage
-----
    python -m devmate.eval.run_ragas --mode offline
    python -m devmate.eval.run_ragas --mode offline --recorded recordings/retrieval-topk.jsonl
    python -m devmate.eval.run_ragas --mode live          # needs Qdrant + embeddings
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from devmate.eval.datasets import (
    PROMPT_GOLDEN_PATH,
    RAG_GOLDEN_PATH,
    load_prompt_golden,
    load_rag_golden,
    write_report,
)
from devmate.eval.metrics import (
    EvalSummary,
    format_metrics_table,
    score_answer_properties,
    score_retrieval,
    summarize,
)
from devmate.eval.validate_prompt_golden import REPO_ROOT

# Recorded retrieval top-k used by offline mode when --recorded is omitted.
# Keys are rag golden case ids; values are ordered retrieved path basenames.
DEFAULT_RECORDINGS_PATH = (
    REPO_ROOT / "evaluations" / "rag" / "baselines" / "devmate-offline-recordings.jsonl"
)

# Offline answers for prompt golden cases (recorded / fixture strings).
# These are structural fixtures, not live model outputs.
DEFAULT_ANSWERS_PATH = (
    REPO_ROOT / "evaluations" / "prompts" / "golden-cases" / "devmate-offline-answers.jsonl"
)


def _load_recorded_retrieval(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        return {}
    mapping: dict[str, list[str]] = {}
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            case_id = row.get("id") or row.get("case_id")
            retrieved = row.get("retrieved") or row.get("retrieved_paths") or []
            if case_id:
                mapping[str(case_id)] = [str(x) for x in retrieved]
    return mapping


def _load_recorded_answers(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    mapping: dict[str, str] = {}
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            case_id = row.get("id") or row.get("case_id")
            answer = row.get("answer") or row.get("expected_answer") or ""
            if case_id:
                mapping[str(case_id)] = str(answer)
    return mapping


def _default_retrieval_from_expected(cases: list[dict[str, Any]]) -> dict[str, list[str]]:
    """Fixture mode: pretend retrieval returned the expected context basenames.

    Used only when no recordings file exists so offline runs still produce a
    metrics table. This is NOT a live measurement — notes say so explicitly.
    """
    mapping: dict[str, list[str]] = {}
    for case in cases:
        expected = case.get("expected_context") or []
        # Put expected first, then a couple of decoy basenames from other cases
        decoys = ["main.py", "config.py", "__init__.py", "README.md"]
        mapping[str(case["id"])] = list(expected) + decoys
    return mapping


async def _live_retrieve(query: str, top_k: int = 10) -> list[str]:
    """Live retrieval via DevMate vector store. Returns path-like source strings."""
    from devmate.index.embeddings import embedding_service
    from devmate.index.vector_store import get_vector_store
    from devmate.retrieve.retriever import get_retriever

    if hasattr(embedding_service, "embed_single"):
        vector = await embedding_service.embed_single(query)
    else:
        result = await embedding_service.embed([query])
        vector = result.embeddings[0] if result.embeddings else []
    retriever = await get_retriever()
    results = await retriever.retrieve(query, vector, use_reranker=False)
    paths: list[str] = []
    for item in results[:top_k]:
        meta = getattr(item, "metadata", None) or {}
        source = meta.get("source") or meta.get("path") or item.id
        paths.append(str(source))
    if not paths:
        store = await get_vector_store()
        hits = await store.search(query_vector=vector, limit=top_k)
        for hit in hits:
            meta = hit.metadata or {}
            paths.append(str(meta.get("source") or hit.id))
    return paths


def run_offline(
    rag_cases: list[dict[str, Any]],
    prompt_cases: list[dict[str, Any]],
    recorded_retrieval: dict[str, list[str]] | None,
    recorded_answers: dict[str, str] | None,
    use_expected_as_retrieval: bool,
) -> tuple[EvalSummary, list[dict[str, Any]], list[dict[str, Any]]]:
    retrieval_map = recorded_retrieval or {}
    if use_expected_as_retrieval or not retrieval_map:
        retrieval_map = {**_default_retrieval_from_expected(rag_cases), **retrieval_map}

    answers = recorded_answers
    if answers is None:
        answers = _load_recorded_answers(DEFAULT_ANSWERS_PATH)
    retrieval_scores = []
    for case in rag_cases:
        case_id = str(case["id"])
        retrieved = retrieval_map.get(case_id, [])
        retrieval_scores.append(
            score_retrieval(
                case_id=case_id,
                expected_context=list(case.get("expected_context") or []),
                retrieved_paths=retrieved,
            )
        )

    answer_scores = []
    for case in prompt_cases:
        case_id = str(case["id"])
        answer = answers.get(case_id) or case.get("expected_answer") or ""
        keywords = list((case.get("metadata") or {}).get("mention_keywords") or [])
        answer_scores.append(
            score_answer_properties(
                case_id=case_id,
                answer=str(answer),
                expected_properties=dict(case.get("expected_properties") or {}),
                mention_keywords=keywords,
                retrieved_paths=retrieval_map.get(
                    str((case.get("metadata") or {}).get("rag_case_id", case_id)), []
                ),
            )
        )

    notes = []
    if not recorded_retrieval:
        notes.append("retrieval fixtures used expected_context as top-k (not a live measurement)")
    if recorded_answers is None and not answers:
        notes.append("answers scored from expected_answer fixtures (not live model output)")
    elif recorded_answers is None:
        notes.append("answers from offline recordings file (not live model output)")

    summary = summarize(retrieval_scores, answer_scores)
    summary.notes.extend(notes)
    return summary, [s.to_dict() for s in retrieval_scores], [s.to_dict() for s in answer_scores]


async def run_live(
    rag_cases: list[dict[str, Any]],
    prompt_cases: list[dict[str, Any]],
    with_llm: bool,
    top_k: int,
) -> tuple[EvalSummary, list[dict[str, Any]], list[dict[str, Any]]]:
    retrieval_scores = []
    for case in rag_cases:
        retrieved = await _live_retrieve(str(case["question"]), top_k=top_k)
        retrieval_scores.append(
            score_retrieval(
                case_id=str(case["id"]),
                expected_context=list(case.get("expected_context") or []),
                retrieved_paths=retrieved,
            )
        )

    answer_scores: list[Any] = []
    notes = ["live retrieval only"]
    if with_llm:
        notes.append("live LLM answer scoring requested but not wired in this commit")
    else:
        notes.append(
            "LLM answers not requested (--with-llm off); answer pass rate from fixtures skipped"
        )

    # Score answer properties using expected answers as stand-ins only when
    # --with-llm is off AND caller wants a non-zero answer section; otherwise
    # leave answer_cases at 0 to avoid fake production claims.
    summary = summarize(retrieval_scores, answer_scores)
    summary.notes.extend(notes)
    return summary, [s.to_dict() for s in retrieval_scores], [s.to_dict() for s in answer_scores]


def build_report(
    summary: EvalSummary,
    mode: str,
    retrieval_details: list[dict[str, Any]],
    answer_details: list[dict[str, Any]],
) -> str:
    today = date.today().isoformat()
    lines = [
        f"# DevMate Eval Report — {today}",
        "",
        f"- Mode: `{mode}`",
        f"- RAG golden set: `{RAG_GOLDEN_PATH.relative_to(REPO_ROOT)}` ({summary.retrieval_cases} cases)",
        f"- Prompt golden set: `{PROMPT_GOLDEN_PATH.relative_to(REPO_ROOT)}` ({summary.answer_cases} cases)",
        "",
        "## Metrics",
        "",
        "```",
        format_metrics_table(summary),
        "```",
        "",
        "## Retrieval detail",
        "",
        "| Case | Hit@1 | Hit@5 | Hit@10 | RR | Expected | Top retrieved |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in retrieval_details:
        expected = ", ".join(row.get("expected") or [])
        retrieved = ", ".join((row.get("retrieved") or [])[:5])
        lines.append(
            f"| {row['case_id']} | {row['hit_at_1']} | {row['hit_at_5']} | "
            f"{row['hit_at_10']} | {row['reciprocal_rank']:.3f} | {expected} | {retrieved} |"
        )

    if answer_details:
        lines.extend(
            [
                "",
                "## Answer property detail",
                "",
                "| Case | Passed | Checks | Failures |",
                "| --- | --- | --- | --- |",
            ]
        )
        for row in answer_details:
            checks = ", ".join(f"{k}={v}" for k, v in (row.get("checks") or {}).items())
            failures = "; ".join(row.get("failures") or [])
            lines.append(f"| {row['case_id']} | {row['passed']} | {checks} | {failures} |")

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "- [ ] Accept (Hit@5 and answer pass rate meet or exceed baseline)",
            "- [ ] Reject (metrics below baseline — investigate before merging prompt/model changes)",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="DevMate evaluation harness")
    parser.add_argument(
        "--mode",
        choices=["offline", "live"],
        default="offline",
        help="offline (default) or live retrieval",
    )
    parser.add_argument(
        "--recorded",
        type=Path,
        default=DEFAULT_RECORDINGS_PATH,
        help="JSONL of recorded retrieval top-k for offline mode",
    )
    parser.add_argument(
        "--answers",
        type=Path,
        default=DEFAULT_ANSWERS_PATH,
        help="JSONL of recorded answers for offline prompt scoring",
    )
    parser.add_argument(
        "--use-expected-as-retrieval",
        action="store_true",
        help="Force fixture retrieval from expected_context even if recordings exist",
    )
    parser.add_argument(
        "--with-llm",
        action="store_true",
        help="live mode only: also score LLM answers (requires provider key)",
    )
    parser.add_argument("--top-k", type=int, default=10, help="live retrieval depth")
    parser.add_argument(
        "--report-name",
        default=None,
        help="Report filename under evaluations/rag/reports/ (default: dated)",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Print metrics only; do not write a report file",
    )
    parser.add_argument(
        "--fail-under-hit-at-5",
        type=float,
        default=0.0,
        help="Exit 1 if Hit@5 rate is below this threshold (0 disables)",
    )
    return parser.parse_args(argv)


async def amain(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    rag_cases = load_rag_golden()
    prompt_cases = load_prompt_golden()

    if args.mode == "offline":
        recorded_retrieval = _load_recorded_retrieval(args.recorded)
        recorded_answers = _load_recorded_answers(args.answers)
        summary, retrieval_details, answer_details = run_offline(
            rag_cases,
            prompt_cases,
            recorded_retrieval=recorded_retrieval,
            recorded_answers=recorded_answers,
            use_expected_as_retrieval=args.use_expected_as_retrieval,
        )
    else:
        summary, retrieval_details, answer_details = await run_live(
            rag_cases,
            prompt_cases,
            with_llm=args.with_llm,
            top_k=args.top_k,
        )

    sys.stdout.write(format_metrics_table(summary) + "\n")
    for note in summary.notes:
        sys.stdout.write(f"Note: {note}\n")

    if not args.no_report:
        name = args.report_name or f"{date.today().isoformat()}-eval-harness.md"
        body = build_report(summary, args.mode, retrieval_details, answer_details)
        path = write_report(name, body)
        sys.stdout.write(f"Report written: {path}\n")

    if args.fail_under_hit_at_5 > 0 and summary.hit_at_5_rate < args.fail_under_hit_at_5:
        sys.stderr.write(
            f"FAIL: Hit@5 {summary.hit_at_5_rate:.3f} < threshold {args.fail_under_hit_at_5:.3f}\n"
        )
        return 1
    return 0


def main() -> int:
    return asyncio.run(amain())


if __name__ == "__main__":
    raise SystemExit(main())
