"""
Challenge 20: Patterns - The Gateway - Tests
=============================================
Default run targets starter.py and MUST FAIL (NotImplementedError) until solved.

Validate the reference solution:
    $env:CHALLENGE_USE_SOLUTION = "1"
    python -m pytest 02-advanced-python/challenges/20-patterns/test_challenge.py -q

Guards are measured (comparison counts, probe-call counts), never wall-clock.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from typing import Any

import pytest

TARGET = "solution" if os.environ.get("CHALLENGE_USE_SOLUTION") == "1" else "starter"
_spec = importlib.util.spec_from_file_location(TARGET, Path(__file__).parent / f"{TARGET}.py")
assert _spec is not None and _spec.loader is not None
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


class CountingStr(str):
    """String that counts == comparisons. Hash stays str's so dicts accept it."""

    comparisons = 0

    __hash__ = str.__hash__

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, str):
            return NotImplemented
        CountingStr.comparisons += 1
        return str.__eq__(self, other)


MODELS: list[dict] = [
    {"name": "a", "cost_per_1k_cents": 1.0, "quality": 0.7},
    {"name": "b", "cost_per_1k_cents": 1.0, "quality": 0.9},
    {"name": "c", "cost_per_1k_cents": 4.0, "quality": 0.95},
]
LATENCY: dict[str, float] = {"a": 120.0, "b": 80.0, "c": 40.0}


class FakeProbe:
    """Probe each name at most once; a second call for a name raises."""

    def __init__(self, latency: dict[str, float] | None = None) -> None:
        self.calls: list[str] = []
        self._seen: set[str] = set()
        self._latency = dict(LATENCY if latency is None else latency)

    def __call__(self, name: str) -> dict:
        if name in self._seen:
            raise RuntimeError(f"probe called twice for {name!r}")
        self._seen.add(name)
        self.calls.append(name)
        return {"p50_ms": self._latency[name]}


def route(
    router: Any,
    *,
    cost: float | None = None,
    latency: float | None = None,
    strategy: str = "cheapest",
) -> str:
    return str(router.route(max_cost_cents=cost, max_latency_ms=latency, strategy=strategy))


def make_router(
    models: list[dict] | None = None, latency: dict[str, float] | None = None
) -> tuple[Any, FakeProbe]:
    probe = FakeProbe(latency)
    router = mod.ModelRouter(list(MODELS) if models is None else models, probe)
    return router, probe


# ---------------------------------------------------------------- Bronze


def test_bronze_openai_shape():
    assert mod.adapt("openai", "gpt-4o-mini", "hi", 128) == {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 128,
    }


def test_bronze_ollama_shape():
    assert mod.adapt("ollama", "llama3.2", "hi", 64) == {
        "model": "llama3.2",
        "prompt": "hi",
        "options": {"num_predict": 64},
    }


def test_bronze_empty_prompt_is_valid():
    out = mod.adapt("openai", "m", "", 1)
    assert out["messages"] == [{"role": "user", "content": ""}]


def test_bronze_unknown_provider_raises():
    with pytest.raises(ValueError):
        mod.adapt("cohere", "m", "hi", 8)


def test_bronze_provider_names_are_exact():
    with pytest.raises(ValueError):
        mod.adapt("OpenAI", "m", "hi", 8)


def test_bronze_invalid_max_tokens_raises():
    for bad in (0, -1):
        with pytest.raises(ValueError):
            mod.adapt("openai", "m", "hi", bad)


# ---------------------------------------------------------------- Silver


def test_silver_publish_unknown_topic_returns_zero():
    bus = mod.EventBus()
    assert bus.publish("eval/start", {"i": 0}) == 0


def test_silver_subscribe_publish_and_payload_identity():
    bus = mod.EventBus()
    seen: list[dict] = []

    def record(payload: dict) -> None:
        seen.append(payload)

    payload = {"answer": 42}
    bus.subscribe("eval/start", record)
    assert bus.publish("eval/start", payload) == 1
    assert len(seen) == 1
    assert seen[0] is payload


def test_silver_handlers_run_in_subscription_order():
    bus = mod.EventBus()
    order: list[str] = []

    def first(payload: dict) -> None:
        order.append("first")

    def second(payload: dict) -> None:
        order.append("second")

    bus.subscribe("eval/start", first)
    bus.subscribe("eval/start", second)
    assert bus.publish("eval/start", {}) == 2
    assert order == ["first", "second"]


def test_silver_duplicate_subscribe_is_noop():
    bus = mod.EventBus()
    calls: list[int] = []

    def handler(payload: dict) -> None:
        calls.append(1)

    bus.subscribe("eval/start", handler)
    bus.subscribe("eval/start", handler)
    assert bus.publish("eval/start", {}) == 1
    assert len(calls) == 1


def test_silver_unsubscribe_semantics():
    bus = mod.EventBus()

    def handler(payload: dict) -> None:
        pass

    bus.subscribe("eval/start", handler)
    assert bus.unsubscribe("eval/start", handler) is True
    assert bus.publish("eval/start", {}) == 0
    assert bus.unsubscribe("eval/start", handler) is False


def test_silver_topics_are_isolated():
    bus = mod.EventBus()
    calls: list[str] = []

    def handler(payload: dict) -> None:
        calls.append("hit")

    bus.subscribe("eval/error", handler)
    assert bus.publish("eval/start", {}) == 0
    assert calls == []
    assert bus.publish("eval/error", {}) == 1


def test_silver_comparison_budget():
    CountingStr.comparisons = 0
    bus = mod.EventBus()
    topics = [CountingStr(f"eval/run-{i:04d}/request/completed") for i in range(300)]

    def handler(payload: dict) -> None:
        pass

    for topic in topics:
        bus.subscribe(topic, handler)
    delivered = 0
    for topic in topics:
        delivered += bus.publish(topic, {"i": 1})
    assert delivered == 300
    budget = 6 * (len(topics) + len(topics))
    assert CountingStr.comparisons <= budget, (
        f"{CountingStr.comparisons} comparisons exceed the budget of {budget}; "
        "index handlers by topic instead of scanning a flat list per publish"
    )


# ------------------------------------------------------------------ Gold


def test_gold_cheapest_with_name_tiebreak():
    router, probe = make_router()
    assert route(router, strategy="cheapest") == "a"
    assert len(probe.calls) <= len(MODELS)


def test_gold_fastest_uses_probed_latency():
    router, _ = make_router()
    assert route(router, strategy="fastest") == "c"


def test_gold_highest_quality():
    router, _ = make_router()
    assert route(router, strategy="highest_quality") == "c"


def test_gold_constraints_filter_to_single_candidate():
    router, _ = make_router()
    assert route(router, cost=2.0, latency=100.0, strategy="cheapest") == "b"
    assert route(router, latency=60.0, strategy="fastest") == "c"


def test_gold_no_feasible_model_raises():
    router, _ = make_router()
    with pytest.raises(ValueError):
        route(router, cost=0.5, strategy="cheapest")


def test_gold_unknown_strategy_raises():
    router, _ = make_router()
    with pytest.raises(ValueError):
        route(router, strategy="popular")


def test_gold_empty_models_raises():
    router, _ = make_router(models=[])
    with pytest.raises(ValueError):
        route(router, strategy="cheapest")


def test_gold_single_model():
    router, _ = make_router(
        models=[{"name": "only", "cost_per_1k_cents": 2.0, "quality": 0.5}],
        latency={"only": 10.0},
    )
    assert route(router, strategy="cheapest") == "only"
    assert route(router, strategy="fastest") == "only"


def test_gold_probe_budget_over_many_routes():
    router, probe = make_router()
    strategies = ("cheapest", "fastest", "highest_quality")
    for i in range(60):
        assert route(router, strategy=strategies[i % 3])
    assert len(probe.calls) <= len(MODELS), (
        f"probe called {len(probe.calls)} times for {len(MODELS)} models; "
        "probe once at construction and route from the snapshot"
    )
    assert set(probe.calls) <= {m["name"] for m in MODELS}


def test_gold_route_is_deterministic():
    router, _ = make_router()
    first = route(router, strategy="cheapest")
    second = route(router, strategy="cheapest")
    assert first == second == "a"
