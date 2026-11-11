"""
Data Engineering — 21: Airflow Advanced Authoring
=================================================
Topics: dynamic task mapping, asset-aware scheduling, params validation,
        event-driven scheduling, deferrable operators, YAML Dags.

Why this matters:
    A Dag that fans out at runtime, schedules on data instead of clocks, and
    validates its inputs is the difference between a demo and a pipeline that
    survives contact with changing data. This exercise proves the invariants:
    mapping count is decided at runtime, assets fire consumers, params are
    schema-validated, and an event trigger runs the consumer.

Run:      python 21-airflow-advanced-authoring.py
Verify:   python 21-airflow-advanced-authoring.py --verify
"""

from __future__ import annotations

import sys
from typing import Any


class ValidationError(Exception):
    """A param value failed schema validation."""


def validate_param(value: Any, schema: dict[str, Any]) -> None:
    """Minimal JSON-schema-ish validator for integer params."""
    if schema.get("type") != "integer":
        raise ValidationError("only integer params supported in this exercise")
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(f"expected int, got {type(value).__name__}")
    if "minimum" in schema and value < schema["minimum"]:
        raise ValidationError(f"{value} < minimum {schema['minimum']}")
    if "maximum" in schema and value > schema["maximum"]:
        raise ValidationError(f"{value} > maximum {schema['maximum']}")


class Asset:
    """A typed dataset with a URI that can trigger consumer Dags."""

    def __init__(self, uri: str) -> None:
        self.uri = uri

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Asset) and other.uri == self.uri

    def __hash__(self) -> int:
        return hash(self.uri)


class EventLog:
    """Records asset update events; consumers schedule on them."""

    def __init__(self) -> None:
        self.events: list[Asset] = []

    def emit(self, asset: Asset) -> None:
        self.events.append(asset)

    def consumers_for(self, asset: Asset) -> list[Asset]:
        return [a for a in self.events if a == asset]


def dynamic_map(items: list[Any], fn: Any) -> list[Any]:
    """Runtime fan-out: one result per item, count decided at call time."""
    return [fn(item) for item in items]


def collect(results: list[Any]) -> list[Any]:
    """Gather mapped results into a single list for a downstream task."""
    return list(results)


def event_driven_run(log: EventLog, asset: Asset) -> bool:
    """A consumer runs when at least one event exists for the asset."""
    return len(log.consumers_for(asset)) > 0


def collected_gate(scores: list[float]) -> bool:
    return all(s >= 0.7 for s in scores)


def main() -> None:
    # 1. Dynamic mapping decides the count at runtime, not parse time.
    cases = ["c1", "c2", "c3", "c4"]
    scores = dynamic_map(cases, lambda c: 0.8)
    assert len(scores) == 4, "one result per input item"
    gathered = collect(scores)
    assert gathered == [0.8, 0.8, 0.8, 0.8]
    assert collected_gate(gathered) is True

    # 2. Asset event fires the consumer Dag.
    log = EventLog()
    asset = Asset("athar://passages")
    assert event_driven_run(log, asset) is False, "no event yet"
    log.emit(asset)
    assert event_driven_run(log, asset) is True, "consumer runs on asset event"
    assert len(log.consumers_for(asset)) == 1

    # 3. Params are schema-validated at trigger time.
    schema = {"type": "integer", "minimum": 1, "maximum": 30}
    validate_param(7, schema)  # ok
    for bad in (0, 31, 3.5, True, "7"):
        try:
            validate_param(bad, schema)  # type: ignore[arg-type]
            raise AssertionError(f"invalid value {bad!r} was accepted")
        except ValidationError:
            pass

    # 4. Combining asset and time schedules: an event run plus a fallback.
    fallback_ran = False
    if not event_driven_run(EventLog(), asset):
        fallback_ran = True  # cron fallback when no asset event
    assert fallback_ran is True

    print(f"dynamic_map: {len(scores)} instances created at runtime")
    print("asset event: consumer triggered on emit")
    print("params: invalid values rejected by schema")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
