# Model Governance — Glossary 17

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Bias | Governance | Systematic, unfair error against a group |
| Demographic parity | Fairness | Equal positive-decision rate across groups |
| Disparate impact | Fairness | Ratio of positive rates; < 0.8 signals adverse impact |
| Equalized odds | Fairness | Equal TPR and FPR across groups |
| Explainability | Governance | Reasons a human can inspect for a decision |
| Fairness gate | CI/CD | A promotion gate on group-fairness metrics |
| Global explanation | Explainability | What the model learned overall |
| Local explanation | Explainability | Why this one prediction |
| Model card | Governance | Standard artifact stating use, metrics, limits |
| Predictive parity | Fairness | A score means the same thing in every group |
| Proxy feature | Bias | A "neutral" feature correlated with a protected one |
| Protected attribute | Governance | A group attribute (age, region, sex) protected by policy |

## Detailed Definitions
### Bias
**Definition**: A systematic, repeatable error that disadvantages a group; enters
through historical data, sampling, labels, proxies, or measurement.
**Related**: Proxy feature, Fairness metrics

### Demographic parity
**Definition**: The fairness definition that each group receives positive
decisions at the same rate; measured as the max minus min group rate.
```python
dp_gap = max(rates.values()) - min(rates.values())
```
**Related**: Disparate impact, Fairness gate

### Disparate impact
**Definition**: The ratio of a group's positive rate to a reference group's;
below 0.8 (the "80% rule") is a legal red flag in US employment.
```python
di = rate_unprivileged / rate_privileged
```
**Related**: Demographic parity

### Equalized odds
**Definition**: Each group has the same true-positive and false-positive rates —
the definition that cares about errors, not just positive rates.
**Related**: Demographic parity, Predictive parity

### Explainability
**Definition**: The production of reasons a human can inspect for a model's
decisions, at global (model) and local (single decision) scope.
**Related**: Local explanation, Model card

### Fairness gate
**Definition**: A CI/registry gate that blocks promotion when a candidate exceeds
the fairness threshold or widens the group gap versus the champion.
**Related**: Governance, Disparate impact

### Global explanation
**Definition**: What the model learned overall — feature importance, SHAP
summary, partial dependence — for developers and reviewers.
**Related**: Local explanation

### Local explanation
**Definition**: Why one prediction was made — reason codes, LIME, per-row SHAP —
the deliverable for the affected person and for regulators.
**Related**: Global explanation, Explainability

### Model card
**Definition**: The standard governance artifact: intended use, out-of-scope,
training data, evaluation metrics, and known limits.
**Related**: Governance, Fairness gate

### Predictive parity
**Definition**: The property that a given score carries the same meaning in every
group (equal precision across groups).
**Related**: Equalized odds

### Proxy feature
**Definition**: A feature that looks neutral but correlates with a protected
attribute (zip code for race), reintroducing bias after the attribute is dropped.
**Related**: Bias

## Key Concepts Summary
### The four fairness definitions
- Demographic parity: equal positive rates.
- Equalized odds: equal error rates.
- Predictive parity: equal meaning of a score.
- Disparate impact: the legal ratio.

### Two scopes of explanation
- Global: what the model learned.
- Local: why this decision.

### The hard truth
- Fairness and accuracy trade off; you choose and record, not pretend.

## Practice Terms
Match each term to its definition (answers at the bottom).
1. Proxy feature — ___
2. Disparate impact — ___
3. Local explanation — ___
4. Model card — ___
5. Equalized odds — ___

**Answers:** 1-c, 2-d, 3-e, 4-a, 5-b where a=standard governance artifact,
b=equal TPR/FPR across groups, c=neutral feature correlated with a protected one,
d=ratio of positive rates below 0.8, e=why this one prediction.
