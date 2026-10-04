# 12-Month Learning Plan — Long Track (not active)

> ## ⚠️ Not the active plan
>
> Superseded 2026-08-02 by
> [`docs/roadmap/active-track-10-week.md`](../roadmap/active-track-10-week.md)
> ([ADR-0004](../decisions/0004-adopt-10-week-ai-engineer-track.md)).
>
> This plan schedules "Python basics for AI" at weeks 37–38 and "chatbot with LLM API" at
> weeks 39–40. The repo already contains 354 Python files including all 20 advanced topics and
> 25 FastAPI topics, so months 1–9 would largely re-cover completed material.
>
> The Go and frontend phases were **removed** to focus on AI Engineering; the AI and DevOps
> sequencing resumes post-employment.

Tailored for the `fullstack-ai-engineer-lab` stack:
FastAPI + PostgreSQL/Redis/Qdrant + LLMs/RAG + Agents.

**Last updated:** 2026-08-02 (demoted) · **Originally written:** 2026-06-26

---

## Philosophy

> **Write code yourself first**, then use AI as assistant — not replacement.

- **Few sources, many projects** — don't collect 10 courses, complete 3
- **Crash course → guided projects → your own projects**
- **Active recall + spaced repetition** — test yourself, don't re-read
- **AI as tool, not author** — understand every line you ship

---

## Phase 1: Programming Foundations (Months 1–3)

### Goal
Understand programming basics + web fundamentals. Build your first web pages.

### Sources

| Source | What You Learn | When |
|--------|---------------|------|
| **FreeCodeCamp** – Responsive Web + JS Algorithms | HTML, CSS, JS basics | Month 1-2 |
| **The Odin Project** – Foundations | Project-based JS, git, commands | Month 2-3 |
| **YouTube Crash Course** (JS) | Quick language intro | Month 1, week 1 |
| **CS50** (Harvard) – first 5-6 weeks | CS fundamentals, logic | Optional, Month 1 |

### What to Build

| Week | Project | Lab Location |
|------|---------|-------------|
| 1-2 | Landing page (HTML/CSS) | `projects/00-core-foundations/` |
| 3-4 | Portfolio site (HTML/CSS/JS) | `projects/00-core-foundations/` |
| 5-6 | Interactive form with validation | `projects/00-core-foundations/` |
| 7-8 | Simple JS game or calculator | `projects/00-core-foundations/` |
| 9-10 | Git practice: branches, commits, PRs | `projects/00-core-foundations/git-linux/` |
| 11-12 | Review: rebuild best project from memory | Active recall exercise |

### Daily Schedule (2-3 hours)
- 1 hour: Course/lesson
- 1-2 hours: Build something small
- Last 10 min: Active recall — explain without notes

### Checkpoint
- [ ] Can build a static website from scratch
- [ ] Can write basic JavaScript functions
- [ ] Can use Git for version control
- [ ] Have 3+ projects in portfolio

---

## Phase 2: Full-Stack Web (Months 4–6)

> **Removed.** This phase covered React/Next.js frontend and a Go backend — both retired to
> focus on AI Engineering.

---

## Phase 3: Backend Mastery + Databases + DevOps (Months 7–9)

> **Removed.** This phase covered a Go backend with PostgreSQL/Redis — retired to focus on AI
> Engineering. The PostgreSQL, Redis, and Docker content lives on in
> `projects/03-databases/` and `projects/06-devops/`.

---

## Phase 4: AI Engineering (Months 10–12)

### Goal
Understand AI/LLMs/RAG. Build an AI-powered application.

### Sources

| Source | What You Learn | When |
|--------|---------------|------|
| **ML for Beginners** (Microsoft) | ML fundamentals | Month 10 |
| **Neural Networks: Zero to Hero** (Karpathy) | How neural nets work | Month 10 |
| **Hugging Face NLP/LLM Course** | Transformers, practical usage | Month 11 |
| **Illustrated Transformer** (Jay Alammar) | Attention mechanism, visual | Month 11 |
| **DeepLearning.AI – RAG** | RAG pipeline | Month 11-12 |
| **DeepLearning.AI – Multi-agent (CrewAI)** | Agent orchestration | Month 12 |
| **Hugging Face Agents Course** | Agent fundamentals | Month 12 |
| **Arize AI – Agents Mastery** | Monitoring, eval, guardrails | Month 12 |

### What to Build

| Week | Project | Lab Location |
|------|---------|-------------|
| 37-38 | Python basics for AI | `projects/04-ai-engineering/` |
| 39-40 | Simple chatbot with LLM API | `projects/04-ai-engineering/` |
| 41-42 | Embeddings + vector search | `projects/04-ai-engineering/embeddings/` |
| 43-44 | RAG pipeline (chunk → embed → retrieve → generate) | `projects/04-ai-engineering/rag-system/` |
| 45-46 | Simple AI agent with tool calling | `projects/04-ai-engineering/agents/` |
| 47-48 | **Capstone: AI project** | Complete AI application |

### Checkpoint
- [ ] Can call LLM APIs and handle responses
- [ ] Can implement RAG pipeline
- [ ] Can design effective prompts
- [ ] Can build a simple AI agent
- [ ] Can evaluate AI output quality
- [ ] Have an AI project in portfolio

---

## Resource → Lab Mapping

```
Month 1-3:  FreeCodeCamp + Odin → projects/00-core-foundations/
Month 7-9:  PostgreSQL/Redis + Docker → projects/03-databases/ + projects/06-devops/
Month 10-12: ML + HF + DeepLearning.AI → projects/04-ai-engineering/
```

---

## Evidence-Based Study Rules

1. **Active Recall > Re-reading**: Test yourself before reviewing
2. **Spaced Repetition > Cramming**: Review at 1 day → 3 days → 1 week → 1 month
3. **Interleaving > Blocking**: Mix RAG, LLM, system design in same week
4. **Elaboration > Highlighting**: Explain concepts in your own words
5. **Project-Based > Course-Based**: Every lesson → real code in the lab

---

## Progress Tracking

### Weekly Review (every Saturday)
- Self-assessment (1-10) per skill area
- What was learned this week
- What needs more practice
- Next week's plan

### Monthly Review (every 4 weeks)
- The 30-Day Rule: something must be working
- Phase progress check
- Gap identification
- Resource priority adjustment

### Portfolio Milestones

| Month | Milestone | Portfolio Item |
|-------|-----------|---------------|
| 3 | Programming foundations complete | 3+ static websites |
| 9 | Databases + DevOps mastery | Deployed FastAPI service with DB |
| 12 | AI Engineering capable | 1 AI-powered application |
