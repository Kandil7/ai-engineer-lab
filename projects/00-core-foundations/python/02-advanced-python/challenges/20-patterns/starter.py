"""
Challenge 20: Patterns - The Gateway - Starter Code
====================================================
Fill in the bodies. Do not modify signatures.
"""

from __future__ import annotations

from collections.abc import Callable


def adapt(provider: str, model: str, prompt: str, max_tokens: int) -> dict:
    """Return the provider's request dict; see README for exact shapes."""
    raise NotImplementedError


class EventBus:
    def __init__(self) -> None:
        raise NotImplementedError

    def subscribe(self, topic: str, handler: Callable[[dict], None]) -> None:
        raise NotImplementedError

    def unsubscribe(self, topic: str, handler: Callable[[dict], None]) -> bool:
        raise NotImplementedError

    def publish(self, topic: str, payload: dict) -> int:
        raise NotImplementedError


class ModelRouter:
    def __init__(self, models: list[dict], probe: Callable[[str], dict]) -> None:
        raise NotImplementedError

    def route(
        self, *, max_cost_cents: float | None, max_latency_ms: float | None, strategy: str
    ) -> str:
        raise NotImplementedError
