"""
Challenge 20: Patterns - The Gateway - Reference Solution
==========================================================
"""

from __future__ import annotations

from collections.abc import Callable


def adapt(provider: str, model: str, prompt: str, max_tokens: int) -> dict:
    if max_tokens < 1:
        raise ValueError(f"max_tokens must be >= 1, got {max_tokens}")
    if provider == "openai":
        return {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
        }
    if provider == "ollama":
        return {"model": model, "prompt": prompt, "options": {"num_predict": max_tokens}}
    raise ValueError(f"unknown provider: {provider}")


class EventBus:
    def __init__(self) -> None:
        self._subs: dict[str, list[Callable[[dict], None]]] = {}

    def subscribe(self, topic: str, handler: Callable[[dict], None]) -> None:
        if topic not in self._subs:
            self._subs[topic] = []
        if handler not in self._subs[topic]:
            self._subs[topic].append(handler)

    def unsubscribe(self, topic: str, handler: Callable[[dict], None]) -> bool:
        handlers = self._subs.get(topic)
        if handlers is None or handler not in handlers:
            return False
        handlers.remove(handler)
        if not handlers:
            del self._subs[topic]
        return True

    def publish(self, topic: str, payload: dict) -> int:
        handlers = self._subs.get(topic)
        if not handlers:
            return 0
        for handler in list(handlers):
            handler(payload)
        return len(handlers)


class ModelRouter:
    def __init__(self, models: list[dict], probe: Callable[[str], dict]) -> None:
        self._models: list[dict] = []
        for model in models:
            stats = probe(model["name"])
            self._models.append({**model, "p50_ms": stats["p50_ms"]})

    def route(
        self, *, max_cost_cents: float | None, max_latency_ms: float | None, strategy: str
    ) -> str:
        feasible = [
            m
            for m in self._models
            if (max_cost_cents is None or m["cost_per_1k_cents"] <= max_cost_cents)
            and (max_latency_ms is None or m["p50_ms"] <= max_latency_ms)
        ]
        if not feasible:
            raise ValueError("no feasible model")
        keys: dict[str, Callable[[dict], tuple]] = {
            "cheapest": lambda m: (m["cost_per_1k_cents"], m["name"]),
            "fastest": lambda m: (m["p50_ms"], m["name"]),
            "highest_quality": lambda m: (-m["quality"], m["name"]),
        }
        key = keys.get(strategy)
        if key is None:
            raise ValueError(f"unknown strategy: {strategy}")
        return str(min(feasible, key=key)["name"])
