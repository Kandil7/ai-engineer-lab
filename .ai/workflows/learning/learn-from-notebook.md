---
id: learning/learn-from-notebook
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: learning
entry_point: true
---

# Learning Workflow — Learn From Notebook

- **Prompt:** `.ai/prompts/roles/source-learning-agent.md`
- **Template:** `templates/source-notebook.template.md`

## Inputs

- A Jupyter/Colab notebook
- The technique/pipeline you want to understand (often RAG/AI)

## Steps

1. State why this notebook.
2. Walk the cells; capture what it demonstrates step by step (confirmed).
3. Note data/model/hyperparameter assumptions.
4. Reproduce it yourself; record the result.
5. Modify one parameter, predict the effect, verify (the exercise).
6. Write the Arabic summary.

## Artifacts Produced

- `docs/learning/source-summaries/<slug>.md`
- Entry in `learning-sources/source-index.md`

## Exit Criteria

- Notebook reproduced; one variation tested; linked to a project task.

## Next

→ Apply the technique in `projects/04-ai-engineering/...`.
