# Scope Definition

> **Long-track context.** Written 2026-08-06, before the 10-week active track. The plan
> of record is [`active-track-10-week.md`](../roadmap/active-track-10-week.md); treat
> roadmap-specific claims here as historical.

**Last updated:** 2026-08-06

## Purpose

This document defines what is **in scope**, **out of scope**, and **future scope** for the Full-Stack AI Engineer Lab. Clear scope boundaries prevent feature creep and keep the workspace focused on its primary mission: learning and experimentation.

---

## In Scope

### 1. Monorepo Structure
- Go backend services (`services/`)
- FastAPI AI services (`services/`)
- Flutter mobile application (`mobile/`)
- Shared libraries (`libs/`)
- Configuration and deployment (`deploy/`)
- Documentation (`docs/`)
- Prompts and workflows (`prompts/`)

### 2. Modular Prompts
- Versioned prompt templates with metadata
- Prompt evaluation and scoring
- A/B testing of prompt variants
- Composable prompt chains
- Anti-hallucination patterns
- Structured output formatting

### 3. Structured Workflows
- Step-by-step execution plans
- Quality gates and checkpoints
- Agent orchestration patterns
- Pipeline definitions for common tasks
- Workflow versioning and rollback

### 4. Templates
- Project scaffolds for new services
- ADR templates for decisions
- Workflow templates for common patterns
- Prompt templates for different use cases
- Documentation templates

### 5. ADR Tracking
- Architecture Decision Records for all key choices
- Decision lifecycle (proposed → accepted → deprecated)
- Reversibility analysis
- Trade-off documentation
- Context and consequences recorded

### 6. Source Learning
- Learning paths for each technology
- Hands-on exercises and examples
- Reference implementations
- Best practices documentation
- Common pitfalls and solutions

### 7. Project Scaffolds
- Go backend starter with auth patterns
- FastAPI service with RAG integration
- Flutter app with state management
- PostgreSQL schema templates
- Docker Compose configurations

---

## Out of Scope

### 1. SaaS Product
- No user authentication for multi-tenant access
- No billing or subscription management
- No production deployment infrastructure
- No SLA or uptime guarantees
- No customer support system

### 2. Autonomous Agents
- No fully autonomous agent loops without human oversight
- No self-modifying code or prompts
- No unbounded tool use
- No automatic escalation without confirmation
- No self-deploying systems

### 3. UI/UX Polish
- No production-grade UI design
- No accessibility compliance (WCAG)
- No responsive design for all devices
- No localization or internationalization
- No design system or component library

### 4. Enterprise Secrets
- No production API keys or secrets
- No real customer data
- No PII or sensitive information
- No compliance certifications (SOC2, HIPAA)
- No enterprise SSO integration

### 5. Auto-Execution
- No automatic code execution without review
- No CI/CD that deploys without approval
- No self-healing systems
- No automatic dependency updates
- No auto-merge of PRs

---

## Future Scope

### Near-Term (3-6 months)
- CLI tool for workspace management
- Search across prompts, workflows, and docs
- CI/CD pipeline with quality gates
- Dashboard for tracking progress
- Integration with external LLM providers

### Medium-Term (6-12 months)
- Advanced prompt evaluation framework
- Prompt regression testing
- Multi-agent orchestration patterns
- Plugin system for extending workflows
- Collaborative editing of prompts

### Long-Term (12+ months)
- Visual workflow builder
- Agent marketplace
- Prompt versioning with semantic diffing
- Automated documentation generation
- Cross-repo knowledge sharing

---

## Scope Boundaries

| Aspect | In Scope | Out of Scope |
|--------|----------|--------------|
| **Code** | Learning projects, experiments | Production systems |
| **Prompts** | Modular, versioned, evaluated | Untracked, ad-hoc |
| **Workflows** | Documented, reproducible | Implicit, tribal knowledge |
| **Decisions** | ADR-tracked, reversible | Ad-hoc, undocumented |
| **Infrastructure** | Docker Compose, local dev | Kubernetes, production |
| **Data** | Synthetic, public datasets | Real user data, PII |
| **Agents** | Tool-use, planning, reflection | Fully autonomous loops |
| **Evaluation** | Manual, semi-automated | Fully automated CI |

---

## Decision Framework

When evaluating whether something is in scope, ask:

1. **Does it support learning?** — Will someone learn something from this?
2. **Is it reproducible?** — Can another person fork and follow?
3. **Does it fit the monorepo?** — Can it live alongside existing code?
4. **Is it documented?** — Can it be understood without tribal knowledge?
5. **Is it modular?** — Can it be extended or replaced independently?

If the answer to most of these is "yes," it's likely in scope.

---

## Related Documents

- [Workspace Goals](workspace-goals.md)
- [Feature Priorities](feature-priorities.md)
- [Architecture Overview](../architecture/overview.md)
