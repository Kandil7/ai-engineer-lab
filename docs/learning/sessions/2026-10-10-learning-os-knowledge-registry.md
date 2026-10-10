# Learning OS Phase 1 — Knowledge Registry backbone

### Context

Repo: ai-engineer-lab. Goal of the session: evolve the workspace from a 10-week execution track into a permanent, comprehensive learning system. The diagnosed gap was not content volume but a missing machine-readable link between a concept, where it is taught, its source, its exercise, the project that uses it, and the mastery evidence. Owner decisions: scope = software/AI projects; automation = prompts + workflow first; evolve in place; start with the registry.

### Explanation

Phase 1 built the backbone and its first consumer. New artifacts: registries/knowledge-registry.yaml (concept graph, 29 nodes across python, ai-engineering, backend, databases, devops, system-design; each node carries id, name, level, prerequisites, taught_in, sources, exercises, used_by_projects, evidence, status). tests/knowledge/validate.ps1 gates it: unique ids, resolvable prerequisites, existing paths, resolvable source-index#N anchors, and no orphan/cyclic node via a fixpoint reachability check. The gate is wired into infra/scripts/local-ci.ps1, .github/workflows/ci.yml, and tests/repo-structure/validate.ps1 (registry + test file added to the required lists). The first consumer is .ai/workflows/learning/project-to-learning-map.md, registered in workflow-registry.yaml, with templates/learning-map.template.md registered in template-registry.yaml, reusing the existing role.learning-coach prompt. Decision recorded as docs/decisions/0007-adopt-learning-os-knowledge-registry.md, mirrored in registries/decision-log.yaml and docs/decisions/README.md.

### Alternatives

Considered a docs-only concept index (no tooling) — rejected because links drift silently and no workflow can consume it. Considered a full RAG/agent over the repo immediately — rejected as premature: without the structured graph there is nothing authoritative to retrieve; deferred to a later phase. Chose the validated YAML graph + workflow because it matches the repo's existing "registries are source of truth" idiom and reuses role.learning-coach instead of inventing a new prompt.

### Rationale (Why this?)

A registry with a CI gate is the smallest change that makes the concept-to-project link explicit and self-checking. It grows one node at a time and keeps the graph honest: a moved path or a dangling prerequisite fails the suite. Because the same corpus can later power DevMate, the learning system and the active project converge rather than duplicate. Revisit if the graph becomes a dumping ground (nodes without real taught_in or evidence) — the gate is designed to reject that.

### Exercises

1. Add a new domain (e.g. fine-tuning) by appending nodes to registries/knowledge-registry.yaml and confirm tests/knowledge/validate.ps1 stays green. 2. Run the learning/project-to-learning-map workflow on DevMate and produce docs/learning/paths/devmate-learning-map.md from the template. 3. Break the gate on purpose: point one node's taught_in at a nonexistent path and read the exact failure. 4. Add a prerequisite cycle (A needs B, B needs A) and confirm the orphan/cycle check catches it. 5. Cross-check a node's evidence line against docs/roadmap/skills-matrix.md to see where the two models diverge.

### Next Steps

Phase 2: mastery/recall state under docs/learning/state/ so skills-matrix.md becomes a rendered view. Phase 3: a concept-oriented docs/reference/ index generated from the registry. Phase 4: DevMate indexes the repo as the query engine over the graph (also the A3 live-RAG deliverable). Seed remaining domains: fine-tuning, model-serving, security, career/technical-English.

---
