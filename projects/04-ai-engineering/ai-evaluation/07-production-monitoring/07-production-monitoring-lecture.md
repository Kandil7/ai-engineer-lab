# AI Evaluation 07: Production Monitoring

## Topic Overview

A system that passes its evals can still fail in production. The evals run on fixed
sets in a quiet room; production is a moving target with a changing corpus, real
traffic, an evolving user base, and dependencies that go down. Monitoring is how you
find out that the system is degrading before your users tell you, or after they do but
with a number attached.

This lecture covers the three groups of production metrics (latency, errors, and
quality), the dashboard that makes them visible, the alerts that fire on threshold
crossings, the feedback loop that turns production failures into test cases, and drift
detection. It also covers the signals that are specific to AI systems, where "the
answer got worse" is not visible in a traditional error rate.

Monitoring is the production counterpart of the eval harness: the harness catches
regressions before they ship, and monitoring catches the ones that ship anyway and the
ones caused by the world changing underneath the system.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Choose the production metrics for a RAG or LLM system.
2. Design a dashboard that shows latency, errors, and quality over time.
3. Set alert thresholds that fire on real degradations and not on noise.
4. Close the feedback loop from production failures to the eval set.
5. Detect quality drift against the baseline.
6. Add AI-specific signals such as abstention rate, citation failure, and cost.

## Prerequisites

- AI Evaluation 06 (eval in CI) for the baseline and threshold discipline.
- Basic familiarity with a percentile and a time series.

---

## 1. The Metrics

Production metrics fall into three groups:

| Group | Metrics | What it answers |
| --- | --- | --- |
| **Latency** | time to first token, total time, p50/p95/p99 | Is it fast enough? |
| **Errors** | 5xx rate, 429 rate, timeouts, retries | Is it reliable? |
| **Quality** | faithfulness, citation precision, user feedback | Is the answer good? |

The first two are standard service metrics. The third is what makes an AI system
different: the service can be fast and reliable while the answers quietly get worse.

### Percentiles, not averages

Report p50, p95, and p99, not the mean. Averages hide the tail, and the tail is what
users experience on the worst queries. A p95 latency of 2 seconds with a p99 of 30
seconds is a system with a serious problem that the average conceals.

## 2. The Dashboard

### What it shows

The dashboard displays the metrics over time. Latency percentiles show the tail; the
error rate shows reliability; quality metrics show the answer's health. Time series
make a trend visible where a single number would not.

### Why over time

A snapshot cannot distinguish a stable system from one that is drifting. The dashboard's
value is the slope: recall or faithfulness trending down over two weeks is a signal no
single-day number provides.

### Grouped by segment

Break quality metrics down by query type (verse, hadith, fiqh, unanswerable) where
possible. An aggregate that holds steady can hide one segment collapsing under a
corpus or traffic shift.

## 3. Alerts

### Fire on threshold crossings

Alerts fire when a metric crosses a threshold: latency above p95 target, error rate
above 1%, quality below the baseline. The exercise's `should_alert` returns the list of
breached thresholds:

```python
def should_alert(latency_p95: float, error_rate: float, thresholds: dict) -> list[str]:
    alerts = []
    if latency_p95 > thresholds["latency_p95"]:
        alerts.append("latency")
    if error_rate > thresholds["error_rate"]:
        alerts.append("error_rate")
    return alerts
```

### Alert quality

An alert that fires constantly is ignored, and an ignored alert is worse than none. Set
thresholds from measured normal behavior, add a short duration requirement so a single
spike does not page anyone, and alert on the signals that correspond to real user pain.

### Alert on quality separately

Latency and error alerts do not catch a quality regression. A faithful, fast, reliable
system that started hallucinating needs its own alert, derived from the rolling quality
metric below.

## 4. The Feedback Loop

### Collect feedback

User feedback, whether explicit (thumbs up/down, corrections) or implicit (retries,
abandonment, follow-up questions), is a stream of labels about the system's real
behavior.

### Feed the eval set

The loop turns production failures into test cases. A query that produced a bad answer
becomes a candidate golden-set entry once its correct answer is verified. Over time the
golden set reflects the failures real users hit, not only the ones the author imagined.

### Close the loop all the way

Collecting feedback that nobody reads is theater. The loop is closed only when a
production failure becomes a new test case that the harness runs on every future
change, so the same failure cannot return silently.

## 5. Quality Drift

### What it is

Quality drift is the slow degradation of answer quality over time. The cause is usually
a changing corpus (new documents shift retrieval), a changing user base (new query
types), or a model or dependency update on the provider side.

### Detect against the baseline

Detect drift by comparing a rolling quality metric to the baseline:

```python
def detect_drift(rolling: list[float], baseline: float, tolerance: float) -> bool:
    """Drift when the rolling quality drops below the baseline minus tolerance."""
    recent = rolling[-3:]
    avg = sum(recent) / len(recent)
    return avg < baseline - tolerance
```

The exercise asserts no drift on stable data and drift detected when the rolling
average drops, which is the mechanism: a short window average compared to the baseline
with a tolerance that absorbs normal variation.

### Why drift is easy to miss

Drift has no single dramatic event. Each day looks slightly like the last, so nothing
alarms until the aggregate has moved a lot. The rolling metric against a fixed baseline
is what makes the slow slide visible early.

## 6. AI-Specific Signals

Beyond latency and errors, watch signals that only an LLM system produces:

- **Abstention rate.** A sudden rise means retrieval is failing; a sudden fall may mean
  the system stopped abstaining and started answering unsupported questions.
- **Citation failure rate.** The fraction of answers whose claims are not supported by
  their citations; a rise is a fidelity regression.
- **Cost per request.** Token usage creeping up is a quiet budget leak and often
  precedes a quality change.
- **Guardrail trigger rate.** A spike can mean an attack, a corpus change, or an
  over-aggressive filter.

Each of these is a leading indicator that a traditional error rate would miss entirely.

## 7. Incident Response Link

Monitoring is the detection half of operations. When an alert fires, incident response
takes over: triage, mitigation, recovery, and a postmortem that names the gap and
creates the test that will catch it next time. The postmortem feeds the adversarial or
golden set, which is how an incident makes the system permanently better rather than
just restored.

## Real-World Application

- A p95 latency alert on the DevMate `/ask` endpoint and a quality alert on rolling
  faithfulness.
- A dashboard segmenting Athar retrieval quality by question type so one segment's
  collapse is visible.
- Turning a bad production answer into a golden-set entry after verifying the correct
  answer.
- Noticing a rising abstention rate as the early signal that a corpus change broke
  retrieval.

## Common Mistakes

1. **No dashboard.** Metrics that nobody can see do not exist.
2. **No alerts.** Failures are detected by users first.
3. **No feedback loop.** The same production failure repeats.
4. **No drift detection.** Slow degradation is invisible until it is large.
5. **Monitoring latency but not quality.** A fast, reliable, wrong system looks healthy.
6. **Averaging latency.** The tail, where users suffer, is hidden.
7. **Alerts that fire constantly.** They get ignored, which defeats the alert.

## Key Takeaways

1. Three metric groups: latency (percentiles), error rate, and quality.
2. The dashboard shows the metrics over time; the slope is the signal.
3. Alerts fire on threshold crossings derived from measured normal behavior; quality
   needs its own alert.
4. The feedback loop turns production failures into golden-set entries, closing the
   loop between production and the harness.
5. Drift is detected by a rolling quality metric against the baseline, and AI-specific
   signals (abstention, citation failure, cost) catch what error rates miss.

## Self-Check Questions

1. Why report p95 and p99 latency instead of the average?
2. Why can a system be fast and reliable and still be unhealthy?
3. How does the feedback loop connect production to the eval harness?
4. What is quality drift, and what are two common causes?
5. Name two AI-specific signals and what each one tells you.

## Further Reading / Connections

- AI Evaluation 06 (eval in CI) — the pre-ship half of the same discipline.
- `projects/04-ai-engineering/rag-system/05-abstention-citations` — the abstention and
  citation signals.
- `docs/reference/llm-production-architecture.md` — the observability and monitoring
  section.
- `docs/WEEKLY_PROTOCOL.md` — the operating cadence that reviews these metrics.
