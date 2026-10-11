"""Tests for LLM provider selection (Groq reuses the OpenAI-compatible path)."""

from __future__ import annotations

import pytest

from devmate.llm.client import GroqProvider, LLMAuthError, LLMProvider


def test_groq_provider_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("devmate.config.settings.groq_api_key", "test-key")
    provider = GroqProvider()
    assert provider.provider_name == LLMProvider.GROQ
    assert provider.base_url == "https://api.groq.com/openai/v1"


def test_groq_provider_requires_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("devmate.config.settings.groq_api_key", None)
    with pytest.raises(LLMAuthError):
        GroqProvider()
