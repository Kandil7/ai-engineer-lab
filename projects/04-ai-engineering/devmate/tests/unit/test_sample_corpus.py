"""Tests for the startup sample-corpus ingest."""

from __future__ import annotations

from pathlib import Path

import pytest

from devmate.ingest import sample_corpus as sc


class _FakeStore:
    def __init__(self, count: int) -> None:
        self._count = count

    async def count(self) -> int:
        return self._count


def _corpus(tmp_path: Path) -> Path:
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "a.md").write_text("# Title\n\nChunking splits text into pieces.", encoding="utf-8")
    return corpus


@pytest.mark.asyncio
async def test_skips_when_store_non_empty(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    async def fake_store():
        return _FakeStore(3)

    monkeypatch.setattr("devmate.index.vector_store.get_vector_store", fake_store)
    assert await sc.ensure_sample_corpus(_corpus(tmp_path)) == 0


@pytest.mark.asyncio
async def test_ingests_when_store_empty(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    async def fake_store():
        return _FakeStore(0)

    class _FakePipeline:
        async def ingest_documents(self, documents: list) -> int:
            return len(documents)

    async def fake_pipeline():
        return _FakePipeline()

    monkeypatch.setattr("devmate.index.vector_store.get_vector_store", fake_store)
    monkeypatch.setattr("devmate.retrieve.rag.get_rag_pipeline", fake_pipeline)

    assert await sc.ensure_sample_corpus(_corpus(tmp_path)) >= 1


@pytest.mark.asyncio
async def test_missing_corpus_is_noop(tmp_path: Path) -> None:
    assert await sc.ensure_sample_corpus(tmp_path / "nope") == 0


@pytest.mark.asyncio
async def test_ingest_failure_is_swallowed(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    async def boom():
        raise RuntimeError("no embedding provider")

    monkeypatch.setattr("devmate.index.vector_store.get_vector_store", boom)
    assert await sc.ensure_sample_corpus(_corpus(tmp_path)) == 0
