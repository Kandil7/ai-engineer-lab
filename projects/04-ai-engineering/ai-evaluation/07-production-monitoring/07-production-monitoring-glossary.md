# AI Evaluation 07: Production Monitoring — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Production metrics | Latency, error rate, quality | tracked over time |
| Dashboard | The metrics display | p50, p95, p99 |
| Alert | The threshold-crossing signal | latency > p95 |
| Feedback loop | User feedback -> eval set | failures become tests |
| Quality drift | Slow degradation over time | rolling metric |
| Baseline | The reference quality level | comparison target |
| Error rate | 5xx, 429, timeouts | reliability |

---

## Alphabetical Glossary

### Alert

**Definition:** The signal fired when a metric crosses a threshold. The
notification that something is wrong.

**Example:**
```python
# alert when p95 latency > 2s or error rate > 1%
```

**Related concepts:** Dashboard

---

### Baseline

**Definition:** The reference quality level. Drift is measured against it.

**Example:**
```python
# faithfulness baseline 0.92; drift if rolling < 0.88
```

**Related concepts:** Quality drift

---

### Dashboard

**Definition:** The display of production metrics over time. Shows latency
percentiles, error rate, and quality.

**Example:**
```python
# p50, p95, p99 latency; error rate; faithfulness
```

**Related concepts:** Alert

---

### Error rate

**Definition:** The fraction of failed requests: 5xx, 429, timeouts. The
reliability metric.

**Example:**
```python
# error rate = 0.5% under normal load
```

**Related concepts:** Production metrics

---

### Feedback loop

**Definition:** Collecting user feedback (thumbs up/down, corrections) and
feeding it into the eval set. Failures become test cases.

**Example:**
```python
# user complaint -> golden set entry
```

**Related concepts:** Quality drift

---

### Production metrics

**Definition:** The three groups tracked in production: latency, error
rate, and quality.

**Example:**
```python
# latency: p95; error rate: 1%; quality: faithfulness 0.92
```

**Related concepts:** Dashboard

---

### Quality drift

**Definition:** The slow degradation of answer quality over time. Caused
by a changing corpus, user base, or model. Detected against the baseline.

**Example:**
```python
# rolling faithfulness drops from 0.92 to 0.85 -> drift
```

**Related concepts:** Baseline

---

## Related Concepts

- **Eval in CI**: the pre-production gate (topic 06)
- **Faithfulness**: the quality metric (topic 02)
- **LLM-as-judge**: the quality grader (topic 04)

## Key Takeaways

1. Three metric groups: latency, error rate, quality.
2. The dashboard shows the metrics over time.
3. Alerts fire on threshold crossings.
4. Feedback feeds the eval set.
5. Drift is detected against the baseline.