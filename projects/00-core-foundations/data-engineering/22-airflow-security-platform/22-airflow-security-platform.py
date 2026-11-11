"""
Data Engineering — 22: Airflow Security and Platform
====================================================
Topics: secrets backends, RBAC roles, listener registration, version pinning,
        and the data-vs-coordination-state split.

Why this matters:
    A scheduler that runs is not a scheduler that is safe. This exercise proves
    the invariants that keep a production Airflow honest: no secret stored in a
    Dag file, roles grant least privilege, listeners fire on lifecycle events,
    versions are pinned, and data lives in object storage while coordination
    state lives in the state store.

Run:      python 22-airflow-security-platform.py
Verify:   python 22-airflow-security-platform.py --verify
"""

from __future__ import annotations

import sys


class SecretLeakError(Exception):
    """A secret was found where it must not be."""


class Role:
    """A composable RBAC role with a set of permissions."""

    def __init__(self, name: str, permissions: set[str]) -> None:
        self.name = name
        self.permissions = set(permissions)

    def has(self, permission: str) -> bool:
        return permission in self.permissions


class SecretsBackend:
    """External credential store; Dags resolve connections through it."""

    def __init__(self) -> None:
        self.store: dict[str, str] = {}

    def put(self, key: str, value: str) -> None:
        self.store[key] = value

    def get(self, key: str) -> str:
        if key not in self.store:
            raise KeyError(f"missing secret: {key}")
        return self.store[key]


class ListenerRegistry:
    """Registers listeners on Airflow lifecycle events."""

    def __init__(self) -> None:
        self.listeners: dict[str, list] = {}

    def register(self, event: str, callback) -> None:
        self.listeners.setdefault(event, []).append(callback)

    def fire(self, event: str, payload) -> list:
        return [cb(payload) for cb in self.listeners.get(event, [])]


def scan_dag_for_secrets(dag_source: str, known_secrets: set[str]) -> None:
    """Fail if any known secret literal appears in Dag source."""
    for secret in known_secrets:
        if secret in dag_source:
            raise SecretLeakError(f"secret '{secret}' found in Dag source")


def main() -> None:
    backend = SecretsBackend()
    backend.put("qdrant_url", "https://qdrant.example")
    backend.put("llm_api_key", "sk-secret-value")

    # 1. No secret lives in the Dag file.
    dag_source = "def ingest():\n    return backend.get('qdrant_url')\n"
    try:
        scan_dag_for_secrets(dag_source, {"sk-secret-value"})
    except SecretLeakError:
        raise AssertionError("clean Dag was wrongly flagged")
    leaked = "api_key = 'sk-secret-value'\n"
    try:
        scan_dag_for_secrets(leaked, {"sk-secret-value"})
        raise AssertionError("leaked secret was not detected")
    except SecretLeakError:
        pass

    # 2. RBAC: least privilege — a trigger-only role cannot read connections.
    trigger_role = Role("dag_trigger", {"trigger:devmate_ingest"})
    admin_role = Role("admin", {"trigger:devmate_ingest", "read:connections"})
    assert trigger_role.has("trigger:devmate_ingest")
    assert not trigger_role.has("read:connections"), "least privilege violated"
    assert admin_role.has("read:connections")

    # 3. Listener fires on a lifecycle event.
    reg = ListenerRegistry()
    seen: list[str] = []
    reg.register("dag_import_error", lambda p: seen.append(p) or "handled")
    results = reg.fire("dag_import_error", "broken_dag.py")
    assert results == ["handled"]
    assert seen == ["broken_dag.py"]

    # 4. Version is pinned, not "latest".
    pinned = "apache-airflow==3.4.0"
    assert "==" in pinned and "latest" not in pinned

    # 5. Data lives in object storage; coordination state in the state store.
    object_storage: dict[str, bytes] = {}
    state_store: dict[str, str] = {}
    object_storage["passages/2026-03-04.jsonl"] = b"..."
    state_store["ingest_checkpoint"] = "page_42"
    assert "passages/2026-03-04.jsonl" in object_storage
    assert "ingest_checkpoint" in state_store
    assert "passages/2026-03-04.jsonl" not in state_store

    # 6. Secrets resolve through the backend, never from source.
    assert backend.get("llm_api_key") == "sk-secret-value"

    print("secrets: Dag source clean, backend resolves credentials")
    print("rbac: trigger-only role lacks read:connections")
    print("listener: dag_import_error fired and handled")
    print("version: pinned to 3.4.0, not latest")
    print("storage: data in object storage, coordination in state store")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
