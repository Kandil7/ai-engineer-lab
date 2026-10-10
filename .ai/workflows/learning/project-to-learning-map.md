---
id: learning/project-to-learning-map
layer: workflow
version: 1.0.0
status: active
owner: workspace
category: learning
entry_point: true
---

# Learning Workflow — Project To Learning Map

Turn any software/AI project into a learning map: the concepts it requires,
your current level, the gaps, and an ordered study plan tied to real content.

- **Prompt:** `.ai/prompts/roles/learning-coach.md`
- **Template:** `templates/learning-map.template.md`
- **Backbone:** `registries/knowledge-registry.yaml`

## Inputs

- A project path or a short description of what you want to build
- Your current mastery snapshot (`docs/roadmap/skills-matrix.md`)

## Steps

1. Decompose the project into the concepts it needs, using node ids from
   `registries/knowledge-registry.yaml`. If a concept is missing, add a node
   (with prerequisites, taught_in, sources, exercises, used_by_projects, and
   evidence) before continuing.
2. Order the concepts by prerequisites (topological order from the registry).
3. For each concept, read its `taught_in`, `sources`, and `exercises`.
4. Compare against your current level; mark each concept known / shaky / gap.
5. Build the study plan: gap concepts first, each with its source, exercise,
   and evidence check.
6. Fill the map from `templates/learning-map.template.md`.

## Artifacts Produced

- `docs/learning/paths/<project>-learning-map.md`
- New concept nodes appended to `registries/knowledge-registry.yaml` if missing

## Exit Criteria

- Every required concept maps to a registry node, a source, and an evidence check.
- Gaps are ordered by prerequisites and each has a concrete next action.

## Next

→ `learn-from-docs.md` or `source-to-exercise.md` for the top gap, then apply
directly in the project.
