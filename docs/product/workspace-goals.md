# Workspace Goals

> **Long-track context.** Written 2026-08-06, before the 10-week active track. The plan
> of record is [`active-track-10-week.md`](../roadmap/active-track-10-week.md); treat
> roadmap-specific claims here as historical.

**Last updated:** 2026-08-06

## Overview

This repository serves as a **repo-centric learning OS** — a self-contained workspace where learning, experimentation, and project execution happen in one place. The workspace is designed to be explored, extended, and iterated upon, not just consumed.

## Primary Goal

Build a structured, reproducible environment for learning full-stack AI engineering through hands-on projects, modular prompts, and documented decisions. Every artifact in this repo — prompts, workflows, scaffolds, ADRs — is designed to be learned from, forked, and extended.

---

## 5-Axis Learning System

All learning resources are organized into 5 axes (see [`learning-sources/source-index.md`](../../learning-sources/source-index.md) and [`learning-strategy.md`](./learning-strategy.md)):

| Axis | Focus | Key Sources |
|------|-------|-------------|
| 1 | Web / Full-Stack Foundations | MDN, FreeCodeCamp, Odin Project, Roadmap.sh |
| 2 | Backend / DevOps | Pro Git, PostgreSQL/Redis docs, Docker courses |
| 3 | AI Engineering / LLMs / RAG | DeepLearning.AI, Boot.dev, OpenAI Cookbook |
| 4 | Agents / Prompt Engineering | Anthropic guides, production patterns |
| 5 | Evidence-Based Learning | Active recall, spaced repetition, interleaving |

**Rule:** Every source studied MUST produce a tangible artifact in the repo.

---

## Learning Targets

| Target | Description | Depth |
|--------|-------------|-------|
| **FastAPI** | AI service APIs, async patterns, dependency injection | Proficient |
| **PostgreSQL** | Schema design, migrations, query optimization | Proficient |
| **Redis** | Caching, pub/sub, session management | Working |
| **Qdrant** | Vector storage, similarity search, hybrid retrieval | Working |
| **RAG** | Retrieval-augmented generation, chunking, reranking | Proficient |
| **Agents** | Tool use, planning, multi-agent orchestration | Working |
| **System Design** | Architecture patterns, trade-offs, scaling strategies | Working |

---

## Project Targets

| Project | Purpose | Stack |
|---------|---------|-------|
| **RAG Pipeline** | Document ingestion, retrieval, generation | FastAPI + Qdrant + PostgreSQL |
| **AI Assistant** | Tool-using agent with memory and planning | FastAPI + Redis + Qdrant |
| **ThanaweyaGPT** | Domain-specific educational AI | Full stack — all services |

---

## Quality Targets

### Code Quality
- All Python code passes `ruff` with zero errors
- Test coverage ≥ 80% for core business logic

### Prompt Quality
- Every prompt has a documented purpose and expected output
- Prompts are versioned and tracked in git
- Eval scores are recorded for each prompt variant
- No prompt exceeds 2000 tokens without explicit justification

### Documentation Quality
- Every ADR follows the established template
- Every project scaffold includes a README
- Every workflow is documented with examples
- Cheat sheets are kept under 200 lines and updated quarterly

### Infrastructure Quality
- All services have health checks
- Docker Compose defines all dependencies
- Environment variables are documented (not hardcoded)
- Secrets are never committed to the repository

---

## Timeline

### Phase 0 — Foundation (Week 1)
- [x] Monorepo structure defined
- [x] ADR template and first decisions recorded
- [x] Core cheat sheets created
- [x] Workspace goals documented
- [ ] Initial project scaffolds generated

### Phase 1 — Learning Workflows (Weeks 2-3)
- [ ] FastAPI AI services learning path completed
- [ ] PostgreSQL fundamentals practiced
- [ ] Redis caching patterns implemented
- [ ] First ADR: database choice for AI service

### Phase 2 — Core Projects (Weeks 4-6)
- [ ] Auth system scaffolded and functional
- [ ] RAG pipeline with Qdrant operational
- [ ] Chat application backend complete
- [ ] First prompt evaluation framework in place

### Phase 3 — AI Integration (Weeks 7-9)
- [ ] AI assistant with tool use working
- [ ] Agent planning patterns implemented
- [ ] Multi-agent orchestration prototype
- [ ] Prompt regression testing established

### Phase 4 — Polish & Production (Weeks 10-12)
- [ ] ThanaweyaGPT MVP complete
- [ ] All services containerized and orchestrated
- [ ] CI/CD pipeline operational
- [ ] Documentation complete and published

---

## Success Metrics

### Quantitative
- **12+ ADRs** recorded covering key architectural decisions
- **5 projects** scaffolded with working boilerplates
- **20+ prompts** versioned with evaluation scores
- **100+ commits** demonstrating iterative learning
- **80%+ test coverage** across core modules

### Qualitative
- Every decision is documented with rationale and trade-offs
- Learning paths are reproducible by others
- Prompts are modular, composable, and well-documented
- The repo can be forked and used as a starting point
- Architecture evolves through ADRs, not ad-hoc changes

### Process Metrics
- **Weekly review**: Are we on track with the timeline?
- **Monthly audit**: Are prompts and workflows still relevant?
- **Quarterly update**: Are cheat sheets current?
- **ADR velocity**: Are we making and recording decisions at a healthy pace?

---

## Guiding Principles

1. **Learning over shipping** — This repo exists to learn, not to ship a product
2. **Decisions over defaults** — Every choice should be documented in an ADR
3. **Modularity over monoliths** — Prompts, workflows, and code should be composable
4. **Reproducibility over speed** — Someone else should be able to fork and follow
5. **Documentation as code** — Docs live with the code, not in a separate silo

---

## References

- [Architecture Overview](../architecture/overview.md)
- [Monorepo Structure](../architecture/monorepo-structure.md)
- [ADRs](../decisions/README.md)
- [Learning Paths](../learning/paths/)
