---
id: evaluation/rag-quality-check
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: evaluation
entry_point: true
---

# Evaluation Workflow — RAG Quality Check

- **Prompt:** `.ai/prompts/roles/principal-system-designer.md`
- **Template:** `templates/evaluation-report.template.md`

## Inputs

- A RAG pipeline (chunking → embedding → retrieval → LLM) and a labeled dataset under
  `evaluations/rag/datasets/`

## Steps

1. Define retrieval and answer-quality metrics (e.g. recall@k, faithfulness, hallucination rate).
2. Run queries; record retrieved contexts and answers.
3. Compare against `evaluations/rag/baselines/`.
4. Capture failure cases (wrong retrieval, hallucination) with likely cause.
5. Decide: ship or iterate.

## Artifacts Produced

- `evaluations/rag/reports/<date>-report.md`

## Exit Criteria

- Metrics measured vs. baseline; failures categorized; accept/reject decision recorded.

## Next

→ Tune chunking/retrieval/re-ranking; re-run; record ADR for strategy changes.
