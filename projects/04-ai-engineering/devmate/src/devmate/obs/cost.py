"""
Cost tracking for LLM API calls.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from threading import Lock

from devmate.config import settings


@dataclass
class TokenUsage:
    """Token usage for a single request."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    def to_dict(self) -> dict[str, int]:
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
        }


# Pricing per 1M tokens (input, output) - update as needed
MODEL_PRICING = {
    # Anthropic
    "claude-3-5-sonnet-20241022": (3.00, 15.00),
    "claude-3-5-haiku-20241022": (0.80, 4.00),
    "claude-3-opus-20240229": (15.00, 75.00),
    "claude-3-sonnet-20240229": (3.00, 15.00),
    "claude-3-haiku-20240307": (0.25, 1.25),
    # OpenAI
    "gpt-4o": (5.00, 15.00),
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4-turbo": (10.00, 30.00),
    "gpt-3.5-turbo": (0.50, 1.50),
    # Embeddings
    "text-embedding-3-small": (0.02, 0.0),
    "text-embedding-3-large": (0.13, 0.0),
    "text-embedding-ada-002": (0.10, 0.0),
}


@dataclass
class CostRecord:
    """Record of a single LLM call with cost."""

    timestamp: datetime
    provider: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency_ms: float
    cost_usd: float
    request_id: str = ""


@dataclass
class CostSummary:
    """Aggregated cost summary."""

    total_requests: int = 0
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    total_latency_ms: float = 0.0
    by_model: dict[str, dict[str, float]] = field(
        default_factory=lambda: defaultdict(
            lambda: {"requests": 0, "tokens": 0, "cost": 0.0, "latency_ms": 0.0}
        )
    )
    by_provider: dict[str, dict[str, float]] = field(
        default_factory=lambda: defaultdict(
            lambda: {"requests": 0, "tokens": 0, "cost": 0.0, "latency_ms": 0.0}
        )
    )


class CostTracker:
    """Tracks LLM usage and costs with thread-safe operations."""

    def __init__(self) -> None:
        self._records: list[CostRecord] = []
        self._lock = Lock()
        self._enabled = settings.cost_tracking_enabled

    def record_usage(
        self,
        provider: str,
        model: str,
        usage: TokenUsage,
        latency_ms: float,
        request_id: str = "",
    ) -> float:
        """Record a usage event and return the cost in USD."""
        if not self._enabled:
            return 0.0

        # Calculate cost
        pricing = MODEL_PRICING.get(model, (0.0, 0.0))
        input_cost_per_m, output_cost_per_m = pricing

        prompt_cost = (usage.prompt_tokens / 1_000_000) * input_cost_per_m
        completion_cost = (usage.completion_tokens / 1_000_000) * output_cost_per_m
        total_cost = prompt_cost + completion_cost

        record = CostRecord(
            timestamp=datetime.now(UTC),
            provider=provider,
            model=model,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
            latency_ms=latency_ms,
            cost_usd=total_cost,
            request_id=request_id,
        )

        with self._lock:
            self._records.append(record)

        return total_cost

    def get_summary(
        self,
        since: datetime | None = None,
        provider: str | None = None,
        model: str | None = None,
    ) -> CostSummary:
        """Get aggregated cost summary."""
        with self._lock:
            records = self._records.copy()

        if since:
            records = [r for r in records if r.timestamp >= since]
        if provider:
            records = [r for r in records if r.provider == provider]
        if model:
            records = [r for r in records if r.model == model]

        summary = CostSummary()

        for record in records:
            summary.total_requests += 1
            summary.total_prompt_tokens += record.prompt_tokens
            summary.total_completion_tokens += record.completion_tokens
            summary.total_tokens += record.total_tokens
            summary.total_cost_usd += record.cost_usd
            summary.total_latency_ms += record.latency_ms

            # By model
            m = summary.by_model[record.model]
            m["requests"] += 1
            m["tokens"] += record.total_tokens
            m["cost"] += record.cost_usd
            m["latency_ms"] += record.latency_ms

            # By provider
            p = summary.by_provider[record.provider]
            p["requests"] += 1
            p["tokens"] += record.total_tokens
            p["cost"] += record.cost_usd
            p["latency_ms"] += record.latency_ms

        return summary

    def get_recent_requests(self, limit: int = 100) -> list[CostRecord]:
        """Get most recent requests."""
        with self._lock:
            return self._records[-limit:]

    def estimate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Estimate cost for a hypothetical request."""
        pricing = MODEL_PRICING.get(model, (0.0, 0.0))
        input_cost_per_m, output_cost_per_m = pricing
        return (prompt_tokens / 1_000_000) * input_cost_per_m + (
            completion_tokens / 1_000_000
        ) * output_cost_per_m

    def reset(self) -> None:
        """Clear all records (for testing)."""
        with self._lock:
            self._records.clear()


# Global cost tracker instance
cost_tracker = CostTracker()
