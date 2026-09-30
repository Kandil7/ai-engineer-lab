# Operating Manual — Implementation Guide

How to use the AI Learning Operating Manual in daily practice. This guide
maps the manual's concepts to concrete files, commands, and habits.

---

## Quick Reference

| What | Where | When |
|------|-------|------|
| The manual | `docs/product/ai-learning-operating-manual.md` | Reference |
| Agent prompts | `docs/product/agents/` | Before each AI session |
| Workflows | `docs/product/workflows/` | Every session |
| Templates | `templates/` | When creating artifacts |
| Learning artifacts | `docs/learning/` | After learning sessions |
| Mistakes | `mistakes.md` (in project folder) | After a mistake |
| Reviews | `ai-review.md` (in project folder) | After a feature |
| Debugging | `debugging-session.md` (in project folder) | After a bug |
| Source learning | `docs/learning/source-summaries/` | After reading a source |
| ADRs | `docs/decisions/` | After a decision |

---

## Starting a Session

1. Open `docs/product/workflows/session-procedure.md`
2. Fill in the Session Goal card
3. Pick the right agent from `docs/product/agents/`
4. Copy the prompt template from the agent file
5. Start with the smallest question

## During the Session

Follow the 7-phase workflow:
1. **Understand** — use Learning Coach
2. **Plan** — use Project Planner
3. **Write** — write code yourself (the big block)
4. **Hints** — use Pair Programmer if blocked
5. **Review** — use Code Reviewer
6. **Debug** — use Debugging Specialist if broken
7. **Reflect** — write the artifact

## Ending the Session

1. Create at least one artifact
2. Write the closing reflection
3. Commit the artifact
4. Identify the next step

---

## Agent Selection

| Situation | Agent | Prompt location |
|-----------|-------|-----------------|
| Starting a new topic | Learning Coach | `agents/learning-coach.md` |
| Breaking down a feature | Project Planner | `agents/project-planner.md` |
| Stuck on the next step | Pair Programmer | `agents/pair-programmer.md` |
| Code works but is ugly | Code Reviewer | `agents/code-reviewer.md` |
| Something is broken | Debugging Specialist | `agents/debugging-specialist.md` |
| Reading docs/repo/article | Source Learning Agent | `agents/source-learning-agent.md` |

---

## The Four-Level Help Model

Before asking for help, identify the level:

| Level | Symptom | What to ask |
|-------|---------|-------------|
| **1. Explain** | "I don't understand" | Explain simply + example |
| **2. Hint** | "I know X but stuck on Y" | Smallest hint, next step |
| **3. Review** | "I wrote it, check it" | Review, identify weaknesses |
| **4. Rescue** | "I tried everything" | Minimal working example |

**After rescue:** Rewrite the logic from memory. If you can't, you didn't
learn it.

---

## Writing "Full Detail" Lectures

The lectures in `projects/*/` follow this standard:

```markdown
# [Section] [NN]: [Topic Title]

## Topic Overview (2-3 paragraphs)
What, why, context, what makes it hard.

## Learning Objectives (5-7 bullets)
What you can do after this lecture.

## Prerequisites (1-3 bullets)
What you need before starting.

## 1. [Concept] (deep explanation + code + analogy)
- The core idea (3-5 paragraphs)
- A real-world analogy
- A complete code example
- When it works, when it fails
- Connection to the roadmap exit test

## 2. [Concept] (same depth)
...

## 3-7. [More concepts]

## Real-World Application
Where this shows up in production.

## Common Mistakes (5-7 items with examples)

## Key Takeaways (5 bullets)

## Self-Check Questions (3-5 questions)

## Further Reading / Connections
Links to related topics and sections.
```

**Target length:** 250-400 lines per lecture (versus ~90 in the
abbreviated format).

---

## Measuring Progress

Track these weekly:
- [ ] Sessions completed (target: 5/week)
- [ ] Artifacts created (target: 5/week)
- [ ] Code written by you (target: >70% of lines)
- [ ] Mistakes recorded (target: 2-3/week)
- [ ] Gaps closed (from `mistakes.md`)

---

## Integration with Existing Systems

| System | How it connects |
|--------|----------------|
| `.ai/prompts/` | Agent prompts can be registered as role prompts |
| `registries/` | Templates registered in `template-registry.yaml` |
| CI validators | Artifacts follow template structure |
| `/session-log` | Quick capture from any session |
| `/document-project` | Full documentation sweep |
