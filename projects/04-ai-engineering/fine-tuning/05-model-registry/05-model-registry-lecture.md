# Fine-Tuning 05: Model Registry and Release

## Topic Overview

A fine-tuned model is an artifact that must be versioned, documented, and evaluated before
release. Unlike source code, a model cannot be read to understand what it does; its
behavior is in the weights, and the only way to know what it is and how it was made is the
registry entry and the model card that ship with it. Without them the artifact is
unmaintainable: nobody can say which base model it needs, what data trained it, or whether
it is safe to deploy.

This lecture covers the registry entry with full provenance, the model card, the eval gate
that blocks release, immutable versioning, and rollback. The registry is the safety net:
it is what makes a regression recoverable by pointing deployment at the previous version
rather than re-training from scratch.

The discipline here mirrors the model-choice ADR (Model Serving 01) and the eval gate (AI
Evaluation 06): decisions and artifacts are recorded, and nothing reaches production
without passing the bar that was set in advance.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Register a model artifact with its full provenance.
2. Write a model card that documents what the model is and its limits.
3. Enforce an eval gate before release.
4. Version a model immutably and record its dependencies.
5. Roll back to a previous version.
6. Explain why the adapter is meaningless without its base version.

## Prerequisites

- Fine-Tuning 04 (training runs) for the config and eval results the entry records.
- AI Evaluation 06 (eval in CI) for the gate discipline.

---

## 1. The Registry Entry

### What it records

The entry records the artifact and its provenance: base model, adapter, config hash, data
version, eval results, and the model card reference.

```python
registry_entry = {
    "id": "athar-sft-v1",
    "base": "qwen2.5-7b",
    "adapter": "athar-sft-v1.safetensors",
    "config_hash": "a1b2c3",
    "data_version": "v1",
    "eval": {"eval_loss": 0.42, "faithfulness": 0.92},
}
```

### The single source of truth

The entry is the source of truth for what the model is and how it was made. Given an
adapter file, the entry tells you which base it needs, which data trained it, and what it
scored. Without it, the file is an opaque blob.

### Provenance for rollback and audit

Provenance is what makes rollback and audit possible: you can trace a production answer
back to the exact model version, the adapter, and the data version that produced it.

## 2. The Model Card

### What it documents

The model card documents what the model is, what it was trained on, how it performs, and
its limitations. It is written at release, not after.

### The sections

- **Base model and adapter.**
- **Training data** (the data version and its coverage).
- **Evaluation results** (the golden set and adversarial set scores).
- **Known failure modes** (what it does badly, honestly stated).
- **Intended use** (what it is for and what it is not).

### Why it is written at release

A model without a card is an artifact without a story. The card is what lets a future
engineer, a reviewer, or a user understand the model without re-deriving everything. It is
the model's README.

## 3. Evaluate Before Release

### The gate

A model is released only after it passes the eval gate: the same golden set and adversarial
set that gate the RAG system (AI Evaluation 01, 05, 06). The exercise enforces it at
registration:

```python
def register(entry: dict, registry: dict) -> None:
    """Register an immutable version. A duplicate id is rejected."""
    assert entry["id"] not in registry, "versions are immutable"
    assert entry["eval"]["faithfulness"] >= 0.9, "eval gate before release"
    registry[entry["id"]] = entry
```

A model that improves eval loss but fails faithfulness is blocked. Improving one metric
while failing another is the tradeoff the gate exists to catch.

### Why before, not after

Evaluating after release means a bad model is already serving users. The gate runs before
the artifact is released, so a failing model never reaches production.

## 4. Versioning

### Immutable versions

The model version is the registry id, and it is immutable. A change to the adapter, the
data, or the config is a new version, never an edit:

```python
v2 = dict(v1, id="athar-sft-v2", eval={"eval_loss": 0.38, "faithfulness": 0.94})
register(v2, registry)
assert registry["athar-sft-v1"]["eval"] == v1["eval"], "v1 unchanged"
```

Editing a version destroys the ability to reproduce or roll back to what actually ran.

### Dependencies are versioned

The base model version and the adapter version are both recorded, because the adapter is
meaningless without its exact base. The data version and config hash are recorded too, so
the artifact can be traced back to a reproducible run (Fine-Tuning 04).

## 5. Rollback

### Mechanical rollback

A released model can regress in production. The registry makes rollback mechanical: point
deployment at the previous version:

```python
def rollback(registry: dict, current: str) -> str:
    """Point deployment at the previous registered version."""
    ...
    return ids[idx - 1]
```

### The precondition

Rollback works only if the previous version is still registered and its artifact is still
available. Never delete a released version's artifact while it might be needed; the
registry is the safety net, and an empty history has no net.

### Rollback is a decision

Rolling back is a real decision with its own tradeoffs (the previous version may lack a
fix). Record it, and treat it as a signal that the release gate or the eval set needs
attention.

## Real-World Application

- Registering the Athar SFT adapter with its base model, data version, and eval results.
- Writing the model card with the honest failure modes (for example, weaker on rare query
  types) so users are not surprised.
- Blocking a release whose faithfulness dropped below the gate even though eval loss
  improved.
- Rolling back to the previous adapter when a production regression appears.

## Common Mistakes

1. **Releasing without a registry entry.** The artifact has no provenance.
2. **No model card.** The artifact has no story; failure modes are undocumented.
3. **Releasing before the eval gate.** A bad model serves users.
4. **Editing a version instead of creating a new one.** Reproducibility and rollback break.
5. **Deleting a released artifact.** Rollback becomes impossible.
6. **Forgetting the base model version.** The adapter cannot be reconstructed.

## Key Takeaways

1. The registry entry records the artifact and its provenance; it is the single source of
   truth.
2. The model card documents what the model is, how it was made, how it performs, and its
   limits.
3. The eval gate blocks release; evaluate before, never after.
4. Versions are immutable; a change is a new version, and dependencies are versioned too.
5. The registry makes rollback mechanical, and rollback is a recorded decision.

## Self-Check Questions

1. Why is a model card written at release rather than later?
2. What does the eval gate block, and why run it before release?
3. Why is editing a model version harmful even if the edit is small?
4. What precondition must hold for rollback to work?
5. Why is an adapter meaningless without its base model version?

## Further Reading / Connections

- Fine-Tuning 04 (training runs) — the config and eval results the registry records.
- AI Evaluation 01, 05, 06 — the golden and adversarial sets and the gate.
- Model Serving 01 (choosing a model) — the ADR discipline that pairs with the registry.
- `docs/decisions/` — where related release decisions are recorded.
