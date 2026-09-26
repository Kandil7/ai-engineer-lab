---
id: learning/learn-from-repo
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: learning
entry_point: true
---

# Learning Workflow — Learn From Repo

- **Prompt:** `.ai/prompts/roles/source-learning-agent.md`
- **Template:** `templates/source-repo.template.md`

## Inputs

- A GitHub/code repository URL
- The pattern or problem you're investigating

## Steps

1. Map the repo: entry points, layers, key packages.
2. Identify patterns worth adopting and anti-patterns to avoid.
3. Separate confirmed structure from your inferences about design intent.
4. Port/adapt one small piece in your own style (with attribution).
5. Write the Arabic summary.

## Artifacts Produced

- `docs/learning/source-summaries/<slug>.md`
- Entry in `learning-sources/source-index.md`

## Exit Criteria

- At least one adoptable pattern identified and linked to a project task.

## Next

→ Apply the pattern in the relevant `projects/...` folder.
