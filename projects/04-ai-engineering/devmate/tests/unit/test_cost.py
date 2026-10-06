"""Unit tests for devmate.obs.cost."""

from datetime import UTC, datetime, timedelta

import pytest

from devmate.obs.cost import MODEL_PRICING, CostTracker, TokenUsage


def _usage(prompt: int = 1_000_000, completion: int = 1_000_000) -> TokenUsage:
    return TokenUsage(
        prompt_tokens=prompt,
        completion_tokens=completion,
        total_tokens=prompt + completion,
    )


def test_estimate_cost_matches_pricing_table() -> None:
    tracker = CostTracker()
    prompt_price, completion_price = MODEL_PRICING["gpt-4o"]
    expected = prompt_price + completion_price  # 1M prompt + 1M completion tokens
    assert tracker.estimate_cost("gpt-4o", 1_000_000, 1_000_000) == pytest.approx(expected)


def test_record_usage_returns_cost_and_stores_record() -> None:
    tracker = CostTracker()
    tracker.reset()

    cost = tracker.record_usage(
        provider="openai",
        model="gpt-4o-mini",
        usage=_usage(prompt=1_000_000, completion=1_000_000),
        latency_ms=120.0,
        request_id="req-1",
    )

    assert cost > 0
    records = tracker.get_recent_requests()
    assert len(records) == 1
    assert records[0].model == "gpt-4o-mini"
    assert records[0].request_id == "req-1"


def test_get_summary_aggregates_by_model() -> None:
    tracker = CostTracker()
    tracker.reset()
    tracker.record_usage("openai", "gpt-4o", _usage(1_000_000, 0), 100.0)
    tracker.record_usage("openai", "gpt-4o", _usage(500_000, 500_000), 200.0)
    tracker.record_usage("anthropic", "claude-3-5-haiku-20241022", _usage(1_000, 1_000), 50.0)

    summary = tracker.get_summary()
    assert summary.total_requests == 3
    assert summary.total_tokens == 2_002_000
    assert summary.by_model["gpt-4o"]["requests"] == 2
    assert summary.by_provider["openai"]["requests"] == 2
    assert summary.by_provider["anthropic"]["requests"] == 1


def test_get_summary_since_filters_by_time() -> None:
    tracker = CostTracker()
    tracker.reset()
    tracker.record_usage("openai", "gpt-4o", _usage(1_000, 0), 10.0)
    old = datetime.now(UTC) - timedelta(days=2)
    # Force a stale record by editing the stored timestamp.
    with tracker._lock:
        tracker._records[0].timestamp = old

    summary = tracker.get_summary(since=datetime.now(UTC) - timedelta(days=1))
    assert summary.total_requests == 0


def test_unknown_model_cost_is_zero() -> None:
    tracker = CostTracker()
    cost = tracker.record_usage("openai", "not-a-model", _usage(1_000_000, 1_000_000), 10.0)
    assert cost == 0.0
