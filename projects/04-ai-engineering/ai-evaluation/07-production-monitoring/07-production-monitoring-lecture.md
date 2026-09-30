# AI Evaluation 07: Production Monitoring

## 🎯 Topic Overview

A system that passes its evals can still fail in production. Monitoring
tracks the metrics that matter: latency, error rate, and answer quality.
This lecture covers the dashboard, the alerts, and the feedback loop.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Choose the production metrics
2. Design the dashboard
3. Set alert thresholds
4. Close the feedback loop
5. Detect quality drift

---

## 1. The Metrics

Production metrics fall into three groups: latency (time to first token,
total time), error rate (5xx, 429, timeouts), and quality (faithfulness,
citation precision, user feedback). The roadmap's exit test: "production
metrics are tracked."

## 2. The Dashboard

The dashboard displays the metrics over time. Latency percentiles (p50,
p95, p99) show the tail; the error rate shows reliability; quality
metrics show the answer's health. The roadmap's exit test: "a dashboard
is designed."

## 3. Alerts

Alerts fire when a metric crosses a threshold: latency above p95, error
rate above 1%, quality below the baseline. The alert is the signal that
something is wrong. The roadmap's exit test: "alert thresholds are set."

## 4. The Feedback Loop

User feedback — thumbs up/down, corrections, complaints — is collected
and fed into the eval set. The loop turns production failures into test
cases. The roadmap's exit test: "user feedback feeds the eval set."

## 5. Quality Drift

Quality drift is the slow degradation of answer quality over time. The
cause is a changing corpus, a changing user base, or a model update. The
detection is a rolling quality metric compared to the baseline. The
roadmap's exit test: "quality drift is detected."

## Common Mistakes

- No dashboard (metrics invisible).
- No alerts (failures undetected).
- No feedback loop (failures repeat).
- No drift detection (slow degradation invisible).
- Monitoring latency but not quality.

## Key Takeaways

1. Three metric groups: latency, error rate, quality.
2. The dashboard shows the metrics over time.
3. Alerts fire on threshold crossings.
4. Feedback feeds the eval set.
5. Drift is detected against the baseline.