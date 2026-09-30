# Daily 90-Minute Session Schedule

> **Superseded.** The canonical, validator-gated workflow chain is
> [`.ai/workflows/feature/`](../../../.ai/workflows/feature/01-plan.md)
> (`01-plan` through `06-reflect`). Edit `.ai/` and not this file; this copy is kept
> as product-era documentation.

The recommended daily rhythm for consistent learning progress.

---

## The Schedule

| Time | Activity | Agent | Output |
|------|----------|-------|--------|
| 0-10 min | Choose topic, define goal | — | Session goal card |
| 10-25 min | Learn/explain | Learning Coach | Concept notes |
| 25-60 min | Write code manually | — | Working code |
| 60-70 min | Unblocked if stuck | Pair Programmer | Next step |
| 70-80 min | Review or debug | Code Reviewer / Debugger | `ai-review.md` / `debugging-session.md` |
| 80-90 min | Write artifact + reflect | — | Learning artifact |

---

## Daily Minimum

Each day must produce at least one:
- Code change (committed)
- Review note (`ai-review.md`)
- Debugging note (`debugging-session.md`)
- Learning summary (`docs/learning/`)
- ADR draft (`docs/decisions/`)

**If nothing was produced, the session was passive. Adjust tomorrow.**

---

## Weekly Rhythm

| Day | Focus | Time |
|-----|-------|------|
| Mon | New concept (Learning Coach) | 90 min |
| Tue | Implement (write code) | 90 min |
| Wed | Review + fix (Code Reviewer) | 60 min |
| Thu | Debug + harden (Debugger) | 60 min |
| Fri | Reflect + document (Source Learning) | 60 min |
| Weekend | Catch up or capstone | flexible |

---

## Time Budget for 90 Minutes

```
Understand:   10 min (11%)
Plan:          5 min (6%)
Write:        35 min (39%)  <-- the most important block
Unblock:      10 min (11%)
Review:       10 min (11%)
Reflect:      10 min (11%)
Buffer:       10 min (11%)
```

**Key insight:** Writing gets the most time. Learning and reviewing are
supporting acts. If writing takes less than 30 minutes, the session was
too shallow.

---

## Signs of a Good Session

- You wrote more code than you read
- You can explain what you built without looking
- The review found 1-3 issues (not 10+)
- You identified a specific gap to fix
- An artifact exists in the repo

## Signs of a Bad Session

- AI wrote most of the code
- You can't explain a line you "wrote"
- No artifact was created
- The session was all reading/learning
- The same gap appears again
