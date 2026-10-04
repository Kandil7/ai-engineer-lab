# 1) Executive Summary

## Vision

The **AI Engineering Workspace / Learning OS** is a practical monorepo that combines: project-based learning, AI workflows, versioned prompts, architecture reviews, code reviews, debugging logs, and capstone projects within one organized repository.

The goal is not just a learning repo, but an **engineering operating system** that helps the user learn, execute, review, and evolve from AI Engineer to higher production levels.

## Architecture

The appropriate design here is a **hybrid architecture**: content/documentation-centric repo first, with clear workflow, prompt, and template layers — instead of starting with a massive software platform featuring a complex orchestration runtime from day one.

The current system derived from the plan focuses on: FastAPI for AI services, PostgreSQL, Redis, Qdrant, plus AI workflows inside the `.ai/` namespace.

### Component Separation

Components are separated into:
- **Learning content** — `docs/`, `learning-sources/`
- **Project workspaces** — `projects/`
- **Reusable prompts** — `.ai/prompts/`
- **Review artifacts** — `ai-review.md`, `notes.md`, `mistakes.md`
- **Decision records** — `docs/decisions/` (ADRs)
- **Evaluation assets** — `evaluations/`
- **Workflow templates** — `.ai/workflows/`

### Prompt Architecture

A **modular prompt architecture** is adopted instead of a single giant prompt: teacher, planner, reviewer, debugger, architect, feature-builder, source-learning.

No unnecessary agent runtimes are proposed; in the MVP, most "agents" are **prompted operating modes** within the workspace, not distributed autonomous agents. This is simpler and more aligned with the current goal.

### Engineering Artifacts

Prompts, templates, ADRs, and review outputs are treated as **engineering artifacts** that must be versioned, tested, and reviewed.

### Source-Driven Learning

Source-driven learning from books, repos, notebooks, and official documentation is supported via dedicated workflows for each source type.

### Scope Boundary

The current system is a **repo-centric implementation system** supporting human execution and AI-assisted workflows. Building a multi-user SaaS to manage these processes is not required now.

---

## 2) Problem Framing

The system solves the problem that learning plans, projects, prompts, and reviews are often scattered across files, chats, notebooks, and scattered tools — making progress unstructured and unmeasurable.

The primary user is an engineer who wants to become an AI Engineer at a production level, linking learning with practical projects in AI engineering, databases, system design, and devops. The system must also suit actual projects like Athar and Baligh that are RAG/LLM-heavy.

### Core Inputs

- Roadmap/plan
- Source materials (docs, books, repos, notebooks)
- Feature ideas
- Code under review
- Bugs/errors
- Architectural questions
- AI project artifacts

### Expected Outputs

- Project plans
- Implementation workflows
- Code reviews
- Architecture reviews
- Debugging sessions
- Source-learning notes
- ADRs
- Evaluation artifacts
- Capstone project structure

### Domain Constraints

- The system must remain practical and individually executable.
- Over-engineering in the agent runtime layer must be avoided.
- The architecture must be extensible later to serve AI production projects like RAG systems and agentic applications.

---

## 3) Scope Definition

### In Scope

- Organized monorepo for learning, execution, and review.
- Project folders for paths: foundations, databases, AI engineering, system design, devops, capstone.
- Modular prompt system divided by function.
- Workflows for planning, building, reviewing, debugging, and learning from sources.
- Documentation system: README, roadmap, ADRs, learning notes, review logs.
- Source-learning system from books/repos/notebooks/official docs.
- Evaluation folders and initial reports for AI-heavy projects.

### Out of Scope

- SaaS multi-user product for managing these processes.
- Autonomous multi-agent runtime orchestrator running in production.
- Full UI for managing repo workflows.
- Enterprise-grade secret management platform.
- Automatic code execution engine within the system itself.

### Future Scope

- Dashboard for tracking progress.
- CLI for generating templates, ADRs, and review files.
- Local retrieval layer for searching within docs, decisions, and prompts.
- More rigorous evaluation harness for Athar/Baligh projects.
- Integration with GitHub Actions for prompt, doc, and file checks.

---

## 4) System Architecture

### High-Level Architecture

The proposed architecture is a **Repo-Centric Agentic Workspace**:

1. **Content Layer** — roadmap, docs, learning paths, deep dives, source materials, decision records.
2. **Project Layer** — actual applied projects: DevMate, rag-system, ai-assistant, capstone.
3. **Workflow Layer** — step-by-step workflows for planning, building, reviewing, debugging, and learning from sources.
4. **Prompt Layer** — modular prompts used as operating modes: mentor, planner, architect, reviewer, debugger, interviewer, source-learning.
5. **Template Layer** — standardized templates for plans, reviews, ADRs, bug reports, daily logs, source summaries.
6. **Evaluation Layer** — golden cases, review outputs, eval reports, release gates for AI projects.
7. **Delivery Layer** — infra, docker, scripts, app structure for complete projects (FastAPI + Docker).

### Core Modules

| Module | Responsibility | Inputs | Outputs |
|:--|:--|:--|:--|
| `docs/` | Knowledge preservation & decisions | Plans, decisions, learnings | Structured docs |
| `templates/` | Output standardization | Task or source context | Filled artifact |
| `.ai/prompts/` | Modular prompt system | User task + context | Constrained AI output |
| `projects/` | Project execution | Features, tasks | Working software |
| `evaluations/` | Quality control | Outputs/models/retrieval | Quality evidence |
| `learning-sources/` | Source-driven learning | Books/repos/docs/notebooks | Structured lessons |

### Orchestration Layer

There is no separate orchestrator runtime in the MVP. Orchestration is **human-led + workflow-driven** via workflow files and prompts. This is simpler because it achieves the current goal without building a complete agent platform.

### Agent Layer

"Agents" here are **logical roles**, not independent processes:
- Learning Coach
- Project Planner
- System Architect
- Pair Programmer
- Code Reviewer
- Debugging Specialist
- Source Learning Agent
- Principal System Designer

### Request Lifecycle (Feature Example)

```
START → feature request → planner prompt → plan artifact
  → architect prompt → architecture review
  → implementation in project folder → code review
  → fixes → reflection/learning log → END
```

### Control Flow

- Entry from one of: new feature, new bug, new source, new design question.
- Workflow selects template + prompt + target folder.
- Human executes/edits artifacts.
- Output stored in repo at deterministic path.
- Reviews feed into fixes, ADRs, or learning notes.

### Failure Points

- Overly broad prompts.
- Duplication between docs and project notes.
- Turning every capability into an "agent".
- Lack of naming conventions.
- Reviews without follow-up.
- Source learning without project linkage.

### Fallback Paths

- Downgrade multi-agent concept to single workflow + prompt.
- If insufficient information: create `open-questions.md`.
- If task is small: use pair-programmer or reviewer only.
- If design is immature: write ADR draft instead of implementation.

---

## 5) Project Structure

```text
ai-engineer-lab/
  README.md
  ROADMAP.md
  MAKEFILE.md
  .gitignore

  docs/
    architecture/
      overview.md
      monorepo-structure.md
      ai-workspace-architecture.md
    decisions/
      README.md
      0001-repo-centric-workspace.md
      0002-prompt-modularization.md
      0003-hybrid-stack-go-fastapi.md
    learning/
      paths/
        fastapi-ai-services.md
        rag-qdrant.md
        system-design.md
      deep-dives/
        rag-system-deep-dive.md
        athar-retrieval-deep-dive.md
        baligh-training-deep-dive.md
      source-summaries/
    product/
      workspace-goals.md
      scope-definition.md
      feature-priorities.md
    cheat-sheets/
      git.md
      docker.md
      postgres.md
      qdrant.md
      prompt-design.md

  templates/
    adr.template.md
    project-plan.template.md
    feature-spec.template.md
    architecture-review.template.md
    code-review.template.md
    bug-report.template.md
    debugging-session.template.md
    daily-log.template.md
    weekly-review.template.md
    monthly-review.template.md
    source-doc.template.md
    source-repo.template.md
    source-book.template.md
    source-notebook.template.md
    evaluation-report.template.md

  .ai/
    prompts/
      system/
        workspace-governor.md
        output-format-rules.md
      roles/ (8 agent roles)
      tasks/ (feature-builder, adr-writer, etc.)
      critics/ (validators)
      repair/ (error recovery)
    workflows/
      feature/ (01-plan → 06-reflect)
      debugging/ (01-symptom-capture → 04-fix-verification)
      learning/ (5 workflows)
      architecture/ (propose, record, review)
      evaluation/ (ai-feature-eval, prompt-regression, rag-quality-check)

  registries/
    prompt-registry.yaml
    workflow-registry.yaml
    template-registry.yaml
    decision-log.yaml
    skills-registry.yaml

  learning-sources/
    source-index.md
    books/
    repos/
    notebooks/
    official-docs/

  evaluations/
    prompts/ (golden-cases, regressions)
    rag/ (datasets, reports, baselines)
    projects/ (rag-system, capstone)

  projects/
    00-core-foundations/ (git-linux, ds-algo, python)
    03-databases/ (postgres-design, redis-cache, qdrant-rag)
    04-ai-engineering/ (prompt-engineering, embeddings, rag-system, agents)
    05-system-design/
    06-devops/ (docker, ci-cd, deployment)
    07-capstone/ (thanaweyagpt)

  infra/
    docker/ (docker-compose.yml, postgres/, redis/)
    scripts/ (setup, new-adr, new-review, new-source-note)

  tests/
    prompts/
    workflows/
    templates/
    repo-structure/
```

### Key Files

| File Path | Purpose |
|:--|:--|
| `README.md` | Repository entry — overview, stack, workflow rules |
| `ROADMAP.md` | Learning progression — phases, milestones |
| `docs/decisions/README.md` | ADR index — prevents lost decisions |
| `.ai/prompts/roles/project-planner.md` | Feature planning prompt |
| `.ai/workflows/feature/01-plan.md` | Plan workflow entry |
| `templates/adr.template.md` | ADR standard |
| `registries/prompt-registry.yaml` | Prompt inventory and versioning |
| `learning-sources/source-index.md` | Source map |
| `evaluations/rag/reports/` | AI quality evidence |
| `infra/scripts/new-adr.sh` | Automation helper |

---

## 6) Agents Design

### Agents Table

| Agent Name | Role | Inputs | Outputs | Invocation Trigger |
|:--|:--|:--|:--|:--|
| Learning Coach | Mentor mode | Topic, current level, source | Lesson, exercise, gaps | When learning a topic |
| Project Planner | Planning mode | Feature request, constraints | plan.md | Start of any feature |
| System Architect | Architecture mode | Feature/system idea | Architecture review/ADR | Large features or services |
| Pair Programmer | Guided implementation | Code task, current code | Next steps, partial guidance | During building |
| Code Reviewer | Review mode | Code diff/files | ai-review.md | After implementation |
| Debugging Specialist | Bug triage mode | Bug report, logs, code | Debugging session doc | When bug/error occurs |
| Source Learning Agent | Source extraction | Source file/link/notes | Source summary + exercises | When studying a source |
| Principal System Designer | Senior design mode | System problem | Design doc | Capstone/large systems |

### Why This Division Is Optimal

This division covers the confirmed needs in the plan: learning, planning, design, guided execution, review, debugging, and system design. There is no current need for additional runtime agents (security/devops/product managers) as independent entities within the repo because those functions can be temporarily represented as prompts/task modes or review templates.

### Single-Agent vs Multi-Agent

- Use **single-agent mode** for:
  - Explaining a topic
  - Code review
  - Bug triage
  - Small feature tasks
  - Source learning

- Use **multi-agent mode** for:
  - Complex feature development (planner → architect → builder → reviewer)
  - Full project lifecycle
  - Debugging sessions requiring hypothesis generation + diagnostics
  - Architecture decisions requiring tradeoff analysis

### Agent Collaboration Patterns

#### Feature Development (Sequential)
```
Project Planner → System Architect → Pair Programmer → Code Reviewer
```

#### Debugging (Iterative)
```
Debugging Specialist → (hypothesis) → Pair Programmer → (fix) → Code Reviewer
```

#### Learning (Parallel)
```
Learning Coach (concept explanation) + Source Learning Agent (structured notes)
```

#### Architecture Decision (Collaborative)
```
System Architect (propose) → Principal System Designer (review) → ADR written
```

---

## 7) Workflows Design

### Feature Workflow

```
01-plan.md   →  Project Planner creates plan.md
02-design.md →  System Architect creates architecture review or ADR (if needed)
03-build.md  →  Pair Programmer guides implementation
04-review.md →  Code Reviewer creates ai-review.md
05-fix.md    →  Issues addressed, mistakes.md updated
06-reflect.md→  Learning Coach creates learning notes
```

### Debugging Workflow

```
01-symptom-capture.md     →  Collect error output, logs, expected vs actual behavior
02-hypothesis-ranking.md  →  Generate and rank possible root causes
03-diagnostics.md         →  Suggest diagnostic commands and queries
04-fix-verification.md    →  Verify fix, update mistakes.md
```

### Learning Workflow

```
learn-from-docs.md        →  Extract key concepts from official docs
learn-from-repo.md        →  Extract patterns from reference repos
learn-from-book.md        →  Chapter-by-chapter structured notes
learn-from-notebook.md    →  Convert notebooks to exercises
source-to-exercise.md     →  Create practice exercises from sources
```

### Architecture Workflow

```
propose-decision.md       →  Document options, tradeoffs, and recommendations
record-adr.md             →  Formalize decision with accepted status
review-architecture.md    →  Review existing architecture for drift or improvements
```

### Evaluation Workflow

```
ai-feature-eval.md        →  Evaluate AI feature quality and edge cases
prompt-regression.md      →  Detect prompt quality degradation
rag-quality-check.md      →  Measure RAG pipeline precision, recall, faithfulness
```

---

## 8) Prompt Design

### Layering Order

Every prompt is assembled deterministically from layers:

```text
1. system/workspace-governor.md      (global rules)
2. roles/<role>.md                   (who you are)
3. tasks/<task>.md                   (the specific job, optional)
4. system/output-format-rules.md     (output shape)
5. critics/<critic>.md | repair/*    (optional follow-up pass)
```

### Key Principles

- **DRY:** Format rules live once in `output-format-rules.md` — never duplicated.
- **Small:** Each prompt declares only its own constraints.
- **Registry:** Every prompt is registered in `registries/prompt-registry.yaml`.
- **Versioned:** Prompt changes are tracked in git with evals.

---

## 9) Memory Model

- **Short-term:** Current task, workflow step, active source, project folder, prompt constraints.
- **Long-term:** Explicit repo artifacts — ADRs, reviews, debugging sessions, learning notes, eval reports, mistakes logs.
- **Retrieval:** By path → registry → folder convention. No hidden opaque memory in MVP.

---

## 10) Implementation Phases

### Phase 0 — Foundation (Complete)
- [x] Monorepo structure defined
- [x] ADR templates and first decisions recorded
- [x] Core cheat sheets created
- [x] Workspace goals documented
- [x] Learning paths documented

### Phase 1 — Learning Workflows (Weeks 2-3)
- [ ] FastAPI learning path exercises
- [ ] PostgreSQL fundamentals practiced
- [ ] Redis caching patterns

### Phase 2 — Core Projects (Weeks 4-6)
- [ ] RAG pipeline with Qdrant operational
- [ ] First prompt evaluation framework

### Phase 3 — AI Integration (Weeks 7-9)
- [ ] AI assistant with tool use
- [ ] Agent planning patterns
- [ ] Multi-agent orchestration prototype

### Phase 4 — Capstone (Weeks 10-12)
- [ ] ThanaweyaGPT MVP
- [ ] All services containerized
- [ ] Documentation complete

---

## 11) Success Criteria

### Quantitative
- 12+ ADRs recording key architectural decisions
- 5 projects scaffolded with working boilerplates
- 20+ prompts versioned with evaluation scores
- 100+ commits demonstrating iterative learning
- 80%+ test coverage across core modules

### Qualitative
- Every decision documented with rationale and tradeoffs
- Learning paths reproducible by others
- Prompts modular, composable, well-documented
- Repo forkable as a starting point
- Architecture evolves through ADRs, not ad-hoc changes

### Process Metrics
- Weekly review: on track with timeline?
- Monthly audit: prompts and workflows still relevant?
- Quarterly update: cheat sheets current?
- ADR velocity: healthy pace of decision recording?

---

## 12) ملخص عربي (Arabic Summary)

مساحة عمل مهندس AI متكاملة مبنية على monorepo تجمع بين التعلم بالمشاريع، سير العمل بالذكاء الاصطناعي، البرومبتات المقسمة، مراجعات الكود والعمارة، وتوثيق القرارات الهندسية.

**البنية:** 7 طبقات — محتوى، مشاريع، سير عمل، برومبتات، قوالب، تقييم، توصيل.

**الأدوار:** 8 أدوار منطقية (مدرب تعلم، مخطط مشاريع، مهندس عمارة، مبرمج زميل، مراجع كود، مختص تصحيح، وكيل تعلم من المصادر، مصمم أنظمة رئيسي).

**النهج:** الإنسان هو القائد، الـ AI مساعد. البرومبتات معيارية وقابلة لإعادة الاستخدام. كل قرار يُوثق كـ ADR.

**المرحلة الحالية:** Phase 0 — Foundations، الأسبوع 1 بدأ.

## 13) Related Documents

- [Architecture Overview](../architecture/overview.md)
- [Monorepo Structure](../architecture/monorepo-structure.md)
- [AI Workspace Architecture](../architecture/ai-workspace-architecture.md)
- [ADR Index](../decisions/README.md)
- [Workspace Goals](../product/workspace-goals.md)
- [Scope Definition](../product/scope-definition.md)
- [Feature Priorities](../product/feature-priorities.md)
- [Master Roadmap](../roadmap/master-roadmap.md)
- [Progress Dashboard](../roadmap/progress-dashboard.md)
