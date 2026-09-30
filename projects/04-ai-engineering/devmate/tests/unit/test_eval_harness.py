"""Offline tests for the DevMate eval harness (no API, no Qdrant)."""

from __future__ import annotations

import json

import pytest

from devmate.eval.datasets import load_prompt_golden, load_rag_golden
from devmate.eval.metrics import (
    format_metrics_table,
    score_answer_properties,
    score_retrieval,
    summarize,
)
from devmate.eval.run_ragas import (
    DEFAULT_ANSWERS_PATH,
    DEFAULT_RECORDINGS_PATH,
    _load_recorded_answers,
    _load_recorded_retrieval,
    run_offline,
)


def test_rag_golden_set_has_ten_cases() -> None:
    cases = load_rag_golden()
    assert len(cases) == 10
    assert cases[0]["id"] == "dev-golden-001"


def test_prompt_golden_set_has_ten_cases() -> None:
    cases = load_prompt_golden()
    assert len(cases) == 10


def test_score_retrieval_hit_and_mrr() -> None:
    score = score_retrieval(
        case_id="c1",
        expected_context=["chunker.py"],
        retrieved_paths=["main.py", "src/devmate/ingest/chunker.py", "config.py"],
    )
    assert score.hit_at_1 is False
    assert score.hit_at_5 is True
    assert score.reciprocal_rank == pytest.approx(0.5)


def test_score_retrieval_miss() -> None:
    score = score_retrieval(
        case_id="c2",
        expected_context=["chunker.py"],
        retrieved_paths=["main.py", "config.py"],
    )
    assert score.hit_at_5 is False
    assert score.reciprocal_rank == 0.0


def test_answer_properties_forbidden_and_citations() -> None:
    good = score_answer_properties(
        case_id="a1",
        answer="Uses cost_tracker.record_usage in src/devmate/obs/cost.py [1].",
        expected_properties={
            "must_be_grounded_in_context": True,
            "must_cite_sources": True,
            "must_not_invent_api": True,
            "forbidden_phrases": ["I don't have access"],
        },
        mention_keywords=["cost_tracker"],
    )
    assert good.passed is True
    assert good.checks["forbidden_phrases_absent"] is True
    assert good.checks["mention_keywords_present"] is True
    assert good.checks["has_citation_signal"] is True

    bad = score_answer_properties(
        case_id="a2",
        answer="I don't have access to that code.",
        expected_properties={
            "must_be_grounded_in_context": True,
            "must_cite_sources": True,
            "must_not_invent_api": True,
            "forbidden_phrases": ["I don't have access"],
        },
        mention_keywords=["cost_tracker"],
    )
    assert bad.passed is False
    assert "forbidden phrases present" in bad.failures[0]


def test_offline_harness_fixture_mode() -> None:
    rag_cases = load_rag_golden()
    prompt_cases = load_prompt_golden()
    summary, retrieval_details, answer_details = run_offline(
        rag_cases,
        prompt_cases,
        recorded_retrieval=None,
        recorded_answers=None,
        use_expected_as_retrieval=True,
    )
    assert summary.retrieval_cases == 10
    assert summary.hit_at_5_rate == 1.0
    assert summary.answer_cases == 10
    assert summary.answer_pass_rate == 1.0
    assert len(retrieval_details) == 10
    assert len(answer_details) == 10
    assert any("not a live measurement" in n for n in summary.notes)
    assert any("offline recordings" in n or "expected_answer" in n for n in summary.notes)


def test_recordings_and_answers_files_exist_and_load() -> None:
    assert DEFAULT_RECORDINGS_PATH.exists()
    assert DEFAULT_ANSWERS_PATH.exists()
    retrieval = _load_recorded_retrieval(DEFAULT_RECORDINGS_PATH)
    answers = _load_recorded_answers(DEFAULT_ANSWERS_PATH)
    assert len(retrieval) == 10
    assert len(answers) == 10

    rag_cases = load_rag_golden()
    prompt_cases = load_prompt_golden()
    summary, _, answer_details = run_offline(
        rag_cases,
        prompt_cases,
        recorded_retrieval=retrieval,
        recorded_answers=answers,
        use_expected_as_retrieval=False,
    )
    assert summary.hit_at_5_rate == 1.0
    assert summary.answer_pass_rate == 1.0
    assert not summary.notes  # recorded mode should not use fixture notes
    assert all(row["passed"] for row in answer_details)


def test_metrics_table_formats() -> None:
    summary = summarize([], [])
    text = format_metrics_table(summary)
    assert "Hit@5" in text
    assert "Retrieval cases" in text


@pytest.mark.asyncio
async def test_amain_offline_writes_report(tmp_path, monkeypatch) -> None:
    # Point reports dir at tmp by patching write_report target via run path
    from devmate.eval import datasets as datasets_mod
    from devmate.eval import run_ragas as run_mod

    report_dir = tmp_path / "reports"
    monkeypatch.setattr(
        run_mod,
        "write_report",
        lambda name, body: (
            report_dir.mkdir(parents=True, exist_ok=True),
            (report_dir / name).write_text(body, encoding="utf-8"),
            report_dir / name,
        )[-1],
    )
    monkeypatch.setattr(
        datasets_mod,
        "REPO_ROOT",
        report_dir,  # not used by patched write_report
    )

    code = await run_mod.amain(
        [
            "--mode",
            "offline",
            "--use-expected-as-retrieval",
            "--report-name",
            "unit-eval-harness.md",
        ]
    )
    assert code == 0
    report = report_dir / "unit-eval-harness.md"
    assert report.exists()
    body = report.read_text(encoding="utf-8")
    assert "Hit@5" in body
    assert "DevMate Eval Report" in body


def test_jsonl_recordings_are_valid_json() -> None:
    for path in (DEFAULT_RECORDINGS_PATH, DEFAULT_ANSWERS_PATH):
        lines = path.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 10
        for line in lines:
            obj = json.loads(line)
            assert "id" in obj
