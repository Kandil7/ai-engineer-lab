# Monorepo Structure

```text
fullstack-ai-engineer-lab/
  README.md  ROADMAP.md  MAKEFILE.md  .gitignore  .editorconfig  .gitattributes

  .ai/
    prompts/   system/ roles/ tasks/ critics/ repair/
    workflows/ feature/ debugging/ learning/ architecture/ evaluation/

  templates/            # 16 artifact templates

  registries/           # prompt / workflow / template / decision / skills YAML

  docs/
    architecture/       # overview, monorepo-structure, ai-workspace-architecture
    decisions/          # ADR index + numbered ADRs (0001-0006)
    learning/           # paths/ deep-dives/ source-summaries/
    product/            # workspace-goals, scope-definition, feature-priorities, learning-strategy
    cheat-sheets/       # git, docker, postgres, qdrant, prompt-design
    plan/               # executive summary, builder progress
    roadmap/            # master-roadmap, milestones, progress-dashboard, skills-matrix
    tracking/           # current-focus (what to work on right now)
    reviews/            # weekly/ and monthly/ review templates

  learning-sources/     # source-index + books/ repos/ notebooks/ official-docs/

  evaluations/
    prompts/  golden-cases/ regressions/
    rag/      datasets/ reports/ baselines/
    projects/ rag-system/ capstone/

  projects/
    00-core-foundations/  git-linux/ ds-algo/ python/
                          # python/: 10 phases (core→advanced→libraries→databases→
                          # web→DSA→ML→MLOps→GenAI→system-design) + SKILLS_MASTERY_MAP.md
                          # + per-module challenge sets (Bronze/Silver/Gold)
    03-databases/         postgres-design/ redis-cache/ qdrant-rag/
    04-ai-engineering/    prompt-engineering/ embeddings/ rag-system/ agents/ ai-automation/ security/
    05-system-design/
    06-devops/            docker/ ci-cd/ deployment/
    07-capstone/          thanaweyagpt/ backend/ frontend/ ai/ infra/ docs/

  infra/
    docker/   docker-compose.yml + postgres/ redis/ mongodb/ qdrant/ langfuse/
    scripts/  setup.ps1 new-adr.ps1 new-review.ps1 new-source-note.ps1

  tests/
    repo-structure/ templates/ workflows/ prompts/
```

## Naming Conventions

| Artifact | Pattern | Example |
|----------|---------|---------|
| ADRs | `NNNN-kebab-title.md` (4-digit, zero-padded) | `0001-repo-centric-workspace.md` |
| Source summaries | `<type>-<slug>.md` | `fastapi-dependency-injection.md` |
| Project artifacts | Standard filenames inside project folders | `plan.md`, `ai-review.md`, `notes.md`, `mistakes.md` |
| Prompts | `<layer>.<name>` ids | `system.workspace-governor`, `roles.project-planner` |
| Workflows | `<group>/<NN-step>` ids | `feature/01-plan`, `debugging/01-symptom-capture` |

## Why `.ai/` (not `99-ai-workflow/`)

See [ADR-0002](../decisions/0002-prompt-modularization.md). `.ai/` is concise, sorts to the top,
and signals "machine/AI workspace" distinct from human docs in `docs/`. It follows the
convention established by projects like .github/ and .vscode/.

## Directory Roles

| Directory | Purpose |
|-----------|---------|
| `docs/` | Human-readable documentation — architecture, decisions, learning, product |
| `.ai/` | AI operating instructions — prompts, workflows, critics |
| `templates/` | Standardized artifact shapes for reuse |
| `registries/` | YAML inventories of all workspace assets |
| `projects/` | Actual code — organized by skill area |
| `infra/` | Infrastructure — Docker, scripts |
| `evaluations/` | Quality metrics — prompt evals, RAG evals, project release gates |
| `learning-sources/` | External reference materials indexed and summarized |

*Last updated: 2026-08-06*
