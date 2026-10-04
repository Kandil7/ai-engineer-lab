# MLOps — 17: Model Governance

## Topic Overview

Model governance is the set of policies, measurements, and artifacts that make a
model's behavior **auditable, explainable, and fair** — and that make those
properties checkable by someone who did not build the model. A registry (Lecture
04) tracks *which* model is live; governance answers the harder questions: is it
biased against a group, can its decisions be explained, and can you prove both to
a regulator, a customer, or a court?

Governance is not one tool but four practices layered on the lifecycle. **Bias
detection** measures whether the model treats groups unequally. **Fairness
metrics** turn that measurement into numbers with agreed definitions.
**Explainability** produces reasons a human can inspect — globally (what the
model learned) and locally (why this prediction). **Model cards** and audit
trails record all of it as durable evidence. Together they turn "we think the
model is fair" into "here is the measurement, the definition, and the record."

This matters most exactly where models decide about people: credit, hiring,
lending, insurance, medical triage, and content moderation. It is also a hard
engineering problem, because fairness and accuracy trade off against each other —
there is no free lunch, only explicit choices. The AI engineer's job is to make
those choices visible, measured, and recorded, not to pretend they do not exist.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Explain what model governance is and the four practices it comprises
2. Identify the sources of bias in data, labels, sampling, and proxies
3. Compute the core group-fairness metrics and state their trade-offs
4. Distinguish global from local explainability and when each is required
5. Write a model card that records a model's intended use and limits
6. Explain why fairness and accuracy conflict, and how to choose explicitly
7. Wire governance gates into the lifecycle (registry, CI, audit)

## Prerequisites

| Need | Where |
|---|---|
| Model registry + lifecycle | `08-mlops/lectures/04-model-registry-lecture.md` |
| Metrics (precision/recall/AUC) | `07-machine-learning/advanced/27-metrics-deep-lecture.md` |
| Experiment tracking | `08-mlops/lectures/02-experiment-tracking-lecture.md` |
| CI gates | `08-mlops/lectures/12-ci-cd-for-ml-lecture.md` |

## 1. What Model Governance Is

Governance is the answer to four questions a stakeholder will ask about any model
that touches people:

1. **What does it decide, and for whom?** (scope and population)
2. **Is it fair across groups?** (bias and fairness)
3. **Why did it decide this?** (explainability)
4. **Can you prove all of the above?** (audit and documentation)

A registry records the *artifact*; governance records the *justification*. The
distinction matters because a model can be perfectly reproducible (Lecture 01),
correctly versioned (Lecture 04), and still be discriminatory or unexplainable.

```python
# A governance record is a first-class artifact, like a model version.
governance_record = {
    "model": "credit_risk",
    "version": "3.1.0",
    "intended_use": "loan pre-screening for adults",
    "protected_attributes": ["age", "region"],
    "fairness": {"demographic_parity_gap": 0.03, "threshold": 0.05},
    "explainability": "global SHAP + per-decision reason codes",
    "approved_by": "risk-committee",
    "evidence": ["model_card.md", "bias_report.json", "eval_gate_run_4821"],
}
```

The record is what an auditor reads. If it does not exist, the model is
ungoverned regardless of how good it is.

## 2. Where Bias Comes From

Bias is not a single bug; it enters at five distinct points, and each has a
different fix.

| Source | What happens | Example |
|---|---|---|
| Historical | The world's past inequity is the training signal | Loan data reflects past lending discrimination |
| Sampling | Some groups are under-represented | A dataset with few older applicants |
| Label | The label encodes a biased judgement | "Promoted" labels from a biased manager |
| Proxy | A neutral feature correlates with a protected one | Zip code as a proxy for race |
| Measurement | The target itself is measured unequally | Health cost as a proxy for health need |

The proxy source is the most insidious: dropping the protected attribute does not
remove bias if a correlated feature remains. A model that never sees "race" can
still discriminate through "zip code". This is why fairness is measured on
*outcomes by group*, never by checking that the feature list looks clean.

```python
def proxy_correlation(df, protected, candidate):
    """A high correlation between a 'neutral' feature and a protected one is a red flag."""
    return abs(df[[protected, candidate]].corr().iloc[0, 1])
```

## 3. Fairness Metrics

There is no single definition of fairness. The four common ones measure different
things, and a model can satisfy one while violating another.

- **Demographic parity**: each group receives positive decisions at the same rate.
- **Equalized odds**: each group has the same true-positive and false-positive rates.
- **Predictive parity**: a given score means the same thing in each group.
- **Disparate impact**: the ratio of positive rates clears a legal threshold (the
  "80% rule" in US employment law).

```python
def demographic_parity_gap(y_pred, group):
    """Max difference in positive-decision rate across groups."""
    rates = {g: y_pred[group == g].mean() for g in set(group)}
    return max(rates.values()) - min(rates.values())


def disparate_impact(y_pred, group, privileged, unprivileged):
    """Ratio of positive rates; < 0.8 or > 1.25 signals adverse impact."""
    rp = y_pred[group == privileged].mean()
    ru = y_pred[group == unprivileged].mean()
    return ru / rp if rp else float("inf")
```

The metric you choose is a *policy decision*, not a technical one. A hiring model
might be held to equalized odds; a lending model to disparate impact. Naming the
metric and the threshold is part of governance.

## 4. Explainability Requirements

Explainability has two scopes, and different stakeholders need different ones.

- **Global**: what the model learned overall — feature importances, SHAP summary
  plots, partial-dependence. This is for model developers and reviewers.
- **Local**: why *this* prediction — per-decision reason codes, LIME, SHAP values
  for one row. This is for the person affected and for regulators.

```python
# A local reason code is a human-readable "why", not a raw weight vector.
def reason_codes(row, contributions, top_k=3):
    ranked = sorted(contributions.items(), key=lambda kv: abs(kv[1]), reverse=True)
    return [f"{name}: {'+' if w > 0 else ''}{w:.2f}" for name, w in ranked[:top_k]]
```

The "right to explanation" in regulations such as GDPR turns local explainability
from a nice-to-have into a legal requirement for automated decisions. A reason
code ("declined because: debt-to-income +1.2, recent delinquency +0.8") is the
deliverable.

## 5. Model Cards

A model card is the standard governance artifact: a short, structured document
that states what a model is for, how it was evaluated, and where it must not be
used. It is the human-readable companion to the registry's machine-readable
metadata.

```markdown
# Model Card: credit_risk v3.1.0
- Intended use: loan pre-screening for adults (>= 18)
- Out-of-scope: final credit decisions; minors; non-residents
- Training data: 2019-2024 applications, n=1.2M
- Evaluation: AUC 0.81; DP gap 0.03; DI 0.92
- Known limits: under-represents rural applicants; cost-based label proxy
- Ethical considerations: reviewed by risk committee; reason codes served
```

The card's most valuable section is *out-of-scope*: naming where the model must
not be used is how governance prevents misuse, not just documents it.

## 6. Fairness Versus Accuracy

The impossibility results (Chouldechova, Kleinberg et al.) say you cannot, in
general, satisfy all fairness definitions at once when base rates differ between
groups. Improving one metric degrades another, and improving fairness often
costs accuracy.

This is the central governance insight: there is no technically "correct" answer,
only an explicit trade-off. The job is to:

1. Measure the trade-off curve (accuracy and each fairness metric).
2. Choose a point *with the stakeholder* and record the choice.
3. Monitor the chosen point in production (Lecture 11), because drift moves it.

```python
def fairness_accuracy_tradeoff(thresholds, scores, y_true, group):
    """Sweep the decision threshold; report accuracy and DP gap at each point."""
    rows = []
    for t in thresholds:
        y_pred = (scores >= t).astype(int)
        acc = (y_pred == y_true).mean()
        rows.append(
            {"threshold": t, "accuracy": acc, "dp_gap": demographic_parity_gap(y_pred, group)}
        )
    return rows
```

Presenting this table, and the recorded decision, is governance. Hiding it is
how organizations ship a model they cannot defend.

## 7. Governance in the Lifecycle

Governance is not a one-time report; it is wired into the lifecycle as gates,
exactly like the eval gate (Lecture 12).

- **Training**: bias detection runs on the data and the labels; proxy features
  are flagged before training.
- **Pre-deploy**: a fairness gate joins the eval gate — a candidate that widens
  the group gap beyond the threshold does not ship.
- **Registry (Lecture 04)**: the governance record (model card, bias report,
  approver) is attached to the version; promotion requires it.
- **Production (Lecture 11)**: fairness metrics are monitored like accuracy;
  drift in a group gap triggers an alert.
- **Audit**: the trail (who approved, what evidence, which thresholds) is the
  compliance artifact.

```python
def governance_gate(candidate, champion, max_dp_gap=0.05):
    """A candidate must not exceed the fairness threshold, nor widen the gap."""
    if candidate["dp_gap"] > max_dp_gap:
        return False, f"FAIL: dp_gap {candidate['dp_gap']:.3f} > {max_dp_gap}"
    if candidate["dp_gap"] > champion["dp_gap"] + 0.01:
        return False, "FAIL: fairness regressed vs champion"
    return True, "PASS: fairness within bounds"
```

## Every Use Case

- **Credit and lending**: disparate-impact measurement is a legal requirement;
  reason codes are served to applicants.
- **Hiring**: equalized-odds review before any model touches candidates.
- **Healthcare triage**: measurement-bias checks (cost vs need) before deployment.
- **Content moderation**: fairness across languages and dialects, not just the
  majority language.
- **Insurance pricing**: predictive-parity checks so a score means the same thing
  for every group.
- **Recommendation**: exposure fairness (which creators get shown).
- **Internal ML platform**: a shared governance gate so no team can ship an
  unmeasured model.

## Real-World Use Cases for AI Engineers

- **Fintech engineer**: the fairness gate runs in CI alongside the eval gate; a
  candidate that improves AUC but widens the DP gap is rejected automatically,
  and the rejection is recorded in the registry as audit evidence.
- **Health-tech engineer**: a model trained on cost data is caught by a
  measurement-bias review — cost under-represents need for under-served groups —
  and the label is rebuilt around a clinical outcome before training.
- **HR-tech engineer**: every model card names "final hiring decision" as
  out-of-scope; the card is a gate item, so a team cannot deploy a model whose
  intended use is misstated.
- **Platform engineer**: governance is packaged as a reusable CI job (bias report
  + fairness gate + model-card lint), so 20 teams inherit the same bar.
- **Arabic/Islamic content system (Athar)**: fairness across dialect and
  era-of-source, so retrieval does not systematically under-serve a register.

## Common Mistakes to Avoid

### Mistake 1: Dropping the protected attribute and calling it fair
Bias persists through proxies (zip code, device, name). Measure outcomes by
group, not the feature list.

### Mistake 2: Reporting accuracy only
A single accuracy number hides group harm. Report accuracy and the fairness
metrics together, always.

### Mistake 3: Picking the fairness metric after seeing the numbers
Choosing the definition that flatters the model is not governance. Fix the
metric and threshold *before* measuring.

### Mistake 4: A model card with no out-of-scope section
Naming where the model must not be used is the point. A card without limits is
marketing.

### Mistake 5: Explaining only globally
A global SHAP plot does not tell an affected person why *they* were declined.
Local reason codes are the legal deliverable.

### Mistake 6: Governance as a one-time report
Fairness drifts (Lecture 11). A report filed once and never monitored is stale
the moment the data shifts.

### Mistake 7: Hiding the fairness/accuracy trade-off
Pretending there is no trade-off is the failure mode that produces indefensible
models. Surface the curve and record the choice.

## Best Practices

1. Name the protected attributes and the fairness metric before training
2. Measure outcomes by group, never by inspecting the feature list
3. Check for proxy features (correlation with protected attributes)
4. Report accuracy and fairness together, never accuracy alone
5. Sweep the fairness/accuracy trade-off and record the chosen point
6. Serve local reason codes for every automated decision about a person
7. Write a model card with a real out-of-scope section
8. Gate promotion on fairness, not just on the eval metric
9. Attach the governance record to the registry version
10. Monitor group fairness in production and alert on drift

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Bias scan on data | minutes | O(data) | sample the dataset |
| Fairness metric | O(n) | O(1) | — |
| Global explainability (SHAP) | minutes-hours | O(data) | sample background set |
| Local reason codes | ms per decision | O(features) | cached explainer |
| Model card + review | hours (human) | — | — |
| Production fairness monitoring | per-window | O(predictions) | sampled monitoring |

## AI Engineering Relevance

**Where this shows up:** every model that decides about people. Governance is
what makes those models defensible; without it, an accurate model is still a
liability.

| Concept here | Used for |
|---|---|
| Bias sources | Finding harm before it ships |
| Fairness metrics | Turning harm into measured numbers |
| Explainability | The right to explanation |
| Model cards | Durable, auditable evidence |
| Fairness gate | Wiring governance into the lifecycle |

**Scale note:** at 20 teams × 50 models, governance must be a reusable gate, not
a per-model manual review. The bias report + fairness gate + model-card lint
packaged as a CI job is how a platform team enforces one bar across many teams.

## Practice Exercises

### Exercise 1: Demographic Parity (Easy)
Implement `demographic_parity_gap(y_pred, group)` and test it on a group split
where one group's positive rate is double the other's.

### Exercise 2: Disparate Impact (Medium)
Implement `disparate_impact(y_pred, group, privileged, unprivileged)` and flag
the 80% rule; test the pass, fail, and zero-rate cases.

### Exercise 3: Proxy Detector (Medium)
Implement `proxy_features(df, protected, candidates, threshold)` returning the
candidate features correlated above the threshold — the "neutral feature" trap.

### Exercise 4: Fairness Gate (Hard)
Implement `governance_gate(candidate, champion, max_dp_gap)` and integrate it
with an accuracy check so a candidate must pass *both* to promote; write the
pass/fail/regress cases as tests.

## Summary

| Concept | Description |
|---|---|
| Governance | Policies + measurements + artifacts that make a model auditable |
| Bias sources | Historical, sampling, label, proxy, measurement |
| Fairness metrics | Parity, equalized odds, predictive parity, disparate impact |
| Explainability | Global (what it learned) vs local (why this decision) |
| Model card | The standard governance artifact, with out-of-scope |
| Fairness gate | Governance wired into CI and the registry |

Model governance turns a model's fairness, explainability, and provenance from
claims into measured, recorded facts. It is the discipline that makes an accurate
model also a defensible one — and in regulated domains, it is the difference
between shipping and not shipping at all.

## Quick Reference

| Task | Idiom |
|---|---|
| Parity gap | `max(rate) - min(rate)` across groups |
| Disparate impact | `rate_unprivileged / rate_privileged` (flag < 0.8) |
| Proxy check | correlation of candidate vs protected attribute |
| Local reason | top-k signed feature contributions |
| Model card | intended use + out-of-scope + metrics + limits |
| Fairness gate | `candidate.dp_gap <= threshold` and not worse than champion |

## Next Steps

Next: **[18 Tracking Platforms](18-tracking-platforms-lecture.md)** — MLflow,
W&B, Comet, Neptune, Sacred, and how to choose.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs: https://fairmlbook.org/, https://modelcards.withgoogle.com/about
