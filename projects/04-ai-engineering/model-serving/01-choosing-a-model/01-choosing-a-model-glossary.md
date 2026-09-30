# Model Serving 01: Choosing a Model — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Capability | How well the model solves the task | golden-set score |
| Cost | Price per token | $/1M tokens |
| Latency | Time to first token | p95 |
| License | Open vs proprietary | usage rights |
| Golden set | The evaluation yardstick | 50 queries |
| ADR | The recorded decision | rationale + trigger |
| Re-evaluation | Re-running the golden set on change | task/corpus/model |

---

## Alphabetical Glossary

### ADR

**Definition:** Architecture decision record: the problem, candidates,
chosen model, rationale, and re-evaluation trigger. Evidence the choice
was deliberate.

**Example:**
```python
# ADR: chose model X for task Y; re-evaluate if corpus grows 2x
```

**Related concepts:** Golden set

---

### Capability

**Definition:** How well the model solves the task. Measured on the golden
set.

**Example:**
```python
# accuracy 0.92 on the golden set
```

**Related concepts:** Golden set

---

### Cost

**Definition:** Price per token. A per-call cost that scales with volume.

**Example:**
```python
# $0.02 / 1M tokens
```

**Related concepts:** Latency

---

### Golden set

**Definition:** The fixed evaluation yardstick. Candidates are compared on
the same queries and scored output.

**Example:**
```python
# 50 queries with verified answers
```

**Related concepts:** Capability

---

### Latency

**Definition:** Time to first token. The responsiveness axis.

**Example:**
```python
# p95 < 500ms
```

**Related concepts:** Cost

---

### License

**Definition:** Open vs proprietary. Determines whether the model can be
used and how.

**Example:**
```python
# Apache 2.0 vs commercial
```

**Related concepts:** Capability

---

### Re-evaluation

**Definition:** Re-running the golden set when the task, corpus, or model
landscape changes.

**Example:**
```python
# corpus grew 2x -> re-evaluate the model choice
```

**Related concepts:** ADR

---

## Related Concepts

- **Fine-tuning**: the alternative to a bigger model (fine-tuning 06)
- **Self-hosted models**: the deployment axis (topic 02)
- **Inference serving**: the serving axis (topic 03)

## Key Takeaways

1. Four axes: capability, cost, latency, license.
2. The task narrows the candidates.
3. The golden set evaluates the candidates.
4. The ADR records the choice.
5. Re-evaluate on change.