# AI Evaluation 06: Eval in CI — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Eval harness | One deterministic command running all sets | run_eval.py |
| Baseline | The captured metric floors to enforce | recall@5 >= 0.8 |
| Threshold | The metric floor that fails the build | faithfulness >= 0.9 |
| Delta | Current metric minus baseline | +0.05 |
| Verdict | Pass or fail per metric | PASS / FAIL |
| Eval report | The metric table committed with the change | metric, baseline, delta |
| Eval discipline | Evaluation runs on every relevant change | prompt, retriever, chunker |

---

## Alphabetical Glossary

### Baseline

**Definition:** The captured metric floors, reviewed once, then enforced.
A change that drops below the floor fails CI.

**Example:**
```python
# recall@5 baseline 0.8, enforced as the floor
```

**Related concepts:** Threshold, Delta

---

### Delta

**Definition:** Current metric minus baseline. The change is judged against
the baseline, not in isolation.

**Example:**
```python
# current 0.85, baseline 0.80 -> delta +0.05
```

**Related concepts:** Baseline, Verdict

---

### Eval discipline

**Definition:** Evaluation runs on every change that touches the prompt,
retriever, chunker, or guardrails. Not an afterthought.

**Example:**
```python
# a chunker change re-runs the harness
```

**Related concepts:** Eval harness

---

### Eval harness

**Definition:** The single deterministic command that runs the golden and
adversarial sets, computes metrics, and compares to the baseline.

**Example:**
```python
# python eval/run_eval.py --golden ... --adversarial ...
```

**Related concepts:** Eval discipline, Eval report

---

### Eval report

**Definition:** The metric table committed with the change: metric,
baseline, current, delta, verdict. Regressions visible at a glance.

**Example:**
```python
# recall@5 | 0.80 | 0.75 | -0.05 | FAIL
```

**Related concepts:** Delta, Verdict

---

### Threshold

**Definition:** The metric floor that fails the build. Thresholds without a
baseline are guesses.

**Example:**
```python
# faithfulness >= 0.9, else FAIL
```

**Related concepts:** Baseline, Verdict

---

### Verdict

**Definition:** Pass or fail per metric, decided by the threshold. The
harness's output.

**Example:**
```python
# recall@5 PASS, faithfulness FAIL
```

**Related concepts:** Threshold, Delta

---

## Related Concepts

- **Gold dataset**: the golden set runs in the harness (topic 01)
- **Adversarial set**: resistance metrics run in the harness (topic 05)
- **Faithfulness**: one of the gated metrics (topic 02)

## Key Takeaways

1. The harness is one deterministic command.
2. Thresholds come from a baseline and are enforced.
3. A change is judged against the baseline.
4. The report makes regressions visible at a glance.
5. Evaluation is part of the pipeline, not an afterthought.