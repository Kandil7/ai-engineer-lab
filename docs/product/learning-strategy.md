# Learning Strategy

> **Long-track context.** Written 2026-08-06, before the 10-week active track. The plan
> of record is [`active-track-10-week.md`](../roadmap/active-track-10-week.md); treat
> roadmap-specific claims here as historical.

**Last updated:** 2026-08-06

How to use the 5-axis resource system with the AI Engineer Lab workspace.

---

## The 5 Axes

| Axis | Focus | Key Sources | Lab Integration |
|------|-------|-------------|-----------------|
| 1 | Web / Full-Stack Foundations | MDN, FreeCodeCamp, Odin Project, Roadmap.sh | Frontend projects, API integration |
| 2 | Backend / DevOps | Pro Git, PostgreSQL/Redis docs, Docker courses | FastAPI services, infra scripts |
| 3 | AI Engineering / LLMs / RAG | DeepLearning.AI, Boot.dev, OpenAI Cookbook | rag-system, embeddings, prompt-engineering |
| 4 | Agents / Prompt Engineering | Anthropic guides, production patterns articles | .ai/prompts/, agents project |
| 5 | Evidence-Based Learning | Active recall research, spaced repetition guides | daily-log, weekly-review, notes system |

---

## Source → Artifact Pipeline

Every source you study MUST produce a tangible artifact in the repo:

```
1. READ: One focused session (30-60 min)
    ↓
2. EXTRACT: Key concepts + one example + one exercise
    ↓
3. APPLY: Build something real in the lab
    ↓
4. REVIEW: Use code-reviewer or architect prompt
    ↓
5. REFLECT: Write in daily-log template
    ↓
6. LINK: Connect to at least one project task
```

### Artifact Checklist

For every source studied:

- [ ] Source summary exists in `docs/learning/source-summaries/`
- [ ] At least one code change in `projects/`
- [ ] At least one note in `docs/learning/notes/weekly/`
- [ ] Status updated in `learning-sources/source-index.md`
- [ ] Project task linked in the source summary

---

## Daily Learning Loop (6 hours)

### Hour 1: Learn (Theory)
- Pick ONE topic from ONE source
- Read/watch for 30 minutes
- Extract key concepts (no copying — understand)

### Hours 2-4: Build (Practice)
- Apply what you learned in a lab project
- Write code yourself first
- Use AI for hints when stuck (not for full solutions)

### Hour 5: Review
- AI code review using `.ai/prompts/roles/code-reviewer.md`
- Fix issues found
- Run validation tests

### Hour 6: Recall & Plan
- Active recall: explain what you learned without notes
- Write daily reflection using `daily-log.template.md`
- Plan tomorrow's topic

---

## Interleaving Schedule

Don't study one axis exclusively. Mix them:

| Week | Monday | Tuesday | Wednesday | Thursday | Friday | Saturday |
|------|--------|---------|-----------|----------|--------|----------|
| Focus | RAG System | LLM APIs | RAG System | Agents | Prompt Eng | Review |
| Axis | 3 | 3 | 3 | 4 | 4 | 5 |

This follows the interleaving principle: mixing topics produces deeper learning than studying one topic at a time.

---

## Spaced Repetition Schedule

For every concept learned:

| Review | When | How |
|--------|------|-----|
| 1st | Same day | Active recall in Hour 6 |
| 2nd | +1 day | Quick self-test before starting |
| 3rd | +3 days | Explain to AI without notes |
| 4th | +1 week | Apply in a different project |
| 5th | +1 month | Teach it or write a deep-dive |

---

## Resource Priority (Don't Collect — Complete)

### Tier 1: Complete First (Foundations)
1. **FreeCodeCamp** or **Odin Project** → Web fundamentals
2. **Pro Git** → Git mastery
3. **FastAPI learning path** → `docs/learning/paths/fastapi-ai-services.md`

### Tier 2: Complete Next (Core Skills)
4. **DeepLearning.AI Generative AI with LLMs** → AI fundamentals
5. **DeepLearning.AI RAG course** → RAG pipeline
6. **RAG learning path** → `docs/learning/paths/rag-qdrant.md`

### Tier 3: Complete Later (Advanced)
7. **Anthropic agent guides** → Agent architecture
8. **Production patterns article** → Prompt engineering
9. **System design** → `docs/learning/paths/system-design.md`

### Don't Collect
- Don't bookmark 20 courses and start none
- Pick ONE per tier, COMPLETE it, then move to next
- Use docs + hands-on guides for supplementary topics

---

## Evidence-Based Study Rules

Based on research from axis 5:

1. **Active Recall > Re-reading**: Test yourself before reviewing source material
2. **Spaced Repetition > Cramming**: Review at increasing intervals
3. **Interleaving > Blocking**: Mix RAG, LLM, system design in same week
4. **Elaboration > Highlighting**: Explain concepts in your own words
5. **Project-Based > Course-Based**: Every lesson → real code in the lab

### Self-Test Prompts

Use these in Hour 6 (Recall):

```text
Explain [concept] without opening any files.
What are the 3 key steps in [process]?
What's the difference between [A] and [B]?
When would you use [pattern] vs [alternative]?
```

---

## Progress Tracking

### Weekly Review (every Saturday)

Use `weekly-review.template.md`:
- Self-assessment (1-10) per axis
- What was learned this week
- What needs more practice
- Next week's plan

### Monthly Review (every 4 weeks)

Use `monthly-review.template.md`:
- The 30-Day Rule: something must be working
- Phase progress check
- Gap identification
- Resource priority adjustment

---

## Quick Reference: Which Source for What

| I need to learn... | Start with | Then apply in |
|-------------------|------------|---------------|
| PostgreSQL | PostgreSQL docs + GeeksforGeeks | `projects/03-databases/postgres-design/` |
| Redis | Redis commands reference | `projects/03-databases/redis-cache/` |
| RAG | DeepLearning.AI RAG + OpenAI Cookbook | `projects/04-ai-engineering/rag-system/` |
| Agents | Anthropic guides + production patterns | `projects/04-ai-engineering/agents/` |
| System Design | Roadmap.sh + DDIA book | `projects/05-system-design/` |
| Docker/DevOps | Docker course + Compose docs | `projects/06-devops/docker/` |
| Prompt Engineering | Production patterns article | `.ai/prompts/` system |
