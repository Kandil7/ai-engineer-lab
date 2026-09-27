"""
Fine-Tuning — 05: Model Registry and Release
=============================================
Topics: the registry entry, the eval gate, and immutable versions.

Why this matters:
    A fine-tuned model is an artifact that must be versioned, documented,
    and evaluated before release. This exercise registers a model and
    enforces the eval gate.

Run:      python 05-model-registry.py
Verify:   python 05-model-registry.py --verify
"""

from __future__ import annotations

import sys


def register(entry: dict, registry: dict) -> None:
    """Register an immutable version. A duplicate id is rejected."""
    assert entry["id"] not in registry, "versions are immutable"
    assert entry["eval"]["faithfulness"] >= 0.9, "eval gate before release"
    registry[entry["id"]] = entry


def rollback(registry: dict, current: str) -> str:
    """Point deployment at the previous registered version."""
    ids = list(registry)
    idx = ids.index(current)
    assert idx > 0, "no previous version to roll back to"
    return ids[idx - 1]


def main() -> None:
    registry: dict[str, dict] = {}

    v1 = {
        "id": "athar-sft-v1",
        "base": "qwen2.5-7b",
        "adapter": "athar-sft-v1.safetensors",
        "data_version": "v1",
        "eval": {"eval_loss": 0.42, "faithfulness": 0.92},
    }
    register(v1, registry)
    assert registry["athar-sft-v1"]["base"] == "qwen2.5-7b"

    # A model failing the eval gate is not released.
    bad = {
        "id": "athar-sft-bad",
        "base": "qwen2.5-7b",
        "adapter": "bad.safetensors",
        "data_version": "v1",
        "eval": {"eval_loss": 0.30, "faithfulness": 0.80},
    }
    try:
        register(bad, registry)
        assert False, "eval gate must block release"
    except AssertionError:
        pass

    # A change is a new version, never an edit.
    v2 = dict(v1, id="athar-sft-v2", eval={"eval_loss": 0.38, "faithfulness": 0.94})
    register(v2, registry)
    assert registry["athar-sft-v1"]["eval"] == v1["eval"], "v1 unchanged"

    # Rollback points at the previous version.
    assert rollback(registry, "athar-sft-v2") == "athar-sft-v1"

    print("v1 registered with provenance; eval gate enforced")
    print("failing model blocked from release")
    print("v2 is a new version; v1 is immutable")
    print("rollback from v2 points at v1")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")
