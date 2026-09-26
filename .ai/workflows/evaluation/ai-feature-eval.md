---
id: evaluation/ai-feature-eval
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: evaluation
entry_point: true
---

# Evaluation Workflow — AI Feature Eval

- **Prompt:** `.ai/prompts/roles/principal-system-designer.md` (eval-planning) + `roles/code-reviewer.md`
- **Template:** `templates/evaluation-report.template.md`

## Inputs

- An AI feature (chat, retrieval, agent) and a golden/test set

## Steps

1. Define what decision the eval informs and the metrics + targets.
2. Assemble or reference the golden cases under `evaluations/...`.
3. Run the feature against the set; record metrics and failures.
4. Analyze: improvement vs. regression; accept or iterate.

## Artifacts Produced

- `evaluations/projects/<system>/<date>-report.md`

## Exit Criteria

- Metrics measured against targets; explicit accept/reject decision with rationale.

## Next

→ Iterate, or record an ADR if a model/architecture choice is implied.
