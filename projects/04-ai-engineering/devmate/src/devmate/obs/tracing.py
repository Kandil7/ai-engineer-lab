"""
Tracing and observability with Langfuse integration.
"""

import uuid
from collections.abc import AsyncGenerator, Generator
from contextlib import AbstractContextManager, asynccontextmanager, contextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from devmate.config import settings


@dataclass
class Span:
    """A single trace span."""

    trace_id: str
    span_id: str
    parent_span_id: str | None
    name: str
    start_time: datetime
    end_time: datetime | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    events: list = field(default_factory=list)
    status: str = "ok"
    error: str | None = None

    def set_attribute(self, key: str, value: Any) -> None:
        """Set a span attribute."""
        self.attributes[key] = value

    def add_event(self, name: str, attributes: dict[str, Any] | None = None) -> None:
        """Add an event to the span."""
        self.events.append(
            {
                "name": name,
                "timestamp": datetime.now(UTC).isoformat(),
                "attributes": attributes or {},
            }
        )

    def set_status(self, status: str, error: str | None = None) -> None:
        """Set span status."""
        self.status = status
        if error:
            self.error = error
            self.attributes["error"] = error

    def finish(self) -> None:
        """Mark span as finished."""
        self.end_time = datetime.now(UTC)

    def duration_ms(self) -> float:
        """Get span duration in milliseconds."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "name": self.name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_ms": self.duration_ms(),
            "attributes": self.attributes,
            "events": self.events,
            "status": self.status,
            "error": self.error,
        }


@dataclass
class Trace:
    """A complete trace with multiple spans."""

    trace_id: str
    name: str
    start_time: datetime
    spans: dict[str, Span] = field(default_factory=dict)
    root_span_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_span(self, span: Span) -> None:
        """Add a span to the trace."""
        self.spans[span.span_id] = span
        if self.root_span_id is None:
            self.root_span_id = span.span_id

    def get_span(self, span_id: str) -> Span | None:
        """Get a span by ID."""
        return self.spans.get(span_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "name": self.name,
            "start_time": self.start_time.isoformat(),
            "spans": {sid: span.to_dict() for sid, span in self.spans.items()},
            "root_span_id": self.root_span_id,
            "metadata": self.metadata,
        }


class _DualContext:
    """Wrap a sync context manager so it also works with ``async with``.

    Span tracking is purely in-memory, so there is nothing to await; this
    lets the 18 ``async with tracer.trace(...)`` call sites work instead of
    raising ``TypeError: _GeneratorContextManager does not support the
    asynchronous context manager protocol``.
    """

    def __init__(self, cm: AbstractContextManager[Span]) -> None:
        self._cm = cm

    def __enter__(self) -> Span:
        return self._cm.__enter__()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: Any,
    ) -> bool | None:
        return self._cm.__exit__(exc_type, exc, tb)

    async def __aenter__(self) -> Span:
        return self.__enter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: Any,
    ) -> bool | None:
        return self.__exit__(exc_type, exc, tb)


class Tracer:
    """Tracing system with optional Langfuse export."""

    def __init__(self) -> None:
        self.enabled = settings.tracing_enabled
        self._traces: dict[str, Trace] = {}
        self._current_trace_id: str | None = None
        self._current_span_id: str | None = None
        self._langfuse_client = None
        self._init_langfuse()

    def _init_langfuse(self) -> None:
        """Initialize Langfuse client if configured."""
        if not self.enabled:
            return

        public_key = settings.langfuse_public_key
        secret_key = settings.langfuse_secret_key

        if public_key and secret_key:
            try:
                from langfuse import Langfuse

                self._langfuse_client = Langfuse(
                    public_key=public_key,
                    secret_key=secret_key,
                    host=settings.langfuse_host,
                )
            except ImportError:
                pass
            except Exception:
                pass
        else:
            pass

    def start_trace(self, name: str, metadata: dict[str, Any] | None = None) -> Trace:
        """Start a new trace."""
        trace_id = str(uuid.uuid4())
        trace = Trace(
            trace_id=trace_id,
            name=name,
            start_time=datetime.now(UTC),
            metadata=metadata or {},
        )
        self._traces[trace_id] = trace
        self._current_trace_id = trace_id
        return trace

    def get_current_trace(self) -> Trace | None:
        """Get the currently active trace."""
        if self._current_trace_id:
            return self._traces.get(self._current_trace_id)
        return None

    @contextmanager
    def _trace_sync(self, name: str, **attributes) -> Generator[Span, None, None]:
        """Context manager for synchronous tracing."""
        span = self.start_span(name, **attributes)
        try:
            yield span
            span.set_status("ok")
        except Exception as e:
            span.set_status("error", str(e))
            raise
        finally:
            self.end_span(span)

    def trace(self, name: str, **attributes) -> _DualContext:
        """Trace a block; works with both ``with`` and ``async with``."""
        return _DualContext(self._trace_sync(name, **attributes))

    @asynccontextmanager
    async def trace_async(self, name: str, **attributes) -> AsyncGenerator[Span, None]:
        """Async context manager for tracing."""
        span = self.start_span(name, **attributes)
        try:
            yield span
            span.set_status("ok")
        except Exception as e:
            span.set_status("error", str(e))
            raise
        finally:
            self.end_span(span)

    def start_span(
        self,
        name: str,
        parent_span_id: str | None = None,
        **attributes,
    ) -> Span:
        """Start a new span."""
        trace_id = self._current_trace_id or str(uuid.uuid4())
        span_id = str(uuid.uuid4())[:16]

        parent = parent_span_id or self._current_span_id

        span = Span(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent,
            name=name,
            start_time=datetime.now(UTC),
            attributes=attributes,
        )

        # Get or create trace
        if trace_id not in self._traces:
            self._traces[trace_id] = Trace(
                trace_id=trace_id,
                name=name,
                start_time=datetime.now(UTC),
            )

        self._traces[trace_id].add_span(span)
        self._current_span_id = span_id

        return span

    def end_span(self, span: Span) -> None:
        """End a span."""
        span.finish()
        self._current_span_id = span.parent_span_id

        # Export to Langfuse if available
        if self._langfuse_client:
            self._export_span_to_langfuse(span)

    def _export_span_to_langfuse(self, span: Span) -> None:
        """Export span to Langfuse."""
        try:
            trace = self._traces.get(span.trace_id)
            if not trace:
                return

            langfuse_trace = self._langfuse_client.trace(
                id=span.trace_id,
                name=trace.name,
                metadata=trace.metadata,
            )

            langfuse_trace.span(
                id=span.span_id,
                name=span.name,
                parent_span_id=span.parent_span_id,
                start_time=span.start_time,
                end_time=span.end_time,
                metadata=span.attributes,
                level="ERROR" if span.status == "error" else "DEFAULT",
                status_message=span.error,
            )

            self._langfuse_client.flush()
        except Exception:
            pass

    def get_trace(self, trace_id: str) -> Trace | None:
        """Get a trace by ID."""
        return self._traces.get(trace_id)

    def get_recent_traces(self, limit: int = 100) -> list:
        """Get recent traces."""
        return list(self._traces.values())[-limit:]

    def clear(self) -> None:
        """Clear all traces (for testing)."""
        self._traces.clear()
        self._current_trace_id = None
        self._current_span_id = None


# Global tracer instance
tracer = Tracer()


# Convenience decorators
def traced(name: str | None = None, **attributes):
    """Decorator to trace a function."""

    def decorator(func):
        trace_name = name or f"{func.__module__}.{func.__qualname__}"

        if asyncio.iscoroutinefunction(func):

            async def async_wrapper(*args, **kwargs):
                async with tracer.trace_async(trace_name, **attributes) as span:
                    span.set_attribute("function", func.__qualname__)
                    return await func(*args, **kwargs)

            return async_wrapper

        def sync_wrapper(*args, **kwargs):
            with tracer.trace(trace_name, **attributes) as span:
                span.set_attribute("function", func.__qualname__)
                return func(*args, **kwargs)

        return sync_wrapper

    return decorator


import asyncio  # noqa: E402
