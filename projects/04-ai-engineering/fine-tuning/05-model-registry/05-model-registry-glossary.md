# Fine-Tuning 05: Model Registry and Release — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Registry entry | The artifact + full provenance record | id, base, adapter, eval |
| Model card | The documentation of what/how/how well | base, data, eval, limits |
| Eval gate | The golden + adversarial set pass before release | faithfulness >= 0.9 |
| Immutable version | A change is a new version, never an edit | athar-sft-v2 |
| Rollback | Pointing deployment at a previous version | registry history |
| Provenance | Base, adapter, config, data, eval | the entry's fields |

---

## Alphabetical Glossary

### Eval gate

**Definition:** The golden and adversarial set pass required before
release. A model that improves eval loss but fails faithfulness is not
released.

**Example:**
```python
# faithfulness >= 0.9 and resistance >= 0.9 to release
```

**Related concepts:** Registry entry

---

### Immutable version

**Definition:** The model version is the registry id and never edited. A
change to the adapter, data, or config is a new version.

**Example:**
```python
# athar-sft-v1 -> athar-sft-v2, never an edit to v1
```

**Related concepts:** Registry entry, Rollback

---

### Model card

**Definition:** The documentation of what the model is, what it was trained
on, how it performs, and its limitations. Written at release.

**Example:**
```python
# base, training data, eval results, known failure modes, intended use
```

**Related concepts:** Registry entry

---

### Provenance

**Definition:** The full record of how the model was made: base model,
adapter, config hash, data version, eval results.

**Example:**
```python
# base qwen2.5-7b, adapter athar-sft-v1, data v1, eval 0.42
```

**Related concepts:** Registry entry

---

### Registry entry

**Definition:** The single source of truth for what the model is and how it
was made. The artifact plus its provenance.

**Example:**
```python
{"id": "athar-sft-v1", "base": "qwen2.5-7b", "eval": {"faithfulness": 0.92}}
```

**Related concepts:** Provenance, Model card

---

### Rollback

**Definition:** Pointing the deployment at a previous registered version.
Mechanical only if the previous version and its artifact are still
available.

**Example:**
```python
# deploy athar-sft-v1 after v2 regresses
```

**Related concepts:** Immutable version

---

## Related Concepts

- **Training runs**: the run's output is registered (topic 04)
- **Eval in CI**: the eval gate reuses the golden and adversarial sets (ai-evaluation 06)
- **RAG vs fine-tuning**: the registry holds the fine-tuned model (topic 06)

## Key Takeaways

1. The registry entry records the artifact and its provenance.
2. The model card documents what, how, and how well.
3. Evaluate before release, not after.
4. Versions are immutable; a change is a new version.
5. The registry makes rollback mechanical.