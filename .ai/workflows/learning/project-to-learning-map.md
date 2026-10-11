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

1. Run the deterministic analyzer first:
   `powershell -NoProfile -ExecutionPolicy Bypass -File infra/scripts/learning-map.ps1 -Project <name>`
   It selects the project's concepts from `registries/knowledge-registry.yaml`,
   reads current levels from `registries/evidence.yaml`, and prints a
   prerequisite-ordered study plan with the gaps. No LLM needed for this part.
2. Decompose anything the registry is missing into new concept nodes (with
   prerequisites, taught_in, sources, exercises, used_by_projects, and
   evidence) before continuing.
3. Order the concepts by prerequisites (the script already does this).
4. For each concept, read its `taught_in`, `sources`, and `exercises`.
5. Compare against your current level; mark each concept known / shaky / gap.
6. Build the study plan: gap concepts first, each with its source, exercise,
   and evidence check.
7. Fill the map from `templates/learning-map.template.md`.

## Artifacts Produced

- `docs/learning/paths/<project>-learning-map.md`
- New concept nodes appended to `registries/knowledge-registry.yaml` if missing

## Exit Criteria

- Every required concept maps to a registry node, a source, and an evidence check.
- Gaps are ordered by prerequisites and each has a concrete next action.

## Next

→ `learn-from-docs.md` or `source-to-exercise.md` for the top gap, then apply
directly in the project.
