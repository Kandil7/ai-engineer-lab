"""Tests for the OpenAI-compatible embeddings provider (provider-agnostic)."""

from __future__ import annotations

import pytest

from devmate.index.embeddings import OpenAIEmbeddingProvider


def test_uses_configured_base_url_and_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("devmate.config.settings.embedding_api_key", "jina-key")
    monkeypatch.setattr("devmate.config.settings.embedding_base_url", "https://api.jina.ai/v1")
    monkeypatch.setattr("devmate.config.settings.embedding_model", "jina-embeddings-v3")
    monkeypatch.setattr("devmate.config.settings.embedding_dimensions", 1024)

    provider = OpenAIEmbeddingProvider()
    assert str(provider.client.base_url).rstrip("/") == "https://api.jina.ai/v1"
    assert provider.model_name == "jina-embeddings-v3"
    assert provider.dimensions == 1024


def test_requires_a_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("devmate.config.settings.embedding_api_key", None)
    monkeypatch.setattr("devmate.config.settings.openai_api_key", None)
    with pytest.raises(ValueError):
        OpenAIEmbeddingProvider()
