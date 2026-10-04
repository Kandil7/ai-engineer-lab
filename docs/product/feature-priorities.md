# Feature Priorities

> **Long-track context.** Written 2026-08-06, before the 10-week active track. The plan
> of record is [`active-track-10-week.md`](../roadmap/active-track-10-week.md); treat
> roadmap-specific claims here as historical.

**Last updated:** 2026-08-06

## Overview

This document defines the priority matrix for features in the Full-Stack AI Engineer Lab. Features are categorized into four priority levels (P0-P3) based on their impact on learning, project execution, and workspace quality.

---

## Priority Levels

| Priority | Description | Timeline | Acceptance Criteria |
|----------|-------------|----------|---------------------|
| **P0** | Critical — blocks core workflows | Immediate | Must be complete before any P1 work |
| **P1** | Important — enables primary learning | Weeks 1-4 | Required for meaningful progress |
| **P2** | Useful — improves efficiency | Weeks 5-8 | Enhances existing workflows |
| **P3** | Nice-to-have — advanced capabilities | Weeks 9-12 | Optional but valuable |

---

## P0 — Critical Features

### Feature Workflow
- **Description**: Structured process for implementing features from idea to completion
- **Components**: Issue template, branch strategy, PR template, review checklist
- **Success Criteria**: Every feature follows the workflow; no ad-hoc implementations
- **Dependencies**: Git conventions, branch protection rules

### Architecture Decision Records
- **Description**: Documented decisions with context, options, and rationale
- **Components**: ADR template, decision log, review process
- **Success Criteria**: All significant decisions have ADRs; decisions are reversible
- **Dependencies**: ADR template, git workflow

### Code Review Process
- **Description**: Systematic review of code changes before merge
- **Components**: PR template, review checklist, approval requirements
- **Success Criteria**: All PRs reviewed; feedback documented and addressed
- **Dependencies**: Git conventions, team agreement

### Project Scaffolds
- **Description**: Ready-to-use project starters for each technology stack
- **Components**: FastAPI service, PostgreSQL schema, Docker Compose
- **Success Criteria**: New projects can be scaffolded in < 5 minutes
- **Dependencies**: Technology choices documented in ADRs

---

## P1 — Important Features

### Learning Workflows
- **Description**: Structured paths for learning each technology
- **Components**: Learning paths, exercises, examples, assessments
- **Success Criteria**: Each technology has a documented learning path
- **Dependencies**: P0 project scaffolds

### Evaluation Framework
- **Description**: Systematic evaluation of prompts and workflows
- **Components**: Eval metrics, scoring rubrics, comparison tools
- **Success Criteria**: All prompts have evaluation scores; variants are compared
- **Dependencies**: P0 prompt architecture

### Infrastructure Setup
- **Description**: Local development environment and dependencies
- **Components**: Docker Compose, environment config, health checks
- **Success Criteria**: All services run locally with one command
- **Dependencies**: P0 project scaffolds

### Documentation Standards
- **Description**: Consistent documentation across all artifacts
- **Components**: README templates, doc conventions, style guide
- **Success Criteria**: All code and prompts have documentation
- **Dependencies**: P0 documentation templates

---

## P2 — Useful Features

### CLI Tool
- **Description**: Command-line interface for workspace management
- **Components**: Scaffold generator, workflow runner, eval scorer
- **Success Criteria**: Common tasks accessible via CLI
- **Dependencies**: P1 learning workflows

### Search Functionality
- **Description**: Search across prompts, workflows, and documentation
- **Components**: Full-text search, semantic search, filters
- **Success Criteria**: Any artifact findable in < 3 seconds
- **Dependencies**: P1 documentation standards

### CI/CD Pipeline
- **Description**: Automated testing and deployment
- **Components**: Linting, testing, building, deployment
- **Success Criteria**: All changes validated automatically
- **Dependencies**: P1 infrastructure setup

### Progress Dashboard
- **Description**: Visual tracking of learning and project progress
- **Components**: Metrics, charts, milestones, status
- **Success Criteria**: Progress visible at a glance
- **Dependencies**: P1 evaluation framework

---

## P3 — Nice-to-Have Features

### Advanced Evaluation
- **Description**: Sophisticated prompt evaluation and comparison
- **Components**: A/B testing, statistical significance, regression detection
- **Success Criteria**: Prompt improvements measurable and validated
- **Dependencies**: P2 evaluation framework

### Prompt Regression Testing
- **Description**: Automated detection of prompt quality degradation
- **Components**: Baseline scores, regression alerts, rollback
- **Success Criteria**: Regressions caught before deployment
- **Dependencies**: P3 advanced evaluation

### Multi-Agent Orchestration
- **Description**: Coordination of multiple AI agents
- **Components**: Task decomposition, agent selection, result aggregation
- **Success Criteria**: Complex tasks broken down and executed
- **Dependencies**: P2 agent patterns

### Plugin System
- **Description**: Extensible architecture for adding capabilities
- **Components**: Plugin API, registry, lifecycle management
- **Success Criteria**: Third-party plugins can be added easily
- **Dependencies**: P2 CLI tool

---

## Priority Matrix

| Feature | Impact | Effort | Priority | Phase |
|---------|--------|--------|----------|-------|
| Feature Workflow | High | Low | P0 | 0 |
| ADR Tracking | High | Low | P0 | 0 |
| Code Review | High | Low | P0 | 0 |
| Project Scaffolds | High | Medium | P0 | 0-1 |
| Learning Workflows | High | Medium | P1 | 1 |
| Evaluation Framework | High | High | P1 | 1-2 |
| Infrastructure | Medium | Medium | P1 | 1 |
| Documentation | Medium | Low | P1 | 1 |
| CLI Tool | Medium | High | P2 | 2-3 |
| Search | Medium | Medium | P2 | 2-3 |
| CI/CD | Medium | High | P2 | 2-3 |
| Dashboard | Low | High | P2 | 3 |
| Advanced Eval | Medium | High | P3 | 3-4 |
| Regression Testing | Medium | High | P3 | 3-4 |
| Multi-Agent | Low | Very High | P3 | 4 |
| Plugin System | Low | Very High | P3 | 4 |

---

## Trade-offs

### Speed vs. Completeness
- **P0**: Prioritize completeness — these features are foundational
- **P1**: Balance speed and completeness — these enable learning
- **P2**: Prioritize speed — these improve efficiency
- **P3**: Prioritize exploration — these are experimental

### Scope vs. Quality
- **All priorities**: Quality is non-negotiable for P0 and P1
- **P2-P3**: Acceptable to ship with known limitations
- **Documentation**: Required for P0 and P1; optional for P2-P3

### Learning vs. Shipping
- **P0-P1**: Learning is primary; shipping is secondary
- **P2-P3**: Balance learning with practical utility
- **Overall**: This repo is for learning, not shipping products

---

## Related Documents

- [Workspace Goals](workspace-goals.md)
- [Scope Definition](scope-definition.md)
- [Architecture Overview](../architecture/overview.md)
