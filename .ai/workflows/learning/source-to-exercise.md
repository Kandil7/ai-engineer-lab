---
id: learning/source-to-exercise
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: learning
entry_point: false
---

# Learning Workflow — Source To Exercise

Convert any source summary into a concrete, gradeable exercise.

- **Prompt:** `.ai/prompts/roles/learning-coach.md` + `roles/source-learning-agent.md`

## Inputs

- An existing `docs/learning/source-summaries/<slug>.md`

## Steps

1. Identify the single most useful skill from the summary.
2. Design a small exercise that forces applying it in the active project.
3. Define a clear "done" / success check for the exercise.
4. After completion, do active recall and capture gaps.

## Artifacts Produced

- Exercise section appended to the source summary
- Code/artifact in the relevant `projects/...` folder

## Exit Criteria

- Exercise completed and tied to project code; gaps recorded.

## Next

→ Reflect (`feature/06-reflect.md` pattern) or schedule spaced repetition.
