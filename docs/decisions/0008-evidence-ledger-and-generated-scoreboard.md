# ADR-0008: Evidence ledger and a generated skills scoreboard

- **Status:** Accepted
- **Date:** 2026-10-10
- **Deciders:** Workspace owner
- **Tags:** learning, registry, evaluation

## Context

[ADR-0007](0007-adopt-learning-os-knowledge-registry.md) introduced the knowledge registry as the
concept graph, and its Phase 2 was named but not built: a mastery/recall state where
`docs/roadmap/skills-matrix.md` becomes a rendered view rather than a hand-edited file.

Today mastery lives in three places that drift independently: `docs/roadmap/skills-matrix.md`
(hand-edited levels with prose evidence), `docs/roadmap/production-skills-matrix.md` (12 axes,
Provable/Partial/Not yet), and now the registry's `level_target` per node. Nothing joins a
concept to the artifact that proves it in a machine-checkable way, so the numbers are trusted,
not verified. The repo's own rule already says a level requires evidence, a path, a test, or a
URL; the missing piece is the ledger that records that evidence and the generated view that
renders it.

## Decision Drivers

- **Evidence over assertion.** A level should point at a real artifact that exists on disk.
- **One source of truth.** Current mastery should be data, not prose edited in three files.
- **CI-verifiable.** Every evidence path must resolve, and the rendered view must not drift.
- **Fits the existing idiom.** A registry plus a validator plus a generated doc plus a drift
  gate is the same shape as the knowledge registry and the knowledge index.

## Options Considered

### Option A — Keep `skills-matrix.md` hand-edited
- Pros: no new files.
- Cons: drifts; evidence paths rot silently; the registry's targets have nothing to join to.

### Option B — Evidence ledger (`registries/evidence.yaml`) plus a generated scoreboard (chosen)
- Pros: every level points at an existing artifact; the scoreboard is generated and gated;
  the registry's `level_target` and the ledger's current level join into a gap table.
- Cons: one more registry and one more generated doc to maintain; the ledger is hand-seeded
  at first, so it can still be optimistic until `checked_by: script` dominates.

### Option C — Fully automated scoring from test/CI artifacts
- Pros: no self-assessment bias.
- Cons: premature; most concepts have no automated signal yet; would stall on tooling.

## Decision

Adopt **Option B**.

1. **`registries/evidence.yaml`** is the source of truth for current mastery. Each entry carries
   `id`, `skill` (a knowledge-registry node id), `level`, `type` (test, eval_report, adr, pr,
   deployment, teaching, benchmark), `path` (must exist), `date`, and `checked_by`.
2. **`docs/roadmap/skills-scoreboard.md`** is generated from the ledger joined with the registry
   by `infra/scripts/build-skills-scoreboard.ps1`. It shows target, current, gap, and evidence
   per concept, grouped by domain.
3. **The gate runs in CI.** `tests/knowledge/validate.ps1` validates the ledger (skill resolves,
   type allowed, path exists, level and date well formed), and the scoreboard drift check runs
   in `infra/scripts/local-ci.ps1` and the CI workspace job.
4. **`skills-matrix.md` stays as the narrative.** It keeps the level definitions, targets, and
   the monthly review ritual; the numbers move to the generated scoreboard, which it references.

## Consequences

- **Positive:** every claimed level is anchored to an artifact that must exist; the gap table is
  generated and consistent with the registry; `checked_by: script` entries make automation
  measurable as the eval and test surface grows.
- **Negative:** the ledger is hand-seeded, so early levels can be optimistic; the drift gate
  means an evidence file that moves must update its ledger entry in the same change.
- **Watch:** if most entries stay `checked_by: self`, the ledger is a claim, not a proof. Prefer
  promoting entries to `script` as CI signals appear.
- **Follow-ups / new ADR candidates:** generate `skills-matrix.md`'s active-track table from the
  ledger too; wire `checked_by: script` entries to their producing jobs; a spaced-repetition
  layer (deferred).

## Links

- Related ADRs: [ADR-0007](0007-adopt-learning-os-knowledge-registry.md)
- Source of truth: `registries/evidence.yaml`, `registries/knowledge-registry.yaml`
- Generated: `docs/roadmap/skills-scoreboard.md`
- Gate: `tests/knowledge/validate.ps1`, `infra/scripts/build-skills-scoreboard.ps1`
- Narrative: `docs/roadmap/skills-matrix.md`
