# Fine-Tuning 05: Model Registry and Release

## 🎯 Topic Overview

A fine-tuned model is an artifact that must be versioned, documented, and
evaluated before release. The model registry tracks every artifact: the
base model, the adapter, the config, the eval results, and the model card.
This lecture covers the registry entry, the model card, and the release
gate.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Register a model artifact with its full provenance
2. Write a model card that documents the training
3. Evaluate before release, not after
4. Version the model and its dependencies
5. Roll back to a previous version

---

## 1. The Registry Entry

A registry entry records the artifact and its provenance: base model,
adapter, config hash, data version, eval results, and the model card. The
entry is the single source of truth for what the model is and how it was
made. The roadmap's exit test: "the model is registered with its
provenance."

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

## 2. The Model Card

The model card documents what the model is, what it was trained on, how it
performs, and its limitations. It is written at release, not after. The
card answers: base model, training data, eval results, known failure
modes, and intended use. A model without a card is an artifact without a
story.

## 3. Evaluate Before Release

A model is released only after it passes the eval gate: the same golden
set and adversarial set that gate the RAG system. A model that improves
eval loss but fails faithfulness is not released. The roadmap's exit test:
"the model is evaluated before release."

## 4. Versioning

The model version is the registry id. The version is immutable — a change
to the adapter, the data, or the config is a new version, never an edit.
The base model version and the adapter version are both recorded, because
the adapter is meaningless without its base.

## 5. Rollback

A released model can regress in production. The registry makes rollback
mechanical: point the deployment at the previous version. Rollback is only
possible if the previous version is still registered and its artifact is
still available. The registry is the safety net.

## Common Mistakes

- Releasing without a registry entry.
- No model card (the artifact has no story).
- Releasing before the eval gate.
- Editing a version instead of creating a new one.
- No rollback path (the registry is empty of history).

## Key Takeaways

1. The registry entry records the artifact and its provenance.
2. The model card documents what, how, and how well.
3. Evaluate before release, not after.
4. Versions are immutable; a change is a new version.
5. The registry makes rollback mechanical.