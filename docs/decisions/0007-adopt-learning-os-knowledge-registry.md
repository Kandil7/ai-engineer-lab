# ADR-0007: Adopt a knowledge registry as the Learning OS backbone

- **Status:** Accepted
- **Date:** 2026-10-10
- **Deciders:** Workspace owner
- **Tags:** learning, architecture, registry, ai

## Context

The workspace is a strong **execution** system (workflows, prompts, registries, templates,
ADRs) with substantial **learning content** (`docs/curriculum/`, `projects/00-core-foundations/python/`,
`learning-sources/source-index.md`) and a **mastery model** (`docs/roadmap/skills-matrix.md`).
What it lacks is a single machine-readable link between the three.

Today the connections live in prose and are scattered: `source-index.md` maps sources to
projects, `skills-matrix.md` maps skills to evidence, `SKILLS_MASTERY_MAP.md` maps skills to
topics. Nothing connects a *concept* to its prerequisites, where it is taught, its source, its
exercise, the project that uses it, and the evidence that proves mastery. As a result the system
cannot answer the question the owner actually asks: **given a project, what must I learn to
build it, and what is my gap?** The 10-week track is also time-boxed to a job search; the owner
wants a permanent companion that keeps teaching across projects.

## Decision Drivers

- **The gap is a link, not a volume.** The material already exists; it needs one index that
  resolves in CI, matching the repo's established "registries are source of truth" idiom.
- **Fits existing infrastructure.** Registries + a validator + a workflow + a template is the
  same shape as `prompt-registry.yaml`, `tests/registries/validate.ps1`, and `.ai/workflows/`.
  No new runtime, no new framework.
- **Scope is software/AI projects.** The reference grows domain by domain, not to every subject.
- **Evolve in place.** The 10-week track becomes one consumer of the same knowledge graph, not a
  parallel system, so there is one definition of sources and mastery.

## Options Considered

### Option A — A docs-only concept index
- Pros: no tooling; readable.
- Cons: links drift silently; no validation; cannot be consumed by a workflow.

### Option B — A validated YAML concept graph + a learning workflow (chosen)
- Pros: resolves in CI like every other registry; feeds the `project-to-learning-map` workflow;
  grows one node at a time; reuse of the existing `role.learning-coach` prompt.
- Cons: one more registry and validator to maintain; the graph must be kept honest by the gate.

### Option C — A full RAG/agent over the repo immediately
- Pros: natural-language "what should I learn"; doubles as DevMate's corpus.
- Cons: premature; without the structured graph there is nothing authoritative to retrieve;
  deferred to a later phase.

## Decision

Adopt **Option B**.

1. **`registries/knowledge-registry.yaml`** is the backbone. Each node carries `id`, `name`,
   `level`, `prerequisites`, `taught_in`, `sources`, `exercises`, `used_by_projects`, `evidence`,
   `status`. The first slice is the `ai-engineering` domain (29 nodes across `python`,
   `ai-engineering`, `backend`, `databases`, `devops`, `system-design`).
2. **`tests/knowledge/validate.ps1`** gates it: unique ids, resolvable prerequisites, existing
   paths, resolvable `source-index#N` anchors, and no orphan or cyclic node. It is wired into
   `infra/scripts/local-ci.ps1`, `.github/workflows/ci.yml`, and `tests/repo-structure/validate.ps1`.
3. **`learning/project-to-learning-map`** is the first consumer: a workflow (with
   `templates/learning-map.template.md` and the existing `role.learning-coach`) that turns a
   project into a learning map (required skills, current level, gaps, ordered study plan).
4. **Later phases** (separate ADRs): a mastery/recall state where `skills-matrix.md` becomes a
   rendered view; a concept-oriented `docs/reference/` index generated from the registry; and
   DevMate indexing the repo as the query engine over the graph.

## Consequences

- **Positive:** the concept-to-project link is now explicit and validated; the learning workflow
  has an authoritative source; the graph grows incrementally and safely; the same corpus later
  powers DevMate, so the learning system and the active project converge.
- **Negative:** a new registry and validator add maintenance surface; a node that names a moved
  path will fail CI until updated (intended, but it is work).
- **Watch:** the graph must not become a dumping ground; every node needs real `taught_in` and
  `evidence`, or the gate will reject it.
- **Follow-ups / new ADR candidates:** mastery/recall state; generated reference index;
  DevMate-as-query-engine.

## Links

- Related ADRs: [ADR-0004](0004-adopt-10-week-ai-engineer-track.md),
  [ADR-0006](0006-adopt-master-ai-engineering-curriculum.md)
- Backbone: `registries/knowledge-registry.yaml`
- Gate: `tests/knowledge/validate.ps1`
- Consumer: `.ai/workflows/learning/project-to-learning-map.md`,
  `templates/learning-map.template.md`
- Mastery source: `docs/roadmap/skills-matrix.md`
