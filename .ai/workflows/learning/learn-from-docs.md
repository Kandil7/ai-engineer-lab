---
id: learning/learn-from-docs
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: learning
entry_point: true
---

# Learning Workflow — Learn From Docs

- **Prompt:** `.ai/prompts/roles/source-learning-agent.md` (+ `tasks/source-extractor.md`)
- **Template:** `templates/source-doc.template.md`

## Inputs

- A documentation page / article URL
- The project task that motivated reading it

## Steps

1. State why you're reading this (the concrete problem).
2. Extract confirmed key concepts; separate your inferences.
3. Keep minimal examples worth retaining.
4. Produce one practical exercise tied to a project task.
5. Write the Arabic summary.

## Artifacts Produced

- `docs/learning/source-summaries/<slug>.md`
- Entry in `learning-sources/source-index.md`

## Exit Criteria

- Summary links to a real project task; confirmed vs. inferred separated.

## Next

→ `source-to-exercise.md` to expand the exercise, or apply directly in the project.
